# Code4Projects — Editorial Plan

Last updated: 2026-10
Author: Salvatore D'Angelo

This document defines the strategic direction of the blog, the active series, and the week-by-week execution plan. It is the **why** and **what next** — `_data/roadmap.yml` is the **operational status** of each individual article.

Bob reads this file automatically when using `blog-advisor` and `blog-planner`.

---

## Blog Mission

> "A website about software programming where I write everything I learnt in over 30 years of experience."

Primary goal: **professional growth and reputation**.
Secondary goal: **reader value** — practitioners who want depth, not tutorials copied from the docs.
Tertiary goal: **audience growth** — newsletter subscribers via ebook lead magnets.

---

## The Series Model (non-negotiable)

Every major topic becomes a **series**:

1. 6–10 progressive articles with a shared `post_series_id`
2. Entry in `_data/post_sidebar.yml` so readers can navigate
3. An **ebook** compiled from the series (like the Docker 2025 ebook)
4. A **lead magnet**: any article in the series shows the ebook → newsletter signup

Docker 2025 is the reference implementation. All new series follow this model.

---

## Series Status Overview

| Series ID | Title | Status | Articles |
|---|---|---|---|
| `getting-started-with-docker-2025` | Getting Started with Docker 2025 | ✅ Complete | 8 published |
| `python-cli` | Python CLI (standalone mini-series) | ✅ Complete | 3 published |
| `llm-chatbot-langchain` | Build Your Own LLM Chatbot with LangChain | ✅ Complete | 4 published |
| `agentic-ai-protocols` | Agentic AI: Protocols and Patterns | 🔵 In progress | 2 published, 3 planned |
| `modern-python-application` | Modern Python Application Development | 🔵 In progress | 10 published, 1 planned |
| `software-architecture-patterns` | Software Architecture Patterns | 🔵 In progress | 0 published, 2 planned, 4 ideas |
| `getting-started-with-html` | Getting Started with HTML & CSS | 🔵 In progress | 3 published, 1 planned |
| `getting-started-with-git` | Getting Started with Git | 🔵 Planned | 0 published, 2 planned, 2 ideas |
| `getting-started-with-kubernetes-2026` | Getting Started with Kubernetes 2026 | 🔵 Planned | 0 published, 10 ideas |
| `generative-and-agentic-ai` | Generative and Agentic AI | 🔵 Planned | 0 published, 5 ideas |
| `android-game-programming` | Android Game Programming | ⚙️ Decision pending | 12 published, stopped mid-series |
| `getting-started-with-docker` | Getting Started with Docker (legacy 2018) | 🗄️ Archived | 7 published |
| `getting-started-with-kubernetes` | Getting Started with Kubernetes (legacy 2019) | 🗄️ Archived | 4 published |
| `getting-started-with-amazon-web-services` | Getting Started with AWS | 🗄️ Archived | 16 published |
| `raspberry-media-center` | Raspberry Media Center | 🗄️ Archived | 8 published |

---

## Active Series — Detail

### ✅ COMPLETE — Getting Started with Docker 2025
`post_series_id: getting-started-with-docker-2025`
8 articles published (Jul–Aug 2026). Ebook exists. Lead magnet active.
**No further articles needed.** Model to replicate for all future series.

---

### ✅ COMPLETE — Python CLI
`post_series_id: python-cli`
3 articles published (Nov 2025, Jan 2026, Aug 2026). Intentionally short — topic is exhausted.
**No further articles needed.**

---

### ✅ COMPLETE — LangChain Chatbot
`post_series_id: llm-chatbot-langchain`
4 articles published (Feb 2026). Series complete.
Ebook title: **"Build Your Own LLM Chatbot with Python & LangChain"**
**No further articles needed** unless a Part 5 (Deployment or Agents & Tools) is explicitly approved.

---

### 🔵 IN PROGRESS — Modern Python Application Development
`post_series_id: modern-python-application`
Planned title: **"Modern Python Application Development"**

**Philosophy**: Python is the vehicle, the principles are universal. Every article teaches a pattern applicable in any language.

Current state:
| # | Title | Status |
|---|---|---|
| 1 | How to Set Up Your Next Python Project | ✅ published (2025-11-08) |
| 2 | Managing Application Configuration in Python with Pydantic Settings | ✅ published (2025-12-30) |
| 3 | How to Create Cron Jobs in Python for Your Applications | ✅ published (2026-01-02) |
| 4 | Building a Database Layer in Python with SQLAlchemy ORM | ✅ published (2026-08-24) |
| 5 | Concurrency in Python: Threads, Processes, and the Event Loop | ✅ published (2026-09-06) |
| 6 | Async and the Event Loop in Python: asyncio in Practice | ✅ published (2026-09-13) |
| 7 | Designing REST APIs in Practice: A Kubernetes Case Study | ✅ published (2026-09-16) |
| 8 | From Domain Design to REST API: Building FastURL with FastAPI | ✅ published (2026-10-03) |
| 9 | Layered Architecture with FastAPI: Routers, Services, and Repositories | ✅ published (2026-10-06) |
| 10 | Async, Background Tasks, and Error Handling in FastAPI | ✅ published (2026-10-06) |
| 11 | Testing Python Applications with pytest: Patterns for Real Code | 🔵 planned (2026-10-13) |

Next step: write and publish article 11 (pytest) → series complete → compile ebook.

---

### 🔵 IN PROGRESS — Agentic AI: Protocols and Patterns
`post_series_id: agentic-ai-protocols`
Planned title: **"Agentic AI: Protocols and Patterns"**

Current state:
| # | Title | Status |
|---|---|---|
| 1 | Understanding A2A: The Protocol for Agent Collaboration | ✅ published (2026-04-30) |
| 2 | Understanding MCP: The Protocol for Agent-Tool Communication | ✅ published (2026-05-10) |
| 3 | Building a Real Agent with A2A + MCP | 🔵 planned (Phase 5) |
| 4 | Multi-Agent Orchestration Patterns | 🔵 planned (Phase 5) |
| 5 | Agentic AI in Production — observability, failure modes, cost control | 🔵 planned (Phase 5) |

No further articles until Phase 5 begins.

---

### 🔵 IN PROGRESS — Software Architecture Patterns
`post_series_id: software-architecture-patterns`
Planned title: **"Software Architecture Patterns"**

Current state:
| # | Title | Status |
|---|---|---|
| 1 | From Requirements to Architecture: A Decision Guide to Software Architectural Patterns | 🔵 planned (2026-10-19) |
| 2 | Layered Architecture in Practice: Package by Layer, Feature, and Component | 🔵 planned (2026-10-16) |
| 3 | Hexagonal Architecture (Ports and Adapters) | 💡 idea |
| 4 | Clean Architecture: Building Testable and Framework-Independent Systems | 💡 idea |
| 5 | Event-Driven Architecture: Decoupling Systems with Events and Brokers | 💡 idea |
| 6 | Pragmatic Hybrid Architectures: Combining Patterns for Real-World Systems | 💡 idea |

---

### 🔵 IN PROGRESS — Getting Started with HTML & CSS
`post_series_id: getting-started-with-html`
Planned title: **"Getting Started with HTML & CSS"**

Current state:
| # | Title | Status |
|---|---|---|
| 1 | Getting Started with HTML: A Beginner's Guide | ✅ published (2023-01-23) |
| 2 | Mastering the Basics of CSS: A Beginner's Guide | ✅ published (2023-02-13) |
| 3 | Building a Professional Website Layout with CSS | ✅ published (2026-10-07) |
| 4 | Building the Complete Website: Real Pages, HTML Forms, and a Photo Gallery | 🔵 planned (2026-10-10) |

---

### 🔵 PLANNED — Getting Started with Kubernetes 2026
`post_series_id: getting-started-with-kubernetes-2026`
Planned title: **"Getting Started with Kubernetes 2026"**

**Approach**: completely new series, from scratch. The 2019–2020 articles are left as-is (archived). Same model as Docker 2025. Part of the **DevOps super-series** (see below).

Planned sequence:
| # | Title | Status |
|---|---|---|
| 1 | What is Kubernetes and Why It Exists | 💡 idea |
| 2 | Your First Kubernetes Cluster | 💡 idea |
| 3 | Pods, Deployments, and ReplicaSets: The Building Blocks of Kubernetes | 💡 idea |
| 4 | Kubernetes Services: ClusterIP, NodePort, LoadBalancer, and Ingress | 💡 idea |
| 5 | Kubernetes ConfigMaps and Secrets: Configuration Management | 💡 idea |
| 6 | Kubernetes Persistent Volumes and Storage: Stateful Workloads | 💡 idea |
| 7 | Kubernetes Networking: How Pods Talk to Each Other | 💡 idea |
| 8 | Helm: Packaging and Deploying Applications on Kubernetes | 💡 idea |
| 9 | Kubernetes Security Best Practices | 💡 idea |
| 10 | Kubernetes in Production: Resource Limits, Health Checks, and HPA | 💡 idea |

Ebook: yes — same pipeline as Docker 2025.
Lead magnet: yes — tag `Virtualization`.
Priority: **Q4 2026 / Q1 2027**.

---

### 🔵 PLANNED — Getting Started with Git
`post_series_id: getting-started-with-git`
Planned title: **"Getting Started with Git"**

Planned sequence:
| # | Title | Status |
|---|---|---|
| 1 | What is Git and Basic Commands | 💡 idea |
| 2 | Beyond Push and Pull: Understanding Git's Core Concepts to Avoid Common Pitfalls | 🔵 planned (import from Medium) |
| 3 | The Hidden Challenges of Git: Lessons from Working in Large Projects | 🔵 planned (import from Medium) |
| 4 | Git Merge vs Rebase: When to Use Which and Why It Matters | 💡 idea |

Ebook: evaluate after completion (may combine with a broader DevOps ebook).
Priority: **Q1 2027** (after Kubernetes 2026).

---

### 🔵 PLANNED — DevOps Super-Series (umbrella)
Three sub-series grouped under a single DevOps umbrella:
**"DevOps: From Containers to Orchestration"**

| Sub-series | Series ID | Status |
|---|---|---|
| Getting Started with Docker 2025 | `getting-started-with-docker-2025` | ✅ Complete (8 articles) |
| Getting Started with Kubernetes 2026 | `getting-started-with-kubernetes-2026` | 🔵 Planned (Q4 2026) |
| Getting Started with Git | `getting-started-with-git` | 🔵 Planned (Q1 2027) |

Implementation tasks:
- [ ] Create a DevOps landing page or sidebar section in `_data/post_sidebar.yml` grouping the 3 sub-series
- [ ] Each sub-series intro article links to the DevOps landing page
- [ ] Evaluate a combined DevOps ebook once all 3 sub-series are complete (Q2 2027)

---

### 🔵 PLANNED — Generative and Agentic AI
`post_series_id: generative-and-agentic-ai`
Planned title: **"Generative and Agentic AI: A Practical Guide"**

Planned sequence:
| # | Title | Status |
|---|---|---|
| 1 | Artificial Intelligence: A Practical Introduction for Beginners | 💡 idea |
| 2 | Don't Fear Intelligent Machines: Work with Them | 💡 idea |
| 3 | What Is an AI Agent? Building Autonomous Workflows with LangChain and LangGraph | 💡 idea |
| 4 | Multi-Agent Design Patterns: Supervisor, Pipeline, and Fan-Out/Fan-In | 💡 idea |
| 5 | Architecting an Agentic Platform: File-Based Agents, SKILL.md, and Golem | 💡 idea |

Priority: **Q2 2027**.

---

### ⚙️ DECISION PENDING — Android Game Programming
`post_series_id: android-game-programming`
12 articles published (2018–2019). Series stopped mid-implementation.

**Decision needed**: complete the original series (3–4 more articles to close the game framework) or freeze consciously.

Arguments for completing:
- Game loop principles are timeless — they don't expire
- Leaving a series mid-implementation is a reader trust issue
- Low effort: the framework is already designed

Arguments against:
- Android ecosystem has changed significantly (Kotlin, Jetpack Compose)
- The audience for Java Android game programming is shrinking

**Recommended**: complete the original series with the original technology, add a final "What Has Changed Since 2019" bridge article. Then freeze.

Status: **deferred to Q3 2027**.

---

## Ebook Pipeline

| Series | Status | Target |
|---|---|---|
| Getting Started with Docker 2025 | ✅ Published | — |
| LangChain Chatbot | ⚠️ Formalise ebook | Q4 2026 |
| Modern Python App Dev | 🔵 1 article remaining | Q4 2026 |
| HTML & CSS | 🔵 1 article remaining | Q4 2026 |
| Software Architecture Patterns | 🔵 Series in progress | Q1 2027 |
| Kubernetes 2026 | 🔵 Not started | Q2 2027 |
| Getting Started with Git | 🔵 Not started | Q2 2027 |
| DevOps combined ebook | 🔵 Evaluate post-completion | Q3 2027 |
| Generative and Agentic AI | 🔵 Not started | Q3 2027 |

---

## Week-by-Week Execution Plan

The pace is **1 productive action per week** — not always 1 article per week. Some weeks are setup (formalise a series, add IDs), some are writing.

### Phase 1 — Housekeeping ✅ Done
*Goal: get the existing content properly organised.*

- [x] Add `post_series_id: llm-chatbot-langchain` to the 4 LangChain chatbot posts
- [x] Add `llm-chatbot-langchain` entry to `_data/post_sidebar.yml`
- [x] Add `post_series_id: agentic-ai-protocols` to the A2A and MCP posts
- [x] Add `agentic-ai-protocols` entry to `_data/post_sidebar.yml`
- [x] Import "Python Blueprint" article from Medium
- [x] Add `modern-python-application` entry to `_data/post_sidebar.yml`

---

### Phase 2 — Modern Python App Dev ✅ Nearly complete

- [x] Import "Configuration & Logging" from Medium
- [x] Import "Cron Jobs & Scheduled Tasks" from Medium
- [x] Write "Data Persistence in Python" (SQLAlchemy)
- [x] Write "Concurrency in Python"
- [x] Write "Async & Event Loop in Python"
- [x] Write "Designing REST APIs in Practice"
- [x] Write "From Domain Design to REST API: Building FastURL with FastAPI"
- [x] Write "Layered Architecture with FastAPI"
- [x] Write "Async, Background Tasks, and Error Handling in FastAPI"
- [ ] Write "Testing Python Applications with pytest" → **series complete → compile ebook**

---

### Phase 3 — HTML & CSS series close-out

- [x] Write "Building a Professional Website Layout with CSS" (Part 3)
- [ ] Write "Building the Complete Website" (Part 4) → **series complete → compile ebook**

---

### Phase 4 — Software Architecture Patterns (Weeks current+1 to +4)
*Goal: publish first 2 articles of the new series.*

- [ ] Write "From Requirements to Architecture: A Decision Guide" (Part 1) — planned 2026-10-19
- [ ] Write "Layered Architecture in Practice" (Part 2) — planned 2026-10-16
- [ ] Write "Hexagonal Architecture" (Part 3) — idea
- [ ] Write "Clean Architecture" (Part 4) — idea
- [ ] Write "Event-Driven Architecture" (Part 5) — idea
- [ ] Write "Pragmatic Hybrid Architectures" (Part 6) — idea → **series complete → compile ebook**

---

### Phase 5 — Kubernetes 2026 (Q4 2026 / Q1 2027)
*Goal: publish all 10 articles of the Kubernetes series.*

- [ ] Create `getting-started-with-kubernetes-2026` entry in `post_sidebar.yml`
- [ ] Write Part 1: "What is Kubernetes and Why It Exists"
- [ ] Write Part 2: "Your First Kubernetes Cluster"
- [ ] Write Part 3: "Pods, Deployments, and ReplicaSets"
- [ ] Write Part 4: "Kubernetes Services"
- [ ] Write Part 5: "Kubernetes ConfigMaps and Secrets"
- [ ] Write Part 6: "Kubernetes Persistent Volumes and Storage"
- [ ] Write Part 7: "Kubernetes Networking"
- [ ] Write Part 8: "Helm"
- [ ] Write Part 9: "Kubernetes Security Best Practices"
- [ ] Write Part 10: "Kubernetes in Production" → **series complete → compile ebook**

---

### Phase 6 — Git Series + DevOps umbrella (Q1 2027)

- [ ] Write Part 1: "What is Git and Basic Commands"
- [ ] Import Part 2 from Medium: "Beyond Push and Pull"
- [ ] Import Part 3 from Medium: "The Hidden Challenges of Git"
- [ ] Write Part 4: "Git Merge vs Rebase"
- [ ] Create DevOps landing page / sidebar group linking all 3 sub-series
- [ ] Evaluate combined DevOps ebook

---

### Phase 7 — Agentic AI expansion + Generative AI intro (Q2 2027)

- [ ] Write Agentic AI Part 3: "Building a Real Agent with A2A + MCP"
- [ ] Write Agentic AI Part 4: "Multi-Agent Orchestration Patterns"
- [ ] Write Agentic AI Part 5: "Agentic AI in Production"
- [ ] Begin Generative and Agentic AI series (5 articles)

---

### Phase 8 — Android completion (Q3 2027)

- [ ] Write 3–4 articles to close the Android Game Framework
- [ ] Write "What Has Changed Since 2019" bridge article
- [ ] Freeze the series

---

## Series ID Reference

| Series ID | Title | Status |
|---|---|---|
| `getting-started-with-docker-2025` | Getting Started with Docker 2025 | ✅ Complete — DevOps sub-series |
| `python-cli` | Python CLI | ✅ Complete |
| `llm-chatbot-langchain` | Build Your Own LLM Chatbot with LangChain | ✅ Complete |
| `agentic-ai-protocols` | Agentic AI: Protocols and Patterns | 🔵 In progress (2 of 5) |
| `modern-python-application` | Modern Python Application Development | 🔵 In progress (10 of 11) |
| `software-architecture-patterns` | Software Architecture Patterns | 🔵 In progress (0 of 6) |
| `getting-started-with-html` | Getting Started with HTML & CSS | 🔵 In progress (3 of 4) |
| `getting-started-with-git` | Getting Started with Git | 🔵 Planned — DevOps sub-series |
| `getting-started-with-kubernetes-2026` | Getting Started with Kubernetes 2026 | 🔵 Planned — DevOps sub-series |
| `generative-and-agentic-ai` | Generative and Agentic AI: A Practical Guide | 🔵 Planned |
| `android-game-programming` | Android Game Programming | ⚙️ Decision pending — Q3 2027 |
| `getting-started-with-docker` | Getting Started with Docker (legacy 2018) | 🗄️ Archived |
| `getting-started-with-kubernetes` | Getting Started with Kubernetes (legacy 2019) | 🗄️ Archived |
| `getting-started-with-amazon-web-services` | Getting Started with AWS | 🗄️ Archived |
| `raspberry-media-center` | Raspberry Media Center | 🗄️ Archived |
| `getting-started-with-yaml` | Getting Started with YAML | 🗄️ Standalone (2 articles) |

---

## How to Use This Document

- **Before planning a new post**: read this file to understand where it fits in the series sequence.
- **Before a blog-advisor session**: Bob reads this file automatically.
- **Update this file** when: a series is completed, a new series starts, priorities shift, or a decision is made on a pending item.
- **Do not** track per-article status here — that lives in `_data/roadmap.yml`.
