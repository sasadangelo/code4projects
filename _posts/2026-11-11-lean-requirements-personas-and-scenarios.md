---
layout: post
title: "From Requirements to Architecture: Lean Requirements with Personas and Scenarios"
post_series_id:
  - modern-python-application
  - software-architecture-patterns
date: 2026-11-11
author: sasadangelo
slug: lean-requirements-personas-and-scenarios
image: /assets/img/lean-requirements-personas-and-scenarios-hero.svg
excerpt: "Requirements without the paperwork: actors, main and alternative scenarios, and acceptance criteria in one Markdown file that stays in sync with the code."
categories:
  - "Software Architecture"
---

![From Requirements to Architecture: Lean Requirements with Personas and Scenarios]({{ site.baseurl }}/assets/img/lean-requirements-personas-and-scenarios-hero.svg){:width="760" height="400" .responsive_img}

## Introduction

Every generation of software engineering has tried to pin requirements down on paper, and every generation has ended up maintaining documents instead of software. I lived through several of those generations: the thick requirements specification nobody read after sign-off, the UML models that drifted away from the code within a month, and the Agile backlog where the real decisions lived only in people's heads.

The lesson I took from all of them is not that requirements are useless. It is that a requirements document survives only if it is small enough to keep up to date and precise enough to settle an argument. Whenever maintaining the documents took longer than building the features, the documents lost. This article shows how I collect requirements today: a single, lean Markdown file that captures who uses the system, what they need to do, and how you know it works — reduced to the bone, and always readable by the people who stay in control of the system.

This article opens both the Modern Python Application series and the Software Architecture Patterns series, because every application starts from its requirements. In the Modern Python Application series I build [FastURL](https://github.com/sasadangelo/fasturl), a URL shortener, from its [domain design]({{ site.baseurl }}/from-domain-design-to-rest-api-building-fasturl-with-fastapi/) all the way to its [tests]({{ site.baseurl }}/testing-fastapi-in-practice/). Its requirements document is the input of every design document that follows, and it is the real example I'll use throughout this article.

You should read this article if:

- you have abandoned requirements documents in the past because they cost more to maintain than they were worth;
- your team agrees on the happy path but discovers the error cases in production;
- you want a minimal, repeatable template that connects requirements to design and tests.

## A Short History of Requirements (and Why We Keep Over-Documenting)

Before proposing yet another template, it is worth looking at what each era got right and why it collapsed. Every element of the lean template comes from one of these eras.

![Timeline of requirements practices from the 1970 waterfall paper to today's lean requirements, showing the amount of documentation rising and falling]({{ site.baseurl }}/assets/img/lean-requirements-personas-and-scenarios-timeline.svg){:width="760" height="300" loading="lazy" .responsive_img}
*Fifty years of requirements practices*

### Waterfall and the Requirements Specification

The sequential model we call "waterfall" traces back to Winston Royce's 1970 paper [Managing the Development of Large Software Systems](https://en.wikipedia.org/wiki/Winston_W._Royce). The irony is that Royce drew the famous sequence of phases as a warning: he wrote that the implementation he described "is risky and invites failure". The industry kept the diagram and skipped the text.

The requirements artifact of that era was the Software Requirements Specification (SRS), later standardized as IEEE 830-1998: a formal, exhaustive document signed off before design began. In my experience, it had one fatal property — it was complete only on the day it was approved. Every change request meant updating the SRS, re-reviewing it, and re-approving it, and teams soon spent more effort keeping the document consistent than building the product. Eventually the code became the real specification and the SRS became an archive.

What survives: the idea that **constraints, non-functional requirements, and scope boundaries must be written down**, because nobody discovers them by reading code.

### UML and Use Cases

In the 1990s, Ivar Jacobson's use cases and the Unified Modeling Language (standardized by the OMG in 1997) promised to make requirements visual and precise. Processes like the Rational Unified Process wrapped them in use case diagrams, sequence diagrams, and activity diagrams.

The diagrams were the weak part. They were expensive to draw, impossible to diff, and drifted from the code as soon as the first refactoring landed. Once again, maintaining the models cost more than the value they returned.

The text was the strong part. Alistair Cockburn's [Writing Effective Use Cases](https://ptgmedia.pearsoncmg.com/images/9780201702255/samplepages/0201702258.pdf) (2000) structured each use case as a **main success scenario** — the path where nothing goes wrong — plus a list of **extensions**: everything that can happen differently, numbered by the step where it is detected. Those two ideas are exactly what we still need today: a main scenario and its alternatives.

### Personas

Around the same time, Alan Cooper popularized [personas](https://en.wikipedia.org/wiki/Persona_(user_experience)) in *The Inmates Are Running the Asylum*: archetypal users with names, goals, and context, used to design for someone specific instead of an "elastic user" who bends to every feature idea.

Personas solved a real problem — "the user" is too vague to design for — but many teams turned them into posters with stock photos, ages, and hobbies. For a development team, most of that detail is noise. What survives is the core: **a role, a goal, and the context in which the goal arises**.

### Agile and User Stories

The [Agile Manifesto](https://agilemanifesto.org/) (2001) valued "working software over comprehensive documentation", and Extreme Programming replaced the SRS with user stories on index cards. Ron Jeffries described a story as [Card, Conversation, Confirmation](https://agilealliance.org/glossary/three-cs/): the card is a reminder, the conversation is where the details are agreed, and the confirmation is the test that proves it works. Mike Cohn's *User Stories Applied* (2004) made the "As a … I want … so that …" format mainstream.

This was the right correction, and it is the approach I describe in [Agile Methodology: A Practical Guide]({{ site.baseurl }}/demystifying-agile-unleashing-flexibility-project-management/). Its weak point is the Conversation: it lives in meetings, chat threads, and people's memory. A stable team can afford that for a while. When people leave, join, or come back to the code a year later, the decisions are gone and only the cards remain.

### DDD, BDD, and Job Stories

Three ideas from the 2000s and early 2010s filled the gaps:

- **Domain-Driven Design** (Eric Evans, 2003) introduced the *ubiquitous language*: the same words in conversations, documents, and code. When requirements say `Link` and `ShortCode`, the code should say `Link` and `ShortCode`. It also put a **domain model** at the centre of the design: a technology-independent description of the entities and their relationships, from which the database, the API, and every other interface are derived.
- **Behaviour-Driven Development** (Dan North, [Introducing BDD](https://dannorth.net/blog/introducing-bdd/), 2006) gave acceptance criteria a shape: *Given some initial context, When an event occurs, Then ensure some outcomes*. Each criterion is a scenario you can turn into a test.
- **Job Stories** came out of Intercom in 2013 and were named by Alan Klement in [Replacing the User Story with the Job Story](https://jtbd.info/replacing-the-user-story-with-the-job-story-af7cdee10c27). They replace `As a <role>` with `When <situation>`: the trigger matters more than the persona label.

![Table comparing five requirements eras by main artifact, what it got right, and why it collapsed]({{ site.baseurl }}/assets/img/lean-requirements-personas-and-scenarios-eras.svg){:width="760" height="400" loading="lazy" .responsive_img}
*What each era got right, and why it collapsed*

Read the last column again. None of these methods failed because its ideas were wrong. They fell out of use because keeping their artifacts up to date grew faster than the project itself: every change in the product triggered a change in the documents, and the documents started to set the pace of delivery instead of the code. Teams responded the only way they could — they stopped updating the documents, and the documents died.

That is the lesson I keep: tracking requirements is worth it only if the cost of maintaining them stays a small fraction of the cost of the changes they describe.

## Lean by Design: Three Principles

Before the template, here are the three principles that decide what goes into it and what stays out.

1. **Cut it to the bone.** Every section must earn its maintenance cost. If nobody would notice a section missing when making a decision, it does not belong in the document. Diagrams that must be redrawn on every change, glossaries that duplicate the code, and traceability matrices maintained by hand are the first things to go.
2. **Write for a human first.** The document must be readable in one sitting: plain Markdown, no special tooling, ideally under 150 lines. If a new team member cannot read it in fifteen minutes and explain what the system does, it is too big.
3. **Keep a human in control.** The requirements are where decisions about the system's evolution are made and recorded. Tools can consume them — today even the AI agents used for vibe coding can read them and let them steer their choices, a topic for a future article — but a person owns every decision and approves every change. That only works if the document stays simple enough for that person to keep the whole system in their head.

## What Every Requirements Document Still Needs

Strip away the ceremony of each era and three things remain: who interacts with the system, what they need to accomplish in which situations, and the rules the system must respect. Everything else is optional.

### Actors and Personas

An **actor** is anyone or anything that interacts with the system: a human role, an external system, or even an internal background process. A **persona** adds the goal and the context. For a lean document, I merge the two into one table row per actor: a name, one sentence of description, and a type.

FastURL has three actors:

| Actor | Description | Type |
|---|---|---|
| `API Client` | An external system or developer that manages short links and inspects metadata through the REST API | System / Human |
| `Public Visitor` | An internet user who opens a short URL and expects an immediate redirect | Human / System |
| `Background Inspector` | An internal asynchronous worker that checks target URL health and metadata after creation | System |

Notice the third actor. Treating the background worker as an actor forces you to write down *its* goals and failure cases, and those became the inspection job stories. Without it, background processing would be treated as an implementation detail, and whoever wrote the code would decide its behaviour alone.

You don't need age, photo, or hobbies. You need enough to answer one question when a requirement is ambiguous: *whose goal does this serve?*

### Scenarios: the Main Path and the Alternatives

A **scenario** is one concrete path through an interaction. Cockburn's two kinds are all you need:

- the **main scenario** (happy path): the actor reaches their goal and nothing goes wrong;
- the **alternative scenarios**: invalid input, conflicts, missing data, timeouts — every way the interaction can deviate, and what the system does then.

In the lean template, a **job story** states the goal, and its **acceptance criteria** list the scenarios: the first Given/When/Then is the main scenario, and every following one is an alternative.

![Anatomy of a job story: the When/I want to/so that statement on top, then one main-scenario acceptance criterion and three alternative-scenario criteria, each mapped to an integration test]({{ site.baseurl }}/assets/img/lean-requirements-personas-and-scenarios-job-story.svg){:width="760" height="420" loading="lazy" .responsive_img}
*A job story with its main and alternative scenarios*

The alternatives are where teams disagree most. Everybody agrees on what "create a short link" means when the input is valid. Whether a past expiry date returns `400` or is silently accepted, or whether a URL pointing at the service itself is rejected, depends on who wrote the code — unless the requirements say it first.

### Constraints, Non-Functional Requirements, Scope, and Open Questions

Four short sections complete the document. Each one prevents a specific kind of drift:

- **Business constraints** are rules that cut across stories ("redirects must use temporary status codes"). Without them, each story re-decides the rule, inconsistently.
- **Non-functional requirements** describe how well the system must work, and they drive the architecture. They are the bridge to the rest of this series. The categories I check every time are:
  - **Performance:** measurable targets, such as FastURL's "under 50 ms at the 95th percentile".
  - **Concurrency:** how much work runs in parallel, and what must never block a request.
  - **Resiliency:** timeouts, retries, and limits on external calls, such as the inspector's 5-second timeout.
  - **Caching:** what can be cached, where, and for how long — and what must never be cached.
  - **Scalability and availability:** expected load, number of instances, and acceptable downtime.
  - **Security:** authentication, authorization, and data protection, even when the answer is "out of scope for now".
  - **Logging and observability:** what to log, what never to log, and how long to keep it.
  - **Configuration:** where settings live, how they are validated, and where secrets go.
- **Out of scope** lists what the system will *not* do. Scope grows by default; this section is how you stop authentication, dashboards, and QR codes from sneaking into the first release.
- **Open questions** record decisions you have not made yet. A developer who sees an open question asks or applies the stated default; a developer who sees nothing invents an answer.

## How to Collect Requirements: an Interview in Three Rounds

A template tells you what to write. It does not tell you how to get the content out of people's heads. I collect requirements with a short interview — with the stakeholders, or with myself when I am the stakeholder — in three rounds, always one question at a time.

![The three interview rounds: round 1 asks seven big-picture questions, round 2 turns goals into job stories and alternative scenarios, round 3 defines Given/When/Then acceptance criteria; each round fills specific sections of the requirements document]({{ site.baseurl }}/assets/img/lean-requirements-personas-and-scenarios-interview.svg){:width="760" height="440" loading="lazy" .responsive_img}
*Collecting requirements in three rounds*

### Round 1: the Big Picture

Seven questions, in this order:

1. **System name.** What are we building?
2. **Purpose.** In two or three sentences, what problem does it solve, and for whom?
3. **Actors.** Who or what interacts with the system — people, external systems, background processes?
4. **Goals.** For each actor, what are the three to five most important things they need to accomplish?
5. **Business constraints.** Which rules must always hold, regardless of the feature?
6. **Non-functional requirements.** Response times, availability, security, compliance, configuration.
7. **Out of scope.** What looks like part of the system but is explicitly not?

At the end of the round, I read the answers back as a short summary and ask for confirmation. Misunderstandings are cheap to fix here and expensive to fix in code.

### Round 2: Job Stories and Alternatives

For each actor and each goal, I ask: *what situation triggers this need, and what outcome do you expect?* The answer becomes a job story. Then comes the question that does most of the work: *what can go wrong?* Invalid data, conflicts, missing resources, unavailable dependencies, permissions. Each answer becomes an alternative scenario of that story, or a separate story when it has its own goal.

### Round 3: Acceptance Criteria

Finally, for each story: *what must be true for this to be done?* I write two to four Given/When/Then criteria — at least one for the main scenario and at least one for the most important alternative — and describe only observable behaviour, never the implementation.

### Start from Whatever Already Exists

You rarely start from a blank page. For FastURL, I first wrote a free-form [`idea.md`](https://github.com/sasadangelo/fasturl/blob/v0.1.0/docs/idea.md): a vision, a feature list, and some technical preferences, written the way I would explain the project to a colleague. That file pre-filled most of round 1, so the interview only had to cover what was missing or ambiguous. The same works with meeting notes, an email thread, or an old specification.

## The Minimal Requirements Template

Here is the complete skeleton the interview fills in. It fits in one Markdown file, it is readable in a diff, and every section has a reason to exist:

```markdown
# Requirements — <System Name>
_Last updated: <date>_

## Overview
<Two or three sentences: what the system does and who it serves.>

## Actors
| Actor | Description | Type |
|-------|-------------|------|
| `<name>` | <one sentence: role, goal, context> | Human / System |

## Job Stories

### Actor: <ActorName>

#### JS-001 — <short title>
**When** <situation>, **I want to** <action>, **so that** <benefit>.

**Acceptance criteria:**
- **Given** <precondition>, **When** <action>, **Then** <outcome>.   ← main scenario
- **Given** <precondition>, **When** <action>, **Then** <outcome>.   ← alternative

**Edge cases / notes:**
- <anything that is not a scenario but must not be lost>

## Business Constraints
1. <rule that applies across stories>

## Non-Functional Requirements
| Category | Requirement |
|----------|-------------|
| Performance | <measurable target> |

## Out of Scope
- <what the system explicitly does not do>

## Open Questions
- <decision not made yet, with the default if any>

## Change Log
| Version | Date | Change |
|---------|------|--------|
| 0.1 | <date> | Initial requirements |
```

A few rules keep it lean:

1. **Stable IDs.** Number stories `JS-001`, `JS-002`, … and never reuse a number. The ID is what issues, commits, and tests refer to.
2. **One file until it hurts.** Split into a folder (`docs/requirements/README.md` plus one file per section) only when the file grows past roughly 150 lines.
3. **What, not how.** Requirements describe observable behaviour. For a REST API, status codes and endpoints *are* observable behaviour; class names and database tables are not.
4. **Scenarios versus notes.** An alternative scenario is an observable behaviour with its own acceptance criterion. Anything else worth remembering — such as FastURL retrying when a random code collides with an existing one — goes under *Edge cases / notes*.
5. **Change log, always.** Every change gets a row. It is the cheapest way to tell a new team member — and your future self — why the document looks the way it does.

## Hands-On: FastURL's Requirements, Story by Story

FastURL's [requirements document](https://github.com/sasadangelo/fasturl/blob/v0.1.0/docs/requirements.md) follows this template exactly. It contains 3 actors, 8 job stories, 7 business constraints, 6 non-functional requirements, 5 out-of-scope items, and 2 open questions — in 146 lines.

### JS-001: One Main Scenario, Three Alternatives

This is the first job story, copied from the document:

```markdown
#### JS-001 — Shorten Target URL with Automatic Code
**When** I provide a valid target URL without specifying a custom alias,
**I want to** generate a unique shortened URL with a random alphanumeric code,
**so that** I can share a compact link with visitors immediately.

**Acceptance criteria:**
- **Given** a valid HTTP/HTTPS target URL in the request payload (with optional
  `expires_at` timestamp), **When** I send `POST /api/v1/links`, **Then** the system
  returns HTTP `201 Created` with the generated 7-character Base62 code, full short URL,
  expiration time, initial state `pending_analysis`, and triggers background inspection.
- **Given** an invalid URL format or unsupported scheme (non-HTTP/HTTPS), **When** I send
  `POST /api/v1/links`, **Then** the system returns HTTP `400 Bad Request` with
  standardized validation details.
- **Given** an expiration date in the past (`expires_at <= now`), **When** I send
  `POST /api/v1/links`, **Then** the system returns HTTP `400 Bad Request`.
- **Given** a target URL that points to the FastURL service itself (self-redirect),
  **When** I send `POST /api/v1/links`, **Then** the system rejects the request with
  HTTP `400 Bad Request` to prevent redirect loops.
```

The first criterion is the main scenario. The other three are the alternatives that came out of the "what can go wrong?" question: an invalid scheme, an expiry in the past, and a self-redirect. The last one is a rule nobody invents while coding the happy path — a short link pointing at the shortener itself creates a redirect loop, and only someone who thought about the domain knows to forbid it.

### JS-006: Why Constraints Must Be Written Down

The redirect story requires `307 Temporary Redirect` (or `302 Found`), and Business Constraint 5 explains why:

> Redirections MUST use temporary redirect status codes (307/302) to prevent aggressive browser caching and preserve click tracking.

A permanent `301` is the textbook choice for a URL shortener, and the one many developers would pick. But browsers cache permanent redirects, so repeat visits would never reach the server and FastURL's click counter would stop counting. One sentence in the requirements prevents a bug that no test would catch unless someone had already thought of it.

### From Scenarios to Tests

Because every scenario is a Given/When/Then statement, each one maps to a test almost mechanically. FastURL's integration tests reference the job stories in their docstrings:

```python
class TestCreateLink:
    """JS-001 / JS-002 — create shortened links."""

    async def test_auto_code_returns_201(self, api_client: httpx.AsyncClient) -> None:
        """A valid payload without custom_code returns 201 with a generated code."""
        ...
```

The job story diagram earlier in this article shows the full mapping for JS-001: one integration test per scenario, from `test_auto_code_returns_201` for the main path to `test_self_redirect_returns_400` for the last alternative.

The tests themselves are described in [Testing FastAPI in Practice]({{ site.baseurl }}/testing-fastapi-in-practice/). The point here is traceability: from any test you can walk back to the scenario and the job story that justify it, and from any scenario you can check whether a test covers it.

## Keeping Requirements Alive

Every requirements format in history worked on the day it was written. The hard part is the day after. Three habits keep the document true: keep it in the repository, make it the first link of a chain of design documents, and change it before the code.

### Keep It in the Repository

The file lives at `docs/requirements.md`, versioned with the code. It is not in a wiki, a slide deck, or a ticketing tool. Anyone who checks out the project gets the requirements at the same commit as the code they describe, and every change to them shows up in a pull request.

### Make It the First Link of a Chain

In FastURL, the requirements file is the input of every other design document, and each document is built from the ones before it:

![FastURL document chain: idea.md feeds requirements.md, which feeds domain-design.md, architecture.md, tech-stack.md, db-design.md, api-design.md, and finally the code; requirements.md also feeds test-strategy.md and the backlog]({{ site.baseurl }}/assets/img/lean-requirements-personas-and-scenarios-doc-chain.svg){:width="760" height="360" loading="lazy" .responsive_img}
*From idea to code: every design document starts from the requirements*

- **Domain design** turns the nouns and verbs of the job stories into entities and operations, as I showed in [From Domain Design to REST API]({{ site.baseurl }}/from-domain-design-to-rest-api-building-fasturl-with-fastapi/).
- **Architecture** reads the non-functional requirements to choose a pattern.
- **API design** turns each story into endpoints and status codes, following the principles in [Designing REST APIs in Practice]({{ site.baseurl }}/designing-rest-apis-in-practice-a-kubernetes-case-study/).
- **Test strategy and backlog** come from the stories too: the acceptance criteria define what to test, and the stories define the work items.

Each document stays focused because it does not repeat what the previous one says. It refers to it. And because everything downstream depends on the requirements, nobody is tempted to let them rot.

### One Domain Model, Many Projections

The step I value most in that chain is the domain model, an idea I take from DDD. The nouns and verbs of the job stories become a technology-independent model: entities, value objects, and the relationships between them. In FastURL, that is the `Link` aggregate with its `ShortCode`, `TargetUrl`, `LinkInspection`, and `LinkMetrics`.

![The domain model derived from requirements.md, with the Link aggregate and its value objects, projected onto a database, a REST API, a command line, and a user interface]({{ site.baseurl }}/assets/img/lean-requirements-personas-and-scenarios-domain-projections.svg){:width="760" height="380" loading="lazy" .responsive_img}
*One domain model, many projections*

The domain model plays the role the logical entity-relationship diagram played in classic database design, but it is not tied to a database. From the same model you derive every physical projection:

- **Database.** FastURL's [`db-design.md`](https://github.com/sasadangelo/fasturl/blob/v0.1.0/docs/db-design.md) starts from a logical model of the `Link` aggregate and maps it to a physical `links` table, with the value objects embedded as columns.
- **REST API.** In [`api-design.md`](https://github.com/sasadangelo/fasturl/blob/v0.1.0/docs/api-design.md), the same aggregate becomes the `/api/v1/links` and `/api/v1/links/{code}` resources, and `LinkInspection` becomes the `/inspect` action.
- **Command line.** FastURL has no CLI, but the same model would map to commands such as `links create` or `links inspect`.
- **User interface.** A web or mobile front end would map it to list, detail, and creation screens.

When a requirement changes, you update the domain model once, and each projection follows from it. This is also why requirements must use the domain's words: a term that appears in a job story will reappear in the table, the endpoint, the command, and the screen.

### Change the Requirements Before the Code

When something changes, update the requirements first, then the design, then the code. FastURL's change log records one such decision: version 0.4 added PostgreSQL as an alternative backend and moved secrets to `.env`, and the persistence and configuration requirements changed in the same commit as the code. Months later, the date and the reason are still one line away.

The reverse order — change the code, "update the docs later" — is how every requirements document in history became obsolete.

### Anti-Patterns to Avoid

- **Requirements outside the repository.** A wiki page drifts the moment the code changes without it.
- **Implementation details in requirements.** "Use a `LinkRepository` class" belongs in the design documents. Requirements that dictate structure freeze the architecture before you have chosen one.
- **Only the happy path.** A story without alternative scenarios postpones every hard decision to the person writing the code.
- **Personas as decoration.** If a field does not help resolve an ambiguous requirement, delete it.

## From Requirements to Architecture

The job stories tell you *what* the system does. The non-functional requirements and constraints tell you *how well* it must do it — and that is what drives the architecture.

FastURL's requirements contain two decisive lines: link creation must respond without waiting for the inspection (Business Constraint 4), and the API must answer in under 50 ms at the 95th percentile. Together they require non-blocking I/O and background work, which led to an async FastAPI application with a [layered architecture]({{ site.baseurl }}/layered-architecture-with-fastapi-routers-services-and-repositories/): routers, services, and repositories, with the inspection running outside the request.

![Business Constraint 4 and the 50 ms performance requirement imply background work and non-blocking I/O, which lead to an async, layered FastAPI architecture with BackgroundTasks for link inspection]({{ site.baseurl }}/assets/img/lean-requirements-personas-and-scenarios-nfr-to-architecture.svg){:width="760" height="320" loading="lazy" .responsive_img}
*From two requirements to an architecture*

A different set of requirements — multiple delivery channels, a domain that must outlive its frameworks, or many independent consumers of the same events — would have pointed to hexagonal, clean, or event-driven architecture. The rest of this series covers each of them, always starting from the requirements that justify them.

## Conclusion

Requirements have swung between too much documentation and too little for fifty years, and most methods fell out of use because maintaining their documents slowed projects down more than it helped. The fix is not a new notation: it is a small document that combines the best idea of each era, costs little to keep current, and stays readable by the people who decide how the system evolves.

In this article we covered:

- why each era of requirements engineering collapsed, and which idea from each one survives;
- three principles for lean requirements: cut to the bone, write for a human, keep a human in control;
- the three things every requirements document still needs: actors, scenarios, and cross-cutting rules;
- a three-round interview to collect requirements, from the big picture to acceptance criteria;
- a minimal Markdown template with stable job story IDs and Given/When/Then acceptance criteria;
- how FastURL's `requirements.md` maps main and alternative scenarios to integration tests;
- how one domain model, derived from the requirements, projects onto the database, the API, a CLI, and a UI;
- how to keep requirements alive, and how non-functional requirements lead to an architecture.

From here, the two series take different paths. In the Modern Python Application series, the next step is turning requirements into a working codebase, starting with [How to Set Up Your Next Python Project]({{ site.baseurl }}/how-to-set-up-your-next-python-project/). In the Software Architecture Patterns series, the next article, *Layered Architecture in Practice*, takes the first of those patterns and compares its three packaging styles: by layer, by feature, and by component.

---

If you enjoyed this article, don't forget to **give it a clap 👏**, **share it with your friends 🔗**, and **follow me for more tips and tutorials on software development 📘**. Your support helps me create more content like this — thank you! 🙌

**Note**: English is not my native language, and this article was drafted with the assistance of AI. However, all the ideas, projects, concepts, and content are entirely my own.
