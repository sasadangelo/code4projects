# Code4Projects — Growth Roadmap

Last updated: 2026-08
Author: Salvatore D'Angelo

This document defines the strategic priorities for growing the blog as an authority platform and, eventually, as a revenue source. It is grounded in what already exists — corpus, editorial plan, active channels — not in speculative projections.

**Guiding principle**: writing articles is the primary engine. Everything else (channels, conversion, monetisation) is built around content, not instead of it.

---

## Current Baseline

| Dimension | Status |
|---|---|
| Blog | 88 published articles, 40+ visible on code4projects.org |
| Traffic | ~219 users/month (Google Analytics) |
| Medium | 49 followers — passive mirror, does not convert |
| Substack | 0 subscribers — active but not fed |
| Twitter/X | 3–4 followers — negligible presence |
| Facebook | 2 followers — not relevant for the target audience |
| LinkedIn | Personal profile — not used for the blog |
| Ebook | 1 published (Docker 2025) — lead magnet active but not optimised |

---

## 12-Month Goal

Not a follower count. A positioning statement:

> Be recognisable as the professional with 30+ years of real-world experience who explains in depth **applied AI, modern DevOps, and software architecture** — not tutorials copied from the docs, but genuine understanding from someone who has actually worked on these systems.

Concrete metrics at 12 months:
- Organic traffic: 1,000+ users/month
- Substack: 200+ subscribers
- Active complete series with ebooks: 3 (Docker ✅, Python, Kubernetes)
- New articles published: +20 (at current pace of ~1/week)

---

## Priority 1 — Keep Writing (non-negotiable)

Content is the foundation. Without new quality articles, everything else is optimising emptiness.

The editorial plan in `docs/EDITORIAL_PLAN.md` is already solid. Follow it.

**Recommended sequence:**

1. **Complete Modern Python App Dev** (Phase 2 of the editorial plan)
   - Import "Cron Jobs & Scheduled Tasks" from Medium
   - Write "Concurrency in Python"
   - Write "Async & Event Loop"
   - Write "Building a REST API with FastAPI"
   - Write "Testing with pytest"
   - → Series complete → ebook → lead magnet

2. **Launch Kubernetes 2026** (Phase 3)
   - 10 articles already planned in roadmap.yml as `idea`
   - Same model as Docker 2025 (final ebook)
   - Highest SEO impact of any planned series

3. **Bring forward "How LLMs Work"** (import from Medium — quick win)
   - Almost zero cost: article already written, just needs importing
   - Formally opens the `build-your-own-llm` series earlier
   - Signals AI authority to Google and readers today rather than in Q1 2027

**What NOT to do**: do not stop writing to optimise secondary channels. Every week without a new article is future traffic that will never arrive.

---

## Priority 2 — Activate the Conversion Funnel (low effort, high impact)

Traffic exists (219/month). The problem is that none of it converts into anything measurable.

### 2a. Per-series lead magnets → Substack ✅ First one live

The model: every completed series has its own ebook, and every article in that series promotes its own ebook via a "Download eBook" popup → Substack subscribe.

```
Kubernetes article  → "Download Kubernetes ebook" popup → Substack
AI article          → "Download AI ebook" popup          → Substack
Python article      → "Download Python ebook" popup      → Substack
standalone article  → default "Best of Code4Projects" ebook → Substack
```

**Docker 2025 is live.** Clicking "Download eBook" opens a popup where the reader enters their email and is redirected to Substack to subscribe.

All future series follow the same model: complete the series → compile the ebook → wire the lead magnet → activate on all articles in that series.

**Ebook selection logic (via tags):** the post layout reads the post's tags and maps them to the correct ebook. If no tag matches an active ebook, the default fallback is shown.

```
tag: docker      → Docker 2025 ebook
tag: kubernetes  → Kubernetes 2026 ebook
tag: python      → Modern Python App Dev ebook
tag: ai          → AI / LangChain ebook
(no match)       → default "Best of Code4Projects" ebook
```

This means every post must have at least one meaningful tag in its front matter. The mapping is maintained in the post layout (or a `_data/ebook_map.yml` config file).

**Default ebook (fallback):** articles with no matching tag show a generic lead magnet — e.g. "The Best of Code4Projects" or "Software Engineering Essentials" — so that no article ever runs without a conversion opportunity. This default ebook needs to be created once and wired as the fallback in the post layout.

### 2b. Rewrite the Start Here page ✅

`start-here.md` exists but dates from 2019. It needs to be updated with:
- Current positioning (AI, DevOps, Software Architecture)
- The 3–4 main series with direct links
- Reader orientation by goal ("I want to learn Docker", "I want to understand AI", "I want modern Python")
- Substack CTA at the bottom
- **Effort: medium** — 1–2 hours of writing

### 2c. Author bio at the bottom of every article

`_layouts/post.html` has no author bio. A block needs to be added after the content with:
- Photo + 2 lines ("Salvatore D'Angelo, software engineer with 30+ years of experience in AI, Cloud, and architecture. Writes at code4projects.org.")
- LinkedIn link + Substack link
- **Effort: low** — one layout change, applies to all articles automatically

---

## Priority 3 — Minimal Distribution (do not over-invest)

Goal: not to spread time across all channels, but not to leave value on the table either.

### Medium — change the strategy

Current: full mirror of all articles.
Recommended: publish **only the first article of each new series**, with an explicit CTA: "Read the full series at code4projects.org".

Why: Medium brings external traffic. But if the full series lives only on the blog, the reader has to come to you.

### Twitter/X — when it makes sense to start

Not now. With 3–4 followers, the time investment does not pay off until there is a minimum base (~500 followers). Revisit when:
- Kubernetes 2026 is launched (Q4 2026)
- At least 2 ebooks are published
- There is something substantial to promote

When you start: do not promote articles — share **insights**. "I have worked on distributed systems for 10 years. Here is what actually happens when a Kubernetes pod crashes." The link comes after.

### LinkedIn — medium priority

More useful than Twitter for the consulting/speaker target. Every published article becomes a LinkedIn post with the central point extracted as a strong thesis. Investment: 15 minutes per article.

---

## Priority 4 — Monetisation (distant, but lay the groundwork now)

Not now. The correct sequence is:

```
Traffic → Lead magnet → Substack subscribers → Trust → Paid product
```

Skipping steps burns the list before it is even built.

**When you reach 500+ Substack subscribers**, evaluate:
- Premium ebook editions (exercises, complete projects, advanced examples)
- Downloadable project templates (Python Blueprint is the natural candidate)
- Short email courses (7 emails distilling a blog series)
- Consulting (the blog is the portfolio — it must be solid first)
- Speaking (credibility comes from deep technical articles)

---

## Data to Collect (when it becomes useful)

Optimising for SEO before having enough content is premature. With 219 users/month, GSC data is not yet statistically meaningful.

**When traffic exceeds 1,000 users/month**, collect from Google Search Console:
1. Queries with impressions > 50 and position 8–20 → SEO quick wins
2. Pages with CTR < 3% → titles/meta descriptions to rewrite
3. Pages with the most traffic → confirms the strongest categories

Tool to build: a Python script that queries the GSC API and produces an automatic markdown report. Plan for Q4 2026.

---

## Priority Summary

| # | Action | Effort | Impact | When |
|---|---|---|---|---|
| 1 | Keep writing (follow EDITORIAL_PLAN) | High (ongoing) | High | Always |
| 2 | Import "How LLMs Work" from Medium | Low | Medium | Next week |
| 3 | Connect Substack to Docker lead magnet | Low | High | Next 2 weeks |
| 4 | ~~Author bio + byline on articles~~ ✅ Done | Low | Medium | ~~Next 2 weeks~~ |
| 5 | ~~Rewrite Start Here page~~ ✅ Done | Medium | Medium | ~~Next month~~ |
| 6 | Change Medium strategy (only Part 1 of each series) | Low | Medium | Next month |
| 7 | LinkedIn (post per article) | Low (15 min/article) | Medium | From Kubernetes 2026 launch |
| 8 | Twitter/X | Low/Medium | Low now | After 2 ebooks published |
| 9 | Automated GSC script | Medium | Medium | Q4 2026 |
| 10 | Monetisation | High | High (future) | After 500 Substack subscribers |

---

## One Thing to Do Today

Import "How LLMs Work" from Medium using the `medium-importer`. It costs less than 30 minutes, publishes the first article of the `build-your-own-llm` series, and starts building AI authority **now** — not in Q1 2027.

---

## References

- Detailed editorial plan: `docs/EDITORIAL_PLAN.md`
- Operational article status: `_data/roadmap.yml`
- Post layout (for author bio): `_layouts/post.html`
- Start Here page (to update): `start-here.md`
