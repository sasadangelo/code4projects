---
name: blog-writer
description: Use when the user wants to write a new blog post — takes the plan from post-planner and produces the complete draft in Jekyll Markdown format following the Code4Projects style guide.
---

# Post Writer — Code4Projects

This skill writes the complete draft of a blog post. It requires a plan (from `post-planner`) and applies the style guide automatically.

## Step 1 — Load context

1. Read the post plan from the conversation or ask the user to paste it.
2. Read `.bob/skills/blog-style/style-reference.md` with `read_file` — apply all guidelines throughout.
3. If the post belongs to a series, read 1–2 adjacent posts from `_posts/` to match tone and pick up cross-references correctly.
4. **[Optional Research Step]** If the research folder exists, read the compiled research notes from `.bob/tmp/blog-research/<slug>/notes.md` and any reference article files under `.bob/tmp/blog-research/<slug>/articles/`. Integrate the statistics (especially 2025-2026 data), technical insights, and competitor content gaps into the draft, and use the selected Hero and inline image direct CDN URLs/alt text from the notes. **If the research folder or files do not exist, silently ignore them and proceed to write the draft based purely on the plan and your general knowledge.**

## Step 2 — Write the draft

Produce the complete file content: **front matter + full body**.

Apply these rules without exception:

### Voice and tone

- First-person singular ("I", not "we") unless walking the reader through a hands-on exercise.
- Active voice throughout.
- No filler openers ("In this article, we will…" → cut it; start with the problem or the hook).
- No corporate jargon (leverage, synergy, empower).
- Analogy first for every abstract concept — one sentence scenario, then the technical explanation.

### Structure

Follow this skeleton exactly:

```
---
[front matter]
---

# [Title]
_Posted on **{{ page.date | date_to_string }}**_

![Title]({{ site.baseurl }}/assets/img/filename.ext){:width="760" height="400" .responsive_img}

## Introduction
[problem/context → who should read → series link if applicable]

## [Body sections]

## Conclusion
In this article we covered:
- bullet 1
- bullet 2

The [next article]({{ site.baseurl }}/slug/) [one sentence bridge].

---

If you enjoyed this article, don't forget to **give it a clap 👏**, **share it with your friends 🔗**, and **follow me for more tips and tutorials on software development 📘**. Your support helps me create more content like this — thank you! 🙌
```

### Code blocks

- Language tag on every block: `python`, `shell`, `yaml`, `dockerfile`, `json`, `html`.
- After any command with 2+ flags: break down each flag in a bullet list.
- Inline code for: filenames, commands, flags, class/function names, config keys.

### Comparisons

- Use a Markdown table for any 2+ option comparison.
- First column = property (bold), other columns = options.

### Series cross-references

- Introduction: link to previous article with `{{ site.baseurl }}/slug/`.
- Conclusion: link to next article with `{{ site.baseurl }}/slug/`.
- "How This Series Is Structured" section: **only in Part 1 / first article of a series**.

### Blockquotes

Use `>` only for:

1. A one-line concept summary the reader must remember.
2. Simulated input/output.
3. Literal spec/doc quotes.

## Step 3 — Output the file

Write the draft to `_drafts/<slug>.md` using `write_file`.

Then update `_data/roadmap.yml`:

- Set `status: draft` on the entry using `apply_diff`.

If the post belongs to a series, check `_data/post_sidebar.yml`:

- If an entry with the matching `post_series_id` already exists: do nothing (it will be updated at publish time).
- If no entry exists yet: note it in the Step 4 summary — it must be created when the post is published.

## Step 4 — Summary

After writing, show:

- File path created
- Word count estimate
- Any sections that need the user's input (e.g. actual command output to paste, screenshots needed, GitHub repo links)
- Open questions for the user (e.g. "confirm the next article slug")

## Rules

- Never truncate the draft. Write the complete article.
- Never add sections not in the plan without flagging them.
- Never use emojis in body text (only in the fixed CTA block at the end).
- Do not add a table of contents — the blog does not use them.
- The `_Posted on_` line uses Liquid and must appear exactly as shown — do not hardcode the date.
