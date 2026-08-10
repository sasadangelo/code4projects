---
name: post-reviewer
description: Use when the user wants to review or proofread a blog post draft — checks against the Code4Projects style guide and produces a prioritised fix list with exact line references.
---

# Post Reviewer — Code4Projects

This skill audits a blog post draft and produces an actionable fix list. It does not rewrite — it diagnoses.

## Step 1 — Load the draft

Read the target file from `_drafts/<slug>.md` or `_posts/<filename>.md` using `read_file`.
If the user pastes the content directly, use that.

Also read `.bob/skills/style-guide/style-reference.md` with `read_file` to have the guidelines active.

## Step 2 — Run the checklist

Check every item below. For each violation found, note: severity, line number (approximate), and what to fix.

### FRONT MATTER
- [ ] `layout: post` present
- [ ] `title:` in Title Case, quoted
- [ ] `slug:` present, kebab-case, no trailing slash
- [ ] `image:` starts with `/assets/img/` (not `/wp-content/`)
- [ ] `excerpt:` present, 1–2 sentences, no markdown, ≤160 chars
- [ ] `categories:` uses only allowed values
- [ ] `post_series_id:` present if part of a series

### STRUCTURE
- [ ] H1 is the article title (first line after front matter)
- [ ] `_Posted on **{{ page.date | date_to_string }}**_` line present after H1
- [ ] Hero image line present and uses `{:width="760" height="400" .responsive_img}`
- [ ] `## Introduction` section present
- [ ] "You should read this if:" bullet list in Introduction (3 items, if applicable)
- [ ] `## Conclusion` section present
- [ ] Conclusion has a bullet list starting with "In this article we covered:"
- [ ] Bridge sentence to next article in Conclusion (if series)
- [ ] Fixed CTA block at the very end (exact wording)
- [ ] "How This Series Is Structured" section present **only** in Part 1 of a series

### VOICE AND TONE
- [ ] No filler opener ("In this article we will…", "Today we are going to…")
- [ ] No passive voice as default — flag instances
- [ ] No forbidden words: "basically", "simply", "just", "obviously", "leverage", "synergy"
- [ ] No corporate HR-speak in conclusions
- [ ] Analogies resolve within the same paragraph (not abandoned)

### CODE BLOCKS
- [ ] Every code block has a language tag
- [ ] Shell commands use `shell` (not `bash`)
- [ ] Commands with 2+ flags have a flag breakdown bullet list after them
- [ ] No bare URLs in body text (must be wrapped in `[text](url)`)

### CROSS-REFERENCES (series posts only)
- [ ] Introduction links to previous article
- [ ] Conclusion links to next article
- [ ] Links use `{{ site.baseurl }}/slug/` format (not hardcoded URLs)

### IMAGES
- [ ] Every image has descriptive alt text
- [ ] Internal images use `{{ site.baseurl }}/assets/img/` path

## Step 3 — Produce the report

Output the review as:

```
## Review: "<Post Title>"

### 🔴 CRITICAL (blocks publication)
1. [line ~N] [rule violated] → [what to fix]

### 🟡 IMPORTANT (degrades quality)
1. [line ~N] [rule violated] → [what to fix]

### 🔵 MINOR (polish)
1. [line ~N] [rule violated] → [what to fix]

### ✅ PASSED
- [item]: ok

### Summary
X critical, Y important, Z minor issues.
[One sentence overall assessment — ready to publish / needs work / major revision needed]
```

**Severity guide:**
- 🔴 CRITICAL: missing required front matter field, broken series links, missing Conclusion, missing CTA block.
- 🟡 IMPORTANT: style violations (passive voice, forbidden words, missing flag breakdown, wrong image path).
- 🔵 MINOR: polish issues (capitalisation, minor wording, alt text improvement).

## Step 4 — Offer to fix

After the report, ask the user if they want the fixes applied automatically.

If yes:
- Apply all CRITICAL and IMPORTANT fixes using `apply_diff` or `search_and_replace`.
- Leave MINOR fixes for the user unless they ask for them too.
- After fixing, re-run the checklist mentally and confirm the post is clean.

## Rules

- Report exact issues, not vague suggestions. "Line ~45: missing language tag on code block" not "code blocks need attention".
- Never silently fix without reporting first.
- Do not change the substance of the content — only style, structure, and compliance.
