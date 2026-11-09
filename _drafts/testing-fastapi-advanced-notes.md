---
layout: post
title: "Testing FastAPI in Practice: Async Tests, Dependency Overrides, Coverage, and CI"
post_series_id:
  - modern-python-application
  - building-rest-apis
date: 2026-10-20
author: sasadangelo
slug: testing-fastapi-in-practice
image: /assets/img/testing-fastapi-in-practice-hero.svg
excerpt: "Async tests with pytest-asyncio 1.x, dependency overrides, network isolation, test databases, branch coverage, and CI for a real FastAPI app."
categories:
  - "Programming"
tags:
  - programming
  - python
---

![Testing FastAPI in Practice: Async Tests, Dependency Overrides, Coverage, and CI]({{ site.baseurl }}/assets/img/testing-fastapi-in-practice-hero.svg){:width="760" height="400" .responsive_img}

## Introduction

The [previous article]({{ site.baseurl }}/testing-python-applications-with-pytest-patterns-for-real-code/) ended with a green suite: 79 FastURL tests in about two seconds. Then I pointed the test run at a proxy that does not exist, and the same suite finished in 0.56 seconds. Still green. Every API test that creates a link had been quietly calling `example.com`, and not one of them noticed when the call failed.

Passing tests are not the same as tests that check what you think they check. The concepts from the previous article (test types, mocks, fixtures, independence) apply to any Python project. This article covers the problems that only show up once the code under test is a FastAPI application: an event loop that pytest has to manage, a `lifespan` function that tests skip, dependencies that leak between tests, a network nobody meant to use, a database that is not the production one, and a coverage number that says less than it seems.

Every fix in this article was run against the [FastURL](https://github.com/sasadangelo/fasturl) test suite, and every number comes from a real run.

You should read this article if:

- Your async tests are flaky, or a tutorial's `event_loop` override broke after you upgraded pytest-asyncio.
- You use `app.dependency_overrides` and are not sure your tests are isolated from each other or from the network.
- You want coverage and CI that catch regressions instead of decorating a README badge.

## Async Tests with pytest-asyncio 1.x

pytest knows nothing about coroutines. If you write `async def test_something()` without a plugin, pytest calls the function, gets a coroutine object back, and never awaits it. [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/stable/concepts.html) is the plugin that creates an event loop and runs the coroutine on it. FastURL runs version 1.4.0, and the 1.x line changed enough that half of the async-testing tutorials online no longer work.

### Strict mode and auto mode

pytest-asyncio has two modes. In **strict** mode, the default, it only touches tests marked with `@pytest.mark.asyncio` and fixtures decorated with `@pytest_asyncio.fixture`. In **auto** mode it takes over every `async def` test and every async fixture, with no decorator needed. Strict mode exists so that pytest-asyncio can coexist with other async plugins (trio, anyio). A project that only uses asyncio does not need that caution.

FastURL sets auto mode in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

This makes the four `@pytest.mark.asyncio` decorators still present in `tests/unit/test_database.py` redundant. They are harmless, but they suggest to the next reader that the mark is required, and that is how cargo-cult code spreads. Remove them.

### One event loop per test, unless you ask otherwise

By default, every async test gets a fresh event loop that is closed when the test ends. That is the right default: a test cannot leave a pending task or an open connection behind for the next one. pytest-asyncio calls this the **loop scope**, the pytest scope (`function`, `class`, `module`, `package`, `session`) that owns the loop a test or fixture runs on.

Async fixtures have a loop scope too, and here 1.x has a trap. The setting `asyncio_default_fixture_loop_scope` has no default. When it is unset, a fixture's loop scope silently follows its caching scope, and the plugin's own source code announces that a future version will default to `function` instead. FastURL does not set it. Set it explicitly, so the behaviour does not change under you on the next upgrade:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
```

### The `event_loop` fixture is gone

Many tutorials share an expensive async resource across tests by overriding the `event_loop` fixture with a wider scope:

```python
# Removed in pytest-asyncio 1.0: this fixture is no longer used
@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine() -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(url=TEST_DATABASE_URL)
    yield engine
    await engine.dispose()
```

pytest-asyncio deprecated this override in 0.22 and [removed it in 1.0](https://pytest-asyncio.readthedocs.io/en/stable/reference/changelog.html). The replacement declares the loop scope on the fixture itself:

```python
import pytest_asyncio


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def engine() -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(url=TEST_DATABASE_URL)
    yield engine
    await engine.dispose()
```

Breaking down the two arguments:

- `scope="session"` — how long pytest caches the fixture value: created once, reused by every test
- `loop_scope="session"` — which event loop runs the fixture: the session loop, which outlives every test

There is a second half that most migration guides skip. The engine now lives on the session loop, but each test still runs on its own function-scoped loop. An asyncpg connection created on one loop and awaited from another fails with errors like `Future attached to a different loop`. Every test that uses a session-loop resource must run on the same loop:

```python
# At the top of a test module
pytestmark = pytest.mark.asyncio(loop_scope="session")
```

Or, for the whole project, `asyncio_default_test_loop_scope = "session"` in `pyproject.toml`. Use that option with care: tests that share a loop can also share the leftovers of a task that one of them forgot to await.

> A shared async resource needs two things: a wide `scope` to be cached, and a matching `loop_scope` on both the fixture and the tests that use it.

### Async does not mean parallel

pytest-asyncio runs async tests one after the other. Each test awaits its own coroutines, but two tests never interleave. If you want the suite to use more than one CPU core, the tool is [pytest-xdist](https://pytest-xdist.readthedocs.io/), which spreads tests across worker processes with `pytest -n auto`.

Parallel workers bring back the shared-state problem from the previous article. FastURL's default test database is in-memory SQLite, private to each test, so it parallelises cleanly. Against PostgreSQL, the `db_session` fixture runs `drop_all` after every test, and two workers sharing one database would drop each other's tables in the middle of a test. With xdist and a real database, each worker needs its own database, usually named after the `worker_id` fixture that pytest-xdist provides.

One last note on plugins. The [FastAPI documentation on async tests](https://fastapi.tiangolo.com/advanced/async-tests/) uses `@pytest.mark.anyio`, from the pytest plugin bundled with AnyIO. It is a valid choice. But pick one plugin per project: with pytest-asyncio in auto mode, an `anyio` mark on top only makes the reader wonder which plugin actually runs the test.

## TestClient, AsyncClient, and the Lifespan Gap

FastAPI gives you two ways to send requests to an application inside a test. `TestClient`, from Starlette, offers a synchronous interface: you call `client.get(...)` from a regular `def` test. `httpx.AsyncClient` with an `ASGITransport` offers an async interface: you `await client.get(...)` from an `async def` test. FastURL uses the second one, and the reason is in the third row of this table:

| | **`TestClient`** | **`AsyncClient` + `ASGITransport`** |
|---|---|---|
| **Test style** | Plain `def` tests | `async def` tests |
| **Lifespan** | Runs it, but only inside `with TestClient(app) as client:` | Never runs it |
| **Event loop** | Runs the app on its own loop, in a separate thread | Runs the app on the test's loop |
| **Background tasks** | Run before the call returns | Run before the call returns |
| **Fits when** | Tests only talk to the app over HTTP | Tests also await async resources (sessions, clients) |

`TestClient` drives the app through a portal: a separate event loop in a worker thread. A test that wants to seed a row through the same `AsyncSession` the app uses cannot do that from a sync function, and must not share that session across two loops. FastURL's redirect tests seed links directly through `db_session` and then query them through the API, so `AsyncClient` is the right choice.

### The gap

The price of `AsyncClient` is in the second row: `ASGITransport` does not send the ASGI lifespan events, so FastURL's `lifespan` function never runs in tests. In production, that function does three things: it configures logging, calls `init_db()` to create the engine and the connection pool, and creates the shared `httpx.AsyncClient` on `app.state`.

The coverage report shows the gap clearly:

```text
Name                         Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------------
src/fasturl/core/log.py         52     34      6      0    31%   41-52, 81-90, 95-112, ...
src/fasturl/main.py             37     12      2      0    64%   36-68
```

Lines 36 to 68 of `main.py` are the `lifespan` function. Not one of the 79 tests executes it. If a refactoring broke the startup sequence (a typo in a setting name, a client created with the wrong timeout), the suite would stay green and the application would fail on its first deploy.

### Three ways to close it

**1. Seed `app.state` by hand.** This is what FastURL does today. The `api_client` fixture overrides the database dependency and assigns `app.state.http_client = httpx.AsyncClient()` directly. It works, but the test client is not the production one: no timeout setting, no redirect limit, no `User-Agent`. And as the next section shows, it is a client with full network access.

**2. Run the real lifespan with [asgi-lifespan](https://github.com/florimondmanca/asgi-lifespan).** `LifespanManager` sends the startup event, waits for it to complete, yields, then sends the shutdown event:

```python
from pathlib import Path

import httpx
import pytest
from asgi_lifespan import LifespanManager

from fasturl.core.config import settings
from fasturl.main import app


async def test_lifespan_creates_and_closes_shared_resources(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Startup creates the shared HTTP client; shutdown closes it."""
    monkeypatch.setattr(settings.database.sqlite, "path", str(tmp_path / "lifespan.db"))
    monkeypatch.setattr(settings.log, "file", str(tmp_path / "lifespan.log"))

    async with LifespanManager(app):
        client: httpx.AsyncClient = app.state.http_client
        assert not client.is_closed
    assert client.is_closed
```

The two `monkeypatch` lines matter. The real lifespan calls the real `init_db()` and the real `setup_logging()`, which read their paths from `config.yaml`. Without the patches, my first run of this test created `instance/fasturl.db` and `logs/fasturl.log` in the project folder, the same files the development server uses. `tmp_path` is a built-in pytest fixture that gives each test its own temporary directory, and `monkeypatch` restores both settings when the test ends.

**3. Override the dependency.** Tests do not need the lifespan if every resource it creates is reached through a dependency, and the test overrides that dependency. FastURL reads the shared client through `get_http_client`, so a test can replace it without touching `app.state` at all. The next section does exactly that.

My recommendation combines the second and the third. Endpoint tests override dependencies, so each test controls exactly what the app receives. One smoke test runs the real lifespan with `LifespanManager`, so the startup and shutdown code is executed at least once. That single test raised `main.py` from 64% to 97% coverage on my machine.

> `httpx.AsyncClient` with `ASGITransport` never runs the lifespan. Either test it on its own, or accept that your startup code is untested.

## Dependency Overrides as Fixtures

FastAPI resolves every `Depends(...)` through the `app.dependency_overrides` dictionary first. If the dictionary maps a dependency to another callable, FastAPI calls the replacement instead. The [FastAPI guide on testing dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/) shows the basic pattern:

```python
app.dependency_overrides[get_db] = override_get_db

def test_something() -> None:
    response = client.get("/api/v1/links")
    ...

app.dependency_overrides = {}
```

The dictionary belongs to the `app` object, and the app is a module-level singleton shared by every test in the run. An override set at module level applies to every test that runs after it, in every file. A reset on the last line of a test is skipped when an assertion fails. This is the same leak as the `_session_factory` global from the previous article, in a different place.

FastURL's `api_client` fixture already applies the fix: set the override before `yield`, clear it after. The teardown runs whether the test passes or fails. Here is the fixture extended to override the HTTP client as well:

```python
_FAKE_PAGE: str = "<html><head><title>Example Domain</title></head></html>"


def _fake_target(request: httpx.Request) -> httpx.Response:
    """Answer every outbound request with a small HTML page."""
    return httpx.Response(status_code=200, text=_FAKE_PAGE)


@pytest.fixture()
async def http_client() -> AsyncIterator[httpx.AsyncClient]:
    """Yield an httpx.AsyncClient whose network layer never leaves the process."""
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler=_fake_target)) as client:
        yield client


@pytest.fixture()
async def api_client(
    db_session: AsyncSession, http_client: httpx.AsyncClient
) -> AsyncIterator[httpx.AsyncClient]:
    async def _override_get_db() -> AsyncIterator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_http_client] = lambda: http_client

    transport: httpx.ASGITransport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
```

Three details are worth noticing:

- `http_client` is its own fixture. A test that needs a different answer from the outside world (a 404 page, a timeout) can override that one fixture without rewriting `api_client`.
- The override key is the original function object, `get_http_client`, imported from `fasturl.api.dependencies`. Overriding by name does not work; FastAPI matches the function itself.
- The `app.state.http_client` assignment is gone. Nothing reads `app.state` directly any more, because the router and the service both receive the client through `HTTPClientDep`.

As a second line of defence, an `autouse` fixture can clear the overrides after every test in the project, including tests that set an override without going through `api_client`:

```python
@pytest.fixture(autouse=True)
def _reset_dependency_overrides() -> Iterator[None]:
    """Guarantee that no dependency override survives the test that set it."""
    yield
    app.dependency_overrides.clear()
```

An `autouse` fixture runs for every test in its scope without being requested. Use them sparingly, because they are invisible from the test function. A cleanup that must never be forgotten is a good use of one.

## Isolating the Network

Back to the experiment from the introduction. The `--durations` flag lists the slowest tests, and in the original suite the top of the list looks like this:

```shell
uv run pytest tests/integration -q --durations=4
```

> 0.18s call     test_links_api.py::TestTriggerInspection::test_inspection_status_reset_to_pending
> 0.18s call     test_links_api.py::TestTriggerInspection::test_existing_link_returns_202
> 0.17s call     test_links_api.py::TestTriggerInspection::test_already_pending_is_accepted_idempotent
> 0.14s call     test_links_api.py::TestCreateLink::test_auto_code_returns_201
> 32 passed in 2.06s

Every slow test creates or re-inspects a link. Creating a link schedules `inspect_link` as a background task, and `ASGITransport` waits for the whole ASGI call, background tasks included, before it returns the response to the test. So each of these tests waited for a real `GET https://example.com` made by the stub client in `app.state`.

To prove it, I ran the suite with the proxy variables pointing to a port where nothing listens. `httpx` honours `HTTP_PROXY` and `HTTPS_PROXY` by default, so every outbound request fails immediately with a connection error:

```shell
HTTP_PROXY=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 uv run pytest -q
```

> 79 passed in 0.56s

From 2.41 seconds to 0.56 seconds, and still green. The inspector caught the connection error, marked each link as `unreachable`, and no test checked the result. That reveals three problems at once:

- **Speed.** Three quarters of the suite's run time was spent on network calls that no test needed.
- **Fragility.** The stub client has `httpx`'s default timeout of five seconds. On a CI runner with a slow or filtered connection, the same tests take seconds each, and the timing changes from run to run.
- **Blind spots.** The integration tests never verified what the inspection actually stores, because the result depended on a website outside the project's control.

The `api_client` fixture from the previous section fixes the first two: the inspector now receives a `MockTransport` client, and no request leaves the process. With that change, the suite runs in 0.35 seconds on my machine, with or without a network. The comment on the old stub, `# stub; intercepted per-test via respx`, also goes away. It describes a library the project does not even install.

The third problem needs a new test. With a deterministic fake page, the inspection result becomes something a test can assert:

```python
async def test_inspection_reads_title_of_target_page(api_client: httpx.AsyncClient) -> None:
    """The background inspection runs against the fake page and stores its title."""
    created = await api_client.post(url="/api/v1/links", json={"target_url": "https://example.com"})
    code: str = created.json()["code"]

    response = await api_client.get(url=f"/api/v1/links/{code}")

    inspection = response.json()["inspection"]
    assert inspection["status"] == "active"
    assert inspection["title"] == "Example Domain"
```

This test covers the whole chain end to end: the router schedules the task, the inspector fetches the page through the injected client, parses the title, and the repository stores it where `GET` can read it.

### A guard rail against the next leak

The fix works today. Next month, someone will add a webhook or an analytics call and forget to inject the client. [pytest-socket](https://github.com/miketheman/pytest-socket) turns that mistake into a loud failure. It patches Python's `socket` module during the test run and blocks connections to any host you have not allowed. Install it as a development dependency, then pass the allowed hosts:

```shell
uv add --dev pytest-socket
uv run pytest --allow-hosts=127.0.0.1,::1
```

Breaking down the option:

- `--allow-hosts=127.0.0.1,::1` — allow connections to the loopback address only (IPv4 and IPv6), so a local PostgreSQL still works, and block everything else

Running the original suite with this option fails 13 integration tests with a message that leaves no room for doubt:

> pytest_socket.SocketConnectBlockedError: A test tried to use socket.socket.connect() with host "104.20.23.154" (allowed: "127.0.0.1,::1").

With the fixed `api_client`, all 79 tests pass. pytest-socket also has a stricter `--disable-socket` option that blocks socket creation entirely. Async tests need `--allow-unix-socket` alongside it, because the asyncio event loop creates a Unix socket pair for its own internal wake-ups. Without that flag, 21 of FastURL's async unit tests fail before they even start.

When different tests need different answers per URL (the home page returns 200, `/robots.txt` returns 404), a single handler function becomes awkward. [respx](https://lundberg.github.io/respx/) adds route-based mocking on top of `httpx`. For FastURL's single-endpoint inspector, `MockTransport` is enough.

> If a test can reach the internet, sooner or later it will depend on it. Block the network in the test run, and inject every client the code uses.

## Choosing a Test Database Strategy

FastURL's integration tests run on in-memory SQLite by default, and on PostgreSQL when `TEST_DATABASE_URL` is set. That is one of four common strategies, and each one trades speed against fidelity in a different way:

| | **In-memory SQLite per test** | **Real PostgreSQL, schema per test** | **PostgreSQL + transaction rollback** | **testcontainers** |
|---|---|---|---|---|
| **Speed** | Fastest — no disk, no network | Slowest — `create_all`/`drop_all` on every test | Fast — schema created once | Same as the strategy used inside the container |
| **Fidelity** | Different engine from production | Same engine as production | Same engine as production | Same engine and version as production |
| **Isolation** | A new database per test | Fresh tables per test | Every test's changes rolled back | Depends on the strategy used inside |
| **Setup** | None | A running server and a dedicated database | A running server, plus session-scoped fixtures | Docker on the developer machine and in CI |
| **In FastURL** | Default | `TEST_DATABASE_URL`, CI job | Not used | Not used |

The fidelity row is not theoretical. FastURL's repository contains this comment, in `increment_clicks`:

```python
# Naive UTC from Python, like every other timestamp: the database's now() is in the
# server timezone on PostgreSQL (e.g. Europe/Rome) but UTC on SQLite.
now = datetime.now(UTC).replace(tzinfo=None)
```

When the click timestamp came from the database's `now()`, every test passed on SQLite, because SQLite works in UTC. On a PostgreSQL server configured for `Europe/Rome`, the same code stored local time and the timestamps were off by one or two hours. The regression test `test_last_clicked_at_is_utc` guards that fix, and it only proves something when it runs on PostgreSQL. That is why the CI runs the suite twice, once per engine.

### Transaction rollback: the schema once, the data never

Creating and dropping every table for every test is the slow part of the PostgreSQL run. The common alternative creates the schema once per session, and wraps each test in a transaction that is rolled back at the end. Here is a sketch for FastURL:

```python
@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def engine() -> AsyncIterator[AsyncEngine]:
    engine: AsyncEngine = create_async_engine(url=TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(loop_scope="session")
async def db_session(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    async with engine.connect() as conn:
        transaction = await conn.begin()
        session = AsyncSession(
            bind=conn,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        yield session
        await session.close()
        await transaction.rollback()
```

The key is `join_transaction_mode="create_savepoint"`. FastURL's repository calls `session.commit()` after every write. In this mode, SQLAlchemy turns each of those commits into the release of a SAVEPOINT inside the outer transaction, so the application code runs unchanged. When the test ends, the outer transaction rolls back and every row disappears with it.

Notice the `loop_scope="session"` on both fixtures. The engine and its connections live on the session loop, so the tests that use them need the `pytestmark` from the first section. This is where the pytest-asyncio configuration stops being an abstract detail.

The trade-off: code that manages its own transactions or opens its own connections escapes the rollback. A background task that creates a new session from the engine would write outside the test transaction, and its rows would survive the test. For FastURL that would be the inspector, if it ever stopped receiving its repository through dependency injection.

For a developer who does not want to install PostgreSQL locally, [testcontainers](https://testcontainers-python.readthedocs.io/) starts a throwaway container from the test session itself, as shown in the previous article. It combines well with the rollback strategy: one container and one schema per run, one transaction per test.

## Fixture Patterns That Scale

Fixtures that work for 79 tests can become a burden at 500. Four patterns keep a growing suite readable.

### A factory fixture backed by the database

The previous article introduced factory fixtures with an in-memory `LinkDAO`. The redirect tests need the database version: they insert links through a module-level helper, `_seed_link(db_session, code=...)`, and every test has to pass the session in by hand. As a fixture, the factory requests `db_session` itself:

```python
@pytest.fixture()
def seed_link(db_session: AsyncSession) -> Callable[..., Awaitable[LinkDAO]]:
    """Return a coroutine function that inserts a LinkDAO into the test database."""

    async def _seed(
        *,
        code: str,
        target_url: str = "https://example.com",
        is_active: bool = True,
        expires_at: datetime | None = None,
    ) -> LinkDAO:
        now: datetime = datetime.now(UTC).replace(tzinfo=None)
        link: LinkDAO = LinkDAO(
            code=code,
            target_url=target_url,
            is_active=is_active,
            expires_at=expires_at,
            inspection_status="active",
            clicks_count=0,
            created_at=now,
            updated_at=now,
        )
        db_session.add(instance=link)
        await db_session.commit()
        await db_session.refresh(instance=link)
        return link

    return _seed
```

A test now asks for `seed_link` and calls `await seed_link(code="redir02")`. Because both `seed_link` and `api_client` request `db_session`, pytest hands them the same session, and the link the test seeds is the link the API finds.

### Markers that cannot be misspelled

A marker is a label attached to a test, which you can then use to select or deselect tests from the command line. Markers must be registered, and the registration should be enforced:

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]
addopts = ["--strict-markers", "--strict-config"]
markers = [
    "integration: crosses the HTTP layer and a real database",
    "slow: takes more than a second",
]
```

Breaking down the two options in `addopts`:

- `--strict-markers` — an unregistered marker is an error. Without it, `@pytest.mark.integraton` creates a new, empty marker, and `-m "not integration"` silently runs the test you meant to exclude.
- `--strict-config` — an unknown key in the `[tool.pytest.ini_options]` section is an error, so a typo in `asyncio_mode` cannot silently fall back to strict mode.

Marking every integration test by hand is tedious. A hook in the root `conftest.py` marks them by folder:

```python
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark every test under tests/integration/ as an integration test."""
    for item in items:
        if "integration" in item.path.parts:
            item.add_marker(pytest.mark.integration)
```

The fast suite is now a selection, not a folder name:

```shell
uv run pytest -m "not integration"
```

> 47 passed, 32 deselected in 0.05s

### One `conftest.py` per layer

FastURL keeps all its fixtures in `tests/conftest.py`. As the suite grows, split it. `tests/unit/conftest.py` holds the mocks, and `tests/integration/conftest.py` holds `db_session`, `http_client`, `api_client`, and `seed_link`. Fixtures in a `conftest.py` are visible only to tests in that folder and its subfolders, so a unit test that accidentally requests `db_session` fails with `fixture 'db_session' not found` instead of quietly turning into an integration test.

One trap: hooks are global even when the `conftest.py` that defines them is not. A `pytest_collection_modifyitems` hook inside `tests/integration/conftest.py` still receives every collected test of the session, from every folder. That is why the marking hook above checks the path instead of trusting its own location.

## Coverage That Means Something

Coverage measures which parts of the code ran during the tests. It does not measure whether the tests checked anything, as the network experiment showed. Used with that limit in mind, it is still the cheapest way to find code no test has ever touched.

### Line coverage and branch coverage

**Line coverage** records whether each line ran. **Branch coverage** records whether each possible jump of each decision ran: for an `if`, both the case where the condition is true and the case where it is false. FastURL's `close_db` shows the difference:

```python
async def close_db() -> None:
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
```

The tests call `close_db()` after initialising the engine, so every line runs and line coverage is 100%. But no test calls it when `_engine` is already `None`, the case of a second shutdown, or of a startup that failed before `init_db()`. [coverage.py](https://coverage.readthedocs.io/en/latest/branch.html) reports that as a partial branch, `87->exit`: the jump from line 87 straight to the end of the function never happened.

FastURL enables branch coverage in `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["src/fasturl"]
branch = true

[tool.coverage.report]
fail_under = 85
show_missing = true
skip_covered = true
```

Breaking down the settings:

- `source` — measure only the application package, not the tests or third-party libraries
- `branch = true` — record branches as well as lines
- `fail_under = 85` — the command exits with an error if total coverage drops below 85%
- `show_missing` — list the line numbers and partial branches that never ran
- `skip_covered` — hide files at 100%, so the report shows only what needs attention

This is the real report from `uv run poe test-cov`, before any of the changes in this article:

```text
Name                                          Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------------------------
src/fasturl/api/schemas/link_schemas.py          53      1      6      1    97%   89
src/fasturl/core/config/__init__.py              25      2      2      1    89%   24-25, 62->64
src/fasturl/core/config/__main__.py              18      1      4      1    91%   60
src/fasturl/core/database.py                     35      0      8      2    95%   63->66, 87->exit
src/fasturl/core/exceptions.py                   43      3      2      0    93%   142-145
src/fasturl/core/log.py                          52     34      6      0    31%   41-52, 81-90, ...
src/fasturl/main.py                              37     12      2      0    64%   36-68
src/fasturl/repositories/link_repository.py      47      0      4      1    98%   68->72
src/fasturl/services/inspector_service.py        57      3      2      0    95%   200-202
-----------------------------------------------------------------------------------------
TOTAL                                           668     56     72      6    91%

18 files skipped due to complete coverage.
Required test coverage of 85.0% reached. Total coverage: 90.54%
```

The total says 91%. The details say more. `main.py` at 64% and `log.py` at 31% are the lifespan gap from earlier, made visible. Lines 200-202 of the inspector are the `httpx.RequestError` handler: the timeout path is tested, a DNS failure or a refused connection is not.

### Keep the gate honest

A few practices keep the number meaningful:

- **Ratchet the threshold.** The suite is at 90.54% and the gate is at 85%, so coverage can lose five points without anyone noticing. Raise `fail_under` to the current value, rounded down, every time coverage improves. With the lifespan smoke test, FastURL reaches 96%.
- **Exclude what cannot run, explicitly.** Some lines never execute by design. List them in the configuration rather than writing tests to touch them:

  ```toml
  [tool.coverage.report]
  exclude_also = [
      "if TYPE_CHECKING:",
      "raise NotImplementedError",
      'if __name__ == "__main__":',
  ]
  ```

- **Expect different numbers per layer.** The service layer holds the business rules and should be close to 100% from unit tests alone. Routers are thin and are covered by the API tests. Startup and logging code is covered by one or two smoke tests, not by endless unit tests.

100% is not the goal. The last few percent are usually error handlers for conditions that are hard to provoke, and the tests that reach them are often more fragile than the code they cover. A test written only to move the number is a cost with no benefit.

> Coverage tells you what no test has ever executed. It cannot tell you whether the executed code was checked.

## CI with GitHub Actions

FastURL's [CI workflow](https://github.com/sasadangelo/fasturl/blob/v0.1.0/.github/workflows/ci.yml) runs three jobs on every pull request and on every push to `main`:

- `lint` runs the pre-commit hooks: ruff, mypy, bandit, detect-secrets
- `test-sqlite` runs the full suite on in-memory SQLite, with the coverage gate
- `test-postgresql` runs the full suite again against PostgreSQL 17

The PostgreSQL job relies on a [service container](https://docs.github.com/en/actions/use-cases-and-examples/using-containerized-services/about-service-containers), a Docker container that GitHub Actions starts next to the job and removes when the job ends:

```yaml
services:
  postgres:
    image: postgres:17
    env:
      POSTGRES_USER: fasturl_user
      POSTGRES_PASSWORD: fasturl_ci
      POSTGRES_DB: fasturl_test
    ports:
      - 5432:5432
    options: >-
      --health-cmd "pg_isready -U fasturl_user -d fasturl_test"
      --health-interval 2s
      --health-timeout 3s
      --health-retries 15
```

Breaking down the `options`, which GitHub passes to `docker create`:

- `--health-cmd "pg_isready ..."` — the command Docker runs to decide whether PostgreSQL is ready to accept connections
- `--health-interval 2s` — how often Docker runs the health check
- `--health-timeout 3s` — how long a single check may take before it counts as failed
- `--health-retries 15` — how many consecutive failures mark the container unhealthy

GitHub Actions waits until the container is healthy before it starts the job's steps. Without the health check, the first test can run while PostgreSQL is still initialising, and fail with a connection error that has nothing to do with the code.

### Where the workflow goes from here

With 79 tests that finish in well under a second, running everything on every pull request is the right call. Two changes are worth making when the suite grows.

The first is a Python version matrix. FastURL's `pyproject.toml` declares `requires-python = ">=3.10,<3.15"`, but four modules import `datetime.UTC`, which only exists since Python 3.11. Nothing in CI tests that promise, because the workflow only runs one Python version. A matrix job on the oldest and newest supported versions would have caught it on the first run.

The second is the split from the previous article: fast tests on every pull request, the slow integration run when work lands on `main`. Here is the target shape:

```yaml
jobs:
  unit:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.14"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: uv sync --locked
      - name: Run unit tests
        run: uv run pytest -m "not integration" --allow-hosts=127.0.0.1,::1

  integration-postgresql:
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    services:
      postgres: {}  # abbreviated: same image, env, ports, and options as above
    env:
      TEST_DATABASE_URL: postgresql+asyncpg://fasturl_user:fasturl_ci@127.0.0.1:5432/fasturl_test
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true
      - name: Install dependencies
        run: uv sync --locked
      - name: Run the full suite with coverage
        run: uv run poe test-cov
```

A few decisions in this file deserve a comment:

- The matrix starts at 3.11. Either `requires-python` moves to `>=3.11`, or the code stops using `datetime.UTC`. The matrix forces that decision instead of hiding it.
- `--allow-hosts` runs in CI too, so the network guard from earlier protects every pull request.
- `if: github.event_name == 'push'` skips the integration job on pull requests. The coverage gate moves with it, because unit tests alone do not cover the routers, and a gate on a partial suite would either fail or have to be set uselessly low.

The risk of this split is a pull request that passes the unit job and breaks the integration job after the merge. Teams that cannot accept that use a merge queue, which runs the full suite on the combination of `main` and the pull request before the merge completes. For a project of FastURL's size, the simpler answer is to keep running everything everywhere until the slow job becomes the bottleneck.

## Conclusion

In this article we covered:

- How pytest-asyncio 1.x runs async tests: strict and auto mode, loop scopes, why `asyncio_default_fixture_loop_scope` should be set explicitly, and how `loop_scope` replaces the removed `event_loop` fixture for shared async resources.
- The difference between `TestClient` and `httpx.AsyncClient` with `ASGITransport`, and the lifespan gap that left 36% of FastURL's `main.py` untested, closed with a single `LifespanManager` smoke test.
- Dependency overrides as yield fixtures, with an `autouse` safety net, applied to both the database session and the HTTP client.
- How a dead proxy revealed that 79 green tests depended on `example.com`, how a `MockTransport` client cut the suite from 2.41 to 0.35 seconds, and how pytest-socket makes the next network leak fail loudly.
- Four test database strategies, the timezone bug that only PostgreSQL could reveal, and transaction rollback with SAVEPOINTs.
- Factory fixtures backed by the database, strict markers, folder-based marking, and one `conftest.py` per layer.
- Branch coverage, a real coverage report read line by line, and why the threshold should ratchet up instead of aiming at 100%.
- A CI workflow with a PostgreSQL service container, and how it should evolve: a Python matrix and a split between fast and slow jobs.

This article closes the FastURL implementation arc. The project now has a domain model, a layered architecture, async I/O, background inspection, a consistent error contract, and a test suite that runs offline in under a second, on two database engines, behind a coverage gate.

The [next article]({{ site.baseurl }}/api-design-requests-and-responses/) returns to API design, with the decisions that the first FastURL version left open: when to use path, query, body, or header parameters, how to paginate a collection, and how to version an API without breaking its clients.

---

If you enjoyed this article, don't forget to **give it a clap 👏**, **share it with your friends 🔗**, and **follow me for more tips and tutorials on software development 📘**. Your support helps me create more content like this — thank you! 🙌

**Note**: English is not my native language, and this article was drafted with the assistance of AI. However, all the ideas, projects, concepts, and content are entirely my own.
