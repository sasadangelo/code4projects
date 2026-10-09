---
layout: post
title: "Layered Architecture with FastAPI: Routers, Services, and Repositories"
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
---


![Layered Architecture with FastAPI: Routers, Services, and Repositories]({{ site.baseurl }}/assets/img/layered-architecture-with-fastapi-routers-services-and-repositories-hero.png){:width="760" height="400" .responsive_img}

## Introduction

In the [previous article]({{ site.baseurl }}/from-domain-design-to-rest-api-building-fasturl-with-fastapi/) we defined the domain model and API contract for **FastURL**, our open-source URL shortener and link inspector service hosted on [GitHub](https://github.com/sasadangelo/fasturl). We established how requirements turn into domain entities, how Pydantic v2 schemas act as Value Objects, and how a consistent error envelope isolates clients from internal failure mechanics.

Designing endpoints and validation rules is essential, but code needs a clean home to live in. If you put database queries, HTTP handling, business validation, and external network requests into a single route function, your application will quickly turn into an unmaintainable monolith. We previously explored structuring a [database layer with SQLAlchemy]({{ site.baseurl }}/database-layer-with-sqlalchemy-in-a-layered-python-architecture/) and managing [asyncio event loop concurrency]({{ site.baseurl }}/async-and-event-loop-in-python-asyncio-in-practice/); now we bring those principles together in an API context.

This article shows how to organize a real-world [FastAPI](https://fastapi.tiangolo.com/) application into clean, isolated layers: **Routers**, **Services**, and **Repositories**, connected together seamlessly through FastAPI's **Dependency Injection** system.

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
    └── integration/           # End-to-end HTTP tests with TestClient and SQLite
```

Each module has a clearly delineated responsibility:

- **[`models/`](https://github.com/sasadangelo/fasturl/tree/main/src/fasturl/models)**: Houses SQLAlchemy declarative ORM mappings.
- **[`repositories/`](https://github.com/sasadangelo/fasturl/tree/main/src/fasturl/repositories)**: Contains classes that handle raw SQL operations and query execution using [`AsyncSession`](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html).
- **[`services/`](https://github.com/sasadangelo/fasturl/tree/main/src/fasturl/services)**: Encapsulates pure domain workflows and business rules. Free of any HTTP framework dependencies.
- **[`api/`](https://github.com/sasadangelo/fasturl/tree/main/src/fasturl/api)**: Contains FastAPI routers, input/output schemas (DTOs), and dependency injection wiring.
- **[`core/`](https://github.com/sasadangelo/fasturl/tree/main/src/fasturl/core)**: Provides infrastructure foundations:
  - **`config/`**: Type-safe settings with [Pydantic Settings]({{ site.baseurl }}/managing-application-configuration-in-python-with-pydantic-settings/) across application, database, and logging domains.
  - **`database.py`**: Async SQLAlchemy session lifecycle and engine initialization, expanding on our [SQLAlchemy database layer]({{ site.baseurl }}/database-layer-with-sqlalchemy-in-a-layered-python-architecture/).
  - **`log.py`**: Structured application logging with [Loguru]({{ site.baseurl }}/logging-in-a-flask-application-with-loguru/).
  - **`exceptions.py`**: Clean domain error hierarchy (`AppError`, `ValidationError`, `LinkNotFoundError`).

## Domain Model Mapping: Embedding Value Objects in the ORM

In FastURL's domain design, the `Link` entity is the Aggregate Root. Its Value Objects — `ShortCode`, `TargetUrl`, `LinkInspection`, and `LinkMetrics` — do not have separate lifecycle identities.

In the database, we map this domain structure to a clean single-table schema (`links`), embedding the Value Object properties as flat columns.

Here is the SQLAlchemy 2.0 ORM model in [`src/fasturl/models/link.py`](https://github.com/sasadangelo/fasturl/blob/main/src/fasturl/models/link.py):

```python
from datetime import UTC, datetime
from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""

class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(length=16), nullable=False, unique=True, index=True)
    target_url: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=None)

    # LinkInspection Value Object — embedded columns
    inspection_status: Mapped[str] = mapped_column(String(length=20), nullable=False, default="pending_analysis")
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

Notice a key design decision: the surrogate primary key `id` is internal only. The sole public identifier is `code` (the 7–16 character Base62 string), which is indexed and unique.

## The Repository Layer: Async Data Access

The Repository (`LinkRepository` in [`src/fasturl/repositories/link_repository.py`](https://github.com/sasadangelo/fasturl/blob/main/src/fasturl/repositories/link_repository.py)) has a single job: encapsulate SQL operations using SQLAlchemy's async engine. It contains no business logic, no status code definitions, and no pricing rules.

```python
from datetime import UTC, datetime
from sqlalchemy import func, select, update
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from fasturl.models.link import Link

class LinkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_code(self, code: str) -> Link | None:
        """Return the Link with the given code, or None if not found."""
        result: Result[Link] = await self._session.execute(
            select(Link).where(Link.code == code)
        )
        return result.scalar_one_or_none()

    async def create(self, link: Link) -> Link:
        """Persist a new Link record and return the refreshed instance."""
        self._session.add(instance=link)
        await self._session.commit()
        await self._session.refresh(instance=link)
        return link

    async def soft_delete(self, code: str) -> bool:
        """Set is_active = False for the link with the given code."""
        result: Result[int] = await self._session.execute(
            update(table=Link)
            .where(Link.code == code)
            .values(is_active=False, updated_at=datetime.now(UTC).replace(tzinfo=None))
            .returning(Link.id)
        )
        await self._session.commit()
        return result.scalar_one_or_none() is not None

    async def increment_clicks(self, code: str) -> None:
        """Atomically increment clicks_count and update last_clicked_at."""
        await self._session.execute(
            update(Link)
            .where(Link.code == code)
            .values(
                clicks_count=Link.clicks_count + 1,
                last_clicked_at=func.now(),
                updated_at=func.now(),
            )
        )
        await self._session.commit()

    async def code_exists(self, code: str) -> bool:
        """Return True if any link uses the given code."""
        result: Result[int] = await self._session.execute(
            select(Link.id).where(Link.code == code)
        )
        return result.scalar_one_or_none() is not None
```

All methods are fully asynchronous and use type-safe SQLAlchemy 2.0 select and update constructs. Notice that updates like `increment_clicks` use database-level atomic increments (`clicks_count = Link.clicks_count + 1`) to eliminate race conditions under concurrent traffic.

## The Service Layer: Pure Business Logic

The Service layer (`LinkService` in [`src/fasturl/services/link_service.py`](https://github.com/sasadangelo/fasturl/blob/main/src/fasturl/services/link_service.py)) is the brain of the application. It orchestrates business workflows, generates random Base62 codes, handles code collision retries, and raises domain exceptions.

Crucially, **`LinkService` has zero knowledge of FastAPI or HTTP**. It does not import `Request`, `Response`, or `HTTPException`.

```python
import random
import string
from datetime import UTC, datetime
from loguru import logger
from fasturl.api.schemas.link_schemas import LinkResponse, InspectionResponse, MetricsResponse
from fasturl.core.config import settings
from fasturl.core.exceptions import AliasAlreadyTakenError, LinkExpiredError, LinkNotFoundError, ValidationError
from fasturl.models.link import Link
from fasturl.repositories.link_repository import LinkRepository

_log = logger.bind(name="LinkService")
_BASE62_ALPHABET = string.ascii_letters + string.digits
_MAX_CODE_RETRIES = 10

class LinkService:
    def __init__(self, repository: LinkRepository) -> None:
        self._repository = repository

    def _generate_code(self) -> str:
        """Generate a random Base62 code of the configured length."""
        length = settings.app.code_length
        return "".join(random.choices(_BASE62_ALPHABET, k=length))

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
    ) -> LinkResponse:
        """Create a new shortened link, checking collisions and invariants."""
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
        link = Link(
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
        return self._orm_to_response(persisted)

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

    def _orm_to_response(self, link: Link) -> LinkResponse:
        base = settings.app.base_url.rstrip("/")
        return LinkResponse(
            code=link.code,
            short_url=f"{base}/{link.code}",
            target_url=link.target_url,
            is_active=link.is_active,
            expires_at=link.expires_at,
            inspection=InspectionResponse(
                status=link.inspection_status,
                http_status_code=link.http_status_code,
                latency_ms=link.latency_ms,
                title=link.title,
                description=link.description,
                image_url=link.image_url,
                last_checked_at=link.last_checked_at,
            ),
            metrics=MetricsResponse(
                clicks_count=link.clicks_count,
                last_clicked_at=link.last_clicked_at,
            ),
            created_at=link.created_at,
            updated_at=link.updated_at,
        )
```

Because `LinkService` takes `LinkRepository` in its constructor, testing business logic becomes trivial. In unit tests, you can inject a mock repository without needing a running database or HTTP server.

## The Router Layer: Thin Handlers and HTTP Contracts

The Router layer ([`src/fasturl/api/routers/links.py`](https://github.com/sasadangelo/fasturl/blob/main/src/fasturl/api/routers/links.py) and [`redirect.py`](https://github.com/sasadangelo/fasturl/blob/main/src/fasturl/api/routers/redirect.py)) is responsible strictly for HTTP concerns: routing paths, status codes, query/body parameter parsing, and dispatching background tasks.

### 1. Management Endpoints (`/api/v1/links`)

```python
from typing import Annotated, TypeAlias
from fastapi import APIRouter, BackgroundTasks, Path, status
from fasturl.api.dependencies import HTTPClientDep, LinkServiceDep
from fasturl.api.schemas.link_schemas import LinkCreateRequest, LinkResponse
from fasturl.services.inspector_service import inspect_link

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
    http_client: HTTPClientDep,
    background_tasks: BackgroundTasks,
) -> LinkResponse:
    """Create link and dispatch non-blocking background inspection."""
    response = await service.create_link(
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

@router.get(
    path="/{code}",
    response_model=LinkResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve single link details",
)
async def get_link(code: _CodePath, service: LinkServiceDep) -> LinkResponse:
    return await service.get_link(code)
```

### 2. Public Redirect Endpoint (`/{code}`)

The redirect endpoint in [`src/fasturl/api/routers/redirect.py`](https://github.com/sasadangelo/fasturl/blob/main/src/fasturl/api/routers/redirect.py) lives at the root URL (without `/api/v1`):

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
        func=service._repository.increment_clicks,
        code=code,
    )

    return RedirectResponse(url=target_url, status_code=307)
```

Notice that `307 Temporary Redirect` is chosen instead of `301 Moved Permanently`. A `301` redirect is aggressively cached by web browsers, which would prevent the server from tracking subsequent clicks for the same user.

## Deep Dive: Dependency Injection in FastAPI

### What Is Dependency Injection?

Imagine you are assembling a desktop computer. If the CPU was permanently soldered to the power supply and hardwired to a specific monitor, replacing the monitor or testing the CPU in isolation would be impossible. Instead, standard sockets and cables decouple each component: the power supply plugs in where electricity is needed, and the monitor plugs into the video port.

In software, **Dependency Injection (DI)** is that exact plug-and-socket design.

Without Dependency Injection, a class or function creates its own dependencies internally:

```python
# Anti-pattern: Hardcoded dependency creation (tight coupling)
class LinkService:
    def __init__(self) -> None:
        # LinkService is tightly coupled to AsyncSession and sqlite:///fasturl.db
        self.session = create_async_session("sqlite+aiosqlite:///instance/fasturl.db")
        self.repository = LinkRepository(self.session)
```

With Dependency Injection, an object **receives** its dependencies from an outside provider rather than instantiating them itself:

```python
# Clean pattern: Dependency Injection via constructor
class LinkService:
    def __init__(self, repository: LinkRepository) -> None:
        self._repository = repository
```

`LinkService` no longer cares *how* `LinkRepository` is created, which database connection string was used, or whether it's talking to PostgreSQL, SQLite, or an in-memory mock during tests.

### Why Is Dependency Injection Essential?

Dependency Injection solves four critical software architecture challenges:

1. **Unit Testing without Database or Network Overheads**:
   When writing tests for `LinkService`, you do not want to start a database engine, run migrations, or clean up test records. You can instantiate `LinkService(MockLinkRepository())` directly and verify domain logic in milliseconds.
2. **Deterministic Resource Lifecycles (Session Scoping)**:
   Database sessions, connection pools, and HTTP clients must be opened before a request starts and safely closed (or rolled back) when the request finishes. DI automates this teardown per request without polluting business functions with try-finally blocks.
3. **Inversion of Control (IoC)**:
   High-level modules (business services) do not depend on low-level implementation details (SQLAlchemy engines). Both depend on abstractions.
4. **Declarative and Type-Safe Route Signatures**:
   With Python type hints and FastAPI `Annotated`, handlers state what they need in their signature, and the framework resolves the dependency graph.

### How FastAPI Resolves the Dependency Graph with `Depends`

FastAPI provides a first-class DI system via [`Depends`](https://fastapi.tiangolo.com/tutorial/dependencies/). In FastURL, the entire dependency graph is wired in [`src/fasturl/api/dependencies/__init__.py`](https://github.com/sasadangelo/fasturl/blob/main/src/fasturl/api/dependencies/__init__.py):

```python
from typing import Annotated, TypeAlias
import httpx
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fasturl.core.database import get_db
from fasturl.repositories.link_repository import LinkRepository
from fasturl.services.link_service import LinkService

# 1. Yields an AsyncSession per request and guarantees cleanup
DBSessionDep: TypeAlias = Annotated[AsyncSession, Depends(dependency=get_db)]

# 2. Reuses the shared httpx.AsyncClient stored in FastAPI app.state during lifespan
def _get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client

HTTPClientDep: TypeAlias = Annotated[httpx.AsyncClient, Depends(dependency=_get_http_client)]

# 3. Builds a LinkRepository scoped to the active database session
def _get_link_repository(session: DBSessionDep) -> LinkRepository:
    return LinkRepository(session)

LinkRepoDep: TypeAlias = Annotated[LinkRepository, Depends(dependency=_get_link_repository)]

# 4. Builds LinkService injected with LinkRepository
def _get_link_service(repository: LinkRepoDep) -> LinkService:
    return LinkService(repository=repository)

LinkServiceDep: TypeAlias = Annotated[LinkService, Depends(dependency=_get_link_service)]
```

### The Request Execution Flow

When an HTTP request reaches `POST /api/v1/links`:

```python
@router.post("")
async def create_link(
    body: LinkCreateRequest,
    service: LinkServiceDep,
    http_client: HTTPClientDep,
    background_tasks: BackgroundTasks,
) -> LinkResponse:
    ...
```

FastAPI automatically traverses and resolves the dependency hierarchy:

![FastAPI dependency injection flow from request resolution to session cleanup]({{ site.baseurl }}/assets/img/layered-architecture-with-fastapi-routers-services-and-repositories-dependency-injection-flow.png){:width="760" height="550" .responsive_img}

### Overriding Dependencies in Integration Tests

One of the greatest benefits of FastAPI's DI engine is `app.dependency_overrides`. In integration tests, you can replace any provider in the chain without changing application code:

```python
from fastapi.testclient import TestClient
from fasturl.api.dependencies import _get_link_service
from fasturl.main import app

def test_create_link_with_mocked_service():
    # Override LinkService with a mock or test instance
    app.dependency_overrides[_get_link_service] = lambda: FakeLinkService()

    client = TestClient(app)
    response = client.post("/api/v1/links", json={"target_url": "https://example.com"})

    assert response.status_code == 201
    
    # Clean up overrides after test
    app.dependency_overrides.clear()
```

## Architectural Summary

By enforcing strict boundaries across layers, each part of FastURL has a singular focus:

|                            | Router                                                | Service                                            | Repository                                             | Model                                        |
|----------------------------|-------------------------------------------------------|----------------------------------------------------|--------------------------------------------------------|----------------------------------------------|
| **Module Path**            | `fasturl.api.routers`                                 | `fasturl.services`                                 | `fasturl.repositories`                                 | `fasturl.models`                             |
| **Primary Responsibility** | HTTP request parsing, status codes, background tasks  | Domain workflows, invariants, collision resolution | Database reads and writes, SQL queries, atomic updates | Declarative table mappings, database indexes |
| **Depends On**             | Services (`fasturl.services`), Schemas                | Repositories (`fasturl.repositories`), Models      | Database Sessions (`AsyncSession`), Models            | None (pure declarative schema)               |
| **What It Must NOT Know**  | Database queries, SQL ORM details                     | FastAPI routers, HTTP request and response objects | HTTP headers, validation schemas, routing              | HTTP endpoints, application business logic   |

## Conclusion

In this article we covered:

- **The Layered Architecture pattern**: how organizing code into Routers, Services, and Repositories prevents codebase decay and creates clean separation of concerns.
- **The FastURL project structure**: how `api/`, `services/`, `repositories/`, `models/`, and `core/` packages separate responsibilities cleanly.
- **Domain model to ORM mapping**: mapping the `Link` Aggregate Root and embedded Value Objects to flat SQLAlchemy 2.0 table columns.
- **Async Repository pattern**: executing queries, atomic increments, and soft-deletions using `AsyncSession`.
- **Pure business services**: generating Base62 short codes, verifying self-redirect invariants, and raising domain exceptions without HTTP coupling.
- **Dependency Injection**: constructing automated per-request dependency graphs using FastAPI's `Depends` and typed `Annotated` aliases.

The [next article]({{ site.baseurl }}/fastapi-async-background-tasks-and-error-handling/) covers advanced operational features in FastAPI: async background tasks, managing shared HTTP connection pools with `httpx.AsyncClient` in lifespan context, and global exception handlers.

---

If you enjoyed this article, don't forget to **give it a clap 👏**, **share it with your friends 🔗**, and **follow me for more tips and tutorials on software development 📘**. Your support helps me create more content like this — thank you! 🙌

**Note**: English is not my native language, and this article was drafted with the assistance of AI. However, all the ideas, projects, concepts, and content are entirely my own.
