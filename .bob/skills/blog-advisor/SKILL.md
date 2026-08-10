---
name: blog-advisor
description: Use when the user wants strategic advice about the blog — brainstorming on direction, identifying content gaps, prioritising topics, evaluating growth on channels, or doing a periodic editorial review.
---

# Blog Advisor — Code4Projects

This skill is a strategic thinking partner, not a task executor. It helps the author step back from individual posts and reason about the blog as a whole: what to focus on, where the gaps are, what the audience needs, and how to grow intentionally.

Activate this skill when the user asks questions like:
- "What should I focus on in the next few months?"
- "What is missing from my blog?"
- "How do I differentiate from other tech blogs?"
- "Is it worth investing more in this category?"
- "Give me a strategic review of my blog"
- "What are my content gaps?"

---

## Step 1 — Load the full picture

Read these files before any analysis:

1. `_data/roadmap.yml` — the full post corpus and pipeline
2. `_config.yml` — blog identity, categories, author
3. `docs/EDITORIAL_PLAN.md` — strategic direction, active series, week-by-week plan
4. Run `python3 .bob/skills/roadmap-manager/roadmap.py show` to get the status overview

From this, extract:
- Total published posts by category
- Series: complete vs incomplete
- Time distribution: publishing cadence over the years
- Most recent activity: what topics have been covered in the last 12 months
- Pipeline: what is planned or in draft

---

## Step 2 — Identify the mode

Determine what kind of strategic question the user is asking. Match to one of these modes:

### Mode A: Editorial review
*"Do a review of my blog / Tell me the state of the blog"*
→ Run the full corpus analysis (Step 3) and produce the complete strategic report (Step 4).

### Mode B: Gap analysis
*"What am I missing? / Where am I weak?"*
→ Focus on Step 3c (gap analysis) and produce targeted recommendations.

### Mode C: Direction brainstorm
*"I don't know what to focus on / Give me ideas for upcoming posts"*
→ Combine corpus data with the author's background and current tech trends to suggest 5–10 concrete directions.

### Mode D: Channel strategy
*"Is it worth investing in Instagram? / How do I grow on LinkedIn?"*
→ Analyse distribution gaps from the roadmap, discuss channel-specific strategy.

### Mode E: Series planning
*"I need to finish a series / I want to start a new series"*
→ Review incomplete series, assess effort vs value, suggest next steps.

---

## Step 3 — Analysis framework

### a) Corpus health
- Posts per category (absolute and % of total)
- Series: list complete vs incomplete (incomplete = series with posts in `_posts/` but no clear final article)
- Publishing cadence: posts per year (from `scheduled` dates)
- Recency: categories not touched in 2+ years

### b) Author identity alignment
The author is a 30+ year software professional with hands-on experience in:
- Cloud (AWS, IBM Cloud, Kubernetes, Docker)
- AI/LLM (LangChain, agent protocols A2A/MCP)
- Software engineering fundamentals

The blog's stated purpose: *"a website about software programming where I write everything I learnt in over 30 years of experience"*

Flag mismatches: categories with shallow or outdated coverage vs the author's actual depth.

### c) Gap analysis
Identify:
1. **Topic gaps** — areas the author clearly knows well (from bio and existing posts) but has no or thin coverage on the blog
2. **Depth gaps** — categories with only 1–2 posts that deserve a full series
3. **Recency gaps** — solid series from 2018–2021 that are now outdated and could benefit from a 2025/2026 refresh
4. **Audience gaps** — is there content for beginners AND intermediate readers in each category, or only one level?

### d) Differentiation
What makes this blog distinct from generic tech blogs?
- Personal voice built on real 30-year experience
- Series format with progressive depth
- Practical, hands-on with real commands and code
- Italian author writing in English for a global audience

What could strengthen differentiation further?

### e) Effort vs impact
For the pipeline (ideas/planned/draft items):
- Which items are quick wins (standalone posts, already known topics)?
- Which are high-impact but high-effort (new series, deep dives)?
- Which are low-value (trendy but off-brand, or already covered well)?

---

## Step 4 — Strategic report

Produce a structured report:

```
## Blog Strategic Review — [date]

### Corpus at a glance
| Category | Posts | Last post | Series |
|---|---|---|---|
| ... | N | YYYY-MM | complete / in progress / abandoned |

### Publishing cadence
[Year-by-year count. Trend: accelerating / stable / slowing]

### Strengths
- [What the blog does well, with evidence]

### Gaps and opportunities
#### 🔴 High priority (author authority + clear audience demand)
1. [Gap] — [Why it matters] — [Suggested approach]

#### 🟡 Medium priority (worth exploring)
1. [Gap] — ...

#### 🔵 Low priority or monitor
1. ...

### Incomplete series — recommended actions
| Series | Published | Status | Recommendation |
|---|---|---|---|

### Suggested focus for next 90 days
[3–5 concrete recommendations, ordered by priority]

### One thing to stop doing
[Something consuming energy without proportional value]

### One thing to start doing
[The single highest-leverage new direction]
```

---

## Step 5 — Brainstorm mode (Mode C)

If the user wants concrete topic ideas rather than a full report:

1. List the 5 most underserved topic areas given the author's expertise.
2. For each, suggest 3 specific post ideas with a one-line rationale.
3. Flag which ones could start a new series vs standalone.
4. Rank them by effort (L/M/H) × impact (L/M/H).

Present as a table:

```
| # | Topic idea | Series? | Effort | Impact | Why now |
|---|---|---|---|---|---|
```

---

## Rules

- Be direct and honest. If the blog has been neglected in a category, say so.
- Ground every observation in actual data from the roadmap — no generic advice.
- Never suggest topics outside the author's stated expertise unless explicitly asked to explore new territory.
- The goal is personal growth + professional reputation + reader value. Keep all three in mind.
- This is a thinking-partner conversation — ask follow-up questions if the direction is unclear.
- Always end with a concrete next action the user can take today.
