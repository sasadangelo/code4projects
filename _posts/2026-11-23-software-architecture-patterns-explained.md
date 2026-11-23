---
layout: post
title: "Software Architecture Patterns Explained: Layered, Hexagonal, Clean, Event-Driven, Microservices, and Hybrid"
seo_title: "Software Architecture Patterns Explained"
post_series_id:
  - modern-python-application
  - software-architecture-patterns
date: 2026-11-23
author: sasadangelo
slug: software-architecture-patterns-explained
image: /assets/img/software-architecture-patterns-explained-hero.svg
excerpt: "From a single script to microservices: how architecture patterns evolve as an app grows, who invented each one, what it solved, and when to stop."
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
- **Tests need the real world.** You cannot [test]({{ site.baseurl }}/testing-fastapi-in-practice/) a business rule without a database, a network call, or an API key.
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

![Two axes of software architecture: internal organization (layered, hexagonal, onion, clean) and system structure (monolith, modular monolith, event-driven, microservices)]({{ site.baseurl }}/assets/img/software-architecture-patterns-explained-two-axes.svg){:width="760" height="372" loading="lazy" .responsive_img}
*Internal organization and system structure are separate decisions*

## The Evolution of an Application

The steps below follow the life of a typical application. They are not a ladder you must climb: most applications should stop at step 1 or 2, and knowing when to stop matters as much as knowing when to move on.

![The evolution of software architecture: script, layered (or hexagonal, onion, and clean), modular monolith, event-driven, microservices, and hybrid, with the signal that triggers each step]({{ site.baseurl }}/assets/img/software-architecture-patterns-explained-evolution.svg){:width="760" height="420" loading="lazy" .responsive_img}
*Each pattern answers the limits of the previous one*

### Step 0: The Script

Every application starts as a script. The first version of FastURL is one file that does two things: it saves a long URL under a short code, and it gives the URL back when you pass it the code. The links live in a JSON file next to the script.

```text
shorten.py     # read the command, validate the URL, generate the code, save, print
links.json     # { "aZ3kQ9": "https://code4projects.net/..." }
```

Reading input, validating the URL, generating the code, storing it, and printing the output all live in a few dozen lines, and that is the right choice. You can read the whole program in one minute, and there is nothing to organize.

Notice what the script *cannot* do: it cannot redirect. A redirect is an HTTP response (`301` or `302` with a `Location` header) that a server sends to a browser. A script on your machine has no browser on the other side, so the closest it gets is printing the URL and opening it for you.

This is fine as long as one person runs it and nothing else depends on it. The first signal arrives as soon as you want a real short link: someone clicks `https://fasturl.dev/aZ3kQ9` in a browser and expects to land on the original page. That needs an HTTP server, a second entry point that must reuse the same validation, code generation, and storage. Copying them into a second file is how the big ball of mud starts. Splitting them is step 1.

### Step 1: Layered Architecture

**The idea.** Split the code into horizontal layers, each with one responsibility, and let each layer depend only on the layer below it. The most common version has three: presentation (the API exposed over HTTP), business logic, and data access.

![Layered architecture: presentation, business logic, and data access stacked on top of each other, each depending on the layer below, with the domain data crossing all three]({{ site.baseurl }}/assets/img/software-architecture-patterns-explained-layered.svg){:width="760" height="486" loading="lazy" .responsive_img}
*Dependencies point down; the domain data travels through every layer*

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

**When to stop here.** Most CRUD-heavy applications with thin business rules should. Mark Richards warns about the "architecture sinkhole" in his O'Reilly report [*Software Architecture Patterns*](https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/): requests that pass through every layer without any layer doing real work. If that describes most of your requests, more structure would only add ceremony.

### Step 1 Alternatives: Hexagonal, Onion, and Clean Architecture

The limit of layered architecture is the direction of its dependencies: the business rules sit on top of the database. Between 2005 and 2012, three architects proposed the same fix in three different ways: turn the dependencies around, put the business rules at the center, and push the database and the web framework to the edge. These are not the next step after layered architecture. They are *alternatives* to it, different ways to organize the inside of the same application.

**A note before we start.** FastURL does not need any of them. It has [one entity]({{ site.baseurl }}/from-domain-design-to-rest-api-building-fasturl-with-fastapi/), a handful of use cases, and rules that fit in a few functions: rebuilding it as hexagonal, onion, or clean would be overengineering, and the real FastURL stays layered. In the next sections I redraw it in each style only for educational purposes, because seeing the same small application organized three ways is the fastest way to understand what each style changes.

#### Hexagonal Architecture (Ports and Adapters)

**The idea.** Replace "top and bottom" with "inside and outside". The application core sits inside a hexagon and talks to the world only through *ports*, interfaces that the core itself defines. On the outside, *adapters* plug into those ports: driving adapters (a REST API, a CLI, the tests) call the application, driven adapters (a database, an HTTP client) are called by it.

**Where it comes from.** Alistair Cockburn described [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture) in 2005. His motivation is the limit of layered architecture, almost word for word. Business logic kept leaking into user interface code, and the usual fix was to add another layer with the promise that no business logic would go there. Without a way to detect violations, he wrote, "the organization finds a few years later that the new layer is cluttered with business logic and the old problem has reappeared". His goal was an application that could be driven equally by users, programs, automated tests, or batch scripts, and developed in isolation from its devices and databases.

The timing explains why the idea caught on. The classic layered picture assumes a simple world: requests arrive from the top, through a web page, and the only external system is the database at the bottom. In the early 2000s that world changed. Salesforce and [eBay](https://thehistoryoftheweb.com/ebay-apis-connected-web/) opened their first web APIs in 2000, Amazon Web Services started selling storage through an API with [Amazon S3 in 2006](https://aws.amazon.com/about-aws/whats-new/2006/03/13/announcing-amazon-s3---simple-storage-service/), and applications began to talk to payment gateways, e-mail providers, partner systems, and message queues, while being called in turn by other programs and not only by browsers.

A layered stack has one top and one bottom, so it has no natural place for all of them. Each new integration ended up squeezed into the data layer or, worse, called directly from the business logic, and every new partner made the core harder to change and to test. The hexagon answers this by drawing the application with as many sides as it needs: each external system, on either side, gets its own port and its own adapter, and adding one more does not touch the core.

![Hexagonal architecture applied to FastURL: the core with Link and LinkService inside a hexagon, driving adapters on the left, driven adapters on the right implementing the LinkRepository and UrlInspector ports]({{ site.baseurl }}/assets/img/software-architecture-patterns-explained-hexagonal.svg){:width="760" height="470" loading="lazy" .responsive_img}
*FastURL as a hexagon: the core owns the ports, the adapters plug in from outside*

**FastURL in hexagonal style** would look like this:

```text
src/fasturl/
├── core/
│   ├── link.py           # the Link entity and its rules
│   ├── link_service.py   # use cases: create, resolve, delete
│   └── ports.py          # LinkRepository, UrlInspector
├── adapters/
│   ├── inbound/          # driving: FastAPI routers
│   └── outbound/         # driven: SQLAlchemy repository, httpx inspector
└── main.py               # plugs the adapters into the ports
```

**What changes compared with layered:**

- `LinkRepository` is no longer a class in the data layer. It becomes an interface in the core, and the SQLAlchemy repository is an adapter that implements it. The database now depends on the core, not the other way round.
- The REST API is no longer "the top layer". It is one driving adapter among others, and the tests drive the core through the same port without starting an HTTP server.
- Every external system gets its own port. The web site that the inspector fetches is a second driven side, as important as the database, instead of a call hidden inside `LinkService`.
- The hexagon says nothing about how the inside is organized. `Link` and `LinkService` live together in the core.

#### Onion Architecture

**The idea.** Take the hexagon and organize its inside. Hexagonal architecture tells you what stays out of the core and how the outside plugs in, but treats the core itself as a single block. Onion architecture keeps the dependencies pointing inward and splits that block into concentric rings.

**Where it comes from.** In 2008, Jeffrey Palermo described the [Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/) with the same diagnosis as Cockburn: traditional layering couples the application to its infrastructure, because "transitive dependencies are still dependencies". If the hexagon already existed, why did he need a new name?

- **Same starting point.** Palermo cites Cockburn's work on hexagonal architecture and says that the two share the same premise: keep the infrastructure outside and connect it through adapters. He did not present the onion as a replacement.
- **What was missing: the inside.** Cockburn's hexagon is about the boundary: what stays outside and how it plugs in. The core is a black box called "application", and Cockburn says nothing about how to organize it.
- **Why it mattered to Palermo.** He worked on long-lived enterprise applications built with Domain-Driven Design, the approach Eric Evans described in 2003. There the core holds entities, domain services, repositories, and application services. With a large domain, the question is where each of them goes and which one may depend on which. The hexagon does not say.
- **His answer: the rings.** The domain model sits at the center and depends on nothing. Around it come the repository interfaces and the domain services, then the application services that coordinate the use cases. The outer ring holds the same adapters as the hexagon: the user interface, the infrastructure, and the tests.

In short, the onion is the hexagon plus the vocabulary of Domain-Driven Design to organize the core.

![Onion architecture applied to FastURL: concentric rings with Link at the center, domain services and the LinkRepository interface around it, application services, and API, infrastructure, and tests on the outer ring]({{ site.baseurl }}/assets/img/software-architecture-patterns-explained-onion.svg){:width="760" height="492" loading="lazy" .responsive_img}
*FastURL as an onion: every ring depends only on the rings inside it*

**FastURL in onion style** would look like this:

```text
src/fasturl/
├── domain/
│   ├── model/            # Link
│   └── services/         # short code generation, LinkRepository interface
├── application/          # create, resolve, delete: orchestration and transactions
├── infrastructure/       # SQLAlchemy repository, httpx inspector
├── api/                  # FastAPI routers
└── main.py
```

**What changes compared with hexagonal:**

- The core is split into rings. `Link` sits alone at the center and does not even know that a repository exists.
- The repository interface gets a precise home, the first ring around the model, and so do the application services that run each use case in a transaction.
- The outside does not change: the outer ring holds the same adapters as the hexagon (API, infrastructure, and tests), and nothing inside imports them. Onion is a hexagon with a structured interior.

#### Clean Architecture

**The idea.** Organize the application around its use cases. Robert C. Martin draws four circles: entities (enterprise rules) at the center, use cases (application rules) around them, interface adapters that convert data between the use cases and the outside world, and frameworks and drivers (the web, the database, external services) on the edge. One rule holds the circles together:

> Source code dependencies can only point inwards.

**Where it comes from.** Martin published [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) in 2012, explicitly noting that Hexagonal, Onion, and similar proposals were "very similar" and unifying them under that rule. His contribution was to make the use case the unit of the design, and to describe precisely how data crosses each boundary.

![Clean architecture applied to FastURL: four circles with the Link entity at the center, the CreateLink, ResolveLink, and DeleteLink use cases, controllers, presenters, and gateways as interface adapters, and FastAPI, SQLAlchemy, and httpx on the outer circle]({{ site.baseurl }}/assets/img/software-architecture-patterns-explained-clean.svg){:width="760" height="492" loading="lazy" .responsive_img}
*FastURL as clean architecture: one class per use case, adapters on both sides*

**FastURL in clean style** would look like this:

```text
src/fasturl/
├── entities/             # Link
├── use_cases/            # CreateLink, ResolveLink, DeleteLink, with their input and output
├── adapters/
│   ├── controllers/      # HTTP request → use case input
│   ├── presenters/       # use case output → JSON response
│   └── gateways/         # SQLAlchemy implementation of LinkRepository
└── frameworks/           # FastAPI app, database engine, httpx client
```

**What changes compared with onion:**

- `LinkService` disappears. Each use case becomes its own class (`CreateLink`, `ResolveLink`, `DeleteLink`) with its own input and output models, so the folder lists what the application *does*.
- Adapters work in both directions. A controller turns the HTTP request into use case input, and a presenter turns the use case output into the response. In the other styles the router did both jobs.
- FastAPI and SQLAlchemy are pushed to the outermost circle and treated as details that could be replaced.

#### One Rule, Three Vocabularies

Side by side, the three styles name the same parts differently:

| **Concept** | **Hexagonal** | **Onion** | **Clean** |
|---|---|---|---|
| **Business rules** | Application (inside) | Domain Model, Domain Services | Entities |
| **Use cases** | Application (inside) | Application Services | Use Cases |
| **Boundary** | Ports | Interfaces in the inner rings | Interface Adapters |
| **Technology** | Adapters | Infrastructure (outer ring) | Frameworks and Drivers |

**In Python**, the key tool for all three is the port: an interface owned by the core. A `typing.Protocol` makes it lightweight, because adapters satisfy it structurally without inheriting from it. The core never imports the SQLAlchemy repository, and the tests can pass an in-memory one.

**Their limit.** Indirection has a price. A single feature now spans more files, and data is mapped between the ORM model, the domain entity, and the Pydantic schema. For an application whose logic is mostly "read a row, return a row", like FastURL, that price buys very little.

**When to choose them.** When the domain is rich, the rules must be tested in milliseconds without a database, or you expect to swap infrastructure. Many teams also apply them selectively: ports only around the dependencies that are likely to change, such as an external API or an LLM provider.

### Step 2: Modular Monolith

**The idea.** As the application grows, the problem shifts from "how do I organize the code?" to "how do I organize *many* features/components and *many* developers?". A modular monolith keeps a single deployable application but splits it vertically into modules by business capability, each with its own internal layers or hexagon and a small public interface.

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

### Step 3: Event-Driven Architecture

**The idea.** Instead of calling each other directly, modules announce that something happened ("a link was created") and let whoever cares react. The producer does not know who the consumers are.

Think of a newspaper. The editor publishes the news once; any number of readers subscribe, and the editor does not need to know them or wait for them.

**Where it comes from.** Events are as old as interrupts, but two milestones matter for application architecture. In 2002, David Luckham's *The Power of Events* introduced complex event processing for making sense of event streams in distributed enterprise systems. Around 2010, Greg Young named and popularized CQRS and Event Sourcing in his [CQRS Documents](https://cqrs.wordpress.com/wp-content/uploads/2010/11/cqrs_documents.pdf), building on Bertrand Meyer's command-query separation ([Udi Dahan](https://udidahan.com/2009/12/09/clarified-cqrs/) had written about similar ideas from 2008). Young's problem was that a rich domain model did not fit a classic three-layer architecture, and that some systems need a complete, auditable log of every change.

By 2017 the term had become so overloaded that Martin Fowler wrote [What do you mean by "Event-Driven"?](https://martinfowler.com/articles/201701-event-driven.html) to separate four different patterns:

| **Pattern** | **What the event carries** | **Main trade-off** |
|---|---|---|
| **Event notification** | "Something happened" and an ID | Very low coupling, but the overall flow is hard to see |
| **Event-carried state transfer** | The data consumers need | Consumers avoid calls back to the source, but keep copies of the data |
| **Event sourcing** | Every change, stored as the source of truth | Full history and replay, but more complex storage and queries |
| **CQRS** | Separate models for writes and reads | Each side can be optimized, but two models must be kept in sync |

**In FastURL**, analytics is a natural fit: the redirect must stay fast, so it records a `LinkClicked` event and returns immediately, and the analytics module processes it later. The gentlest way to start is inside the modular monolith, with an in-process message bus (Cosmic Python dedicates two chapters to it). You can move the same events to a broker such as RabbitMQ, Kafka, or Redis Streams later, when a consumer needs to run in a separate process.

**Its limit.** You trade direct calls for eventual consistency, duplicate deliveries, ordering problems, and flows that you can only reconstruct through monitoring. The first production pitfall is usually the *dual write*: saving to the database and publishing to the broker are two operations, and one of them can fail. The Transactional Outbox pattern exists to solve exactly that.

### Step 4: Microservices

**The idea.** Split the system into small services that are deployed, scaled, and owned independently, each with its own data, communicating over the network through APIs or events.

**Where it comes from.** The direct ancestor is Service-Oriented Architecture (SOA), which in the 2000s promised reusable enterprise services but often ended up centralized around heavyweight middleware. The term "microservices" was discussed at a workshop of software architects near Venice in May 2011 and adopted by the same group in May 2012. Netflix, with Adrian Cockcroft, had been pioneering the approach at web scale and called it "fine grained SOA".

In March 2014, James Lewis and Martin Fowler published the article that defined the style, [Microservices](https://martinfowler.com/articles/microservices.html). The problems they described are the limits of the monolith: change cycles are tied together, so a small change means rebuilding and redeploying everything; modular structure erodes over time; and you can only scale the whole application, not the part under load.

**Adoption is real but not universal.** According to the [CNCF and SlashData](https://www.cncf.io/announcements/2025/11/11/cncf-and-slashdata-survey-finds-cloud-native-ecosystem-surges-to-15-6m-developers/) State of Cloud Native Development report of November 2025, 46% of backend developers use microservices, which means that more than half do not.

**Its limit.** Every in-process function call becomes a network call that can be slow or fail. You need service discovery, distributed tracing, versioned APIs, and an operations team that can run all of it. The most quoted counter-example comes from [Amazon Prime Video](https://www.primevideotech.com/video-streaming/scaling-up-the-prime-video-audio-video-monitoring-service-and-reducing-costs-by-90), whose monitoring team in 2023 moved one workload from distributed serverless components back into a single process and reported an infrastructure cost reduction of over 90%. Distribution is a cost you pay for independence, not a default.

**A note on serverless.** Serverless functions (AWS Lambda, Google Cloud Functions, Azure Functions) are often listed next to microservices. They are better understood as a deployment and billing model: you can deploy a modular monolith, a set of microservices, or a single event consumer as serverless functions.

**When to move here.** When independent teams need to release independently, or one part of the system has scaling or availability needs very different from the rest. FastURL's redirect endpoint, latency-critical and read-heavy, is the first candidate it would ever extract, and only if traffic justified it. Remember that each microservice still needs an internal organization: layered, or one of its alternatives.

### Step 5: Hybrid Architectures

**The idea.** Real systems are rarely pure. A typical production system I would recommend today is a modular monolith in which each module is layered, ports appear only around the dependencies that are likely to change, modules communicate through events, and one or two parts with special needs run as separate services.

Hybrid has no inventor because it is not a pattern: it is what happens when you treat patterns as tools instead of identities. The [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/) puts it best: an architecture style "places constraints on the design", and

> Sometimes it's better to relax a constraint than to chase architectural purity.

The risk of a hybrid is inconsistency: if every module follows a different style for no reason, you are back to the big ball of mud. Record each decision and its reason in an Architecture Decision Record, so that the mix is deliberate and the next developer knows why.

## Other Styles Worth Knowing

Two more styles do not fit the evolution above, but you meet them often in the Python ecosystem:

- **Microkernel (plug-in) architecture** — a small core that defines extension points, plus independent plug-ins that add features. pytest is a classic example: most of its features, and every third-party extension, are plug-ins registered through hooks. Apache Airflow providers and VS Code extensions follow the same idea. Choose it when other people must extend your software without changing its core.
- **Pipes and filters (pipeline)** — data flows through a chain of independent processing steps, each consuming the output of the previous one. It is the natural shape of ETL jobs, machine learning pipelines, and Unix shell commands. Choose it when the problem is a transformation of data rather than a set of interactive use cases.

## How to Choose

There is no best architecture, only the one that fits your requirements today and can evolve tomorrow. This is why the series started from requirements: the non-functional requirements and constraints of [Part 1]({{ site.baseurl }}/lean-requirements-personas-and-scenarios/) are the inputs of this decision. FastURL's 50 ms latency target and its constraint that link creation must not wait for the URL inspection led to a layered, async application with [background work]({{ site.baseurl }}/fastapi-async-background-tasks-and-error-handling/). Different requirements would have led elsewhere.

| **If your requirements say...** | **Consider** |
|---|---|
| **One developer, one entry point, short life** | A script or a single module |
| **Web application, mostly CRUD, thin rules** | Layered (MVC) |
| **Rich domain, fast tests, infrastructure may change** | Hexagonal, Onion, or Clean |
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
- hexagonal, onion, and clean architecture as alternatives to layering, with FastURL redrawn in each style to show what changes;
- the modular monolith and how to enforce its boundaries with import-linter;
- the four meanings of event-driven architecture and the dual-write pitfall;
- microservices, their roots in SOA, their real costs, and where serverless fits;
- hybrid architectures, microkernel and pipeline styles, and how to choose from your requirements.

The [next article]({{ site.baseurl }}/layered-architecture-in-practice/) starts the deep dives with layered architecture in practice: layer rules, strict and relaxed layering, and the trade-offs between packaging by layer, by feature, and by component.

---

If you enjoyed this article, don't forget to **give it a clap 👏**, **share it with your friends 🔗**, and **follow me for more tips and tutorials on software development 📘**. Your support helps me create more content like this — thank you! 🙌

**Note**: English is not my native language, and this article was drafted with the assistance of AI. However, all the ideas, projects, concepts, and content are entirely my own.
