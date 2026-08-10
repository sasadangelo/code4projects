---
name: social-content
description: Use when a blog post has been published and the user wants to generate social media content — produces ready-to-post text for Twitter/X thread, LinkedIn post, Instagram caption, Facebook post, and Substack newsletter intro.
---

# Social Content Generator — Code4Projects

This skill generates platform-specific content for distributing a published blog post. Each platform has a different format, tone, and audience expectation. One source post → five distinct outputs.

## Step 1 — Load the source post

Read the post file from `_posts/<filename>.md` using `read_file`.
Extract:
- Title
- Excerpt
- Key sections (H2 headings + opening paragraph of each)
- Code examples (if any — for Twitter/LinkedIn)
- Conclusion bullet list
- Internal links to related posts
- Series context (if part of a series)

Also read the `distributed:` flags from `_data/roadmap.yml` to know which channels still need content.

## Step 2 — Generate content for each channel

---

### Twitter / X Thread

**Format:** 4–8 tweets. First tweet is the hook. Last tweet is the CTA.

Rules:
- Tweet 1: hook — a provocative statement, surprising fact, or the core problem. No "I wrote an article about…".
- Tweets 2–N: one key insight per tweet. Short sentences. Can include a code snippet (max 5 lines) if it is striking.
- Second-to-last tweet: key takeaway or summary in one line.
- Last tweet: link + CTA. Format: `Full article 👇\n[url]\n\nFollow @code4projects for more.`
- Max 280 chars per tweet. Number them: `1/N`, `2/N`, etc.
- No hashtag spam — max 2 relevant hashtags on the last tweet only.

---

### LinkedIn Post

**Format:** 150–300 words. Single flowing post, not a thread.

Rules:
- Open with a 1–2 line hook (problem or surprising insight). No "Excited to share…".
- 2–3 short paragraphs covering the main insight of the article.
- Bullet list of 3–5 key takeaways (use `→` not `-`).
- Closing line: "Full article in the comments 👇" (LinkedIn suppresses external links in posts).
- 3–5 relevant hashtags at the very end.
- Tone: professional but direct. Same voice as the blog — no LinkedIn-speak ("thrilled", "humbled", "passionate about").

---

### Instagram Caption

**Format:** 100–150 words + hashtag block.

Rules:
- Open with a 1-sentence hook strong enough to stop the scroll.
- 3–4 short paragraphs (1–2 sentences each). White space is essential.
- End with: "Link in bio 🔗"
- Hashtag block (separate from caption with a line break): 15–20 hashtags mixing broad (`#docker`, `#programming`) and niche (`#containerization`, `#devops`).
- No code snippets — describe the concept, don't show code.
- Emojis: 1–2 per paragraph maximum, only if they add meaning.

---

### Facebook Post

**Format:** 80–150 words. Conversational.

Rules:
- Slightly warmer tone than LinkedIn — this is a community, not a professional network.
- Open with a question or relatable problem statement.
- 2–3 short paragraphs.
- Direct link to the post (Facebook shows a preview card automatically).
- End with a question to invite comments (e.g. "Have you tried this? What was your experience?").
- 2–3 hashtags maximum.

---

### Substack Newsletter Intro

**Format:** 150–250 words. Opening section of the newsletter issue, not a full summary.

Rules:
- Opens with 1–2 sentences of personal context: why you wrote this, what triggered the idea, or what you were working on when you discovered it.
- Summarises what the reader will learn (3 bullet points).
- Ends with: "Read the full article here: [title]([url])"
- Tone: more personal and conversational than the blog post itself. This is a letter, not a tutorial.
- Do NOT reproduce the article — tease it.

---

## Step 3 — Output format

Present all five outputs in clearly labelled sections:

```
## Twitter / X Thread
[tweet 1/N]
---
[tweet 2/N]
...

## LinkedIn
[full post text]

## Instagram
[caption]

[hashtag block]

## Facebook
[full post text]

## Substack Newsletter Intro
[intro text]
```

## Step 4 — Update distribution flags

Ask the user which channels were actually posted (do not assume all were), then update `distributed:` flags in `_data/roadmap.yml` using `apply_diff`.

## Rules

- Each output must be self-contained — a reader seeing only that platform post must understand the value without reading the others.
- Never start any post with "I wrote an article" or "Check out my new post".
- The blog URL format is: `https://sasadangelo.github.io/code4projects/<slug>/`
- Substack: the newsletter is at `https://code4projects.substack.com`.
