---
name: blog-medium-importer
description: Use when the user wants to import an article from Medium into the Jekyll blog — converts Medium HTML content (pasted by the user) into a Jekyll Markdown draft, downloads images, resolves internal links, and sets the correct front matter.
---

# Medium Importer — Code4Projects

This skill converts a Medium article into a ready-to-review Jekyll draft. The user provides the article content by pasting it directly in the prompt. Bob extracts the needed data and calls the conversion script.

## Prerequisites

```bash
pip install beautifulsoup4 pyyaml
```

## Step 1 — Ask the user for article details

If not already provided in the message, ask (inline, no tool):

1. **Article title** — exact title as it appears on Medium
2. **Publication date** — format `YYYY-MM-DD`
3. **Category** — must be one of:
   `Virtualization`, `Artificial Intelligence`, `Cloud`, `Programming`,
   `Networking`, `Android`, `Multimedia`, `Project Management`, `Design Patterns`,
   `Software Architecture`
4. **Series** — `post_series_id` if this article belongs to a series (optional)
5. **Excerpt** — 1–2 sentence SEO summary, max 160 chars (optional — Bob can suggest one)
6. **Slug** — leave blank to auto-derive from title

## Step 2 — Get the article content

There are three ways to provide the article content, in order of quality:

### Option A — RSS feed HTML (best quality)

The article is in the author's RSS feed (most recent ~10 articles).

1. Open `https://medium.com/feed/@sasadangelo` in the browser
2. Find the `<content:encoded>` block for the target article
3. Copy the HTML and paste it in the prompt

This preserves all formatting: headings, code blocks, lists, bold/italic, images.

### Option B — Paste the article text directly in the prompt (good)

If the article is not in the RSS feed, the user can copy the full article text from the Medium page (select all, copy) and paste it directly into the prompt.

**When the user pastes plain text:**
Bob must reconstruct minimal HTML before passing to the script. Apply these rules:

- Each paragraph separated by a blank line → wrap in `<p>...</p>`
- Lines starting with `#` → convert to `<h3>`, `##` → `<h4>` (Medium style)
- Fenced code blocks (` ``` `) → convert to `<pre><code>...</code></pre>`, preserving newlines as `<br/>`
- `**bold**` → `<strong>bold</strong>`
- `*italic*` → `<em>italic</em>`
- Bare URLs or `[text](url)` → `<a href="url">text</a>`

Do this reconstruction inline (no tool call needed) before calling the script.

### Option C — HTML from browser DevTools (best for old articles)

1. Open the Medium article in Chrome/Safari
2. Open DevTools → Network tab → reload the page
3. Find the RSS feed request or use: right-click on page → "View Page Source"
4. Copy the article body HTML from `<article>` tag
5. Paste in the prompt

## Step 3 — Run the conversion script

Once HTML content and metadata are available, call:

```bash
python3 .bob/skills/medium-importer/import_medium.py \
  --html "<paste HTML here>" \
  --title "<title>" \
  --date "YYYY-MM-DD" \
  --slug "<slug-or-blank>" \
  --category "<category>" \
  --series "<series-id-or-blank>" \
  --excerpt "<excerpt>" \
  --out "_drafts" \
  --assets "assets/img" \
  --roadmap "_data/roadmap.yml"
```

Use `execute_command` to run this. The `--html` value must be the raw HTML string.

**Important:** escape the HTML string correctly when passing it as a shell argument. If the HTML is very long (>10 000 chars), write it to a temp file first and modify the script call to read from stdin:

```bash
echo '<html>' | python3 .bob/skills/medium-importer/import_medium.py --html "$(cat /tmp/article.html)" ...
```

## Step 4 — Parse the output

The script prints a JSON object:

```json
{
  "draft": "_drafts/<slug>.md",
  "slug": "<slug>",
  "title": "<title>",
  "date": "<date>",
  "category": "<category>",
  "images_downloaded": ["filename.png"],
  "images_count": 1
}
```

Show the user a summary:

- Draft file created at `_drafts/<slug>.md`
- N images downloaded to `assets/img/`
- Any Medium links that were kept as-is (not resolved to internal blog links)

## Step 5 — Review the draft

Read the generated `_drafts/<slug>.md` with `read_file` and flag:

1. **Code blocks without language tag** — Medium strips language hints; Bob should infer and add them based on the code content (Python → `python`, shell commands → `shell`, YAML → `yaml`, etc.)
2. **Heading levels** — Medium uses H3 as top section headings; confirm they map correctly to H2 in the blog style
3. **Medium links that stayed as-is** — list them for the user to decide: import that article too, or leave the Medium link
4. **Missing excerpt** — if the user didn't provide one, suggest one from the introduction

Apply any obvious fixes (language tags on code blocks, heading normalisation) using `apply_diff`.

## Step 6 — Add to roadmap

Append a new entry to `_data/roadmap.yml` with `status: draft`:

```yaml
- id: <slug>
  title: "<title>"
  status: draft
  category: "<category>"
  series: <series-or-omit>
  scheduled: "<date>"
  slug: <slug>
  distributed:
    medium: true # already on Medium — mark as distributed
    substack: false
    twitter: false
    linkedin: false
    instagram: false
    facebook: false
```

Note: `medium: true` because the article originated on Medium.

## Step 7 — Confirm

Tell the user:

- Draft is at `_drafts/<slug>.md` — ready for `post-reviewer`
- Images are in `assets/img/`
- Next step: run `/post-reviewer` on the draft before publishing

## What the script does automatically

- Downloads all images from Medium CDN → `assets/img/`
- Removes the Medium "originally published in…" footer
- Removes the Medium tracking pixel
- Deduplicates the CTA block (Medium articles already contain it)
- Resolves internal Medium links: if the target article's slug exists in `roadmap.yml`, rewrites to `{{ site.baseurl }}/slug/`
- Preserves all external links unchanged
- Fixes `<br/>` newlines inside `<pre>` code blocks (Medium RSS quirk)
- Extracts hero image from the first `<figure>` tag

## What the script does NOT do

- It does not rewrite the content to match the blog style guide — that is `post-reviewer`'s job
- It does not detect language for code blocks without hints — flag these for manual review
- It does not handle paywalled articles (member-only) — the HTML must be accessible
