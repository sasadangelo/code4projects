---
layout: post
title: "Async, Background Tasks, and Error Handling in FastAPI"
post_series_id:
  - modern-python-application
  - building-rest-apis
date: 2026-10-06
author: sasadangelo
slug: fastapi-async-background-tasks-and-error-handling
image: /assets/img/fastapi-async-background-tasks-and-error-handling-hero.svg
excerpt: "Async I/O, fire-and-forget background tasks, a shared httpx client, and three global exception handlers in FastAPI — grounded in the FastURL project."
categories:
  - "Programming"
---


![Async, Background Tasks, and Error Handling in FastAPI]({{ site.baseurl }}/assets/img/fastapi-async-background-tasks-and-error-handling-hero.svg){:width="760" height="400" .responsive_img}

## Introduction

In the [previous article]({{ site.baseurl }}/layered-architecture-with-fastapi-routers-services-and-repositories/) we organized [FastURL](https://github.com/sasadangelo/fasturl) — our open-source URL shortener — into clean layers: routers, services, repositories, and a dependency injection system that wires them together. The structure is in place; now we need to make it behave correctly at runtime.

Three things have to work right in any production FastAPI application that does non-trivial work:

- **Async I/O** must be used correctly so the event loop is never blocked.
- **Background tasks** must fire without delaying the HTTP response.
- **Error handling** must produce a predictable, machine-readable envelope for every possible failure.

This article covers all three, using FastURL as the concrete project.

You should read this article if:

- You understand async/await in Python but are unsure which handlers in FastAPI should be `async def` and which should be `def`.
- You want to implement fire-and-forget background work in FastAPI without introducing an external broker.
- You want a single, consistent error envelope across Pydantic validation failures, domain exceptions, and unhandled errors.

This article is part of the [Modern Python Application]({{ site.baseurl }}/how-to-set-up-your-next-python-project/) series and the FastURL sub-series.

## Async I/O in FastAPI: `async def` vs `def`

Think of a highway with a single lane: every vehicle must wait for the one in front to clear before it can move. A blocking route handler is that stuck vehicle — while it waits for a database query or an HTTP call to return, no other request can be processed. FastAPI runs on an [async event loop]({{ site.baseurl }}/async-and-event-loop-in-python-asyncio-in-practice/) — the same model we covered in depth in the asyncio article — so every `await` is a legal overtaking lane: the handler suspends, the event loop runs something else, and the handler resumes when the I/O is ready.

The rule is simple:

> If a handler calls anything that involves I/O — database queries, outbound HTTP, file reads — declare it `async def` and `await` every call. If it does only CPU work, use plain `def`.

FastAPI handles both correctly. A plain `def` route is run in a thread pool so it does not block the event loop. An `async def` route runs directly on the loop. The mistake to avoid is mixing the two: an `async def` that calls a blocking library (like `requests` or synchronous SQLAlchemy) blocks the event loop entirely, stalling every other request in the process. If you are new to the concurrency model underlying this, the [concurrency in Python]({{ site.baseurl }}/concurrency-in-python-threads-processes-and-the-event-loop/) article covers threads, processes, and the event loop side by side.

The table below maps the most common blocking operations to their async replacements:

| **Operation** | **Blocking (do not use in `async def`)** | **Async replacement** |
|---|---|---|
| **HTTP requests** | `requests.get(url)` | `await httpx.AsyncClient().get(url)` or `aiohttp` |
| **Database queries** | `sqlalchemy.Session.execute(...)` | `await sqlalchemy.ext.asyncio.AsyncSession.execute(...)` |
| **File I/O** | `open(path).read()` | `await aiofiles.open(path)` (`aiofiles` package) |
| **Sleep / delay** | `time.sleep(n)` | `await asyncio.sleep(n)` |
| **DNS / socket** | `socket.getaddrinfo(...)` | `await asyncio.get_event_loop().getaddrinfo(...)` |
| **Subprocess** | `subprocess.run(...)` | `await asyncio.create_subprocess_exec(...)` |
| **Redis** | `redis.Redis().get(key)` | `await redis.asyncio.Redis().get(key)` (`redis-py` ≥ 4.2) |
| **PostgreSQL** | `psycopg2.connect(...)` | `asyncpg` or `psycopg` (v3 async) |

If an existing library has no async version, wrap the blocking call in `await asyncio.get_event_loop().run_in_executor(None, blocking_fn)` to offload it to a thread pool without stalling the loop. The [asyncio docs](https://docs.python.org/3/library/asyncio.html) cover the full executor API.

In FastURL every route handler is `async def` because every one of them calls either the async repository (SQLAlchemy `AsyncSession`) or the background inspector (`httpx.AsyncClient`). Here is the `create_link` handler in full:

```python
@router.post(
    path="",
    response_model=LinkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_link(
    body: LinkCreateRequest,
    service: LinkServiceDep,
    http_client: HTTPClientDep,
    background_tasks: BackgroundTasks,
) -> LinkResponse:
    response: LinkResponse = await service.create_link(
        target_url=str(body.target_url),
        custom_code=body.custom_code,
        expires_at=body.expires_at,
    )
    background_tasks.add_task(
        func=inspect_link,
        code=response.code,
        target_url=response.target_url,
        http_client=http_client,
        repository=service._repository,
    )
    return response
```

`await service.create_link(...)` yields control to the event loop while the database insert is in flight. By the time the `return` statement executes, the link is persisted and the response is ready. The background inspection — which involves an outbound HTTP call to the target URL — is dispatched via `BackgroundTasks` and never blocks the response. More on that in the next section.

### The shared `httpx.AsyncClient`

The `http_client` parameter above comes from `app.state`. Creating a new `httpx.AsyncClient` per request is the most common mistake in async FastAPI code: each new client opens a fresh connection pool, establishes a TCP handshake, and discards both when the request ends. With any meaningful traffic, you get hundreds of redundant connections per second. The [httpx docs on connection pooling](https://www.python-httpx.org/advanced/connection-pools/) explain the mechanics in detail.

The right pattern is one shared client per application, created at startup and closed at shutdown. FastAPI's `lifespan` context manager is exactly the right place for it:

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import httpx
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # --- Startup ---
    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(10.0),
        follow_redirects=True,
        max_redirects=5,
        headers={"User-Agent": "FastURL-Inspector/0.1"},
    )
    yield
    # --- Shutdown ---
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)
```

Breaking down the `httpx.AsyncClient` options:

- `timeout=httpx.Timeout(10.0)` — caps the full request lifecycle (connect + read) at 10 seconds; without a timeout a hanging target URL would hold an open connection indefinitely
- `follow_redirects=True` — the inspector must reach the final destination to extract accurate metadata
- `max_redirects=5` — prevents infinite redirect loops from consuming the client
- `headers={"User-Agent": "..."}` — many servers return `403` for requests that look like anonymous bots; a descriptive `User-Agent` prevents that class of silent failure

The client is retrieved inside a FastAPI dependency and injected into route handlers via `HTTPClientDep`:

```python
def _get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client

HTTPClientDep: TypeAlias = Annotated[httpx.AsyncClient, Depends(_get_http_client)]
```

> One `httpx.AsyncClient` per application, opened in `lifespan`, closed on shutdown. Never create a client inside a route handler or a background task.

The full implementation is in [main.py](https://github.com/sasadangelo/fasturl/blob/main/src/fasturl/main.py).

### The shared database engine

The same principle applies to the SQLAlchemy async engine. The engine owns the **connection pool** — the set of persistent database connections that are checked out per request and returned when the session closes. Creating a new engine per request would open a fresh pool, perform the SQLite handshake, and discard both at the end of the request, identical to the `httpx.AsyncClient` mistake. We first introduced SQLAlchemy's async session in the [database layer article]({{ site.baseurl }}/database-layer-with-sqlalchemy-in-a-layered-python-architecture/) — see that article for the full ORM setup. The [SQLAlchemy async docs](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) cover engine and session lifecycle in depth.

The engine and session factory are created once at startup and disposed at shutdown inside two helpers, `init_db()` and `close_db()`, defined in [database.py](https://github.com/sasadangelo/fasturl/blob/main/src/fasturl/core/database.py):

```python
# database.py
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None

async def init_db() -> None:
    global _engine, _session_factory
    _engine = create_async_engine(url=settings.database.url, echo=settings.database.echo)
    _session_factory = async_sessionmaker(bind=_engine, class_=AsyncSession, expire_on_commit=False)
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db() -> None:
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
```

Both are called from the `lifespan` context manager in [main.py](https://github.com/sasadangelo/fasturl/blob/main/src/fasturl/main.py):

```python
# main.py
await init_db()   # startup
yield
await close_db()  # shutdown — engine.dispose() flushes and closes all pooled connections
```

The per-request session is a separate concern. A session is **not** safe to share across requests: it carries per-request transaction state and is not coroutine-safe. The `get_db` dependency opens a fresh session from the shared factory for every request and closes it automatically when the request ends:

```python
async def get_db() -> AsyncIterator[AsyncSession]:
    async with _session_factory() as session:
        yield session
```

Calling `_session_factory()` is cheap — it checks out a connection from the pool that already exists in the engine; it does not open a new one. The pool is reused; only the session object is fresh.

This creates an important asymmetry between the two shared resources:

| Resource | Scope | Reason |
|---|---|---|
| `httpx.AsyncClient` | Application — one instance | Stateless; connection pool is coroutine-safe |
| `AsyncEngine` | Application — one instance | Stateless; connection pool is coroutine-safe |
| `async_sessionmaker` | Application — one instance | Cheap factory; just wraps the engine |
| `AsyncSession` | Request — one per request | Carries transaction state; not safe to share |

> One `AsyncEngine` per application, opened in `lifespan`, disposed on shutdown. One `AsyncSession` per request, opened by `get_db`, closed after the request. Never share a session across requests.

The full implementation is in [database.py](https://github.com/sasadangelo/fasturl/blob/main/src/fasturl/core/database.py).

![Application Lifespan — Shared Resource Lifecycle]({{ site.baseurl }}/assets/img/fastapi-async-background-tasks-and-error-handling-lifespan.svg){:width="760" height="420" .responsive_img}

## Background Tasks: Fire-and-Forget Without a Broker

When a new link is created, FastURL must immediately return a `201 Created` response to the caller. But it also needs to check the target URL's health, record its HTTP status code and latency, and extract the HTML title and OpenGraph metadata. These operations take hundreds of milliseconds — far too long to include in the response cycle.

FastAPI's `BackgroundTasks` solves this without any external infrastructure. A `BackgroundTask` is a coroutine (or a plain function) that FastAPI runs after the response has been sent to the client. The route handler returns immediately; the background work executes in the same event loop, after Starlette finishes streaming the response bytes.

```python
background_tasks.add_task(
    func=inspect_link,
    code=response.code,
    target_url=response.target_url,
    http_client=http_client,
    repository=service._repository,
)
```

Breaking down the arguments:

- `func=inspect_link` — the coroutine function to run; FastAPI detects `async def` and awaits it automatically
- `code` and `target_url` — positional arguments forwarded to `inspect_link`
- `http_client` — the shared `httpx.AsyncClient` from `app.state`; the background task must reuse it, not create its own
- `repository=service._repository` — the `LinkRepository` instance, already bound to the current database session via dependency injection

### What `inspect_link` does

`inspect_link` is a pure async function in [inspector_service.py](https://github.com/sasadangelo/fasturl/blob/main/src/fasturl/services/inspector_service.py). It has zero FastAPI imports — it knows nothing about HTTP requests, response models, or routing. This is the key constraint that keeps the service layer testable:

```python
async def inspect_link(
    code: str,
    target_url: str,
    http_client: httpx.AsyncClient,
    repository: LinkRepository,
) -> None:
    status = "unreachable"
    http_status_code: int | None = None
    latency_ms: float | None = None
    title: str | None = None
    description: str | None = None
    image_url: str | None = None

    start = time.monotonic()
    try:
        response = await http_client.get(target_url)
        latency_ms = round((time.monotonic() - start) * 1000, 2)
        http_status_code = response.status_code

        if response.is_success or response.is_redirect:
            status = "active"
            html = response.text
            title = _extract_title(html)
            description = _extract_description(html)
            image_url = _extract_image_url(html)
        else:
            status = "unreachable"

    except httpx.TimeoutException:
        latency_ms = round((time.monotonic() - start) * 1000, 2)

    except httpx.RequestError as exc:
        latency_ms = round((time.monotonic() - start) * 1000, 2)

    await repository.update_inspection(
        code,
        status=status,
        http_status_code=http_status_code,
        latency_ms=latency_ms,
        title=title,
        description=description,
        image_url=image_url,
    )
```

The `try/except` block covers two failure modes: `httpx.TimeoutException` for deadline expiry and `httpx.RequestError` for DNS failures, refused connections, and similar network-level errors. In both cases the `status` remains `"unreachable"` and the inspection result is persisted so the caller can see the link was checked but unreachable — rather than leaving the status permanently at `"pending_analysis"`.

The metadata extraction uses three lightweight regex helpers — `_extract_title`, `_extract_description`, `_extract_image_url` — that parse the raw HTML string without adding a full parser dependency. They are pure synchronous functions: by the time they run, the HTTP response body is already in memory, so there is no I/O to await.

![Background Task Sequence — Fire and Forget]({{ site.baseurl }}/assets/img/fastapi-async-background-tasks-and-error-handling-sequence.svg){:width="760" height="460" .responsive_img}

### `BackgroundTasks` vs an external broker

`BackgroundTasks` is not a replacement for a job queue like Celery, RQ, or a message broker. The comparison is worth making explicit:

| | **`BackgroundTasks`** | **External broker (Celery / RQ / etc.)** |
|---|---|---|
| **Infrastructure** | None — runs in the same process | Requires Redis, RabbitMQ, or similar |
| **Durability** | Lost if the process crashes | Persisted; survives restarts |
| **Retries** | Manual — must be coded explicitly | Built-in retry policies |
| **Scalability** | Bounded by the web process | Dedicated worker pool |
| **Best for** | Low-latency, non-critical side effects | Critical work that must not be lost |

FastURL's inspection task is a good fit for `BackgroundTasks`: losing an inspection on a crash is acceptable — the client can re-trigger it via `POST /api/v1/links/{code}/inspect`. A payment processing step or an email confirmation would not be acceptable candidates.

![BackgroundTasks vs External Broker]({{ site.baseurl }}/assets/img/fastapi-async-background-tasks-and-error-handling-broker.svg){:width="760" height="380" .responsive_img}

## Error Handling: One Envelope for Every Failure

A client that calls a production API must be able to branch on the response without parsing human-readable text. The FastURL error contract guarantees this with a single JSON shape for every failure. The [FastAPI exception handlers docs](https://fastapi.tiangolo.com/tutorial/handling-errors/) describe the default behaviour we are overriding here:

```json
{
  "success": false,
  "error": "LINK_NOT_FOUND",
  "details": [
    "code -> No link found with code 'aB3x9zK'"
  ]
}
```

- `success` — always `false` on error; useful for clients that check this flag before parsing the body
- `error` — a machine-readable short code; clients branch on this field
- `details` — a list of human-readable, field-level explanations; used for logging and developer messages

Three global handlers registered in `main.py` cover every failure path.

### Handler 1: Pydantic validation failures (400)

When FastAPI receives a request body or query parameter that fails Pydantic validation, it raises `RequestValidationError`. The default FastAPI behaviour returns a `422 Unprocessable Entity` — but `422` is rarely what API clients expect for bad input. FastURL overrides this to `400 Bad Request`:

```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    error_details: list[str] = []
    for e in exc.errors():
        loc = " -> ".join(str(x) for x in e["loc"])
        msg = e["msg"]
        error_details.append(f"{loc}: {msg}")
    return JSONResponse(
        status_code=400,
        content={"success": False, "error": "VALIDATION_ERROR", "details": error_details},
    )
```

`exc.errors()` returns a list of Pydantic error dicts. Each dict has a `loc` tuple (field path) and a `msg` string. The handler flattens the location into a readable `"body -> target_url: value is not a valid URL"` string and collects all errors into the `details` list — so a single response surfaces every validation failure at once, not just the first one.

### Handler 2: Domain exceptions (4xx)

Domain exceptions are pure Python classes with zero FastAPI imports. They carry the HTTP status code and error payload, but they know nothing about `JSONResponse` or routing. The full set of exceptions lives in [exceptions.py](https://github.com/sasadangelo/fasturl/blob/main/src/fasturl/core/exceptions.py):

```python
class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400, details: list[str] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details: list[str] = details or []

class LinkNotFoundError(AppError):
    def __init__(self, code: str) -> None:
        super().__init__(
            message="LINK_NOT_FOUND",
            status_code=404,
            details=[f"code -> No link found with code '{code}'"],
        )

class LinkExpiredError(AppError):
    def __init__(self, code: str, expired_at: str) -> None:
        super().__init__(
            message="LINK_EXPIRED",
            status_code=410,
            details=[f"code -> Link '{code}' expired on {expired_at}"],
        )
```

The global handler converts any `AppError` subclass into the standard envelope:

```python
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.message, "details": exc.details},
    )
```

The service layer raises `LinkNotFoundError`, `AliasAlreadyTakenError`, or `LinkExpiredError` without ever importing FastAPI. The HTTP layer sees the exception, the handler serialises it, the client gets a consistent envelope. The layers stay clean.

### Handler 3: Unhandled exceptions (500)

The third handler is the safety net. Any exception that escapes the service and repository layers — a database connection drop, a bug, an unexpected `None` — reaches this handler. It logs the full traceback server-side and returns a generic message to the client:

```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    logger.error(f"Unhandled exception at {request.url}:\n{tb}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "INTERNAL_SERVER_ERROR",
            "details": ["An unexpected error occurred. Please contact support."],
        },
    )
```

The traceback goes to the server log — never to the client. Leaking stack traces to API consumers is an information disclosure vulnerability: it reveals internal class names, file paths, and sometimes configuration values. The client sees only the generic message and the correlation ID header (`X-Request-ID`) that makes the server log entry findable.

### The complete handler mapping

| Handler | Triggered by | HTTP status |
|---|---|---|
| `RequestValidationError` | Pydantic schema validation failure | 400 |
| `AppError` | Domain rule violation | 404 / 409 / 410 |
| `Exception` | Any unhandled error | 500 |

The full registration of all three handlers is in [exceptions.py](https://github.com/sasadangelo/fasturl/blob/main/src/fasturl/core/exceptions.py).

## Conclusion

In this article we covered:

- Why every I/O-bound route handler must be `async def` and why mixing `async def` with blocking libraries stalls the entire event loop.
- How to create a single shared `httpx.AsyncClient` in the FastAPI `lifespan` context and inject it via a dependency — and why creating a client per request destroys connection pooling.
- How the same principle applies to the SQLAlchemy `AsyncEngine`: one engine per application, opened in `lifespan`, disposed on shutdown — with a fresh `AsyncSession` per request opened by the `get_db` dependency.
- How `BackgroundTasks` runs `inspect_link` after the `201 Created` response is sent, keeping the HTTP cycle fast while the background work happens asynchronously in the same process.
- When `BackgroundTasks` is the right tool and when an external broker is necessary — durability, retry policies, and scale are the deciding factors.
- How three global exception handlers produce a single `{success, error, details}` envelope for Pydantic validation failures, domain exceptions, and unhandled errors — with no stack traces leaking to clients.

The next article in the [Modern Python Application]({{ site.baseurl }}/how-to-set-up-your-next-python-project/) series will go deeper into testing patterns for Python applications — pytest fixtures, async tests, and coverage strategies for real production code.

---

If you enjoyed this article, don't forget to **give it a clap 👏**, **share it with your friends 🔗**, and **follow me for more tips and tutorials on software development 📘**. Your support helps me create more content like this — thank you! 🙌

**Note**: English is not my native language, and this article was drafted with the assistance of AI. However, all the ideas, projects, concepts, and content are entirely my own.
