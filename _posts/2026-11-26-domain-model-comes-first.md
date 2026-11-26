---
layout: post
title: "The Domain Model Comes First: One Model for Your API, CLI, UI, and Database Schema"
seo_title: "The Domain Model Comes First"
post_series_id:
  - modern-python-application
  - software-architecture-patterns
date: 2026-11-26
author: sasadangelo
slug: domain-model-comes-first
image: /assets/img/domain-model-comes-first-hero.svg
excerpt: "Design the domain model before the architecture: one source of names and entities, projected onto your database, REST API, CLI, SDK, and UI."
categories:
  - "Software Architecture"
  - "Programming"
tags:
  - python
---

![The Domain Model Comes First: One Model for Your API, CLI, UI, and Database Schema]({{ site.baseurl }}/assets/img/domain-model-comes-first-hero.svg){:width="760" height="400" .responsive_img}

## Introduction

Open any project that grew without a plan and look for one concept. The table is called `urls`, the endpoint is `/shortlinks`, the CLI command is `alias add`, and the screen says "My redirects". Four names for the same thing. Every developer who joins the team has to learn the translation, every bug report needs one, and every change has to be made four times, in four slightly different ways.

Nobody chose that mess. It happens when each interface is designed on its own, starting from its own technology: the database person thinks in tables, the API person in resources, the front-end person in screens. What is missing is the one thing they all share: a model of the problem itself.

In the [previous article]({{ site.baseurl }}/lean-requirements-personas-and-scenarios/) I showed how to write lean requirements for [FastURL](https://github.com/sasadangelo/fasturl), the URL shortener I use as a running example, and I closed with a short section on the domain model. This article is the full version of that idea. It is the step between requirements and architecture: before you choose layers, hexagons, or microservices, you decide what your application is about.

You should read this article if:

- your API, database, and user interface use different names for the same things, and you want to know where that comes from;
- you have heard of Domain-Driven Design but want the useful core without the full vocabulary;
- you design APIs or command-line tools and want a method that gives you their resources and commands, instead of inventing them every time.

## Why the Model Comes Before Everything Else

Think of a globe and the maps made from it. A nautical chart preserves angles so a ship can hold a course. A subway map throws away distances so a passenger can count stops. A city map keeps street names readable at walking scale. They look nothing alike, yet they all describe the same Earth, and when a new road is built, every map has to show it. Nobody draws a subway map by looking at a nautical chart: each one is drawn from the globe.

Software works the same way. The **domain model** is the globe: a description of the things your application deals with, their names, and how they relate, written without any technology in mind. The database schema, the REST API, the command line, the client SDK, and the user interface are the maps. Each one is drawn for a different reader and keeps different details, but all of them are drawn from the same model.

> The domain model is the single source of the names, the entities, and the relationships. Each interface is a projection of it, a design step with its own constraints, not an automatic translation.

Both halves of that sentence matter. The first half says the model decides the vocabulary: a `Link` is a `Link` in the table, in the endpoint, in the command, and on the screen. The second half says that projecting is still design work. A subway map is not a shrunken nautical chart, and a good screen is not a database table with buttons. I come back to this in the section on where projections diverge.

### An Old Idea With a New Scope

None of this is new for databases. In 1975, the [ANSI/SPARC](https://en.wikipedia.org/wiki/ANSI-SPARC_Architecture) study group described three levels of a database: a *conceptual* schema that describes the information an organization cares about, the *external* views that each application sees, and the *internal* schema that says how data is stored. A year later, Peter Chen published [The Entity-Relationship Model: Toward a Unified View of Data](https://doi.org/10.1145/320434.320440), giving the conceptual level a notation: entities, attributes, and relationships, drawn before any table exists.

For decades, that was how good database design worked: logical model first, physical tables second. What changed is the number of interfaces. A typical application today exposes the same data through a database, a REST API, a CLI or SDK, and one or more user interfaces. The logical model is still the right starting point, but it is no longer only the database's model. It is the application's model, and every interface is one of its projections.

Eric Evans gave this idea its modern name in [Domain-Driven Design](https://www.domainlanguage.com/ddd/) (2003). His *ubiquitous language* says that the same words should appear in conversations, documents, and code. If the requirements talk about links and short codes, the code must say `Link` and `ShortCode`, and so must the table, the endpoint, and the command.

### Why Before the Architecture

In the [Software Architecture Patterns]({{ site.baseurl }}/software-architecture-patterns-explained/) article, every style organizes code *around* something. Layered architecture passes domain data from the presentation layer down to the data layer. Hexagonal, onion, and clean architecture put the domain at the very center and push everything else to the edge. Microservices split a system along its business capabilities.

In every case, the domain is the input of the architecture, not its output. If you choose the architecture first, you end up organizing folders around names you have not decided yet, and renaming a concept after it has spread through every interface costs far more than spending a day on the model before writing any code.

## What a Domain Model Is, and What It Is Not

You do not need the whole Domain-Driven Design book to build a useful model. Three ideas cover most applications:

- **Entity.** A thing with its own identity that persists over time. A link created today is the same link tomorrow, even after its click count and inspection result have changed. In FastURL, `Link` is an entity, identified by its short code.
- **Value object.** A thing defined only by its value, with no identity of its own. Two `TargetUrl` values with the same address are interchangeable. In practice, value objects are the attributes of an entity that deserve a type of their own, because they carry rules or group several fields: a `ShortCode` must be Base62, a `TargetUrl` must be HTTP or HTTPS, and a `LinkInspection` groups status, latency, and title. A plain flag such as `is_active` stays a simple attribute.
- **Aggregate.** A group of objects that change together and must stay consistent together. One entity is the *root*: it is the only door into the group, and it enforces the rules that span its parts. In an online shop, an `Order` is the root and its `OrderLine` items live inside it: you never add a line without going through the order, because the order must check the total. In FastURL the group is small, because `Link` owns only value objects, so `Link` is both the entity and the root of its aggregate.

![Entities, value objects, and aggregates: on the left an Order aggregate whose root Order owns two OrderLine entities and a ShippingAddress value object, reachable only through the root; on the right FastURL's Link aggregate, where Link is the only entity and owns the ShortCode, TargetUrl, LinkInspection, and LinkMetrics value objects plus plain attributes]({{ site.baseurl }}/assets/img/domain-model-comes-first-building-blocks.svg){:width="760" height="440" loading="lazy" .responsive_img}
*An aggregate is a group that changes together; in FastURL it coincides with the Link entity*

Here is the FastURL model, as I wrote it in [`domain-design.md`](https://github.com/sasadangelo/fasturl/blob/main/docs/domain-design.md) and described it in [From Domain Design to REST API]({{ site.baseurl }}/from-domain-design-to-rest-api-building-fasturl-with-fastapi/):

```text
Link (aggregate root)
├── code          ShortCode       Base62, 7–16 characters, unique
├── target_url    TargetUrl       HTTP or HTTPS only, never FastURL itself
├── is_active     boolean         soft-delete flag
├── expires_at    datetime        optional expiry
├── inspection    LinkInspection  status, latency, title, OpenGraph tags
└── metrics       LinkMetrics     clicks_count, last_clicked_at
```

The model is small on purpose. One entity, which is also the root of the only aggregate, four value objects, and no technology: no table names, no URLs, no Pydantic, no screens.

### More Than Data

There is a trap here, and many teams fall into it. If the domain model is only a list of nouns and their fields, it is a data model, and the application built on it ends up as a set of forms over a database. Martin Fowler called this the [Anemic Domain Model](https://martinfowler.com/bliki/AnemicDomainModel.html): objects that carry data but no behavior, with the rules scattered across the services that use them.

A domain model has two parts:

| | **Information** | **Rules** |
|---|---|---|
| **What it contains** | Entities, attributes, relationships | Invariants and business decisions |
| **FastURL examples** | `Link` has a `ShortCode` and a `TargetUrl` | An inactive or expired link never redirects; a short code is unique; a target cannot point back to FastURL |
| **Where it ends up** | In every projection: columns, fields, arguments, form inputs | In the core of the application, in one place |

The information part projects onto every interface, which is what the rest of this article is about. The rules do not project anywhere. A table cannot know that an expired link must not redirect, and neither can a screen. That rule lives once, in the core, and every interface reaches it through the application. This is exactly the part that the architecture patterns of the next article are designed to protect.

### One Line on Bounded Contexts

When a domain grows, the same word can mean different things in different parts of the business, and DDD calls each consistent part a *bounded context*. FastURL already has two, link management and link inspection, connected by a `LinkCreated` event. For an application of this size that is all you need to know; contexts start to matter when the application splits into modules that talk through events.

## From Job Stories to the Model

The model is not invented: it is read out of the requirements. Lean requirements are written in the domain's language, so most of the work is noticing which words keep coming back. Here are three of the job stories in FastURL's [`requirements.md`](https://github.com/sasadangelo/fasturl/blob/main/docs/requirements.md) and what each one contributes:

| **Job story** | **What it adds to the model** |
|---|---|
| **JS-001** *When I provide a valid target URL, I want a unique shortened URL with a random alphanumeric code* | The `Link` entity, the `ShortCode` and `TargetUrl` value objects, and the uniqueness rule |
| **JS-006** *When I navigate to a short URL, I want to be redirected immediately* | The `resolve` operation, and the rules about active and expired links |
| **JS-007** *When a new link is registered, I want a non-blocking background check on the target URL* | The `LinkInspection` value object and the `inspect` operation |

The reading follows the grammar of the sentences:

1. **Nouns become candidates.** Link, URL, code, inspection, click. Not every noun survives, but every element of the model starts as a noun in a story.
2. **The identity test sorts them.** Ask whether two instances with the same values are the same thing. If not, it is an entity; if yes, it is a value object.
3. **Ownership groups them.** Value objects that only make sense together with an entity belong to its aggregate.
4. **Verbs become operations.** Shorten, resolve, inspect, delete. These are the things the application does, and they become the operations of every projection.
5. **Conditions become rules.** "Valid", "unique", "not expired": every qualifier in a story is a rule waiting to be written down.

![FastURL job story JS-001 with nouns, verbs, and conditions highlighted: nouns become the Link entity and the TargetUrl and ShortCode value objects, the verb becomes the shorten operation, and the conditions become rules]({{ site.baseurl }}/assets/img/domain-model-comes-first-job-story.svg){:width="760" height="420" loading="lazy" .responsive_img}
*The grammar of a job story gives you the model*

I keep the result in a [`domain-design.md`](https://github.com/sasadangelo/fasturl/blob/main/docs/domain-design.md) file next to [`requirements.md`](https://github.com/sasadangelo/fasturl/blob/main/docs/requirements.md) in the repository. Plain text and a small diagram are enough, and when a requirement changes, this is the second file I update, before any code.

## Many Projections of One Model

With the model in place, each interface becomes a translation problem with a clear starting point. Five projections are the most common: the database schema, the REST API, the command line, the client libraries, and the user interface. The mapping between them is surprisingly regular:

| **Model element** | **Database** | **REST API** | **CLI** | **SDK** | **User interface** |
|---|---|---|---|---|---|
| **Entity** | Table | Resource collection | Command group | Client namespace | List screen |
| **Identity** | Primary key | Path parameter | Positional argument | Method argument | Detail page URL |
| **Value object** | Columns | Fields of the representation | Options | Typed fields | Form inputs |
| **Operation** | Not projected | HTTP method | Verb subcommand | Method | Button or task screen |
| **Rule** | Constraints, at most | Status codes when violated | Error messages | Typed exceptions | Validation feedback |

Read the table by rows and you see the vocabulary flow from the model to every interface. Read it by columns and you see what each interface does with it.

![FastURL's domain model, with the Link aggregate, its operations, and its rules, projected onto a database table, REST endpoints, CLI commands, SDK methods, and a task-based screen, while the rules stay in the core]({{ site.baseurl }}/assets/img/domain-model-comes-first-projections.svg){:width="760" height="478" loading="lazy" .responsive_img}
*One model, five projections: the names travel, the rules stay in the core*

### Database Schema

For the database, the domain model *is* the logical schema. The physical schema answers a different question: how to store that model efficiently in a specific engine.

FastURL's aggregate becomes a single `links` table, because the value objects have no identity and no lifecycle of their own. Instead of separate tables, they become groups of columns:

```text
links
├── code (PK)          ← ShortCode
├── target_url         ← TargetUrl
├── is_active, expires_at, created_at
├── inspection_status, inspection_latency_ms, inspection_title, ...   ← LinkInspection
└── clicks_count, last_clicked_at                                      ← LinkMetrics
```

The names survive the projection, which is the point. Notice also what does not appear: operations. A table stores the state that operations change, but it has no verbs.

### REST API

A resource-oriented API is the most direct projection of a domain model. Google's [AIP-121](https://google.aip.dev/121) describes resource-oriented design in exactly this order: first "the resources (nouns) the API will provide", then their relationships and schemas, and only at the end the methods. The standard methods (Get, List, Create, Update, Delete) map onto HTTP verbs, and anything that does not fit becomes a *custom method*.

In FastURL, the `Link` aggregate becomes `/api/v1/links` and `/api/v1/links/{code}`, the value objects become fields of the JSON representation, and the operations become methods: `POST` to shorten, `GET` to read, `DELETE` to deactivate. The `inspect` operation does not fit any standard method, so it becomes the custom action `POST /api/v1/links/{code}/inspect`. The full mapping is in [From Domain Design to REST API]({{ site.baseurl }}/from-domain-design-to-rest-api-building-fasturl-with-fastapi/), and the principles behind it are in [Designing REST APIs in Practice]({{ site.baseurl }}/designing-rest-apis-in-practice-a-kubernetes-case-study/).

### Command Line

Well-designed command-line tools follow the same pattern, with entities as nouns and operations as verbs. `kubectl get pods` and `kubectl delete deployment web` project the Kubernetes resource model; `gh pr list` and `gh issue create` project GitHub's. You can guess the commands of a tool you have never used, because they come from a model you already know.

FastURL has no CLI today, but its model tells you what one would look like:

```shell
fasturl links create https://example.com/a/very/long/path --alias spring-sale --expires 2026-12-31
```

Breaking down the command:

- `links` — the command group, projected from the `Link` entity
- `create` — the verb, projected from the shorten operation
- `https://example.com/...` — the positional argument, the `TargetUrl` value object
- `--alias spring-sale` — an optional `ShortCode` chosen by the user instead of a generated one
- `--expires 2026-12-31` — the optional `expires_at` attribute

The other operations follow without any further design: `links list`, `links get <code>`, `links delete <code>`, `links inspect <code>`. Notice that `inspect`, which needed a special custom action over HTTP, is an ordinary verb on the command line. Each projection has its own constraints, and HTTP's fixed set of methods is one of them.

### SDK and Client Libraries

A client library is the command line's twin for programmers: the same nouns and verbs, expressed as namespaces and methods. Stripe's Python library exposes `client.v1.customers.create(...)` and `client.v1.invoices.list(...)`, where even the API version shows up as a namespace, and the official Kubernetes clients expose one method per resource and verb. A Python SDK for FastURL would follow the model in the same way:

```python
from fasturl import FastURL

client = FastURL(api_key="...")
link = client.links.create("https://example.com/a/very/long/path", alias="spring-sale")
client.links.inspect(link.code)
```

The rules show up as typed exceptions. A caller catches `AliasAlreadyTakenError` or `LinkExpiredError`, the same names that the application uses inside, instead of parsing a status code.

There is one nuance. SDKs are often generated from the API contract, and the Kubernetes clients are generated from its OpenAPI specification. In that case the SDK is a projection of a projection, and any naming mistake in the API is copied into every language. This is one more reason to take the names from the model before the API is designed.

### User Interface

The user interface is where the projection needs the most judgment. The direct mapping gives you the classic trio of screens for each entity: a list, a detail page, and a form. Frameworks have automated this for twenty years. Rails scaffolding generates the table migration, the routes, the controller, and the three views from one model definition. Richard Pawson's [Naked Objects](https://en.wikipedia.org/wiki/Naked_objects) pattern (2002) went to the extreme and generated the entire user interface from the domain objects, with no UI code at all.

For an admin tool, that direct projection is often right. For the screens your users see every day, it usually is not. People do not think in entities, they think in tasks. Greg Young made this point in his [CQRS Documents](https://cqrs.wordpress.com/wp-content/uploads/2010/11/cqrs_documents.pdf) (2010): a CRUD-style interface, which edits records field by field, loses the user's *intent*, and with it the verbs of the domain. A task-based interface asks what the user is trying to do.

For FastURL, the task is "shorten this URL and give me something to share". The right screen is one input field and a button that returns the short link, ready to copy, not a form with every attribute of `Link`. The model still provides the names, the fields, and the rules, but the screen is designed around the task.

### And the Rest

The five projections above are the most visible, not the only ones. Anything that talks about your application benefits from the same names:

- **Events and webhooks.** Domain events such as `LinkCreated` or `LinkExpired` become topic names, message payloads, and webhooks for your customers. Here the operations do project: an event is a verb of the domain in the past tense.
- **Tools for AI agents.** An [MCP]({{ site.baseurl }}/understanding-mcp-the-protocol-for-agent-tool-communication/) server exposes *resources* and *tools*, which map onto entities and operations: `create_link`, `get_link`, `inspect_link`. An agent picks the right tool only if the names are clear.
- **Authorization.** Permissions are entities times operations: `links:create`, `links:delete`, `links:inspect`. Kubernetes RBAC works exactly this way, with resources and verbs.
- **Error codes.** `LINK_NOT_FOUND`, `LINK_EXPIRED`, and `ALIAS_ALREADY_TAKEN` are FastURL's rules, given a public name. They are the one place where the rules, which otherwise stay in the core, become visible from outside.
- **Observability and tests.** Log fields, metric names, audit entries, and Given/When/Then scenarios read like documentation when they use the language of the model.

## Where the Projections Diverge

If projections were automatic translations, you could generate every interface from the model and be done. They are not, because each interface has forces of its own. These are the most common points where a projection departs from the model:

- **Operations that are not CRUD.** Deactivating a link, re-running an inspection, or extending an expiry are verbs of the domain, not edits of a record. The CLI expresses them freely, but HTTP has a fixed set of methods, so you have to choose: update a field (`PATCH` with `is_active: false`), create a sub-resource, or expose a custom action. This is a design decision, not a translation.
- **Data that is not in the domain.** The physical schema adds things the model does not have: indexes, audit columns, denormalized copies for fast reads. If FastURL ever records individual clicks for analytics, it will need a `clicks` table that is not an entity of the model at all, only a storage concern.
- **Tasks that span entities.** A dashboard that shows the most clicked links of the week does not correspond to any single entity. It reads from the model but does not mirror it.
- **Concerns that exist only on the wire.** Pagination, versioning, idempotency, caching, and long-running operations are properties of the API as a contract, not of the domain. A `Link` does not have a page number. They deserve an article of their own, and they will get one in the Modern Python series.

> Projections may differ in shape. They must not differ in names.

One honest caveat. Some teams work *API-first*: they write the OpenAPI contract before anything else and treat it as the source of truth, because other teams start coding against it on day one. That is a sound practice, and it does not contradict the domain-first idea. A good contract is still built from resources, and the resources still come from the model; API-first decides which projection gets published first, not where the names come from.

## Keeping the Model Light

Domain modeling has a bad reputation in some teams, and the reason is usually *Big Design Up Front*: weeks of diagrams before a line of code, and a model that is obsolete by the time development starts. That is not what I am suggesting.

For FastURL, the domain design fits on one page and took less time to write than the first endpoint. A few habits keep it that way:

- **Model only what the stories need.** If no job story mentions a user account, there is no `User` entity yet. The model grows when the requirements grow.
- **Keep it in the repository.** A `domain-design.md` next to the code is reviewed in the same pull requests and changes in the same commits. A diagram in a wiki drifts the day it is drawn.
- **Change it first.** When a requirement changes, update the model before the code, exactly as I suggested for the requirements themselves. Each projection then follows from one decision instead of one per interface.
- **Skip the catalogue.** Entities, value objects, aggregates, and the ubiquitous language are enough for most applications. Repositories, factories, domain events, and context maps are useful tools, but you can adopt them when a real problem calls for them.

## Conclusion

The domain model is the step that most projects skip, and the one that makes every later step easier. It gives the database, the API, the command line, the SDK, and the user interface the same names, the same entities, and the same relationships, so that a concept means one thing everywhere. Projecting it is still design work, because each interface has constraints of its own, but every projection starts from the same place.

In this article we covered:

- why naming problems across tables, endpoints, commands, and screens come from designing each interface on its own;
- the domain model as the single source of names, entities, and relationships, and why it comes before the architecture;
- the roots of the idea, from the ANSI/SPARC conceptual schema and Chen's entity-relationship model to Evans' ubiquitous language;
- the light core of Domain-Driven Design: entities, value objects, aggregates, and the difference between the information that projects and the rules that stay in the core;
- how to read the model out of job stories: nouns, identity, ownership, verbs, and conditions;
- the main projections of FastURL's model onto a database schema, a REST API, a CLI, an SDK, and a user interface, and the less visible ones, from events and AI agent tools to authorization and error codes;
- where the projections diverge, from non-CRUD operations to task-based interfaces, and how to keep the model light.

With the domain in place, the next question is how to organize the code around it. The [next article]({{ site.baseurl }}/software-architecture-patterns-explained/) follows FastURL from a single script to layered, hexagonal, and clean architecture, and then to modular monoliths, events, and microservices.

---

If you enjoyed this article, don't forget to **give it a clap 👏**, **share it with your friends 🔗**, and **follow me for more tips and tutorials on software development 📘**. Your support helps me create more content like this — thank you! 🙌

**Note**: English is not my native language, and this article was drafted with the assistance of AI. However, all the ideas, projects, concepts, and content are entirely my own.
