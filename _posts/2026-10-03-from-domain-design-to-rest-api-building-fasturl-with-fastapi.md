---
layout: post
title: "From Domain Design to REST API: Building FastURL with FastAPI"
post_series_id:
  - modern-python-application
  - building-rest-apis
date: 2026-10-03
author: sasadangelo
slug: from-domain-design-to-rest-api-building-fasturl-with-fastapi
image: /assets/img/from-domain-design-to-rest-api-building-fasturl-with-fastapi-hero.png
excerpt: "Learn how to turn requirements and a domain model into a clean REST API using FastAPI and Pydantic v2, using FastURL — a URL shortener — as a concrete case study."
categories:
  - "Programming"
---

# From Domain Design to REST API: Building FastURL with FastAPI

_Posted on **{{ page.date | date_to_string }}**_

![From Domain Design to REST API: Building FastURL with FastAPI]({{ site.baseurl }}/assets/img/from-domain-design-to-rest-api-building-fasturl-with-fastapi-hero.png){:width="760" height="400" .responsive_img}

## Introduction

In the [previous article]({{ site.baseurl }}/designing-rest-apis-in-practice-a-kubernetes-case-study/) we established the theory: requirements produce domain entities, domain entities become REST resources, and HTTP methods map to the lifecycle operations of those resources. Kubernetes was the illustration — large enough to make the pattern clear, but too complex to implement in a blog post.

This article moves from theory to practice. The project is **FastURL**, a URL shortener and link inspector built with [FastAPI](https://fastapi.tiangolo.com/). It is small enough to fit comfortably in a few articles, but real enough to demonstrate every concept that matters: domain modeling, Pydantic validation as a form of type-safe Value Objects, a standardized error envelope, and a resource hierarchy derived directly from the domain.

You should read this article if:

- You have read the previous article and want to see the methodology applied to real code.
- You want to understand how Pydantic v2 validators enforce domain rules at the HTTP boundary.
- You want to see how a consistent error contract is designed and implemented from scratch.

## What FastURL Does

FastURL is a REST API that shortens long URLs into compact 7-character codes and resolves them back via HTTP redirects. Beyond basic shortening, it runs an asynchronous background inspection on every newly created link: it fetches the target page, records the HTTP status code and latency, and extracts the HTML title and OpenGraph metadata.

Three actors interact with the system:

| Actor | Description |
|---|---|
| **API Client** | Creates, lists, retrieves, and deletes shortened links |
| **Public Visitor** | Navigates to a short URL and gets redirected to the target |
| **Background Inspector** | Asynchronously checks target URL health after creation |

This actor breakdown comes directly from the [requirements document](https://github.com/sasadangelo/fasturl/blob/main/docs/requirements.md) — before any code was written. The nouns in the job stories (`Link`, `ShortCode`, `TargetUrl`, `Inspection`, `Metrics`) became the domain entities. The verbs (`shorten`, `resolve`, `inspect`, `delete`) became the operations.

## From Requirements to Domain Entities

Every requirement in FastURL can be traced to one of eight job stories documented in the [requirements document](https://github.com/sasadangelo/fasturl/blob/main/docs/requirements.md). Three of them are worth looking at closely because they drive the entire domain design.

**JS-001** — *When I provide a valid target URL, I want a unique shortened URL with a random alphanumeric code.* This story introduces two domain concepts: a `Link` (the association between a short code and a target URL) and a `ShortCode` (a validated 7-character Base62 string). The story also establishes a business rule: the code must be unique and collision-resistant.

**JS-006** — *When I navigate to a short URL, I want to be redirected immediately.* This story adds two more rules: the link must be active (`is_active = true`) and must not have passed its expiration date (`expires_at`). If either condition fails, the redirect must not happen.

**JS-007** — *When a new link is registered, I want a non-blocking background check on the target URL.* This story introduces the `LinkInspection` concept: a snapshot of target URL health, latency, and page metadata. Crucially, it must not block the creation response — the system acknowledges the creation immediately and inspects asynchronously. This is the [async I/O pattern]({{ site.baseurl }}/async-and-event-loop-in-python-asyncio-in-practice/) we covered earlier in the series.

These three stories alone define the core of the domain model.

### The Domain Model

FastURL has a single Aggregate Root: `Link`. It owns all the data and enforces all invariants. The Value Objects — `ShortCode`, `TargetUrl`, `LinkMetrics`, and `LinkInspection` — are part of the `Link` aggregate, not separate entities with their own identity.

![FastURL Domain Model Architecture]({{ site.baseurl }}/assets/img/fasturl-domain-model.png){:width="760" height="400" .responsive_img}

```text
Link (Aggregate Root)
├── code          ← ShortCode (Base62, 7–16 chars, unique)
├── target_url    ← TargetUrl (HTTP/HTTPS only, no self-redirect)
├── is_active     ← soft-delete flag
├── expires_at    ← optional expiry
├── inspection    ← LinkInspection (status, latency, title, og:*)
└── metrics       ← LinkMetrics (clicks_count, last_clicked_at)
```

There are two bounded contexts: **LinkManagement** (CRUD and redirect resolution) and **LinkInspection** (async health check and metadata extraction). They communicate via a `LinkCreated` event that triggers the background task.

> A single aggregate with Value Objects as members keeps the domain model flat and readable. `LinkInspection` and `LinkMetrics` have no identity of their own — they only make sense as part of a `Link`.

### Mapping Entities to Resources

The mapping from domain to REST is direct:

| Domain Entity | REST Resource | Methods |
|---|---|---|
| `Link` collection | `/api/v1/links` | `GET`, `POST` |
| `Link` instance | `/api/v1/links/{code}` | `GET`, `DELETE` |
| `LinkInspection` action | `/api/v1/links/{code}/inspect` | `POST` |
| *(public redirect)* | `/{code}` | `GET` |

Notice that `/{code}` carries no `/api/v1/` prefix. This is intentional: it is a consumer-facing URL that must be short and stable, not a versioned management endpoint.

The `POST /api/v1/links/{code}/inspect` endpoint does not map to a CRUD operation — it triggers an action. As discussed in the previous article, `POST` is the correct method for non-CRUD actions on a resource.

## Pydantic as Value Object Implementation

In Domain-Driven Design, a Value Object encapsulates validation rules and equality semantics. In FastAPI, [Pydantic](https://docs.pydantic.dev/latest/) models serve exactly this role at the HTTP boundary. The `LinkCreateRequest` schema enforces every business rule on inbound data before the service layer is ever called.

```python
class LinkCreateRequest(BaseModel):
    target_url: HttpUrl = Field(
        description="Destination URL to shorten. Must be HTTP or HTTPS.",
    )
    custom_code: str | None = Field(
        default=None,
        min_length=7,
        max_length=16,
    )
    expires_at: datetime | None = Field(default=None)

    @field_validator("custom_code")
    @classmethod
    def validate_custom_code(cls, v: str | None) -> str | None:
        if v is not None and not _BASE62_PATTERN.match(v):
            raise ValueError("custom_code must contain only alphanumeric characters [a-zA-Z0-9]")
        return v

    @model_validator(mode="after")
    def validate_expires_at_future(self) -> LinkCreateRequest:
        if self.expires_at is not None:
            now = datetime.now(UTC).replace(tzinfo=None)
            expires = self.expires_at.replace(tzinfo=None)
            if expires <= now:
                raise ValueError("expires_at -> Expiration date must be in the future")
        return self
```

Breaking down what each element enforces:

- **`HttpUrl`** — Pydantic's built-in type rejects any URL that is not HTTP or HTTPS. No custom validator needed for the scheme.
- **[`@field_validator`](https://docs.pydantic.dev/latest/concepts/validators/#field-validators)** — Enforces the Base62 alphabet rule: only `[a-zA-Z0-9]`. This is the `ShortCode` Value Object's constraint, expressed as a Pydantic field-level validator.
- **[`@model_validator(mode="after")`](https://docs.pydantic.dev/latest/concepts/validators/#model-validators)** — Runs after all fields are validated, so it can access `self.expires_at`. It rejects expiration dates in the past. This is a cross-field invariant that requires the full model context.

![Pydantic v2 Validation Workflow]({{ site.baseurl }}/assets/img/fasturl-pydantic-validation.png){:width="760" height="400" .responsive_img}

The response schema mirrors the domain structure: `LinkResponse` embeds `InspectionResponse` and `MetricsResponse`, reflecting the `LinkInspection` and `LinkMetrics` Value Objects in the aggregate.

```python
class LinkResponse(BaseModel):
    code: str
    short_url: str
    target_url: str
    is_active: bool
    expires_at: datetime | None = None
    inspection: InspectionResponse
    metrics: MetricsResponse
    created_at: datetime
    updated_at: datetime
```

Note that `id` — the internal surrogate key — is absent from the response. The `code` is the sole public identifier. This is a deliberate design choice: a sequential integer PK is enumerable and guessable; a Base62 7-character code is not.

## The Error Envelope

One of the most important consistency decisions in any API is the error contract. FastURL uses a single envelope for every error response:

```json
{
  "success": false,
  "error": "LINK_NOT_FOUND",
  "details": [
    "code -> No link found with code 'aB3x9zK'"
  ]
}
```

The `error` field is a machine-readable short code. The `details` list contains human-readable, field-level explanations. This structure lets clients branch on `error` programmatically and display `details` to a developer or end user.

![FastAPI Standardized Error Envelope & Mapping]({{ site.baseurl }}/assets/img/fasturl-error-envelope.png){:width="760" height="400" .responsive_img}

### Domain Exceptions

Domain exceptions are pure Python classes — no FastAPI imports, no HTTP knowledge. They carry only the data needed to build the error response.

```python
class LinkNotFoundError(AppError):
    def __init__(self, code: str) -> None:
        super().__init__(
            message="LINK_NOT_FOUND",
            status_code=404,
            details=[f"code -> No link found with code '{code}'"],
        )

class AliasAlreadyTakenError(AppError):
    def __init__(self, alias: str) -> None:
        super().__init__(
            message="ALIAS_ALREADY_TAKEN",
            status_code=409,
            details=[f"custom_code -> The alias '{alias}' is already in use"],
        )

class LinkExpiredError(AppError):
    def __init__(self, code: str, expired_at: str) -> None:
        super().__init__(
            message="LINK_EXPIRED",
            status_code=410,
            details=[f"code -> Link '{code}' expired on {expired_at}"],
        )
```

The `AppError` base class holds the `message`, `status_code`, and `details`. Subclasses just set the right values in `__init__`. The service layer raises these exceptions; the HTTP layer never needs to know how they are structured.

### Global Exception Handlers

Three handlers registered in `main.py` [cover every failure path](https://fastapi.tiangolo.com/tutorial/handling-errors/):

```python
def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc) -> JSONResponse:
        error_details = []
        for e in exc.errors():
            loc = " -> ".join(str(x) for x in e["loc"])
            msg = e["msg"]
            error_details.append(f"{loc}: {msg}")
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "VALIDATION_ERROR", "details": error_details},
        )

    @app.exception_handler(AppError)
    async def app_error_handler(request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": exc.message, "details": exc.details},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc) -> JSONResponse:
        # Full traceback logged server-side; generic message returned to client
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "INTERNAL_SERVER_ERROR",
                     "details": ["An unexpected error occurred. Please contact support."]},
        )
```

The three handlers map precisely to the three failure categories:

| Handler | Triggered by | HTTP status |
|---|---|---|
| `RequestValidationError` | Pydantic schema validation failure | 400 |
| `AppError` | Domain rule violation (not found, conflict, expired) | 404 / 409 / 410 |
| `Exception` | Any unhandled error | 500 |

The third handler is the safety net. It logs the full traceback server-side but returns only a generic message to the client — no stack traces, no internal details, no information disclosure.

## The Full Endpoint Table

Bringing everything together, here is the complete API surface of FastURL:

| Endpoint | Method | Status codes | Description |
|---|---|---|---|
| `/api/v1/links` | `POST` | 201, 400, 409 | Create a shortened link |
| `/api/v1/links` | `GET` | 200, 400 | List links with optional filters |
| `/api/v1/links/{code}` | `GET` | 200, 404 | Retrieve a single link |
| `/api/v1/links/{code}` | `DELETE` | 204, 404 | Soft-delete a link |
| `/api/v1/links/{code}/inspect` | `POST` | 202, 404 | Trigger background re-inspection |
| `/{code}` | `GET` | 307, 404, 410 | Redirect to target URL |

A few design decisions worth noting:

- `DELETE` returns `204 No Content` — no body, because there is nothing meaningful to return after a deletion.
- `POST /api/v1/links/{code}/inspect` returns `202 Accepted` — not `200 OK`. The inspection runs asynchronously; the client receives the current snapshot immediately and polls `GET /api/v1/links/{code}` for the result.
- `GET /{code}` can return `410 Gone` for expired links. `410` is semantically different from `404`: it signals that the resource existed but is permanently unavailable, not that it was never found.

## Conclusion

In this article we covered:

- **From job stories to domain entities**: how the nouns and verbs in requirements directly produce the `Link` aggregate, the `ShortCode` and `TargetUrl` Value Objects, and the `LinkInspection` and `LinkMetrics` embedded snapshots.
- **Pydantic as Value Object implementation**: using `HttpUrl`, `@field_validator`, and `@model_validator` to enforce domain invariants at the HTTP boundary — before the service layer is called.
- **A consistent error envelope**: a single `{success, error, details}` structure for every failure, backed by domain exceptions that carry no HTTP knowledge and three global handlers that translate them.
- **Resource hierarchy derived from the domain**: five management endpoints plus a public redirect endpoint, each with a clear ownership and a precise set of status codes.

The [next article]({{ site.baseurl }}/layered-architecture-with-fastapi-routers-services-and-repositories/) walks through the layered code structure that makes all of this work: how routers, services, repositories, and the dependency injection system are organized to keep each concern in its own place.

---

If you enjoyed this article, don't forget to **give it a clap 👏**, **share it with your friends 🔗**, and **follow me for more tips and tutorials on software development 📘**. Your support helps me create more content like this — thank you! 🙌

**Note**: English is not my native language, and this article was drafted with the assistance of AI. However, all the ideas, projects, concepts, and content are entirely my own.
