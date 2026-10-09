# Code4Projects — Blog Automation

Last updated: 2026-10
Author: Salvatore D'Angelo

This document describes the full lifecycle of a blog post, from idea to social distribution, using Bob's blog skills. Each step maps to a specific skill invoked via `/blog <command>`.

---

## Full Pipeline

```
idea → planner → research → writer → illustrator → review → roadmap-manager → social
```

| Step | Command | Skill | Output |
|------|---------|-------|--------|
| 1 | `/blog idea <topic>` | `blog-idea` | approve / reject / transform decision |
| 2 | `/blog planner <topic>` | `blog-planner` | outline, front matter, series context, image brief |
| 3 | `/blog research <topic>` | `blog-research` | notes + 5 reference articles + images in `.bob/tmp/blog-research/<slug>/` |
| 4 | `/blog write <topic>` | `blog-writer` | `_drafts/<slug>.md` |
| 5 | `/blog illustrator <slug>` | `blog-illustrator` | `assets/img/<slug>-hero.svg` + inline `assets/img/<slug>-<concept>.svg` |
| 6 | `/blog review <topic>` | `blog-review` | prioritised fix list; fixes applied inline |
| 7 | `/blog roadmap-manager` | `blog-roadmap-manager` | roadmap entry updated to `published` |
| 8 | `/blog social` | `blog-social` | Twitter/X, LinkedIn, Instagram, Facebook, Substack copy |

---

## Step Details

### Step 1 — Idea (`blog-idea`)

Evaluates whether a topic is worth writing about. Checks for duplicates in the roadmap, assesses fit with the blog identity, estimates audience value, and returns one of:

- **Approve** — add to roadmap as `idea`, proceed to planner
- **Reject** — topic is off-brand, already covered, or low value
- **Transform** — the core idea is valid but needs reframing

If approved, the skill adds the entry to `_data/roadmap.yml`.

---

### Step 2 — Planner (`blog-planner`)

Turns an approved idea into a detailed, ready-to-write blueprint. Reads `_data/roadmap.yml` and `docs/EDITORIAL_PLAN.md` for series context.

Produces:
- Complete article outline with concrete H2/H3 section titles
- Jekyll front matter (layout, title, slug, image, excerpt, categories, post_series_id)
- Series placement (previous / this / next)
- Opening hook
- Key terms to define
- Code examples needed
- Image brief for the illustrator

Updates the roadmap entry to `status: planned`.

At the end of the plan, shows the full pipeline reminder:

> **Pipeline:** `blog-research` → `blog-writer` → `blog-illustrator` → `blog-review`

---

### Step 3 — Research (`blog-research`)

Runs before writing. Spawns the `blog-researcher` subagent to:

- Find and fetch the 5 most authoritative articles on the topic
- Download and standardise 5 hero image candidates (760×400 px)
- Generate AI images (Gemini) for hero and content
- Save everything to `.bob/tmp/blog-research/<slug>/`

The writer skill picks up research notes automatically from that folder.

---

### Step 4 — Writer (`blog-writer`)

Writes the complete draft in Jekyll Markdown format, applying the Code4Projects style guide automatically. Reads the plan from the conversation and the research notes from `.bob/tmp/blog-research/<slug>/notes.md`.

Outputs `_drafts/<slug>.md` and updates the roadmap entry to `status: draft`.

At the end of the summary, the skill reminds:

> **Next Step:** Run `/blog illustrator <slug>` to generate the hero image and inline diagrams.

---

### Step 5 — Illustrator (`blog-illustrator`) ← new step

Generates all SVG illustrations for the post. This step is **mandatory** for every post.

**What it creates:**

| File | Purpose |
|------|---------|
| `assets/img/<slug>-hero.svg` | Hero image — overview visual summarising the post's core technical premise. Used in front matter `image:` and at the top of the post body. |
| `assets/img/<slug>-<concept>.svg` | Inline diagrams — one per major concept, replacing prose the reader would otherwise have to imagine. |

**Design system:**
- Standard width: `760px`, `viewBox="0 0 760 H"`
- Color palette: blue `#3b82d4`, purple `#7c5cd8`, teal `#0ea5e9`, green `#10b981`
- Clean white background `#ffffff`, card surfaces `#f7f8fa`
- Typography hierarchy: title 15–16px bold → section 13–14px bold → labels 11–12px

**After generation, the skill:**
1. Saves all SVGs to `assets/img/`
2. Updates the front matter `image:` field in the draft
3. Adds or updates the inline `![alt]({{ site.baseurl }}/assets/img/<slug>-diagram.svg){:width="760" height="400" .responsive_img}` references in the post body

**Goal:** every major concept that can be visualised as an architecture diagram, sequence flow, data pipeline, or component scheme must have its own SVG inline diagram. Minimum: 1 hero + 1 inline diagram.

---

### Step 6 — Review (`blog-review`)

Audits the draft (including illustrations) against the Code4Projects style guide and produces a prioritised fix list with exact line references. Offers to apply fixes inline.

Checks:
- Voice, tone, structure compliance
- Front matter completeness
- Code block language tags
- Hero image present and embedded correctly
- Inline diagrams present where needed
- Series cross-links correct
- CTA block present and unmodified

---

### Step 7 — Roadmap Manager (`blog-roadmap-manager`)

Updates `_data/roadmap.yml` after the post is published:
- `status: published`
- `date:` set to publication date
- `distributed.*` flags updated

Also updates `docs/EDITORIAL_PLAN.md` series tables when a series article is completed.

---

### Step 8 — Social (`blog-social`)

Generates ready-to-post social copy for all active channels:

| Channel | Format |
|---------|--------|
| Twitter/X | 1 promotional tweet, ≤280 chars, with link |
| LinkedIn | Long-form post, central thesis extracted as strong opening |
| Instagram | Caption with hashtags |
| Facebook | Short post |
| Substack | Newsletter intro paragraph |

---

## Medium Import Variant

For posts imported from Medium, replace steps 3–4 with the `blog-medium-importer` skill:

```
idea → planner → medium-importer → illustrator → review → roadmap-manager → social
```

The importer converts Medium HTML to Jekyll Markdown, downloads images, resolves internal links, and sets front matter. After import, run `blog-illustrator` to replace any downloaded raster images with native SVG diagrams where appropriate, then proceed to review.

---

## Skill Reference

| Skill | Trigger | Reads | Writes |
|-------|---------|-------|--------|
| `blog-idea` | `/blog idea` | `_data/roadmap.yml` | `_data/roadmap.yml` (new entry) |
| `blog-planner` | `/blog planner` | `_data/roadmap.yml`, `docs/EDITORIAL_PLAN.md` | `_data/roadmap.yml` (status → planned) |
| `blog-research` | `/blog research` | plan from conversation | `.bob/tmp/blog-research/<slug>/` |
| `blog-writer` | `/blog write` | plan, research notes | `_drafts/<slug>.md`, `_data/roadmap.yml` (status → draft) |
| `blog-illustrator` | `/blog illustrator` | `_drafts/<slug>.md` | `assets/img/<slug>-*.svg`, updates draft |
| `blog-review` | `/blog review` | `_drafts/<slug>.md` | fixes applied to draft |
| `blog-roadmap-manager` | `/blog roadmap-manager` | — | `_data/roadmap.yml`, `docs/EDITORIAL_PLAN.md` |
| `blog-social` | `/blog social` | published post | social copy (chat output only) |
