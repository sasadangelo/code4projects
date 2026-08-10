---
name: style-guide
description: Use when writing, reviewing, editing, or evaluating a blog post for Code4Projects — applies the established style, voice, tone, and structure guidelines derived from the existing corpus.
---

# Blog Style Guide — Code4Projects

When this skill is active, apply the following guidelines to any blog post you write, review, edit, translate, or adapt for Code4Projects (sasadangelo). These guidelines were distilled by analysing the full post corpus.

## 1. Voice

- **First-person singular, direct.** Write as "I" when sharing personal experience or opinion. Use "we" only in tutorial walk-throughs where the reader actively follows along ("let's put it together").
- **Practitioner to practitioner.** The author is a 30+ year software professional writing for fellow developers, not for managers or beginners who have never opened a terminal.
- **Confident, never arrogant.** State facts plainly ("A container is …"). Avoid hedging filler ("it might be worth noting that…").
- **No editorial fluff.** Never open with "Great!", "Sure!", or complimentary padding. Cut it.

## 2. Tone

- **Technical and precise.** Every claim must be grounded. When a concept has a common misconception, name and correct it explicitly (e.g. "isolation is not the same as security").
- **Warm but focused.** Light use of rhetorical questions ("But here's the challenge: how do these agents communicate?") to pull the reader forward. Do not overdo it.
- **Analogy-friendly.** Abstract concepts are introduced through a concrete, real-world analogy first (trip planning → multi-agent systems; HTTP → A2A). The analogy must be simple, relatable, and immediately resolved.
- **No corporate jargon.** Avoid "leverage", "synergy", "empower teams to deliver continuous value" as empty noise. Use plain verbs.
- **Closing CTA is standard** — always end articles with the fixed sentence block (clap, share, follow) from the existing posts.

## 3. Structure

Every post follows this skeleton:

```
## Introduction
  - 1–3 short paragraphs: the problem/context, why the reader should care, who should read it.
  - Optional "You should read this article if:" bullet list (3 items, no more).
  - If part of a series: explicit link back to previous article.

## [Body sections — H2 / H3 hierarchy]
  - Lead each major section with 1–2 sentences of context before diving into content.
  - Use H3 for sub-concepts within a section.
  - Tables for comparisons (Docker vs Podman, A2A vs MCP).
  - Code blocks with explicit language tag for every snippet.
  - Blockquotes (>) for key take-aways or one-line summaries of a concept.

## [Optional: "Putting It All Together" or "X in Action"]
  - A worked example that synthesises the section material.

## Conclusion
  - Bullet list summarising what was covered (past tense: "In this article we covered:").
  - One-sentence or one-paragraph bridge to the next article in the series.

---
[CTA paragraph]
```

## 4. Front Matter (Jekyll)

Required fields for every post:

```yaml
layout: post
title: "..."          # Title Case, quoted
slug: ...             # kebab-case, no trailing slash
image: /assets/img/... # SVG preferred for diagrams, PNG/WebP for photos
excerpt: ...          # 1–2 sentence SEO summary, no markdown
categories:
  - "Category Name"   # exact match to existing category
```

Optional but common:

```yaml
post_series_id: series-slug   # links the post into a series
```

## 5. Headings and Lists

- **H1** — article title only (repeated after front matter, before `_Posted on_`).
- **H2** — major sections.
- **H3** — sub-sections within a major section.
- Never skip heading levels.
- Bullet lists: use `-` not `*`. Keep each item to 1–2 lines. Do not nest more than one level.
- Numbered lists: only for sequential steps or ordered principles.

## 6. Code Style

- Every code block must have a language tag: ` ```python`, ` ```shell`, ` ```yaml`, ` ```dockerfile`, ` ```json`, ` ```html`.
- Shell commands: use `shell` as the language tag (not `bash`).
- Inline code for: file names, commands, flags, class names, function names, config keys.
- After a multi-option command, always break down the flags in a bullet list.

## 7. Links

- Internal links: use Jekyll `{{ site.baseurl }}/slug/` pattern.
- External links: always include display text, never a bare URL (except in quick-start resource lists).
- Link to previous/next articles in a series explicitly in Introduction and Conclusion.

## 8. Images

- Every post has a hero image matching `image:` in front matter.
- Images are embedded with `{:width="760" height="400" .responsive_img}` for full-width hero images.
- Diagrams: prefer SVG. Photos: WebP or PNG.
- Alt text must be descriptive, not decorative.

## 9. Series Posts

- Part 1 of a series must contain a "How This Series Is Structured" section listing all planned articles.
- Every part must open by referencing the previous article and close by bridging to the next.
- `post_series_id` must be identical across all posts in the series.

## 10. Length and Depth

- Typical post: 800–2 500 words. Longer is fine if content demands it; never pad to hit a word count.
- Each section should be complete and self-contained.
- Never truncate a technical explanation to stay short.

## 11. What to Avoid

- Do NOT start sentences with "Basically", "Simply", "Just", "Obviously".
- Do NOT write "In conclusion, it is important to note that…"
- Do NOT add disclaimers unless genuinely relevant.
- Do NOT use passive voice as the default. Active voice throughout.
- Do NOT use emojis in the body text (only in the fixed CTA closing block).

## Usage by Bob

When asked to write or edit a blog post for this project:

1. Read `.bob/skills/style-guide/style-reference.md` with `read_file` for annotated examples.
2. Apply all guidelines above to the draft.
3. If reviewing an existing post, flag deviations as a numbered list grouped by guideline section.
4. If generating a new post, produce the complete front matter + body in one pass.
