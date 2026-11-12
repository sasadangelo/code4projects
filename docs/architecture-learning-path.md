# Architecture Learning Path

A progressive path to learn Software Architecture and System Design by building real applications.

The document has two parts:

- **[Part 1 — Projects in progress](#part-1--projects-in-progress)**: projects I have already started. They come
  first, to avoid dispersion.
- **[Part 2 — New apps](#part-2--new-apps)**: classic system design apps that do not exist yet. Each one is worth
  building only for the deltas Part 1 does not cover.

In both parts every step adds **one main architectural delta** to the previous ones. The order follows the evolution
described in the [Software Architecture Patterns](editorial-plan.md) series: layered → hexagonal/clean → modular
monolith with events → microservices → distributed systems.

# Part 1 — Projects in progress

Instead of opening a new repository for every pattern, each carrier project goes through several versions.

## Carrier projects

| Carrier | Repositories | State (2026-11-12) | Steps |
|---------|--------------|--------------------|-------|
| **Running** | `races`, `runanalyze`, `running-coach-ai` → `software-architect-blueprints/strava-like` | 47 + 224 + 78 commits, active | 1–4, 7, 10, 11, 15–19 |
| **FastURL** | `fasturl` | 21 commits, active | 5, 14 |
| **Investitore Intelligente** | `investitore-intelligente` (absorbs the ETF part of `finance`) | 78 commits, active | 6, 12, 20 |
| **Turni Facili** | `turni-facili` (absorbs `farmacia-turni`, `employee-shift-scheduler`) | 13 commits, MVP in progress | 8, 21 |
| **ChatterPy** | `chatterpy` | 34 commits | 9, 13 |
| **Golem** | `golem-control-plane`, `golem-runner`, `golem-cli` | 79 + 34 + 23 commits, active | 22, 23 |
| **E-shop** | `software-architect-blueprints/eshop` (Node.js + TypeScript backend, React UI) | Docs and code started | Not placed yet: overlaps with steps 16–17 (microservices, saga) |

## Phase 1 — A well-built monolith

| # | Project | Architectural delta | Concrete need |
|---|---------|---------------------|---------------|
| 1 | **races** v0.0.2 ✅ | Three-tier architecture, CRUD, transactions, pagination | Running events in the province of Rome |
| 2 | **races** v0.1.0 | Richer domain model: Users → Events → Races hierarchy, ownership and cascade rules, schema migrations | An event (e.g. a festival) contains several races; each event belongs to a user (planned article: "From CRUD to Web Application: Modeling Users, Events, and Races in Flask") |
| 3 | **races** v0.2.0 | Registrations: N:M relationship with its own attributes (Registration entity), state machine (pending → confirmed → cancelled), business-rule validation | Runners register for races |
| 4 | **races** v0.3.0 | Authentication and authorization: local + Google OAuth login (already partly present), roles (admin, organizer, runner), ownership-based checks (an organizer edits only their own events) | Not everyone can edit everything |
| 5 | **fasturl** v1 (done) → cache | Async REST API, background tasks; next: cache-aside with Redis on redirects | Redirects are the hot path |
| 6 | **investitore-intelligente** v1 | Tactical DDD + Hexagonal: Teleborsa as a port with its adapter, `Decimal`, value objects; add ETFs from `finance` | BOT/BTP and ETF in a single app |
| 7 | **runanalyze** v1 | Idempotent ingestion (Garmin/FIT files deduplicated by hash), raw files on object storage, time-series modeling | Training, weight, sleep, HRV history |
| 8 | **turni-facili** v1 | Multi-tenancy (each pharmacy is a tenant) with tenant isolation, reusing the auth model from step 4 | Shifts for pharmacies and small businesses |

## Phase 2 — Asynchrony, integration, concurrency

| # | Project | Architectural delta | Concrete need |
|---|---------|---------------------|---------------|
| 9 | **chatterpy** v1 | Message queue and workers for document ingestion (PDF, Wikipedia → embeddings), retry with backoff, Dead Letter Queue | DataWeave ingestion is slow and fails on bad documents |
| 10 | **runanalyze** v2 | Integration with an unreliable external API: Anti-Corruption Layer, scheduled sync, outbound rate limiting | Automatic sync from Garmin Connect |
| 11 | **races** v0.4.0 | Concurrency under contention: limited race bibs, optimistic/pessimistic locking, idempotency keys | Registrations open, many runners click at once |
| 12 | **investitore-intelligente** v2 | Scheduler + Transactional Outbox: an operation and its event saved atomically | Alerts on BOT auctions, coupons, and maturities |
| 13 | **chatterpy** v2 | Resilience as an LLM gateway: provider fallback (OpenAI, Ollama, WatsonX), circuit breaker, bulkhead, timeouts, SSE streaming | A provider is down or slow |

## Phase 3 — Scale, modular monolith, microservices

| # | Project | Architectural delta | Concrete need |
|---|---------|---------------------|---------------|
| 14 | **fasturl** v2 | Horizontal scaling: stateless app, load balancer, read replicas, rate limiting, key-space sharding | 100M links |
| 15 | **Running Platform** v1: races + runanalyze + running-coach-ai | Modular monolith: bounded contexts and internal domain events | One platform instead of three separate apps |
| 16 | **Running Platform** v2 | Microservice extraction (Strangler Fig), API Gateway, synchronous vs asynchronous communication | Contexts evolve at different speeds |
| 17 | **Race registration** | Saga: available spot → medical certificate → payment → bib number, with compensations | Registration spans several services |
| 18 | **Activity tracking and live races** | Streaming ingestion (Kafka), geospatial indexing, live updates via WebSocket | GPS tracks and live race tracking |
| 19 | **Runners' social feed** (`strava-like`) | Fan-out on write vs fan-out on read | Following other runners |
| 20 | **investitore-intelligente** v3 | Event Sourcing + CQRS | Portfolio value at any past date |
| 21 | **turni-facili** v2 (mobile) | Offline-first: synchronization and conflict resolution (Last-Write-Wins → CRDT) | Shifts edited on the phone without network |

## Phase 4 — Distributed platform

| # | Project | Architectural delta | Concrete need |
|---|---------|---------------------|---------------|
| 22 | **Golem Control Plane** | Control plane / data plane separation, reconciliation loop (Kubernetes operator model), leader election, runner heartbeats | Several control plane replicas, runners that die |
| 23 | **Golem multi-cluster** | Agent placement across clusters with consistent hashing, per-tenant quotas, distributed observability | Multi-cloud vision of Golem |

## Left out on purpose

- `fantacalcio`, `download-media`, `family-budget`: their deltas (concurrency, queues, idempotent ingestion) moved to
  races, chatterpy, and runanalyze.
- `chess`, `flashcards-app`, `serena`, `scopri-roma`: active or useful, but they do not add a new architectural delta.

# Part 2 — New apps

Apps that do not exist yet: the classic system design catalogue, plus one real need of mine. Three classic apps are
not here because they already exist in Part 1: **FastURL** (`fasturl`), **RaceTracker** (`races`), and
**Bond & ETF Manager** (`investitore-intelligente`). **ShopCore** corresponds to the `eshop` blueprint, already
started.

The *Overlap with Part 1* column shows whether a delta is already learned on a project in progress. Apps marked
**new delta** teach something Part 1 does not cover and are the best candidates to build first.

| # | New app | Domain | Architectural delta | Overlap with Part 1 |
|---|---------|--------|---------------------|---------------------|
| N1 | DocVault | Document management with versions, tags, permissions | Object storage (S3/MinIO), metadata vs blobs, pre-signed URLs, document versioning, RBAC, soft delete | Partly: steps 4, 7. **New delta**: pre-signed URLs, versioning |
| N2 | MediaForge | Image and video upload and transcoding | Message broker, producer/consumer, exponential backoff, Dead Letter Queue | Step 9 |
| N3 | TicketBlitz | Seat booking for concerts and events | Optimistic and pessimistic locking, distributed locks (Redlock), carts with TTL | Step 11 |
| N4 | PayLedger | Digital wallet and transfers between users | Immutable double-entry ledger, Transactional Outbox, double spending prevention | Partly: step 12. **New delta**: double-entry ledger |
| N5 | C4P Publisher | Automatic distribution of blog posts (my need: the `distributed:` flags in `_data/roadmap.yml`) | Scheduler, Transactional Outbox, idempotent publishing to Medium, Substack, LinkedIn, one circuit breaker per channel | Steps 12, 13. Real need, reuses known patterns |
| N6 | NotifyHub | Multi-channel notifications (email, push, SMS, webhook) | Circuit breaker, bulkhead, timeouts, outgoing webhooks signed with HMAC | Partly: step 13. **New delta**: HMAC webhooks |
| N7 | CronPulse | Distributed job scheduler | Leader election, task leasing, heartbeats | Step 22 |
| N8 | TravelFlow | Flight + hotel + car packages from separate suppliers | Saga: orchestration vs choreography, compensations | Step 17 |
| N9 | CatalogSearch | Product search with facets, synonyms, ranking | CQRS with PostgreSQL write model and OpenSearch read model, Change Data Capture (Debezium) | **New delta** (step 20 has CQRS, without search engine and CDC) |
| N10 | MetricStream | High-throughput telemetry and metrics | Kafka ingestion, write batching, time-series DB, time partitioning, retention and downsampling | Partly: steps 7, 18 |
| N11 | GeoFleet | Real-time fleet tracking on a map | Geospatial indexing (PostGIS, Geohash, H3), WebSocket/MQTT ingestion, nearest neighbor | Step 18 |
| N12 | PulseFeed | Feed-based social network with followers | Fan-out on write vs on read, the celebrity problem | Step 19 |
| N13 | ChatSphere | 1:1 and group chat with presence and read receipts | Millions of WebSocket connections, distributed pub/sub, message ordering (Lamport, Snowflake IDs) | **New delta** |
| N14 | CollabPad | Real-time collaborative text editor | CRDT or Operational Transformation | Partly: step 21 |
| N15 | MiniKV | Distributed fault-tolerant key-value store | Consistent hashing with virtual nodes, quorum (R+W>N), vector clocks, gossip | **New delta** (step 23 has only consistent hashing) |

# Common to both parts

## Where to document

- Part 1: each carrier repository, with ADRs in `docs/adr/`.
- Part 2: a folder per app in `software-architect-blueprints`, next to `eshop` and `strava-like`.
- Cross-project case studies: `principal-architecture-journey/case-studies`.
- `software-architect-blueprints/strava-like` becomes the target design of the Running Platform (steps 15–19).

## Routine for each step

1. **ADR** — write the Architecture Decision Records before coding: options, trade-offs, what was discarded.
2. **Capacity estimation** — set realistic targets (throughput, p99 latency, availability) and size storage,
   bandwidth, and cache.
3. **Observability from the start** — OpenTelemetry, Prometheus, Grafana from step 5 onward.
4. **Load testing** — k6 or Locust to find the bottleneck.
5. **Failure injection** — kill Redis under load, add latency to an external provider, kill a worker mid-transaction,
   and verify that retries, circuit breakers, and the outbox actually hold.
