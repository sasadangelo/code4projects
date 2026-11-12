---
layout: post
title: "Layered Architecture with FastAPI: Routers, Services, and Repositories"
seo_title: "Layered Architecture with FastAPI: Routers and Services"
post_series_id:
  - modern-python-application
  - building-rest-apis
date: 2026-10-04
author: sasadangelo
slug: layered-architecture-with-fastapi-routers-services-and-repositories
image: /assets/img/layered-architecture-with-fastapi-routers-services-and-repositories-hero.png
excerpt: "Learn how to structure a production-ready FastAPI project using a layered architecture: Routers, Services, Repositories, and Dependency Injection."
categories:
  - "Programming"
tags:
  - python
---


![Layered Architecture with FastAPI: Routers, Services, and Repositories]({{ site.baseurl }}/assets/img/layered-architecture-with-fastapi-routers-services-and-repositories-hero.png){:width="760" height="400" .responsive_img}

## Introduction

In the [previous article]({{ site.baseurl }}/from-domain-design-to-rest-api-building-fasturl-with-fastapi/) we defined the domain model and API contract for **FastURL**, our open-source URL shortener and link inspector service hosted on [GitHub](https://github.com/sasadangelo/fasturl). We established how requirements turn into domain entities, how Pydantic v2 schemas act as Value Objects, and how a consistent error envelope isolates clients from internal failure mechanics.

Designing endpoints and validation rules is essential, but code needs a clean home to live in. If you put database queries, HTTP handling, business validation, and external network requests into a single route function, your application will quickly turn into an unmaintainable monolith. We previously explored structuring a [database layer with SQLAlchemy]({{ site.baseurl }}/database-layer-with-sqlalchemy-in-a-layered-python-architecture/) and managing [asyncio event loop concurrency]({{ site.baseurl }}/async-and-event-loop-in-python-asyncio-in-practice/); now we bring those principles together in an API context.

This article shows how to organize a real-world [FastAPI](https://fastapi.tiangolo.com/) application into clean, isolated layers: **Routers**, **Services**, and **Repositories**, connected together seamlessly through FastAPI's **Dependency Injection** system. All the code refers to FastURL [v0.1.0](https://github.com/sasadangelo/fasturl/tree/v0.1.0).

You should read this article if:

- You want to structure a production-grade FastAPI codebase beyond trivial single-file tutorials.
- You want to decouple business logic from HTTP frameworks and database ORMs.
- You want to master async SQLAlchemy 2.0 repositories and FastAPI dependency injection (`Depends`).

## The Problem with Fat Route Handlers

Imagine an endpoint that receives a URL shortening request, checks database duplicates, executes an insert, sends a background notification, and formats the JSON response all within the same 50-line route function. 

While this works for simple scripts, it fails in production:

1. **No reusability**: If a background worker or CLI needs to shorten a URL, it cannot reuse the route logic without importing HTTP request objects.
2. **Untestable logic**: Unit testing business rules requires spinning up mock HTTP clients and a live database instance.
3. **Leaky abstractions**: The HTTP layer is tightly coupled to database schema details, table column names, and ORM session states.

To prevent this decay, we structure FastURL using a classic **Layered Architecture**.

![FastURL layered architecture: router, service, and repository responsibilities]({{ site.baseurl }}/assets/img/layered-architecture-with-fastapi-routers-services-and-repositories-overview.png){:width="760" height="400" .responsive_img}

> The dependency arrow points strictly downward: Routers depend on Services, and Services depend on Repositories. Lower layers never know about the layers above them.

## Real Project Folder Structure

Here is how the [FastURL codebase](https://github.com/sasadangelo/fasturl) is organized inside `src/fasturl/`:

```text
fasturl/
├── config.yaml                # Application configuration file
├── pyproject.toml             # Dependencies and build configuration (uv / PEP 621)
├── sql/
│   └── schema.sql             # Reference SQL schema definition
├── src/
│   └── fasturl/
│       ├── api/               # Router layer: endpoints, schemas, dependencies
│       │   ├── dependencies/  # FastAPI dependency providers (Depends factories)
│       │   ├── middleware/    # HTTP middleware (CORS, error handling, etc.)
│       │   ├── routers/       # APIRouter definitions (links, redirect)
│       │   └── schemas/       # Pydantic request and response DTO schemas
│       ├── core/              # Cross-cutting: configuration, logging, database, exceptions
│       │   ├── config/        # Pydantic Settings modules (app, db, log, inspector)
│       │   ├── database.py    # Async SQLAlchemy engine & session factory
│       │   ├── exceptions.py  # Domain error hierarchy (AppError, ValidationError, etc.)
│       │   └── log.py         # Loguru structured logging configuration
│       ├── models/            # SQLAlchemy ORM models (table mappings)
│       │   └── link.py
│       ├── repositories/      # Data access layer (async repositories)
│       │   └── link_repository.py
│       ├── services/          # Business logic layer (LinkService, InspectorService)
│       │   ├── inspector_service.py
│       │   └── link_service.py
│       └── main.py            # FastAPI application factory, lifespan, router registration
└── tests/
    ├── unit/                  # Fast isolated unit tests (mocked repositories)
    └── integration/           # HTTP tests through httpx.ASGITransport (SQLite or PostgreSQL)
```

Each module has a clearly delineated responsibility:

- **[`models/`](https://github.com/sasadangelo/fasturl/tree/v0.1.0/src/fasturl/models)**: Houses SQLAlchemy declarative ORM mappings.
- **[`repositories/`](https://github.com/sasadangelo/fasturl/tree/v0.1.0/src/fasturl/repositories)**: Contains classes that handle raw SQL operations and query execution using [`AsyncSession`](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html).
- **[`services/`](https://github.com/sasadangelo/fasturl/tree/v0.1.0/src/fasturl/services)**: Encapsulates pure domain workflows and business rules. Free of any HTTP framework dependencies.
- **[`api/`](https://github.com/sasadangelo/fasturl/tree/v0.1.0/src/fasturl/api)**: Contains FastAPI routers, input/output schemas (DTOs), and dependency injection wiring.
- **[`core/`](https://github.com/sasadangelo/fasturl/tree/v0.1.0/src/fasturl/core)**: Provides infrastructure foundations:
  - **`config/`**: Type-safe settings with [Pydantic Settings]({{ site.baseurl }}/managing-application-configuration-in-python-with-pydantic-settings/) across application, database, and logging domains.
  - **`database.py`**: Async SQLAlchemy session lifecycle and engine initialization, expanding on our [SQLAlchemy database layer]({{ site.baseurl }}/database-layer-with-sqlalchemy-in-a-layered-python-architecture/).
  - **`log.py`**: Structured application logging with [Loguru]({{ site.baseurl }}/logging-in-a-flask-application-with-loguru/).
  - **`exceptions.py`**: Clean domain error hierarchy (`AppError`, `ValidationError`, `LinkNotFoundError`).

## Domain Model Mapping: Embedding Value Objects in the ORM

In FastURL's domain design, the `Link` entity is the Aggregate Root. Its Value Objects — `ShortCode`, `TargetUrl`, `LinkInspection`, and `LinkMetrics` — do not have separate lifecycle identities.

In the database, we map this domain structure to a clean single-table schema (`links`), embedding the Value Object properties as flat columns.

Here is the SQLAlchemy 2.0 ORM model in [`src/fasturl/models/link.py`](https://github.com/sasadangelo/fasturl/blob/v0.1.0/src/fasturl/models/link.py):

```python
from datetime import UTC, datetime
from sqlalchemy import Boolean, DateTime, Enum, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""

INSPECTION_STATUSES: tuple[str, ...] = ("pending_analysis", "active", "unreachable")

class LinkDAO(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(length=16), nullable=False, unique=True, index=True)
    target_url: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=None)

    # LinkInspection Value Object — embedded columns
    inspection_status: Mapped[str] = mapped_column(
        Enum(*INSPECTION_STATUSES, name="inspection_status", create_constraint=True),
        nullable=False,
        default="pending_analysis",
    )
    http_status_code: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    latency_ms: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)
    title: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    description: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=None)

    # LinkMetrics Value Object — embedded columns
    clicks_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_clicked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=None)

    # Audit timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC).replace(tzinfo=None),
        onupdate=lambda: datetime.now(UTC).replace(tzinfo=None),
    )
```

The class is called `LinkDAO` (Data Access Object) to keep it distinct from the `Link` aggregate of the domain model: it is the table mapping, not the domain concept. `inspection_status` is a native `ENUM` on PostgreSQL and a `VARCHAR` with a `CHECK` constraint on SQLite, so the database itself rejects unknown statuses.

Notice a key design decision: the surrogate primary key `id` is internal only. The sole public identifier is `code` (the 7–16 character Base62 string), which is indexed and unique.

## The Repository Layer: Async Data Access

The Repository (`LinkRepository` in [`src/fasturl/repositories/link_repository.py`](https://github.com/sasadangelo/fasturl/blob/v0.1.0/src/fasturl/repositories/link_repository.py)) has a single job: encapsulate SQL operations using SQLAlchemy's async engine. It contains no business logic, no status code definitions, and no pricing rules.

```python
from datetime import UTC, datetime
from sqlalchemy import select, update
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from fasturl.models.link import LinkDAO

class LinkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_code(self, code: str) -> LinkDAO | None:
        """Return the link with the given code, or None if not found."""
        result: Result[LinkDAO] = await self._session.execute(
            select(LinkDAO).where(LinkDAO.code == code)
        )
        return result.scalar_one_or_none()

    async def create(self, link: LinkDAO) -> LinkDAO:
        """Persist a new link record and return the refreshed instance."""
        self._session.add(instance=link)
        await self._session.commit()
        await self._session.refresh(instance=link)
        return link

    async def soft_delete(self, code: str) -> bool:
        """Set is_active = False for the link with the given code."""
        result: Result[int] = await self._session.execute(
            update(table=LinkDAO)
            .where(LinkDAO.code == code)
            .values(is_active=False, updated_at=datetime.now(UTC).replace(tzinfo=None))
            .returning(LinkDAO.id)
        )
        await self._session.commit()
        return result.scalar_one_or_none() is not None

    async def increment_clicks(self, code: str) -> None:
        """Atomically increment clicks_count and update last_clicked_at."""
        now = datetime.now(UTC).replace(tzinfo=None)
        await self._session.execute(
            update(LinkDAO)
            .where(LinkDAO.code == code)
            .values(
                clicks_count=LinkDAO.clicks_count + 1,
                last_clicked_at=now,
                updated_at=now,
            )
        )
        await self._session.commit()

    async def code_exists(self, code: str) -> bool:
        """Return True if any link uses the given code."""
        result: Result[int] = await self._session.execute(
            select(LinkDAO.id).where(LinkDAO.code == code)
        )
        return result.scalar_one_or_none() is not None
```

All methods are fully asynchronous and use type-safe SQLAlchemy 2.0 select and update constructs. Notice that updates like `increment_clicks` use database-level atomic increments (`clicks_count = LinkDAO.clicks_count + 1`) to eliminate race conditions under concurrent traffic. The timestamps come from Python in UTC, like every other timestamp in FastURL: the database's `now()` returns server-local time on PostgreSQL but UTC on SQLite.

## The Service Layer: Pure Business Logic

The Service layer (`LinkService` in [`src/fasturl/services/link_service.py`](https://github.com/sasadangelo/fasturl/blob/v0.1.0/src/fasturl/services/link_service.py)) is the brain of the application. It orchestrates business workflows, generates random Base62 codes, handles code collision retries, and raises domain exceptions.

Crucially, **`LinkService` has zero knowledge of FastAPI or HTTP**. It does not import `Request`, `Response`, `HTTPException`, or even `BackgroundTasks`.

```python
import secrets
import string
from datetime import UTC, datetime
from loguru import logger
from fasturl.api.schemas.link_schemas import LinkResponse
from fasturl.core.config import settings
from fasturl.core.exceptions import AliasAlreadyTakenError, LinkExpiredError, LinkNotFoundError, ValidationError
from fasturl.models.link import LinkDAO
from fasturl.repositories.link_repository import LinkRepository
from fasturl.services.inspector_service import BackgroundTaskScheduler, InspectorService

_log = logger.bind(name="LinkService")
_BASE62_ALPHABET = string.ascii_letters + string.digits
_MAX_CODE_RETRIES = 10

class LinkService:
    def __init__(self, repository: LinkRepository, inspector: InspectorService) -> None:
        self._repository = repository
        self._inspector = inspector

    def _generate_code(self) -> str:
        """Generate a random Base62 code of the configured length."""
        length = settings.app.code_length
        return "".join(secrets.choice(_BASE62_ALPHABET) for _ in range(length))

    def _validate_target_url(self, target_url: str) -> None:
        """Enforce self-redirect loop prevention."""
        base = settings.app.base_url.rstrip("/").lower()
        if target_url.lower().startswith(base):
            raise ValidationError(["target_url -> URL must not point back to this service (self-redirect)"])

    async def create_link(
        self,
        target_url: str,
        custom_code: str | None,
        expires_at: datetime | None,
        scheduler: BackgroundTaskScheduler,
    ) -> LinkResponse:
        """Create a new shortened link and schedule its background inspection."""
        self._validate_target_url(target_url)

        if custom_code is not None:
            if await self._repository.code_exists(code=custom_code):
                raise AliasAlreadyTakenError(alias=custom_code)
            code: str = custom_code
        else:
            # Collision-retry loop for auto-generated codes
            for _ in range(_MAX_CODE_RETRIES):
                candidate = self._generate_code()
                if not await self._repository.code_exists(code=candidate):
                    code = candidate
                    break
            else:
                _log.error("Failed to generate a unique code after max retries")
                raise ValidationError(["code -> Could not generate a unique short code. Please try again."])

        now: datetime = datetime.now(UTC).replace(tzinfo=None)
        link = LinkDAO(
            code=code,
            target_url=target_url,
            is_active=True,
            expires_at=expires_at,
            inspection_status="pending_analysis",
            clicks_count=0,
            created_at=now,
            updated_at=now,
        )
        persisted = await self._repository.create(link)
        _log.info(f"Link created: code='{code}', target='{target_url}'")
        self._inspector.dispatch_inspection(
            scheduler=scheduler,
            code=persisted.code,
            target_url=persisted.target_url,
            repository=self._repository,
        )
        return _orm_to_response(link=persisted)

    async def resolve_for_redirect(self, code: str) -> str:
        """Resolve a short code for redirect, validating active status and expiry."""
        link = await self._repository.get_by_code(code)
        if link is None or not link.is_active:
            raise LinkNotFoundError(code)

        if link.expires_at is not None:
            expires = link.expires_at.replace(tzinfo=None) if link.expires_at.tzinfo else link.expires_at
            if datetime.now(UTC).replace(tzinfo=None) > expires:
                raise LinkExpiredError(code, expired_at=link.expires_at.isoformat())

        return link.target_url

    async def increment_clicks(self, code: str) -> None:
        """Atomically increment the click counter for a resolved link."""
        await self._repository.increment_clicks(code)
```

`_orm_to_response` is a module-level helper in the same file. It copies the `LinkDAO` columns into a `LinkResponse` DTO. The other methods of the service (`get_link`, `list_links`, `delete_link`, `trigger_reinspection`) follow the same pattern.

Two details keep the service free of FastAPI:

- `scheduler: BackgroundTaskScheduler` is a `Protocol` defined in [`inspector_service.py`](https://github.com/sasadangelo/fasturl/blob/v0.1.0/src/fasturl/services/inspector_service.py). Any object with an `add_task(func, *args, **kwargs)` method satisfies it. FastAPI's `BackgroundTasks` does, but the service never imports it.
- The service does not run the background inspection itself. It hands the work to the injected `InspectorService`, which owns the shared HTTP client and knows how to schedule the task.

Because `LinkService` receives its repository and its inspector in the constructor, testing business logic becomes trivial. In unit tests, you inject mocks for both, without a database, a network, or an HTTP server.

## The Router Layer: Thin Handlers and HTTP Contracts

The Router layer ([`src/fasturl/api/routers/links.py`](https://github.com/sasadangelo/fasturl/blob/v0.1.0/src/fasturl/api/routers/links.py) and [`redirect.py`](https://github.com/sasadangelo/fasturl/blob/v0.1.0/src/fasturl/api/routers/redirect.py)) is responsible strictly for HTTP concerns: routing paths, status codes, query/body parameter parsing, and dispatching background tasks.

### 1. Management Endpoints (`/api/v1/links`)

```python
from typing import Annotated, TypeAlias
from fastapi import APIRouter, BackgroundTasks, Path, status
from fasturl.api.dependencies import LinkServiceDep
from fasturl.api.schemas.link_schemas import LinkCreateRequest, LinkResponse

router = APIRouter(prefix="/api/v1/links", tags=["Links"])

_CodePath: TypeAlias = Annotated[
    str,
    Path(min_length=7, max_length=16, description="Base62 short code or alias"),
]

@router.post(
    path="",
    response_model=LinkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new shortened link",
)
async def create_link(
    body: LinkCreateRequest,
    service: LinkServiceDep,
    background_tasks: BackgroundTasks,
) -> LinkResponse:
    """Create a new shortened link and dispatch a background inspection."""
    return await service.create_link(
        target_url=str(body.target_url),
        custom_code=body.custom_code,
        expires_at=body.expires_at,
        scheduler=background_tasks,
    )

@router.get(
    path="/{code}",
    response_model=LinkResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve single link details",
)
async def get_link(code: _CodePath, service: LinkServiceDep) -> LinkResponse:
    return await service.get_link(code)
```

`create_link` translates HTTP into a service call and nothing more. It unpacks the validated body, passes FastAPI's `BackgroundTasks` as the scheduler, and returns the DTO. It does not know that an inspector exists, that the inspection needs an HTTP client, or which repository the service uses.

### 2. Public Redirect Endpoint (`/{code}`)

The redirect endpoint in [`src/fasturl/api/routers/redirect.py`](https://github.com/sasadangelo/fasturl/blob/v0.1.0/src/fasturl/api/routers/redirect.py) lives at the root URL (without `/api/v1`):

```python
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import RedirectResponse
from fasturl.api.dependencies import LinkServiceDep

router = APIRouter(tags=["Redirect"])

@router.get(
    path="/{code}",
    status_code=307,
    response_class=RedirectResponse,
    summary="Resolve and redirect short URL",
)
async def redirect_short_url(
    code: str,
    service: LinkServiceDep,
    background_tasks: BackgroundTasks,
) -> RedirectResponse:
    """Resolve short code and issue 307 redirect; record clicks in background."""
    target_url = await service.resolve_for_redirect(code)

    # Click counter increment happens non-blockingly after response is returned
    background_tasks.add_task(
        func=service.increment_clicks,
        code=code,
    )

    return RedirectResponse(url=target_url, status_code=307)
```

The click counter goes through `service.increment_clicks`, a public method of the service. The router never touches the repository.

Notice that `307 Temporary Redirect` is chosen instead of `301 Moved Permanently`. A `301` redirect is aggressively cached by web browsers, which would prevent the server from tracking subsequent clicks for the same user.

## Deep Dive: Dependency Injection in FastAPI

### What Is Dependency Injection?

Imagine you are assembling a desktop computer. If the CPU was permanently soldered to the power supply and hardwired to a specific monitor, replacing the monitor or testing the CPU in isolation would be impossible. Instead, standard sockets and cables decouple each component: the power supply plugs in where electricity is needed, and the monitor plugs into the video port.

In software, **Dependency Injection (DI)** is that exact plug-and-socket design.

Without Dependency Injection, a class creates its own dependencies internally:

```python
# Anti-pattern: Hardcoded dependency creation (tight coupling)
class LinkService:
    def __init__(self) -> None:
        # LinkService is tied to one database file and to the real network
        self.session = create_async_session("sqlite+aiosqlite:///instance/fasturl.db")
        self.repository = LinkRepository(self.session)
        self.inspector = InspectorService(http_client=httpx.AsyncClient())
```

With Dependency Injection, an object **receives** its dependencies from an outside provider rather than instantiating them itself:

```python
# Clean pattern: Dependency Injection via constructor
class LinkService:
    def __init__(self, repository: LinkRepository, inspector: InspectorService) -> None:
        self._repository = repository
        self._inspector = inspector
```

`LinkService` no longer cares *how* its collaborators are created: which connection string the repository uses, whether it talks to PostgreSQL, SQLite, or a mock, and whether the inspector's HTTP client reaches the real internet or a fake transport.

### Why Is Dependency Injection Essential?

Dependency Injection solves four critical software architecture challenges:

1. **Unit Testing without Database or Network Overheads**:
   When writing tests for `LinkService`, you do not want to start a database engine, run migrations, or call real websites. You instantiate `LinkService(repository=AsyncMock(), inspector=Mock())` directly and verify domain logic in milliseconds.
2. **Deterministic Resource Lifecycles (Session Scoping)**:
   Database sessions, connection pools, and HTTP clients must be opened before a request starts and safely closed (or rolled back) when the request finishes. DI automates this teardown per request without polluting business functions with try-finally blocks.
3. **Inversion of Control (IoC)**:
   High-level modules (business services) do not depend on low-level implementation details (SQLAlchemy engines). Both depend on abstractions.
4. **Declarative and Type-Safe Route Signatures**:
   With Python type hints and FastAPI `Annotated`, handlers state what they need in their signature, and the framework resolves the dependency graph.

### The Composition Root: One Module Wires Everything

If the service does not create its collaborators, someone else has to. In FastURL it is not the router either. All the construction lives in one module, [`src/fasturl/api/dependencies/__init__.py`](https://github.com/sasadangelo/fasturl/blob/v0.1.0/src/fasturl/api/dependencies/__init__.py). The place where an application assembles its object graph is called the **composition root**:

```python
from typing import Annotated, TypeAlias
import httpx
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fasturl.core.database import get_db
from fasturl.repositories.link_repository import LinkRepository
from fasturl.services.inspector_service import InspectorService
from fasturl.services.link_service import LinkService

# 1. Yields an AsyncSession per request and guarantees cleanup
DBSessionDep: TypeAlias = Annotated[AsyncSession, Depends(dependency=get_db)]

# 2. Reuses the shared httpx.AsyncClient stored in FastAPI app.state during lifespan
def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client

HTTPClientDep: TypeAlias = Annotated[httpx.AsyncClient, Depends(dependency=get_http_client)]

# 3. Builds a LinkRepository scoped to the active database session
def _get_link_repository(session: DBSessionDep) -> LinkRepository:
    return LinkRepository(session)

LinkRepoDep: TypeAlias = Annotated[LinkRepository, Depends(dependency=_get_link_repository)]

# 4. Builds LinkService with its repository and an InspectorService
def _get_link_service(repository: LinkRepoDep, http_client: HTTPClientDep) -> LinkService:
    inspector: InspectorService = InspectorService(http_client=http_client)
    return LinkService(repository=repository, inspector=inspector)

LinkServiceDep: TypeAlias = Annotated[LinkService, Depends(dependency=_get_link_service)]
```

Each factory is an ordinary Python function, and each one declares what it needs with the same `Annotated` aliases that the routers use. `_get_link_repository` asks for a `DBSessionDep`, and `_get_link_service` asks for a `LinkRepoDep` and an `HTTPClientDep`. The module describes the graph, but it does not run anything. FastAPI runs it.

The composition root also decides who knows what:

| Component | What it knows |
|---|---|
| Router | `LinkServiceDep` and the public methods of `LinkService` |
| `LinkService` | The repository and the inspector it receives in the constructor |
| `api/dependencies/__init__.py` | How each piece is built and what it needs |

Suppose `LinkService` needs a new collaborator tomorrow, for example a blocklist of forbidden domains. You change its constructor and `_get_link_service`, and no router changes. To see how the application is assembled, there is exactly one file to read.

> The router asks for a `LinkService`. Only the composition root knows what a `LinkService` is made of.

### How FastAPI Resolves the Dependency Graph

When a request reaches `POST /api/v1/links`, FastAPI reads the handler's signature:

```python
@router.post("")
async def create_link(
    body: LinkCreateRequest,
    service: LinkServiceDep,
    background_tasks: BackgroundTasks,
) -> LinkResponse:
    ...
```

It finds `Depends(_get_link_service)` inside `LinkServiceDep`, reads the signature of `_get_link_service`, and repeats the process until it reaches functions with no dependencies of their own. Then it calls them back up the chain:

![FastURL dependency graph: get_db and get_http_client feed the repository and LinkService factories, which feed the create_link handler]({{ site.baseurl }}/assets/img/layered-architecture-with-fastapi-routers-services-and-repositories-dependency-graph.svg){:width="760" height="410" .responsive_img}

Three rules govern the execution:

- **Leaves first.** A dependency is always built before the function that needs it. By the time `_get_link_service` runs, the repository and the HTTP client already exist.
- **One instance per request.** FastAPI caches the result of each dependency for the duration of a request. If two nodes of the graph ask for `DBSessionDep`, `get_db` runs once and both receive the same session, so they work inside the same transaction. `Depends(get_db, use_cache=False)` opts out of the cache.
- **Cleanup at the end.** `get_db` is a generator: it yields the session, and the code after `yield` closes it, or rolls it back if the request raised an exception. FastAPI runs that code after the response has been sent and after the background tasks have finished. That is why the background inspection can still use the repository it received.

```python
async def get_db() -> AsyncIterator[AsyncSession]:
    async with _session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

The cache lasts one request, and so do the objects. FastAPI builds a new `LinkService`, `LinkRepository`, and `InspectorService` for every request, which costs almost nothing because they only store references. The expensive resources (the database engine and the `httpx.AsyncClient` connection pool) are created once at startup in the `lifespan` function and stored in `app.state`. `get_http_client` does not create a client, it fetches the shared one. The [next article]({{ site.baseurl }}/fastapi-async-background-tasks-and-error-handling/) covers the lifespan in detail.

### Overriding Dependencies in Integration Tests

Before calling a dependency, FastAPI checks the `app.dependency_overrides` dictionary. If it maps the dependency to a replacement, FastAPI calls the replacement instead. A test can therefore swap one node of the graph and let FastAPI build everything else exactly as in production.

FastURL's `api_client` fixture in [`tests/conftest.py`](https://github.com/sasadangelo/fasturl/blob/v0.1.0/tests/conftest.py) replaces the two leaves of the graph, the database session and the HTTP client:

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

Breaking down the choices:

- **Only the leaves are replaced.** `LinkRepository`, `InspectorService`, and `LinkService` are still built by the production factories, so the tests exercise the real wiring. Only the database and the outside world are fake.
- **The key is the function object**, `get_db`, not its name. FastAPI matches the function itself.
- **`clear()` runs after `yield`**, so the overrides never leak into the next test, even when a test fails.

The fixture, `db_session`, and `http_client` are explained step by step in the [pytest article]({{ site.baseurl }}/testing-python-applications-with-pytest-patterns-for-real-code/) of this series.

## Architectural Summary

By enforcing strict boundaries across layers, each part of FastURL has a singular focus:

|                            | Router                                                | Service                                            | Repository                                             | Model                                        |
|----------------------------|-------------------------------------------------------|----------------------------------------------------|--------------------------------------------------------|----------------------------------------------|
| **Module Path**            | `fasturl.api.routers`                                 | `fasturl.services`                                 | `fasturl.repositories`                                 | `fasturl.models`                             |
| **Primary Responsibility** | HTTP request parsing, status codes, background tasks  | Domain workflows, invariants, collision resolution | Database reads and writes, SQL queries, atomic updates | Declarative table mappings, database indexes |
| **Depends On**             | Services (`fasturl.services`), Schemas                | Repositories, `InspectorService`, Models           | Database Sessions (`AsyncSession`), Models            | None (pure declarative schema)               |
| **What It Must NOT Know**  | Database queries, SQL ORM details                     | FastAPI routers, HTTP request and response objects | HTTP headers, validation schemas, routing              | HTTP endpoints, application business logic   |

## Conclusion

In this article we covered:

- **The Layered Architecture pattern**: how organizing code into Routers, Services, and Repositories prevents codebase decay and creates clean separation of concerns.
- **The FastURL project structure**: how `api/`, `services/`, `repositories/`, `models/`, and `core/` packages separate responsibilities cleanly.
- **Domain model to ORM mapping**: mapping the `Link` Aggregate Root and embedded Value Objects to flat SQLAlchemy 2.0 table columns.
- **Async Repository pattern**: executing queries, atomic increments, and soft-deletions using `AsyncSession`.
- **Pure business services**: generating Base62 short codes, verifying self-redirect invariants, and raising domain exceptions without HTTP coupling.
- **Dependency Injection**: a single composition root, `api/dependencies/__init__.py`, that declares the dependency graph with `Depends` and typed `Annotated` aliases, and how FastAPI resolves it on every request: leaves first, one instance per request, cleanup at the end.
- **Dependency overrides**: replacing the leaves of the graph in tests while FastAPI builds everything else as in production.

The [next article]({{ site.baseurl }}/fastapi-async-background-tasks-and-error-handling/) covers advanced operational features in FastAPI: async background tasks, managing shared HTTP connection pools with `httpx.AsyncClient` in lifespan context, and global exception handlers.
