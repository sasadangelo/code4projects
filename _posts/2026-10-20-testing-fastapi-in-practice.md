---
layout: post
title: "Testing FastAPI in Practice: Unit and Integration Tests for a Real Feature"
post_series_id:
  - modern-python-application
  - building-rest-apis
date: 2026-10-20
author: sasadangelo
slug: testing-fastapi-in-practice
image: /assets/img/testing-fastapi-in-practice-hero.svg
excerpt: "Unit and integration tests for a real FastAPI feature: main path first, then one test per rule, with AsyncMock, AsyncClient, and dependency overrides."
categories:
  - "Programming"
tags:
  - python
  - fastapi
  - testing
  - pytest
---

![Testing FastAPI in Practice: Unit and Integration Tests for a Real Feature]({{ site.baseurl }}/assets/img/testing-fastapi-in-practice-hero.svg){:width="760" height="400" .responsive_img}

## Introduction

The [previous article]({{ site.baseurl }}/testing-python-applications-with-pytest-patterns-for-real-code/) was about concepts: the difference between unit, integration, and end-to-end tests, what a mock is, what a fixture is, and why every test must start from zero. This article is about practice. We take the core feature of [FastURL](https://github.com/sasadangelo/fasturl), **shorten a link and then use it**, and build its tests the way I build them for any new feature: the main path first, then one test for each rule that can make it fail.

We do it twice. First with unit tests on the service, where the database is a mock and every test runs in a millisecond. Then with integration tests on the HTTP API, where FastAPI adds its own questions: how to call the app without a server, how to give it a test database, and how to stop it from calling the internet.

You should read this article if:

- You understand the theory of test types but are not sure which test cases to write first, or at which level.
- You have seen `app.dependency_overrides` and `ASGITransport` in tutorials and want to know what they actually replace.
- You wonder whether a small API needs end-to-end tests at all.

## The Feature: Shorten a Link, Then Use It

FastURL's main job takes two requests. A client creates a short link:

```shell
curl -X POST http://localhost:8000/api/v1/links \
  -H "Content-Type: application/json" \
  -d '{"target_url": "https://example.com/article"}'
```

Breaking down the flags:

- `-X POST` — the HTTP method; creating a resource is a `POST` on the collection
- `-H "Content-Type: application/json"` — tells FastAPI that the body is JSON
- `-d '{...}'` — the request body, here with only the required `target_url`

The API answers `201 Created` with a seven-character code, for example `aB3x9zK`. From then on, anyone who opens `http://localhost:8000/aB3x9zK` receives a `307` redirect to the target URL, and FastURL counts the click in a [background task]({{ site.baseurl }}/fastapi-async-background-tasks-and-error-handling/). A second background task, scheduled at creation, downloads the target page and stores its title.

Both requests go through the same layers:

- **Schema** — a Pydantic model in `api/schemas/` validates the request body before any of our code runs
- **Controller** — in FastAPI, the router function in `api/routers/` that receives the request, calls the service, and chooses the status code; it holds no business logic
- **Service** — `LinkService` applies the business rules
- **Repository** — `LinkRepository` reads and writes the `links` table
- **Exception handler** — on the way back, a global handler registered in `main.py` turns any domain exception into an HTTP error

The rules that can make the requests fail are spread across those layers, and where a rule lives decides where it can be tested:

| **Rule** | **Lives in** | **Error the client sees** |
|---|---|---|
| The target URL must be HTTP or HTTPS | Pydantic schema | `400 VALIDATION_ERROR` |
| A custom alias may only contain letters, digits, `_`, `-` | Pydantic schema | `400 VALIDATION_ERROR` |
| The expiry date must be in the future | Pydantic schema | `400 VALIDATION_ERROR` |
| The target URL must not point back to FastURL | `LinkService` | `400 VALIDATION_ERROR` |
| A custom alias must be unique | `LinkService` | `409 ALIAS_ALREADY_TAKEN` |
| A generated code that collides is regenerated | `LinkService` | none, unless every retry collides |
| An inactive or unknown link does not redirect | `LinkService` | `404 LINK_NOT_FOUND` |
| An expired link does not redirect | `LinkService` | `410 LINK_EXPIRED` |

The service never deals with HTTP. When a request breaks a rule, the service raises a domain exception, such as `AliasAlreadyTakenError`, which carries its status code, and the exception handler turns it into FastURL's [standard error envelope]({{ site.baseurl }}/fastapi-async-background-tasks-and-error-handling/).

This table is the test plan. The rules in the service can be tested in isolation, with unit tests. The rules in the schema exist only when a request goes through FastAPI, so only integration tests can see them. And the last column is the contract with the client, which only integration tests can check.

![Where each rule lives decides where it can be tested]({{ site.baseurl }}/assets/img/testing-fastapi-in-practice-rules-by-layer.svg){:width="760" height="440" loading="lazy" .responsive_img}

## Unit Tests for the Service

A unit test isolates the logic from everything it talks to. `LinkService` talks to a repository, so every unit test replaces the repository with an `AsyncMock`. FastURL provides one through a fixture in `tests/conftest.py`:

```python
@pytest.fixture()
def mock_repository() -> AsyncMock:
    """Return an AsyncMock that stands in for LinkRepository in unit tests."""
    return AsyncMock()
```

Two helpers at the top of [test_link_service.py](https://github.com/sasadangelo/fasturl/blob/v0.1.0/tests/unit/test_link_service.py) keep the tests short. `_make_link` builds a `LinkDAO` with sensible defaults, and `_make_service` builds a `LinkService` around the mock repository:

```python
def _make_link(
    code: str = "abcdefg",
    target_url: str = "https://example.com",
    is_active: bool = True,
    expires_at: datetime | None = None,
    inspection_status: str = "pending_analysis",
    clicks_count: int = 0,
) -> LinkDAO:
    """Build a minimal LinkDAO ORM instance for use in unit tests."""
    now: datetime = datetime.now(tz=UTC).replace(tzinfo=None)
    return LinkDAO(
        id=1,
        code=code,
        target_url=target_url,
        is_active=is_active,
        expires_at=expires_at,
        inspection_status=inspection_status,
        clicks_count=clicks_count,
        created_at=now,
        updated_at=now,
    )


def _make_service(repository: AsyncMock) -> LinkService:
    """Build a LinkService with a mock repository and mock inspector."""
    return LinkService(repository=repository, inspector=Mock())
```

Breaking down the two helpers:

- `_make_link` — the `LinkDAO` is a plain object, never saved anywhere; each test overrides only the fields that matter to its case, such as `expires_at` or `is_active`
- `_make_service` — the service receives its collaborators through the constructor, so the test can pass a mock repository and a plain `Mock` as the inspector, which the unit tests never call

This is the payoff of the dependency injection introduced in the [layered architecture article]({{ site.baseurl }}/layered-architecture-with-fastapi-routers-services-and-repositories/): because `LinkService` does not create its own repository, a test can hand it any object that answers the same methods.

### The main path first

The first test I write for a feature is the one that proves it works when everything goes right. If that test fails, nothing else matters. For link creation, it looks like this:

```python
async def test_new_alias_is_persisted(self, mock_repository: AsyncMock) -> None:
    """A new unique alias is passed straight through to the repository."""
    link: LinkDAO = _make_link(code="mybrand1")
    mock_repository.code_exists.return_value = False
    mock_repository.create.return_value = link
    service: LinkService = _make_service(mock_repository)

    result: LinkResponse = await service.create_link(
        target_url="https://example.com",
        custom_code="mybrand1",
        expires_at=None,
        scheduler=Mock(),
    )

    mock_repository.create.assert_called_once()
    assert result.code == "mybrand1"
```

Breaking down the lines that matter:

- `code_exists.return_value = False` — the alias is free: the mock answers the question the service asks the database
- `create.return_value = link` — what the repository returns after saving, again without a database
- `scheduler=Mock()` — the background task scheduler is irrelevant here, so a plain `Mock` accepts the inspection task and does nothing with it
- `assert_called_once()` — the test checks that the service actually saved the link, not only what it returned

The main path for the redirect is shorter, because `resolve_for_redirect` only reads:

```python
async def test_active_link_returns_target_url(self, mock_repository: AsyncMock) -> None:
    """An active, non-expired link resolves to its target URL."""
    mock_repository.get_by_code.return_value = _make_link(target_url="https://example.com")
    service: LinkService = _make_service(mock_repository)

    result: str = await service.resolve_for_redirect(code="abcdefg")

    assert result == "https://example.com"
```

These two tests describe the feature in its simplest form: a link goes in, a target URL comes out.

### Then one test per rule

Next, I go down the service rows of the table and write at least one test per rule. Most of them follow the same shape: set up the mock so that the rule is violated, call the service, and check the exception with `pytest.raises`.

The collision retry is the most interesting one, because it is the rule that only a unit test can provoke. Codes are random, so an integration test would have to create millions of links to see two of them collide. With a mock, the test decides what the database answers, call after call:

```python
async def test_retries_until_unique_code_found(self, mock_repository: AsyncMock) -> None:
    """Repository is called again after a collision on an auto-generated code."""
    link = _make_link(code="abcdefg")
    # First two candidates collide; third succeeds
    mock_repository.code_exists.side_effect = [True, True, False]
    mock_repository.create.return_value = link
    service: LinkService = _make_service(mock_repository)

    result: LinkResponse = await service.create_link(
        target_url="https://example.com",
        custom_code=None,
        expires_at=None,
        scheduler=Mock(),
    )

    assert mock_repository.code_exists.call_count == 3
    assert result.code == "abcdefg"
```

`side_effect` with a list makes the mock return a different value at each call: the first two generated codes "already exist", the third is free. The test then checks that the service asked exactly three times. A twin test sets `code_exists.return_value = True` to make every attempt collide, and checks that the service gives up with a `ValidationError` instead of looping forever.

For a rule with a boundary, such as the expiry date, I test both sides of it: a link that expired yesterday must raise `LinkExpiredError`, a link that expires tomorrow must resolve normally. The test does not freeze the clock: it builds the link with an expiry relative to `now()`, which is enough to make the result deterministic.

Here is the full map from the service rules to their unit tests, all in `tests/unit/test_link_service.py`:

| **Rule** | **Mock set-up** | **Test** |
|---|---|---|
| Unique alias | `code_exists` returns `True` | `test_duplicate_alias_raises_alias_already_taken` |
| Collision retry | `code_exists` returns `True, True, False` | `test_retries_until_unique_code_found` |
| Retry limit | `code_exists` always returns `True` | `test_exceeding_max_retries_raises_validation_error` |
| No self-redirect | No mock needed | `test_self_redirect_raises_validation_error` |
| Unknown link | `get_by_code` returns `None` | `test_nonexistent_code_raises_link_not_found` |
| Inactive link | `get_by_code` returns a link with `is_active=False` | `test_inactive_link_raises_link_not_found` |
| Expired link | `get_by_code` returns a link expired yesterday | `test_expired_link_raises_link_expired` |
| Not yet expired | `get_by_code` returns a link expiring tomorrow | `test_future_expiry_does_not_raise` |

Together with the tests for listing, deleting, and re-inspecting links, the service has 19 unit tests, and the whole unit suite runs in a blink:

```shell
uv run pytest tests/unit -q
```

```text
47 passed in 0.05s
```

What these tests do not prove is equally important. They do not prove that `POST /api/v1/links` calls the service, that the repository finds a link by its code in a real table, or that `LinkExpiredError` becomes a `410`. A mistake in the exception handler would leave every unit test green.

> Unit tests prove the decisions are right: one test for the main path, then at least one per rule, both sides of every boundary.

## Integration Tests for the API

An integration test sends a real HTTP request to the real application and checks the real response. Before writing the first one, a FastAPI project has to answer three practical questions.

### Talking to the app without a server

FastAPI applications speak [ASGI](https://asgi.readthedocs.io/), the interface between a Python web application and the server that runs it. `httpx` can play the role of that server inside the test process, through [`ASGITransport`](https://www.python-httpx.org/advanced/transports/). These three lines are the core of FastURL's `api_client` fixture, which we will see in full in a moment:

```python
transport: httpx.ASGITransport = httpx.ASGITransport(app=app)
async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
    yield client
```

`ASGITransport` replaces the network layer of the client: instead of opening a socket, it calls `app` directly, as a Python function. The fixture does not call any endpoint. It yields the client, and each test sends the request it needs, for example `await api_client.post(url="/api/v1/links", json=...)`.

The client opens no port and creates no socket. The request goes through the same middleware, validation, routers, dependencies, and exception handlers as in production, but the whole round trip is a function call. The `base_url` is a placeholder: the host name is never resolved.

FastAPI also offers `TestClient`, which does the same job with a synchronous interface. FastURL uses `AsyncClient` because its tests also `await` the database session directly, and an async test can do both on the same event loop. [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) runs the `async def` tests, and one line in `pyproject.toml` enables it for every test without a decorator:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### A test database through a dependency override

In production, every request receives a database session through `get_db`, a FastAPI dependency. In a test we want a different session: one bound to a fresh, empty database that the test can also use to insert data.

FastAPI has a dedicated mechanism for this, the [`app.dependency_overrides`](https://fastapi.tiangolo.com/advanced/testing-dependencies/) dictionary. Before resolving a `Depends(...)`, FastAPI checks whether the dictionary maps that dependency to a replacement, and calls the replacement instead. FastURL wraps the override in a fixture, so it is set before the test and removed after it:

```python
@pytest.fixture()
async def api_client(db_session: AsyncSession, http_client: httpx.AsyncClient) -> AsyncIterator[httpx.AsyncClient]:
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

- `db_session` is the fixture from the previous article: a new in-memory SQLite database per test, or PostgreSQL when `TEST_DATABASE_URL` is set. Because both the test and `api_client` request it, they share the same session, so a row inserted by the test is visible to the API.
- The dictionary key is the original function object, `get_db`, not its name. FastAPI matches the function itself.
- `app` is a module-level object shared by every test in the run. The `clear()` after `yield` runs even when the test fails, so an override never leaks into the next test.

![The api_client fixture: ASGITransport and dependency overrides]({{ site.baseurl }}/assets/img/testing-fastapi-in-practice-integration-harness.svg){:width="760" height="450" loading="lazy" .responsive_img}

### A fake network for the inspector

The second override, `get_http_client`, exists because of a mistake I made. When FastURL creates a link, it schedules the background inspection that downloads the target page. In the first version of `api_client`, that task received a plain `httpx.AsyncClient()`, with full network access. Every integration test that created a link was quietly calling `https://example.com`.

The `--durations` flag gave it away: the slowest integration tests were all tests that create a link, at more than 100 ms each, while a redirect test took a few milliseconds. `ASGITransport` waits for background tasks before it returns the response, so each of those tests waited for a real round trip to a website outside the project. The suite was slower than it needed to be, it would fail on a machine without network access, and no test could check what the inspection stored, because the answer depended on someone else's web page.

The fix is the `http_client` fixture shown in the [previous article]({{ site.baseurl }}/testing-python-applications-with-pytest-patterns-for-real-code/): a real `httpx.AsyncClient` whose [`MockTransport`](https://www.python-httpx.org/advanced/transports/#mock-transports) answers every request with a small HTML page, `FAKE_PAGE`. The inspector code did not change. It still receives a real `httpx.AsyncClient`, but the client's transport answers every request from memory. The difference in the numbers:

| | **Before** | **After** |
|---|---|---|
| Full suite | 79 tests in 1.39 s | 80 tests in 0.30 s |
| Integration suite | 1.36 s | 0.22 s |
| Slowest integration test | 0.12 s | 0.01 s |
| Works offline | No | Yes |

The 80th test is the one the fix made possible: with a predictable page on the other side, a test can finally check what the inspection stores. We will meet it in a moment.

> If a test can reach the internet, sooner or later it will depend on it. Inject every client the code uses, and give tests a fake one.

### The main path first, again

With the plumbing in place, the integration tests follow the same order as the unit tests. The first one creates a link through the API:

```python
async def test_auto_code_returns_201(self, api_client: httpx.AsyncClient) -> None:
    """A valid payload without custom_code returns 201 with a generated code."""
    response: httpx.Response = await api_client.post(
        url="/api/v1/links",
        json={"target_url": "https://example.com/article"},
    )
    assert response.status_code == 201
    data = response.json()
    assert len(data["code"]) == 7
    assert data["inspection"]["status"] == "pending_analysis"
    assert data["metrics"]["clicks_count"] == 0
```

Compared to the unit test, this one proves much more with the same number of lines: the JSON body passed validation, the router called the service, the service generated a code of the configured length, the repository wrote a real row, and the response has the shape a client expects.

The second one follows the link. Here the test does not create the link through the API: it inserts it straight into the database, so a bug in the creation endpoint cannot make the redirect tests fail. The helper that does it lives at the top of [test_redirect_api.py](https://github.com/sasadangelo/fasturl/blob/v0.1.0/tests/integration/test_redirect_api.py):

```python
async def _seed_link(
    db_session: AsyncSession,
    *,
    code: str,
    target_url: str = "https://example.com",
    is_active: bool = True,
    expires_at: datetime | None = None,
) -> LinkDAO:
    """Insert a LinkDAO record directly into the test database."""
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
```

It looks like `_make_link` from the unit tests, with one difference: this `LinkDAO` is saved with `commit()`, through the same `db_session` that `api_client` injects into the app. The row is real, and the API finds it with a real `SELECT`. The test itself:

```python
async def test_active_link_returns_307(
    self,
    api_client: httpx.AsyncClient,
    db_session: AsyncSession,
) -> None:
    """A GET on an active, non-expired code returns 307 with a Location header."""
    await _seed_link(db_session, code="redir01", target_url="https://example.com/dest")

    response: httpx.Response = await api_client.get(url="/redir01", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/dest"
```

Breaking down what is specific to a redirect:

- `follow_redirects=False` — by default the client would follow the `307` to the target page; the test wants to see the redirect itself
- `response.headers["location"]` — the redirect target travels in the `Location` header, which is what a browser reads

Two more tests complete the main path, and both check the work of a background task. `test_click_count_incremented_after_redirect` follows a link and then reads the row back to check that `clicks_count` is 1. The new `test_inspection_reads_title_of_target_page` creates a link and checks that the inspector stored the title of the fake page:

```python
async def test_inspection_reads_title_of_target_page(self, api_client: httpx.AsyncClient) -> None:
    """The background inspection runs against the fake page and stores its title."""
    created: httpx.Response = await api_client.post(
        url="/api/v1/links", json={"target_url": "https://example.com"}
    )
    code: str = created.json()["code"]

    response: httpx.Response = await api_client.get(url=f"/api/v1/links/{code}")

    inspection = response.json()["inspection"]
    assert inspection["status"] == "active"
    assert inspection["title"] == "Example Domain"
```

Both tests rely on the behaviour that made the network leak so slow: `ASGITransport` runs the background tasks before the response reaches the test, so by the time the next line runs, the click is counted and the page is inspected. Without the fake network, this test would depend on the current title of `example.com`.

### Then the errors the client sees

Now the error cases. At this level I do not repeat every rule the unit tests already cover. I write one test for each error the client can receive, and one for each rule that lives in the schema, because the unit tests cannot see those. Here is the alias rule, seen from the outside:

```python
async def test_duplicate_alias_returns_409(self, api_client: httpx.AsyncClient) -> None:
    """Creating a link with an already-used custom alias returns 409."""
    payload: dict[str, str] = {"target_url": "https://example.com", "custom_code": "mybrand2"}
    await api_client.post(url="/api/v1/links", json=payload)
    response = await api_client.post(url="/api/v1/links", json=payload)
    assert response.status_code == 409
    assert response.json()["error"] == "ALIAS_ALREADY_TAKEN"
```

There is no mock here. The first request creates the alias for real, the second one collides with it in the database, and the test checks both the status code and the error code that a client would parse. The other error tests follow the same pattern:

| **Request** | **Expected** | **Test** |
|---|---|---|
| `target_url` with an `ftp://` scheme | `400 VALIDATION_ERROR` | `test_invalid_url_scheme_returns_400` |
| Alias with spaces and `!` | `400 VALIDATION_ERROR` | `test_invalid_alias_chars_returns_400` |
| `expires_at` in the past | `400 VALIDATION_ERROR` | `test_past_expiry_returns_400` |
| `target_url` pointing to FastURL itself | `400 VALIDATION_ERROR` | `test_self_redirect_returns_400` |
| The same custom alias twice | `409 ALIAS_ALREADY_TAKEN` | `test_duplicate_alias_returns_409` |
| `GET` on a code that does not exist | `404 LINK_NOT_FOUND` | `test_nonexistent_code_returns_404` |
| `GET` on a deleted link | `404 LINK_NOT_FOUND` | `test_inactive_link_returns_404` |
| `GET` on an expired link | `410 LINK_EXPIRED` | `test_expired_link_returns_410` |

The first three rows have no unit test at all, because those rules live in the Pydantic schema. The last five overlap with unit tests on purpose: the unit test proves the decision, the integration test proves the decision reaches the client as the right status code. If someone breaks the exception handler, only these tests fail.

> Integration tests prove the contract: the main path end to end, then every status code a client can receive.

## How I Choose the Test Cases

Looking back at the two levels, the method fits in four rules:

1. **Start with the main path, at both levels.** It is the cheapest test to write and the most expensive one to break. If it fails, the other tests are noise.
2. **Write at least one unit test per business rule.** For rules with a boundary (a date, a limit, a count), test both sides. Unit tests are where edge cases belong, because a mock can create situations that are hard to provoke for real, like three colliding random codes.
3. **Write one integration test per error the client can see**, and one per rule that lives outside the service (schema validation, routing). Do not copy every unit test at this level: a test that proves the same thing twice costs time and adds no confidence.
4. **Read the coverage report as a list of questions**, not as a score. A missing line means "no test has ever executed this": decide whether it deserves a test, or whether the risk is acceptable.

For the feature in this article, that gives the following split:

| | **Unit** | **Integration** |
|---|---|---|
| **Main path** | Create a link, resolve a link | Create a link, follow it, count the click, inspect the page |
| **Edge cases** | Every service rule, both sides of the expiry boundary, collisions | Only through their status code |
| **Schema rules** | Not visible | One test each |
| **Suite** | 47 tests in 0.05 s | 33 tests in 0.22 s |

## Why There Is No Third Level

The previous article described a third level: end-to-end tests, which talk to a running application from the outside, exactly as a real client would. FastURL does not have them, and it is a deliberate choice.

An integration test like `test_active_link_returns_307` already exercises an HTTP request, every middleware, request validation, routing, dependency injection, the service, the repository, real SQL, and the response a client receives. The only things between this test and a real client are the uvicorn server process and the network socket. For an API with no authentication, no frontend, and no other service to talk to, an end-to-end test would send the same requests, receive the same responses, and take longer, because each test would pay for a real server and a real socket. In FastURL, the integration suite *is* the end-to-end suite.

What the in-process client skips is small but real, and the coverage report shows it:

```text
Name                                          Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------------------------
src/fasturl/core/log.py                          52     34      6      0    31%   41-52, 81-90, 95-112, ...
src/fasturl/main.py                              37     12      2      0    64%   36-68
...
TOTAL                                           668     58     72      7    90%
```

Lines 36 to 68 of `main.py` are the `lifespan` function, which configures logging, creates the database engine, and creates the shared HTTP client when the server starts. `ASGITransport` never sends the startup and shutdown events, so not one test runs it, and most of the missing lines in `log.py` are called from there. For FastURL today, the startup sequence is tested by hand, every time I start the server.

A separate end-to-end suite starts to earn its place when the deployment becomes part of the product (a Docker image whose configuration can break without any code changing), when something sits in front of the API (authentication, a reverse proxy), or when there is more than one process. FastURL's [test strategy](https://github.com/sasadangelo/fasturl/blob/v0.1.0/docs/test-strategy.md) puts that step at the milestone that introduces authentication and containerised deployment.

> Add a test level when it can catch a failure the other levels cannot. Before that, it is a slower copy of tests you already have.

## Conclusion

In this article we covered:

- How to turn a feature into a test plan: list its rules, find the layer each rule lives in, and let that decide which level can test it.
- Unit tests for `LinkService`: the main path first, then one test per rule, with `return_value` to answer the service's questions, `side_effect` to script colliding codes, and `assert_called_once` to check that the link was saved.
- How FastAPI integration tests work: `httpx.AsyncClient` with `ASGITransport` to call the app without a server, and `app.dependency_overrides` inside a yield fixture to inject a test database.
- How a plain HTTP client let every integration test call `example.com`, and how a `MockTransport` client injected as a dependency cut the suite from 1.39 to 0.30 seconds and made the background inspection testable.
- Integration tests for the main path and for every error a client can receive, including the schema rules that unit tests cannot see.
- Why FastURL's integration suite doubles as its end-to-end suite, what the in-process client does not see, and which changes would justify a separate end-to-end level.

This article closes the FastURL implementation arc. The project now has a domain model, a layered architecture, async I/O, background inspection, a consistent error contract, and a test suite that runs offline in a third of a second, on SQLite or PostgreSQL, behind the 85% [coverage gate]({{ site.baseurl }}/testing-python-applications-with-pytest-patterns-for-real-code/).

The [next article]({{ site.baseurl }}/api-design-requests-and-responses/) returns to API design, with the decisions that the first FastURL version left open: when to use path, query, body, or header parameters, how to paginate a collection, and how to version an API without breaking its clients.

---

If you enjoyed this article, don't forget to **give it a clap 👏**, **share it with your friends 🔗**, and **follow me for more tips and tutorials on software development 📘**. Your support helps me create more content like this — thank you! 🙌

**Note**: English is not my native language, and this article was drafted with the assistance of AI. However, all the ideas, projects, concepts, and content are entirely my own.
