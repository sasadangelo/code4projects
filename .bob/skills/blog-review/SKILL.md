---
name: blog-review
description: Use when the user wants to review or proofread a blog post draft — checks against the Code4Projects style guide and produces a prioritised fix list with exact line references.
---

# Post Reviewer — Code4Projects

This skill audits a blog post draft and produces an actionable fix list. It does not rewrite — it diagnoses, then offers to apply fixes.

## Step 0 — Detect the post origin

Before running the checklist, determine whether the draft was:

- **Written from scratch** (via `post-writer`) — full style guide applies
- **Imported from Medium** (via `medium-importer`) — run the Medium-specific checklist first (Step 2b), then the standard checklist

Check for Medium origin: if the roadmap entry has `distributed.medium: true`, or if the draft contains Medium CDN image URLs or `python.plainenglish.io` / `stackademic.com` links, it is a Medium import.

## Step 1 — Load the draft

Read the target file from `_drafts/<slug>.md` or `_posts/<filename>.md` using `read_file`.
If the user pastes the content directly, use that.

Also read the following files with `read_file` to have all guidelines active:

- `.bob/skills/blog-style/SKILL.md` — voice, tone, structure
- `.bob/skills/blog-review/references/quality-scoring.md` — scoring rubric

## Step 2a — Standard checklist (all posts)

Check every item below. For each violation, note: severity, approximate line number, and what to fix.

### FRONT MATTER

- [ ] `layout: post` present
- [ ] `title:` in Title Case, quoted
- [ ] `slug:` present, kebab-case, no trailing slash
- [ ] `image:` starts with `/assets/img/` (not `/wp-content/` or a CDN URL)
- [ ] `excerpt:` present, 1–2 sentences, no markdown, ≤160 chars
- [ ] `categories:` uses only allowed values
- [ ] `post_series_id:` present if part of a series
- [ ] `_data/post_sidebar.yml` has an entry for this `post_series_id` (if series) — if missing, flag as 🔴 CRITICAL

### STRUCTURE

- [ ] H1 is the article title (first line after front matter, no other H1 in body)
- [ ] `_Posted on **{{ page.date | date_to_string }}**_` line present after H1
- [ ] Hero image line present and uses `{:width="760" height="400" .responsive_img}`
- [ ] `## Introduction` section present (H2, not H3)
- [ ] "You should read this if:" bullet list in Introduction (3 items, if applicable)
- [ ] `## Conclusion` section present (H2, not H3)
- [ ] Conclusion has a bullet list starting with "In this article we covered:"
- [ ] Bridge sentence to next article in Conclusion (if series)
- [ ] Fixed CTA block at the very end — exact wording, appears exactly once:
      `If you enjoyed this article, don't forget to **give it a clap 👏**...`
      followed by:
      `**Note**: English is not my native language, and this article was drafted with the assistance of AI. However, all the ideas, projects, concepts, and content are entirely my own.`
- [ ] "How This Series Is Structured" section present **only** in Part 1 of a series

### HEADING HIERARCHY

- [ ] No H1 in the body (only the post title line uses `#`)
- [ ] Top-level sections use H2 (`##`), sub-sections use H3 (`###`)
- [ ] No heading levels skipped (e.g. H2 directly to H4)

### VOICE AND TONE

- [ ] No filler opener ("In this article we will…", "Today we are going to…")
- [ ] No passive voice as default — flag up to 3 clearest instances
- [ ] No forbidden words: "basically", "simply", "just", "obviously", "leverage", "synergy"
- [ ] No corporate HR-speak in conclusions
- [ ] Analogies resolve within the same paragraph (not abandoned mid-section)

### CODE BLOCKS

- [ ] Every fenced code block (` ``` `) has a language tag
- [ ] Shell commands use `shell` tag (not `bash` or no tag)
- [ ] Python code uses `python` tag
- [ ] YAML uses `yaml`, Dockerfile uses `dockerfile`, JSON uses `json`
- [ ] Commands with 2+ flags have a bullet-list flag breakdown immediately after
- [ ] No bare URLs in body text (must be `[text](url)`)

### CROSS-REFERENCES (series posts only)

- [ ] Introduction links to previous article
- [ ] Conclusion links to next article
- [ ] Internal links use `{{ site.baseurl }}/slug/` format (not hardcoded domain)

### IMAGES

- [ ] Hero image alt text is the post title or a descriptive phrase (not empty `""`)
- [ ] All inline images have descriptive alt text
- [ ] All internal image paths use `{{ site.baseurl }}/assets/img/`
- [ ] No remaining Medium CDN URLs (`cdn-images-1.medium.com`)

## Step 2b — Medium import checklist (imported posts only)

Run this section in addition to 2a when the post was imported from Medium.

### CODE BLOCKS (Medium-specific)

- [ ] **All code blocks have a language tag** — Medium strips language hints.
      For each untagged block: infer the language from content (Python imports/decorators → `python`,
      `$` prefix or `pip`/`python3` → `shell`, indented YAML keys → `yaml`, etc.) and add the tag.
- [ ] No single-line code blocks that should be fenced multi-line blocks

### HEADINGS (Medium-specific)

- [ ] No H3 (`###`) used as top-level section heading — should be H2 (`##`)
      (The importer auto-shifts, but verify manually if text was pasted rather than RSS HTML)
- [ ] Section titles that look like numbered chapters (e.g. "3. The Main CLI File") —
      consider removing the number prefix for blog style

### LINKS (Medium-specific)

- [ ] No remaining `medium.com` / `plainenglish.io` / `stackademic.com` links that point to
      articles already present in the blog — these should be `{{ site.baseurl }}/slug/` links.
      List any unresolved Medium links for the user to decide.
- [ ] Adjacent link fragments merged — Medium sometimes splits a single link into two
      consecutive `[text1](url)[text2](url)` fragments; merge them into one.

### CTA (Medium-specific)

- [ ] CTA block appears exactly **once** at the end (importer deduplicates, but verify)

### IMAGES (Medium-specific)

- [ ] No remaining Medium CDN image URLs in body (should all be `/assets/img/`)
- [ ] Hero image is a meaningful image (not a tracking pixel or placeholder)

## Step 3 — Produce the report

```
## Review: "<Post Title>"
[Origin: original / Medium import]

### 🔴 CRITICAL (blocks publication)
1. [line ~N] [rule] → [exact fix]

### 🟡 IMPORTANT (degrades quality)
1. [line ~N] [rule] → [exact fix]

### 🔵 MINOR (polish)
1. [line ~N] [rule] → [exact fix]

### ✅ PASSED
- front matter: complete
- heading hierarchy: correct
- CTA block: present once
- ...

### 📊 Quality Score
Score the post against `references/quality-scoring.md`.
For each failed check, deduct the listed points and record the gap.

| Category | Score | Max |
|---|---|---|
| Content Quality | N | 30 |
| SEO Optimization | N | 25 |
| E-E-A-T Signals | N | 15 |
| Technical Elements | N | 15 |
| AI Citation Readiness | N | 15 |
| **Total** | **N** | **100** |

**Rating:** [Exceptional / Strong / Acceptable / Below Standard / Rewrite]

#### Gaps to fix (score < 100)
List every deducted point as an actionable item, classified by the priority
from `references/quality-scoring.md` (🔴 Critical / 🟡 High / 🟠 Medium / 🔵 Low).
Merge with and do not duplicate issues already listed in the CRITICAL / IMPORTANT / MINOR
sections above.

Example:
- 🟡 [SEO -4] No internal links → add 3–10 contextual links using `{{ site.baseurl }}/slug/`
- 🟠 [Content -2] Hero is the only image → add at least 1 diagram or screenshot
- 🔵 [Technical -1] Images are JPEG → convert to WebP/AVIF

### Summary
Total score: N/100 — [rating]
X critical, Y important, Z minor issues.
[ready to publish / needs minor fixes / needs work / major revision needed]
```

**Severity guide:**

- 🔴 CRITICAL: missing required front matter, H1 in body, broken series links, missing/duplicate CTA, Medium CDN image URLs still present.
- 🟡 IMPORTANT: code blocks without language tag, H3 used as top-level section, unresolved Medium links to blog articles, missing flag breakdown, passive voice, forbidden words.
- 🔵 MINOR: empty alt text, numbered section titles, minor wording, capitalisation.

## Step 4 — Offer to fix

After the report, ask the user if they want the fixes applied automatically.

If yes:

- Apply all CRITICAL and IMPORTANT fixes using `apply_diff` or `search_and_replace`.
  Priority order: language tags on code blocks → heading levels → link resolution → CTA deduplication → front matter gaps → `post_sidebar.yml` series entry.
- For a missing `post_sidebar.yml` series entry: create it with `insert_content`, using the post title and slug. If other posts in the series already exist in `_posts/`, include them too.
- Leave MINOR fixes for the user unless they ask.
- After applying, re-read the relevant sections and confirm each fix is clean.
- Report which fixes were applied and which need manual action (e.g. "I cannot auto-resolve this Medium link — the target article does not exist in the roadmap yet").

## Step 5 — Publish the draft

Once the review is complete and all CRITICAL and IMPORTANT issues are resolved, move the draft to `_posts/`:

1. **Determine the target filename** — use the format `YYYY-MM-DD-<slug>.md`, where the date comes from the `scheduled` field in `_data/roadmap.yml` (or from the post's front matter `date:` if set, or from the date provided at import time).
   Example: `_drafts/how-to-create-cron-jobs-in-python.md` → `_posts/2026-01-02-how-to-create-cron-jobs-in-python.md`

2. **Move the file** using `execute_command`:
   ```shell
   mv _drafts/<slug>.md _posts/YYYY-MM-DD-<slug>.md
   ```

3. **Update the roadmap entry** in `_data/roadmap.yml`: change `status: draft` → `status: published`.

4. **Confirm** to the user:
   - Post is now at `_posts/YYYY-MM-DD-<slug>.md`
   - Roadmap entry updated to `published`
   - Next step: run `/blog social` to generate social media content for the post

## Rules

- Report exact issues: "line ~45: ` ```\nimport click` missing language tag → add `python`" not "code needs tags".
- Never silently fix without reporting first.
- Do not change the substance — only style, structure, and compliance.
- For Medium imports: infer code language from content context, do not guess blindly.
  If uncertain, flag as 🔵 MINOR and suggest the likely language.
