# Code4Projects — Editorial Plan

Last updated: 2026-08  
Author: Salvatore D'Angelo

This document defines the strategic direction of the blog, the active series, and the week-by-week execution plan. It is the **why** and **what next** — `_data/roadmap.yml` is the **operational status** of each individual article.

Bob reads this file automatically when using `blog-advisor` and `post-planner`.

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

## Active Series

### ✅ COMPLETE — Getting Started with Docker 2025
`post_series_id: getting-started-with-docker-2025`  
8 articles published (Jul–Aug 2026). Ebook exists. Lead magnet active.  
**No further articles needed.** Model to replicate.

---

### ✅ COMPLETE — Python CLI with the Command Pattern
`post_series_id: python-cli-command-pattern`  
2 articles published (Nov 2025, Jan 2026). Intentionally short — topic is exhausted.  
**No further articles needed.**

---

### ⚠️ INCOMPLETE — LangChain Chatbot (needs formalisation)
`post_series_id: llm-chatbot-langchain` ← **to be added to all 4 posts**  
4 articles published (Feb 2026). Currently no series ID, no sidebar entry.  
Planned title: **"Build Your Own LLM Chatbot with Python & LangChain"**

Missing:
- [ ] Add `post_series_id: llm-chatbot-langchain` to all 4 post files
- [ ] Add entry to `_data/post_sidebar.yml`
- [ ] Add `series: llm-chatbot-langchain` to all 4 roadmap entries
- [ ] Decide: is Part 4 the final article, or is a Part 5 warranted?

---

### ⚠️ INCOMPLETE — Agentic AI Protocols (needs formalisation)
`post_series_id: agentic-ai-protocols` ← **to be added to A2A and MCP posts**  
2 articles published: A2A (Apr 2026), MCP (May 2026). Currently standalone.  
Planned title: **"Agentic AI: Protocols and Patterns"**

Missing:
- [ ] Add `post_series_id: agentic-ai-protocols` to A2A and MCP posts
- [ ] Add entry to `_data/post_sidebar.yml`
- [ ] Plan next articles (e.g. building a real agent with A2A+MCP, orchestration patterns)

---

### 🔵 PLANNED — Modern Python Application Development
`post_series_id: modern-python-app-dev`  
Planned title: **"Modern Python Application Development"**

**Philosophy**: Python is the vehicle, the principles are universal. Every article teaches a pattern applicable in any language — Python is just the clearest implementation language.

Planned sequence:
1. Python Blueprint — project structure (on Medium, to import)
2. Configuration & Logging — production-grade setup (on Medium, to import)
3. Cron Jobs & Scheduled Tasks (on Medium, to import)
4. **Python CLI with the Command Pattern** ← already published, link into series
5. **Python CLI with Click** ← already published, link into series
6. Data Persistence — files, SQLite, simple ORM patterns
7. Concurrency — threads, processes, when to use which
8. Async & Event Loop — asyncio in practice
9. Building a REST API — FastAPI from scratch
10. Testing — pytest patterns for real applications

Status: articles 1–3 exist on Medium (to import), 4–5 published on blog.  
Articles 6–10 to write.

Missing:
- [ ] Import articles 1–3 from Medium (`medium-importer`)
- [ ] Reassign `post_series_id: modern-python-app-dev` to articles 4–5 (currently `python-cli-command-pattern`)
- [ ] Add entry to `_data/post_sidebar.yml`
- [ ] Plan and write articles 6–10 progressively

> **Note on articles 4–5**: the Python CLI posts currently belong to `python-cli-command-pattern`. Two options: (a) keep them in their own mini-series and reference them from `modern-python-app-dev` with a link, (b) move them into the larger series. Decision deferred — discuss before acting.

---

### 🔵 PLANNED — Getting Started with Kubernetes 2026
`post_series_id: getting-started-with-kubernetes-2026`  
Planned title: **"Getting Started with Kubernetes 2026"**

**Approach**: completely new series, from scratch. The 2019–2020 articles are left as-is (archived). Same model as Docker 2025.

Planned sequence:
1. What is Kubernetes and Why It Exists — concepts, architecture
2. Your First Kubernetes Cluster — minikube / kind locally
3. Pods, Deployments, and ReplicaSets — the building blocks
4. Kubernetes Services — ClusterIP, NodePort, LoadBalancer, Ingress
5. ConfigMaps and Secrets — configuration management
6. Persistent Volumes and Storage — stateful workloads
7. Kubernetes Networking — how pods talk to each other
8. Helm — packaging and deploying applications
9. Kubernetes Security Best Practices
10. Kubernetes in Production — resource limits, health checks, HPA

Ebook: yes — same pipeline as Docker 2025.  
Lead magnet: yes — tag `Virtualization`.

Status: **not started**. Priority for Q4 2026.

---

### 🔵 PLANNED — Build Your Own LLM
`post_series_id: build-your-own-llm`  
Planned title: **"Build Your Own LLM from Scratch"**

High-effort, high-differentiation series. No other blog covers this with 30 years of engineering experience behind it.

Planned sequence (draft — to refine before writing):
1. How LLMs Work — transformers, attention, tokenisation (article exists on Medium, import first)
2. Building a Tokeniser from Scratch
3. Building a Simple Transformer in Python
4. Pre-training — what it means, minimal example
5. Fine-tuning — LoRA, practical approach
6. Inference — serving your model
7. Evaluation — how to know if your model is good

Status: **not started**. Priority Q1 2027. Do not start before Kubernetes 2026 is complete.

---

### ⚙️ DECISION PENDING — Android Game Programming
`post_series_id: android-game-programming`  
12 articles published (2018–2019). Series stopped mid-implementation.

**Decision needed**: complete the original series (3–4 more articles to close the game framework) or freeze consciously.

Arguments for completing:
- Game loop principles are timeless — they don't expire
- Leaving a series mid-implementation is a reader trust issue
- Low effort: the framework is already designed, just needs the missing pieces

Arguments against:
- Android ecosystem has changed significantly (Kotlin, Jetpack Compose)
- The audience for Java Android game programming is shrinking

**Recommended**: complete the original series with the original technology (3–4 articles), add a final "What Has Changed Since 2019" article as a bridge to the modern ecosystem. Then freeze.

Status: **deferred to Q2 2027**.

---

## Week-by-Week Execution Plan

The pace is **1 productive action per week** — not 1 article per week. Some weeks are setup (formalise a series, add IDs), some are writing.

### Phase 1 — Housekeeping (Weeks 1–3)
*Goal: get the existing content properly organised before writing anything new.*

**Week 1**
- [ ] Add `post_series_id: llm-chatbot-langchain` to the 4 LangChain chatbot posts
- [ ] Add `llm-chatbot-langchain` entry to `_data/post_sidebar.yml`
- [ ] Update the 4 roadmap entries with `series: llm-chatbot-langchain`

**Week 2**
- [ ] Add `post_series_id: agentic-ai-protocols` to the A2A and MCP posts
- [ ] Add `agentic-ai-protocols` entry to `_data/post_sidebar.yml`
- [ ] Update the 2 roadmap entries with `series: agentic-ai-protocols`

**Week 3**
- [ ] Import "Python Blueprint" article from Medium (`medium-importer`)
- [ ] Review and publish it
- [ ] Add `modern-python-app-dev` entry to `_data/post_sidebar.yml` (placeholder, will grow)

---

### Phase 2 — Python Modern App Dev (Weeks 4–8)
*Goal: build the series skeleton by importing from Medium + writing the first new article.*

**Week 4**
- [ ] Import "Configuration & Logging" from Medium
- [ ] Review and publish

**Week 5**
- [ ] Import "Cron Jobs & Scheduled Tasks" from Medium
- [ ] Review and publish

**Week 6**
- [ ] Decide: keep Python CLI posts in their own series or absorb into `modern-python-app-dev`
- [ ] Update `post_sidebar.yml` accordingly

**Week 7**
- [ ] Plan and write: "Data Persistence in Python" (article 6 of the series)

**Week 8**
- [ ] Plan and write: "Concurrency in Python — Threads and Processes" (article 7)

---

### Phase 3 — Kubernetes 2026 Launch (Weeks 9–20)
*Goal: publish the first 4 articles of the new Kubernetes series.*

**Week 9**
- [ ] Define the final sequence (10 articles), titles, and `post_series_id`
- [ ] Create `getting-started-with-kubernetes-2026` entry in `post_sidebar.yml`
- [ ] Add all 10 planned articles as `idea` entries in `roadmap.yml`

**Week 10**
- [ ] Plan and write: "What is Kubernetes and Why It Exists" (Part 1)

**Week 11**
- [ ] Plan and write: "Your First Kubernetes Cluster" (Part 2)

**Week 12**
- [ ] Plan and write: "Pods, Deployments, and ReplicaSets" (Part 3)

**Week 13**
- [ ] Plan and write: "Kubernetes Services" (Part 4)

*(Weeks 14–20: Parts 5–10 at the same pace — one article per week)*

---

### Phase 4 — Python Modern App Dev continues (parallel, Weeks 10–20)
*One Python article every 2 weeks, interleaved with Kubernetes.*

- Week 10: "Async & Event Loop in Python" (article 8)
- Week 14: "Building a REST API with FastAPI" (article 9)
- Week 18: "Testing Python Applications with pytest" (article 10)

At the end of Phase 4: **Python Modern App Dev series is complete** → compile ebook.

---

### Phase 5 — Agentic AI expansion (Weeks 21+)
*Q1 2027 — after Kubernetes and Python series are solid.*

- Add articles to the Agentic AI Protocols series
- Begin planning "Build Your Own LLM" series
- Evaluate Android completion

---

## Ebook Pipeline

| Series | Status | Target |
|---|---|---|
| Getting Started with Docker 2025 | ✅ Published | — |
| LangChain Chatbot | ⚠️ Formalise first | Q3 2026 |
| Modern Python App Dev | 🔵 Series not complete | Q4 2026 |
| Kubernetes 2026 | 🔵 Not started | Q2 2027 |
| Build Your Own LLM | 🔵 Not started | Q3 2027 |

---

## Series ID Reference

| Series ID | Title | Status |
|---|---|---|
| `getting-started-with-docker-2025` | Getting Started with Docker 2025 | ✅ Complete |
| `python-cli-command-pattern` | Python CLI with the Command Pattern | ✅ Complete |
| `llm-chatbot-langchain` | Build Your Own LLM Chatbot with LangChain | ⚠️ Needs formalisation |
| `agentic-ai-protocols` | Agentic AI: Protocols and Patterns | ⚠️ Needs formalisation |
| `modern-python-app-dev` | Modern Python Application Development | 🔵 Planned |
| `getting-started-with-kubernetes-2026` | Getting Started with Kubernetes 2026 | 🔵 Planned |
| `build-your-own-llm` | Build Your Own LLM from Scratch | 🔵 Planned |
| `android-game-programming` | Android Game Programming | ⚙️ Decision pending |
| `getting-started-with-docker` | Getting Started with Docker (legacy 2018) | 🗄️ Archived |
| `getting-started-with-kubernetes` | Getting Started with Kubernetes (legacy 2019) | 🗄️ Archived |
| `getting-started-with-amazon-web-services` | Getting Started with AWS | 🗄️ Archived |

---

## How to Use This Document

- **Before planning a new post**: read this file to understand where it fits in the series sequence.
- **Before a blog-advisor session**: Bob reads this file automatically.
- **Update this file** when: a series is completed, a new series starts, priorities shift, or a decision is made on a pending item.
- **Do not** track per-article status here — that lives in `_data/roadmap.yml`.
