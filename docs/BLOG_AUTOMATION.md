# Code4Projects — Blog Automation Guide

This document explains how to use the Bob skill system to manage the blog from idea to distribution.

---

## Prerequisites

- Bob installed and configured in this workspace
- Python 3 available (`python3 --version`)
- Python libraries: `pip install pyyaml beautifulsoup4`

---

## The Complete Workflow

**New post (idea → publish → distribute):**
```
💡 IDEA
   └─► idea-evaluator      → evaluate, approve or reject
         └─► roadmap-manager     → add to the pipeline
               └─► post-planner        → create outline and front matter
                     └─► post-writer         → write the draft in _drafts/
                           └─► post-reviewer       → review and fix
                                 └─► [manually publish to _posts/]
                                       └─► social-content        → content for 5 channels
                                             └─► roadmap-manager → update distribution flags
```

**Import from Medium:**
```
📥 MEDIUM ARTICLE (URL)
   └─► medium-importer     → paste HTML/text → _drafts/<slug>.md + assets/img/
         └─► post-reviewer       → fix headings, code tags, style
               └─► [manually publish to _posts/]
                     └─► social-content        → content for 5 channels
                           └─► roadmap-manager → update distribution flags
```

---

## Available Skills

### `style-guide`
**Activates when:** you write, review, or evaluate any post.
**What it does:** applies voice, tone, structure, and technical conventions derived from the existing post corpus.
**How to trigger:**
```
"Write a post about X"
"Review this draft"
"I'm writing an article, follow the blog style"
```

---

### `roadmap-manager`
**Activates when:** you manage the editorial pipeline.
**Managed file:** `_data/roadmap.yml`
**Script:** `.bob/skills/roadmap-manager/roadmap.py`

**Direct CLI commands (no Bob needed):**
```bash
python3 .bob/skills/roadmap-manager/roadmap.py show      # table grouped by status
python3 .bob/skills/roadmap-manager/roadmap.py calendar  # upcoming scheduled posts
python3 .bob/skills/roadmap-manager/roadmap.py gaps      # published but not distributed
```

**How to trigger via Bob:**
```
"Show me the roadmap"
"Add idea: post about Terraform, category Cloud"
"Schedule post X for 2026-09-15"
"Mark docker-security as distributed on LinkedIn"
"What have I not yet published on Medium?"
"Change idea X status to planned"
```

---

### `idea-evaluator`
**Activates when:** you have a new idea and want to know if it is worth pursuing.
**Script:** `.bob/skills/idea-evaluator/evaluate.py`
**Evaluation rubric (max 15 points):**
- Fit with blog identity (1–3)
- Uniqueness vs existing content (1–3)
- Reader value (1–3)
- Author authority (1–3)
- Series potential (1–3)

**Thresholds:** ≥12 APPROVE · 8–11 TRANSFORM · ≤7 REJECT

**How to trigger:**
```
"Evaluate this idea: post on Kubernetes Operators"
"I have an idea for an article about Rust for beginners, what do you think?"
"Is it worth writing a post on GitHub Actions?"
```

---

### `post-planner`
**Activates when:** an idea is approved and you want to structure the work before writing.
**Output:** complete outline, Jekyll front matter, image brief, length estimate, series placement.

**How to trigger:**
```
"Plan the post about Terraform"
"Create the outline for idea X"
"Structure the post before I start writing"
```

---

### `post-writer`
**Activates when:** you have a plan and want the complete draft.
**Output:** `_drafts/<slug>.md` file with front matter + full body.
**Updates roadmap:** `status: draft`

**How to trigger:**
```
"Write the draft for the Terraform post"
"Write the article following the plan we made"
```

---

### `post-reviewer`
**Activates when:** you want to check a draft before publishing.
**Output:** prioritised fix list (🔴 CRITICAL / 🟡 IMPORTANT / 🔵 MINOR) with line references.
**Can apply fixes automatically** on request.

**How to trigger:**
```
"Review the draft _drafts/terraform-for-beginners.md"
"Check if this post follows the blog style"
"Do a review before I publish"
```

---

### `social-content`
**Activates when:** a post is published and you want to distribute it across channels.
**Output:** 5 ready-to-post formats:
- Twitter/X thread (4–8 numbered tweets)
- LinkedIn post (150–300 words)
- Instagram caption + hashtag block
- Facebook post
- Substack newsletter intro

**Updates roadmap:** `distributed` flags for confirmed channels.

**How to trigger:**
```
"Generate social content for the Docker Security post"
"Write the Twitter thread for article X"
"Prepare all social content to distribute post Y"
```

---

### `medium-importer`
**Activates when:** you want to import an article from Medium into the Jekyll blog.
**Script:** `.bob/skills/medium-importer/import_medium.py`
**What it does:**
- Downloads all images from Medium CDN to `assets/img/`
- Converts Medium HTML to Jekyll Markdown
- Resolves internal Medium links to Jekyll `{{ site.baseurl }}/slug/` if the article exists in the roadmap
- Removes tracking pixels, duplicate CTA, and Medium footer
- Creates `_drafts/<slug>.md` ready for `post-reviewer`
- Adds the entry to `_data/roadmap.yml` with `medium: true`

**How to trigger:**
```
"Import this Medium article: <paste HTML content>"
"I want to bring this Medium post into the blog"
```

**How to provide the article content (3 options):**
1. **RSS feed HTML** (best) — open `https://medium.com/feed/@sasadangelo`, find the `<content:encoded>` block, paste in the prompt
2. **Paste the article text** — copy the full article text from Medium and paste it directly into the prompt; Bob will reconstruct the HTML
3. **Browser DevTools HTML** — copy the article body HTML from the `<article>` tag in View Page Source

---

### `blog-advisor`
**Activates when:** you want to think strategically about the blog.
**What it does:** corpus analysis, gap analysis, direction brainstorming, periodic editorial review, channel strategy.
**Modes:**
- Full editorial review of the blog
- Gap analysis ("where am I weak?")
- Direction brainstorm ("what should I focus on for the next 3 months?")
- Channel strategy ("is it worth investing in Instagram?")
- Series planning ("which incomplete series should I finish?")

**How to trigger:**
```
"Do a strategic review of my blog"
"What should I focus on for the next 6 months?"
"Where are my biggest content gaps?"
"Give me 10 post ideas based on my profile"
"Is it worth continuing the Android series?"
```

---

## Roadmap Status Values

| Status | Meaning | Where the file lives |
|--------|---------|----------------------|
| `idea` | Raw idea, not yet planned | — |
| `planned` | Approved, outline defined | — |
| `draft` | Draft written | `_drafts/<slug>.md` |
| `published` | Live on the blog | `_posts/YYYY-MM-DD-<slug>.md` |

---

## Distribution Channels

| Key | Platform |
|-----|----------|
| `medium` | Medium (mirror) |
| `substack` | Substack newsletter |
| `twitter` | Twitter / X |
| `linkedin` | LinkedIn |
| `instagram` | Instagram |
| `facebook` | Facebook |

---

## File Structure

```
.bob/
  skills/
    style-guide/
      SKILL.md                ← voice, tone, structure guidelines
      style-reference.md      ← annotated examples from the corpus
    roadmap-manager/
      SKILL.md
      roadmap.py              ← CLI: show / calendar / gaps
    idea-evaluator/
      SKILL.md
      evaluate.py             ← keyword similarity checker
    post-planner/
      SKILL.md
    post-writer/
      SKILL.md
    post-reviewer/
      SKILL.md
    social-content/
      SKILL.md
    medium-importer/
      SKILL.md
      import_medium.py        ← HTML→Markdown converter + image downloader
    blog-advisor/
      SKILL.md

_data/
  roadmap.yml                 ← single source of truth for the pipeline

docs/
  BLOG_AUTOMATION.md          ← this guide
```

---

## Quick Start

**At the start of each new conversation:**
Nothing special is required — skills activate automatically based on what you say. Bob recognises the intent and loads the right skill.

**If a skill does not activate:** use the explicit command `/skill-name` (e.g. `/roadmap-manager`).

**To view the pipeline from the terminal (without Bob):**
```bash
cd /path/to/code4projects
python3 .bob/skills/roadmap-manager/roadmap.py show
```
