---
layout: post
title: "Software Architecture Patterns Explained: Layered, Hexagonal, Clean, Event-Driven, Microservices, and Hybrid"
seo_title: "Software Architecture Patterns Explained"
post_series_id: software-architecture-patterns
date: 2026-11-16
author: sasadangelo
slug: software-architecture-patterns-explained
image: /assets/img/software-architecture-patterns-explained-hero.svg
excerpt: "From a single script to microservices: how software architecture patterns evolve as an application grows, who invented each one, which problem it solved, and when to stop."
categories:
  - "Software Architecture"
  - "Programming"
tags:
  - python
---

![Software Architecture Patterns Explained: Layered, Hexagonal, Clean, Event-Driven, Microservices, and Hybrid]({{ site.baseurl }}/assets/img/software-architecture-patterns-explained-hero.svg){:width="760" height="400" .responsive_img}

## Introduction

Nobody designs an architecture for a 50-line script, and nobody should. You open a file, write a few functions, run it, and move on. The trouble starts when the script survives. Someone adds a command-line option, then a REST endpoint, then a background job, then a second developer. One day you open the project and realize that no one, including you, can say where a business rule lives or what will break if you change it.

That moment is when architecture stops being an academic topic. Architecture is not about diagrams with circles and arrows: it is about deciding where code, classes, files, and folders go, and which parts are allowed to know about which others, so that the application stays under your control as it grows.

In the [previous article]({{ site.baseurl }}/lean-requirements-personas-and-scenarios/) I showed how to collect lean requirements for [FastURL](https://github.com/sasadangelo/fasturl), the URL shortener I use as a running example. Requirements tell you what the system must do and how well. This article maps the architecture patterns you can choose from to meet them. Instead of presenting them as a flat catalogue, I tell them as an evolution: each pattern was invented by someone to solve a concrete problem, very often the limit of the pattern before it. For each step you will see the signal that triggers it, the folder structure it produces in Python, and the point where you should stop.

You should read this article if:

- your Python project started as a script and you are no longer sure how to organize it;
- you have heard of hexagonal, clean, onion, and event-driven architecture but cannot tell how they differ, or whether they differ at all;
- you are wondering whether you need microservices, and suspect the honest answer is "not yet".

## When Code Does Not Need an Architecture

Think of a kitchen. If you cook for yourself, a single drawer of utensils is fine: you know where everything is because you put it there. If you open a restaurant with ten cooks, the same drawer becomes chaos within a week. The kitchen did not get worse; the number of people and dishes grew past what one drawer can hold.

Software follows the same rule. A script that one person runs is best written as one module with a few functions. Adding layers, interfaces, and dependency injection to it is pure ceremony: more files, more indirection, no benefit.

The opposite failure has a name. In 1997, Brian Foote and Joseph Yoder described the [Big Ball of Mud](http://www.laputan.org/mud/): "a haphazardly structured, sprawling, sloppy, duct-tape-and-baling-wire, spaghetti-code jungle". Their insight was that nobody designs a big ball of mud. It emerges from *throwaway code* that is never thrown away and grows *piecemeal*, one urgent change at a time. Harry Percival and Bob Gregory open [Architecture Patterns with Python](https://www.cosmicpython.com/book/introduction.html) with the same warning:

> A big ball of mud is the natural state of software in the same way that wilderness is the natural state of your garden.

The cost of that wilderness is measurable. In the [Stack Overflow Developer Survey 2024](https://survey.stackoverflow.co/2024/professional-developers), technical debt was the number one frustration at work, cited by about 62% of professional developers. The [Consortium for Information & Software Quality](https://www.it-cisq.org/press-releases/12-06-22/) estimated accumulated technical debt in the United States at about $1.52 trillion in its latest (2022) report, and called it "the largest obstacle to making changes in existing code bases".

So the real question is not "which architecture is best?" but "when does my code need one?". In my experience, these are the signals that a script has become an application:

- **A second entry point.** The same logic is now reached from a CLI, an API, and a background worker.
- **Duplicated rules.** The same validation or calculation appears in two or three places, and they have started to disagree.
- **Tests need the real world.** You cannot test a business rule without a database, a network call, or an API key.
- **Files everyone edits.** One module has grown past a few hundred lines and every change touches it.
- **More than one developer.** Conventions that lived in your head now need to be explicit.
- **A dependency you might replace.** The database, the message broker, or the LLM provider could change.

Before these signals appear, one module and a few functions is the right architecture. After they appear, every pattern in this article is an answer to one or more of them.

## Two Questions, Not One

Most comparisons of "layered vs hexagonal vs event-driven vs microservices" treat them as rivals. They are not, because they answer two different questions.

Think of a city. One question is how each building is organized inside: where the kitchen is, which rooms connect. A different question is how the buildings are laid out and connected: one large building, a campus, or a district linked by roads. A well-organized building can sit in a badly planned city, and the other way round.

| | **Internal organization** | **System structure** |
|---|---|---|
| **Question it answers** | How is code organized inside one deployable application? | How is the system split into parts, and how do they communicate and deploy? |
| **Patterns** | Layered (MVC), Hexagonal, Onion, Clean | Monolith, Modular monolith, Event-driven, Microservices (SOA, serverless) |
| **Unit of design** | Packages, modules, classes, imports | Modules, services, messages, deployments |
| **Typical driver** | Testability, changing frameworks or databases | Team size, independent scaling, independent releases |

The two axes combine. Every microservice is itself an application that needs an internal organization, and a hexagonal application can publish events. Keep this in mind for the rest of the article: the evolution moves from the first axis to the second as the system grows.

![Two axes of software architecture: internal organization (layered, hexagonal, clean) and system structure (monolith, modular monolith, event-driven, microservices)]({{ site.baseurl }}/assets/img/software-architecture-patterns-explained-two-axes.svg){:width="760" height="360" loading="lazy" .responsive_img}
*Internal organization and system structure are separate decisions*

## The Evolution of an Application

The steps below follow the life of a typical application. They are not a ladder you must climb: most applications should stop at step 2 or 3, and knowing when to stop matters as much as knowing when to move on.

![The evolution of software architecture: script, layered, hexagonal and clean, modular monolith, event-driven, microservices, and hybrid, with the signal that triggers each step]({{ site.baseurl }}/assets/img/software-architecture-patterns-explained-evolution.svg){:width="760" height="400" loading="lazy" .responsive_img}
*Each pattern answers the limits of the previous one*

### Step 0: The Script

Everything lives in one file: reading input, applying rules, talking to the database, printing output.

```text
shorten.py
```

This is fine as long as one person owns it and nothing else depends on it. The first signal from the list above is your cue to move on.

### Step 1: Layered Architecture

**The idea.** Split the code into horizontal layers, each with one responsibility, and let each layer depend only on the layer below it. The most common version has three: presentation (HTTP, CLI, UI), business logic, and data access.

**Where it comes from.** Layering is the oldest idea in this article. In 1968, Edsger W. Dijkstra published [The Structure of the "THE"-Multiprogramming System](https://doi.org/10.1145/363095.363143), an operating system built as a hierarchy of levels in which each level used only the levels below it. The problem he was solving was complexity: the layered structure let his team verify and test the system one level at a time.

A decade later, Trygve Reenskaug applied a similar separation to user interfaces. While visiting Xerox PARC in 1978–79, he conceived [Model-View-Controller](https://doi.org/10.5281/zenodo.3676092) to keep the model of the problem separate from the way it is shown and edited. MVC is the layered architecture most Python developers already know, even if they do not call it that: Django's Model-Template-View is a direct descendant, with models as the data layer and views as the presentation layer.

**In Python**, a layered FastAPI application looks like the structure I described in [Layered Architecture with FastAPI]({{ site.baseurl }}/layered-architecture-with-fastapi-routers-services-and-repositories/):

```text
src/fasturl/
├── api/              # presentation: routers, Pydantic schemas
├── services/         # business logic: LinkService, InspectorService
├── repositories/     # data access: LinkRepository
├── models/           # SQLAlchemy ORM models
└── main.py
```

Each folder answers the question "where does this code go?" with one word, which is the main reason layered architecture is the default for most web applications.

**Its limit.** In a classic layered stack, the business layer imports the data layer. That means your business rules depend on SQLAlchemy, your tests need a database, and replacing the persistence technology touches the core of the application. A second, quieter problem is that nothing *enforces* the layers: a router that queries the database directly works perfectly, and after a few years of deadlines the boundaries exist only in the folder names.

**When to stop here.** Most CRUD-heavy applications with thin business rules should. Mark Richards warns about the "architecture sinkhole" in his O'Reilly report *Software Architecture Patterns*: requests that pass through every layer without any layer doing real work. If that describes most of your requests, more structure would only add ceremony.

### Step 2: Hexagonal, Onion, and Clean Architecture

**The idea.** Turn the dependencies around. Put the domain (business rules and use cases) at the center, define the interfaces it needs from the outside world, and make the infrastructure implement them. The database, the web framework, and the message broker become plug-ins of the domain instead of its foundation.

**Where it comes from.** Alistair Cockburn described [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture), also called Ports and Adapters, in 2005. His motivation is the limit of step 1, almost word for word. Business logic kept leaking into user interface code, and the usual fix was to add another layer with the promise that no business logic would go there. Without a way to detect violations, he wrote, "the organization finds a few years later that the new layer is cluttered with business logic and the old problem has reappeared". His goal was an application that could be driven equally by users, programs, automated tests, or batch scripts, and developed in isolation from its devices and databases.

In 2008, Jeffrey Palermo described the [Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/) with the same diagnosis: traditional layering creates unnecessary coupling to infrastructure, because "transitive dependencies are still dependencies". In 2012, Robert C. Martin published [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html), explicitly noting that Hexagonal, Onion, and similar proposals were "very similar" and unifying them under one rule:

> Source code dependencies can only point inwards.

These are not three rival patterns. They are three vocabularies for the same idea:

| **Concept** | **Hexagonal** | **Onion** | **Clean** |
|---|---|---|---|
| **Business rules** | Application (inside) | Domain Model, Domain Services | Entities |
| **Use cases** | Application (inside) | Application Services | Use Cases |
| **Boundary** | Ports | Interfaces in the inner rings | Interface Adapters |
| **Technology** | Adapters | Infrastructure (outer ring) | Frameworks and Drivers |

**In Python**, the key tool is a port: an interface that the domain owns. `typing.Protocol` makes it lightweight, because adapters satisfy it structurally without inheriting from it:

```python
from typing import Protocol

from fasturl.domain.link import Link


class LinkRepository(Protocol):
    """Port owned by the domain: what the use cases need from storage."""

    async def get_by_code(self, code: str) -> Link | None: ...

    async def save(self, link: Link) -> None: ...


class InMemoryLinkRepository:
    """Adapter for tests: satisfies the port without a database."""

    def __init__(self) -> None:
        self._links: dict[str, Link] = {}

    async def get_by_code(self, code: str) -> Link | None:
        return self._links.get(code)

    async def save(self, link: Link) -> None:
        self._links[link.code] = link
```

A SQLAlchemy adapter implements the same two methods against a real database, and FastAPI's `Depends` decides which one to inject. The use case never imports either. The folder structure reflects the direction of the dependencies:

```text
src/fasturl/
├── domain/           # entities and rules: Link, ShortCode; no imports from outside
├── application/      # use cases and ports: ShortenLink, LinkRepository (Protocol)
└── adapters/
    ├── api/          # driving adapter: FastAPI routers
    ├── persistence/  # driven adapter: SQLAlchemy repository
    └── inspector/    # driven adapter: HTTP client that checks target URLs
```

**Its limit.** Indirection has a price. A single feature now spans more files, and data is mapped between the ORM model, the domain entity, and the Pydantic schema. For an application whose logic is mostly "read a row, return a row", that price buys very little.

**When to stop here.** When the domain is rich, the rules must be tested in milliseconds without a database, or you expect to swap infrastructure, this is often the final internal organization. Many teams also apply it selectively: ports only around the dependencies that are likely to change, such as an external API or an LLM provider.

### Step 3: Modular Monolith

**The idea.** As the application grows, the problem shifts from "how do I organize the code?" to "how do I organize *many* features and *many* developers?". A modular monolith keeps a single deployable application but splits it vertically into modules by business capability, each with its own internal layers or hexagon and a small public interface.

Think of an office building where each company rents its own floor. They share the elevator and the address, but nobody walks into another company's office: they go through reception.

```text
src/fasturl/
├── links/            # create and manage short links
│   ├── domain/
│   ├── application/
│   └── adapters/
├── redirect/         # resolve a code and redirect, latency-critical
├── analytics/        # click statistics
└── shared/           # configuration, logging, database session
```

This is "package by feature" rather than "package by layer", and it is the subject of the next article in this series. The pattern has no single inventor; it is the practical answer many teams reached after splitting into microservices too early.

**The Python catch.** Python has no package-private visibility, so a module boundary is only real if something checks it. A tool such as [import-linter](https://import-linter.readthedocs.io/) turns the rule into a test that fails in CI:

```toml
[tool.importlinter]
root_package = "fasturl"

[[tool.importlinter.contracts]]
name = "Feature modules are independent"
type = "independence"
modules = ["fasturl.links", "fasturl.redirect", "fasturl.analytics"]
```

**When to stop here.** For most teams, this is the sweet spot: clear boundaries, one deployment, one database, and in-process function calls instead of network calls.

### Step 4: Event-Driven Architecture

**The idea.** Instead of calling each other directly, modules announce that something happened ("a link was created") and let whoever cares react. The producer does not know who the consumers are.

Think of a newspaper. The editor publishes the news once; any number of readers subscribe, and the editor does not need to know them or wait for them.

**Where it comes from.** Events are as old as interrupts, but two milestones matter for application architecture. In 2002, David Luckham's *The Power of Events* introduced complex event processing for making sense of event streams in distributed enterprise systems. Around 2010, Greg Young named and popularized CQRS and Event Sourcing, building on Bertrand Meyer's command-query separation (Udi Dahan had written about similar ideas from 2008). Young's problem was that a rich domain model did not fit a classic three-layer architecture, and that some systems need a complete, auditable log of every change.

By 2017 the term had become so overloaded that Martin Fowler wrote [What do you mean by "Event-Driven"?](https://martinfowler.com/articles/201701-event-driven.html) to separate four different patterns:

| **Pattern** | **What the event carries** | **Main trade-off** |
|---|---|---|
| **Event notification** | "Something happened" and an ID | Very low coupling, but the overall flow is hard to see |
| **Event-carried state transfer** | The data consumers need | Consumers avoid calls back to the source, but keep copies of the data |
| **Event sourcing** | Every change, stored as the source of truth | Full history and replay, but more complex storage and queries |
| **CQRS** | Separate models for writes and reads | Each side can be optimized, but two models must be kept in sync |

**In FastURL**, analytics is a natural fit: the redirect must stay fast, so it records a `LinkClicked` event and returns immediately, and the analytics module processes it later. The gentlest way to start is inside the modular monolith, with an in-process message bus (Cosmic Python dedicates two chapters to it). You can move the same events to a broker such as RabbitMQ, Kafka, or Redis Streams later, when a consumer needs to run in a separate process.

**Its limit.** You trade direct calls for eventual consistency, duplicate deliveries, ordering problems, and flows that you can only reconstruct through monitoring. The first production pitfall is usually the *dual write*: saving to the database and publishing to the broker are two operations, and one of them can fail. The Transactional Outbox pattern exists to solve exactly that.

### Step 5: Microservices

**The idea.** Split the system into small services that are deployed, scaled, and owned independently, each with its own data, communicating over the network through APIs or events.

**Where it comes from.** The direct ancestor is Service-Oriented Architecture (SOA), which in the 2000s promised reusable enterprise services but often ended up centralized around heavyweight middleware. The term "microservices" was discussed at a workshop of software architects near Venice in May 2011 and adopted by the same group in May 2012. Netflix, with Adrian Cockcroft, had been pioneering the approach at web scale and called it "fine grained SOA". In March 2014, James Lewis and Martin Fowler published the article that defined the style, [Microservices](https://martinfowler.com/articles/microservices.html). The problems they described are the limits of the monolith: change cycles are tied together, so a small change means rebuilding and redeploying everything; modular structure erodes over time; and you can only scale the whole application, not the part under load.

**Adoption is real but not universal.** According to the [CNCF and SlashData](https://www.cncf.io/announcements/2025/11/11/cncf-and-slashdata-survey-finds-cloud-native-ecosystem-surges-to-15-6m-developers/) State of Cloud Native Development report of November 2025, 46% of backend developers use microservices, which means that more than half do not.

**Its limit.** Every in-process function call becomes a network call that can be slow or fail. You need service discovery, distributed tracing, versioned APIs, and an operations team that can run all of it. The most quoted counter-example comes from Amazon Prime Video, whose monitoring team in 2023 moved one workload from distributed services back into a single process and reported an infrastructure cost reduction of about 90%. Distribution is a cost you pay for independence, not a default.

**A note on serverless.** Serverless functions (AWS Lambda, Google Cloud Functions, Azure Functions) are often listed next to microservices. They are better understood as a deployment and billing model: you can deploy a modular monolith, a set of microservices, or a single event consumer as serverless functions.

**When to move here.** When independent teams need to release independently, or one part of the system has scaling or availability needs very different from the rest. FastURL's redirect endpoint, latency-critical and read-heavy, is the first candidate it would ever extract, and only if traffic justified it. Remember that each microservice still needs an internal organization from steps 1 and 2.

### Step 6: Hybrid Architectures

**The idea.** Real systems are rarely pure. A typical production system I would recommend today is a modular monolith in which each module is layered, ports appear only around the dependencies that are likely to change, modules communicate through events, and one or two parts with special needs run as separate services.

Hybrid has no inventor because it is not a pattern: it is what happens when you treat patterns as tools instead of identities. The [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/) puts it best: an architecture style "places constraints on the design", and

> Sometimes it's better to relax a constraint than to chase architectural purity.

The risk of a hybrid is inconsistency: if every module follows a different style for no reason, you are back to the big ball of mud. Record each decision and its reason in an Architecture Decision Record, so that the mix is deliberate and the next developer knows why.

## Other Styles Worth Knowing

Two more styles do not fit the evolution above, but you meet them often in the Python ecosystem:

- **Microkernel (plug-in) architecture** — a small core that defines extension points, plus independent plug-ins that add features. pytest is a classic example: most of its features, and every third-party extension, are plug-ins registered through hooks. Apache Airflow providers and VS Code extensions follow the same idea. Choose it when other people must extend your software without changing its core.
- **Pipes and filters (pipeline)** — data flows through a chain of independent processing steps, each consuming the output of the previous one. It is the natural shape of ETL jobs, machine learning pipelines, and Unix shell commands. Choose it when the problem is a transformation of data rather than a set of interactive use cases.

## How to Choose

There is no best architecture, only the one that fits your requirements today and can evolve tomorrow. This is why the series started from requirements: the non-functional requirements and constraints of [Part 1]({{ site.baseurl }}/lean-requirements-personas-and-scenarios/) are the inputs of this decision. FastURL's 50 ms latency target and its constraint that link creation must not wait for the URL inspection led to a layered, async application with background work. Different requirements would have led elsewhere.

| **If your requirements say...** | **Consider** |
|---|---|
| **One developer, one entry point, short life** | A script or a single module |
| **Web application, mostly CRUD, thin rules** | Layered (MVC) |
| **Rich domain, fast tests, infrastructure may change** | Hexagonal or Clean |
| **Many features and developers, one deployment** | Modular monolith |
| **Slow or optional work, many reactions to one fact** | Events, in-process first |
| **Independent teams, releases, or scaling needs** | Microservices, for the parts that need them |

One rule sums up the table:

> Move to the next step only when you see the signal that requires it, and enforce every boundary you introduce.

Most Python developers today work with frameworks that leave this choice to them. In the [PSF and JetBrains Python Developers Survey](https://blog.jetbrains.com/pycharm/2025/08/the-state-of-python-2025/) published in August 2025, FastAPI reached 38% usage, ahead of Django (35%) and Flask (34%). Unlike Django, FastAPI does not impose a project structure, so the architecture is a decision you make, whether you make it consciously or not.

## Conclusion

Architecture is the set of decisions that keeps an application understandable as it grows. A script does not need one; an application with several entry points, developers, and dependencies cannot survive without one. Each pattern in this article was invented to fix the limits of the previous one, and each one has a cost that is only worth paying when the problem is real.

In this article we covered:

- why a script needs no architecture, and the signals that a codebase has become an application;
- the difference between internal organization and system structure, and why the two combine;
- layered architecture, from Dijkstra's THE system to MVC and Django;
- hexagonal, onion, and clean architecture as three vocabularies for the same dependency rule, with a Python `Protocol` port;
- the modular monolith and how to enforce its boundaries with import-linter;
- the four meanings of event-driven architecture and the dual-write pitfall;
- microservices, their roots in SOA, their real costs, and where serverless fits;
- hybrid architectures, microkernel and pipeline styles, and how to choose from your requirements.

The [next article]({{ site.baseurl }}/layered-architecture-in-practice/) starts the deep dives with layered architecture in practice: layer rules, strict and relaxed layering, and the trade-offs between packaging by layer, by feature, and by component.

---

If you enjoyed this article, don't forget to **give it a clap 👏**, **share it with your friends 🔗**, and **follow me for more tips and tutorials on software development 📘**. Your support helps me create more content like this — thank you! 🙌

**Note**: English is not my native language, and this article was drafted with the assistance of AI. However, all the ideas, projects, concepts, and content are entirely my own.
