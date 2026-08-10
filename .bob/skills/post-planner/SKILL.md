---
name: post-planner
description: Use when a blog post idea has been approved and the user wants to plan it — produces a complete outline, series placement, front matter, estimated length, and image brief before writing begins.
---

# Post Planner — Code4Projects

This skill turns an approved idea into a detailed, ready-to-write plan. No prose is written here — only structure. The output becomes the blueprint for `post-writer`.

## Step 1 — Gather inputs

Read `_data/roadmap.yml` with `read_file` to find the idea entry. If the user referred to it by title, locate the matching entry by `id` or `title`.

Read `docs/EDITORIAL_PLAN.md` with `read_file` to understand the series context and current priorities before asking the user anything.

If any of these are still missing from the roadmap entry after reading the plan, ask the user (inline):
- Target audience level: beginner / intermediate / advanced
- Standalone post or part of a series? If series: existing or new?
- Is there a companion GitHub repo or code example?
- Scheduled publication date (if not already set)

## Step 2 — Check series context

If the post belongs to a series:
1. List all other posts in that series from `roadmap.yml`.
2. Identify where this post fits in the sequence (before/after which articles).
3. Note what the previous article covered and what the next will cover — for intro/conclusion bridges.
4. Check `_data/post_sidebar.yml` for an existing entry with the same `post_series_id`.
   - If it exists: confirm the new post will be appended to it.
   - If it does not exist: flag that a new series entry must be created in `post_sidebar.yml` when the post is published.

## Step 3 — Produce the plan

Output a structured plan with these sections:

---

```
## Post Plan: "<Working Title>"

### Metadata
| Field         | Value                        |
|---------------|------------------------------|
| id            | kebab-case-id                |
| slug          | same as id (no trailing /)   |
| category      | Category Name                |
| series        | series-id (or — standalone)  |
| audience      | beginner / intermediate / advanced |
| scheduled     | YYYY-MM-DD                   |
| estimated length | ~N words / ~N min read    |

### Hero image brief
[Description of what the image should show. SVG diagram or photo? What concept does it visualise?]

### Excerpt (SEO)
[1–2 sentence summary, no markdown, max 160 chars]

### Series placement
Previous: [title + slug or —]
This post: [title]
Next: [title + slug or — (TBD)]

### Opening hook (1–2 sentences)
[The opening problem statement or scenario that grabs the reader]

### Outline
## Introduction
- Context / problem statement
- "You should read this if:" (3 bullets)
- Link to previous article in series (if applicable)

## Section 1: <Name>
- Key point A
- Key point B
- [Code example / table / diagram if needed]

## Section 2: <Name>
- ...

## [Optional: Hands-on / Putting It All Together]
- Step-by-step walkthrough
- Commands to run
- Expected output

## Conclusion
- Summary bullets (what was covered)
- Bridge to next article

### Key terms to define
- term1: one-line definition
- term2: one-line definition

### Code examples needed
- [ ] Example 1: what it demonstrates
- [ ] Example 2: what it demonstrates

### External links to include
- [resource name](url) — why it's referenced
```

---

## Step 4 — Suggest front matter

Produce the complete Jekyll front matter block ready to paste:

```yaml
---
layout: post
title: "Full Title in Title Case"
post_series_id: series-slug        # omit if standalone
slug: post-slug
image: /assets/img/suggested-filename.svg
excerpt: One to two sentence SEO summary without markdown.
categories:
  - "Category Name"
---
```

## Step 5 — Update roadmap

1. Update the roadmap entry:
   - Set `status: planned`
   - Set `scheduled:` if not already set
   - Set `slug:` to the confirmed slug
2. Apply the change to `_data/roadmap.yml` with `apply_diff`.
3. Confirm the update.

## Step 6 — Series sidebar note

If the post belongs to a series, include a reminder in the plan output:

> **Series sidebar:** When this post is published, add or update the `post_series_id: <id>` entry in `_data/post_sidebar.yml` with the post's name and slug. This is required for the series sidebar to appear on all posts in the series.

## Rules

- The outline must be concrete — actual section titles, not placeholders like "Section about X".
- Estimated length: ~200 words per major H2 section as baseline. Add ~300 for each significant code walkthrough.
- The excerpt must be standalone — readable as a tweet without context.
- Never invent front matter fields beyond those in the style guide.
