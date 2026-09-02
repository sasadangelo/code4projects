---
name: blog-idea
description: Use when the user has a new blog post idea and wants to evaluate it — checks for duplicates, assesses fit with the blog's identity, estimates audience value, and recommends approve/reject/transform.
---

# Idea Evaluator — Code4Projects

When this skill activates, evaluate a blog post idea rigorously before any writing begins. The goal is to protect the author's time: only ideas that pass the evaluation get promoted to `planned` in the roadmap.

## Step 1 — Read the existing corpus

Run the following command to get the full list of published and planned posts:

```
python3 .bob/skills/blog-roadmap-manager/roadmap.py show
```

Read `_data/roadmap.yml` with `read_file` to have the full data available.

## Step 2 — Understand the idea

Ask the user (inline, no tool) if these are not already clear:

- What is the post about? (one sentence)
- Who is the target reader? (beginner / intermediate / advanced)
- What will the reader be able to do or understand after reading it?

If the user gave all this in the original message, skip asking.

## Step 3 — Run the evaluation script

```
python3 .bob/skills/blog-idea/evaluate.py "<idea title or description>"
```

The script checks for duplicate or near-duplicate posts in the roadmap by keyword matching and prints a similarity report.

## Step 4 — Apply the evaluation rubric

Score the idea on these 5 dimensions (1–3 each):

### 1. Fit with blog identity (1–3)

The blog covers: Cloud, Virtualization, AI/LLM, Programming, DevOps, Networking, Android.

- **3** — Core topic. Directly in the author's wheelhouse (30+ years software, cloud, AI focus).
- **2** — Adjacent. Related but not a primary focus area.
- **1** — Off-topic. Unrelated to technology or software.

### 2. Uniqueness vs existing content (1–3)

- **3** — No existing post covers this. Clear gap in the corpus.
- **2** — Existing posts touch on it, but a different angle, depth, or technology justifies a new post.
- **1** — Near-duplicate. An existing post already covers this adequately.

### 3. Reader value (1–3)

- **3** — Solves a concrete problem or teaches a skill directly applicable at work or in projects.
- **2** — Interesting and educational, but not immediately actionable.
- **1** — Generic overview available everywhere; no differentiating perspective.

### 4. Author authority (1–3)

- **3** — The author has direct hands-on experience with this (based on existing posts and bio).
- **2** — Adjacent expertise; the author can write credibly with some research.
- **1** — Outside the author's direct experience; high risk of shallow content.

### 5. Series potential (1–3)

- **3** — Naturally fits into or starts a series of 3+ articles.
- **2** — Could be standalone or a 2-part post.
- **1** — One-off with no obvious follow-up.

**Total: max 15 points.**

## Step 5 — Deliver the verdict

Present the evaluation as a structured report:

```
## Idea Evaluation: "<title>"

| Dimension              | Score | Notes                          |
|------------------------|-------|--------------------------------|
| Fit with blog identity |  X/3  | ...                            |
| Uniqueness             |  X/3  | ...                            |
| Reader value           |  X/3  | ...                            |
| Author authority       |  X/3  | ...                            |
| Series potential       |  X/3  | ...                            |
| **TOTAL**              | XX/15 |                                |

### Verdict: APPROVE / REJECT / TRANSFORM

**Reason:** [1–3 sentences]

**Suggested angle / transformation:** [only if TRANSFORM or to sharpen an APPROVE]

**Suggested category:** [from allowed list]
**Suggested series:** [existing series id or new series name, if applicable]
**Suggested title:** [working title]
```

Thresholds:

- **12–15** → APPROVE — add to roadmap as `planned`
- **8–11** → TRANSFORM — suggest a sharper angle, then re-evaluate
- **≤7** → REJECT — explain why clearly, suggest what would need to change to reconsider

## Step 6 — Add to roadmap on approval

If the verdict is APPROVE (or TRANSFORM and the user accepts the new angle):

1. Ask the user if they want to add it to the roadmap now.
2. If yes: append the entry to `_data/roadmap.yml` with `status: idea` using `insert_content` or `apply_diff`.
3. Confirm with the roadmap entry shown.

Use this template for the new entry:

```yaml
- id: <kebab-case-id>
  title: "<Working Title>"
  status: idea
  category: "<Category>"
  series: <series-id-or-omit>
  distributed:
    medium: false
    substack: false
    twitter: false
    linkedin: false
    instagram: false
    facebook: false
```

## Rules

- Be honest. A low score is more useful than a false positive.
- If a near-duplicate exists, name the specific existing post and explain the overlap.
- Never add to roadmap without the user's explicit confirmation.
- The `id` must be unique in `roadmap.yml` — check before writing.
