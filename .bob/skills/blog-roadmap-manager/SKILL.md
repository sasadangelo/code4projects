---
name: blog-roadmap-manager
description: Use when the user wants to manage the blog roadmap — add ideas, change status, schedule posts, view the pipeline, check what is published but not yet distributed, or update distribution flags.
---

# Roadmap Manager — Code4Projects

The roadmap lives in `_data/roadmap.yml`. Every idea, draft, and published post is tracked there as a single entry. This skill manages that file.

## Data model

Each entry in `roadmap.yml` has this shape:

```yaml
- id: unique-kebab-case-id # required, unique, used as key
  title: "Post Title" # required
  status: idea # idea | planned | draft | published
  category: "Category Name" # must match existing blog categories
  series: series-slug # optional — matches post_series_id
  scheduled: YYYY-MM-DD # optional — planned publication date
  slug: post-slug # optional until draft; required for published
  distributed:
    medium: false
    substack: false
    twitter: false
    linkedin: false
    instagram: false
    facebook: false
```

**Status values:**

- `idea` — raw idea, not yet planned
- `planned` — approved, outline exists or scheduled
- `draft` — post file exists in `_drafts/`
- `published` — post file exists in `_posts/` and is live

**Distribution flags** — set to `true` once a post has been pushed to that channel.

## Allowed categories

Use only these values in `category:`:

- `Virtualization`
- `Artificial Intelligence`
- `Cloud`
- `Programming`
- `Networking`
- `Android`
- `Multimedia`
- `Project Management`
- `Design Patterns`
- `Software Architecture`

## Operations

### 1. View roadmap

When the user asks to see the roadmap, pipeline, calendar, or backlog:

1. Run `python3 .bob/skills/blog-roadmap-manager/roadmap.py show` with `execute_command`.
2. Present the output as a formatted table grouped by status.

### 2. Add an idea

When the user wants to add a new idea:

1. Ask (inline, not with a tool) for: title, category, series (if any), scheduled date (if any).
2. Generate a kebab-case `id` from the title.
3. Add the new entry to `_data/roadmap.yml` using `apply_diff` or `insert_content` — append at the end of the file.
4. Confirm the addition by showing the new entry.

### 3. Change status

When the user promotes an idea to planned/draft/published, or demotes it:

1. Use `apply_diff` to change the `status:` field of the matching entry in `_data/roadmap.yml`.
2. When promoting to `published`, also ensure `slug:` is set.
3. Confirm the change.

### 4. Schedule / reschedule

When the user sets or changes a publication date:

1. Use `apply_diff` to update `scheduled:` on the matching entry.
2. Run `python3 .bob/skills/blog-roadmap-manager/roadmap.py calendar` to show the updated calendar.

### 5. Mark as distributed

When the user says a post has been published on a channel:

1. Set the relevant flag to `true` in `distributed:` using `apply_diff`.
2. Confirm and show the remaining undistributed channels for that post.

### 6. Show distribution gaps

When the user asks what is published but not yet distributed:

1. Run `python3 .bob/skills/blog-roadmap-manager/roadmap.py gaps` with `execute_command`.
2. Show the output as a table: post title × channel, ❌ for missing, ✅ for done.

### 7. Remove an entry

When the user wants to delete an idea or entry:

1. Confirm the id/title to remove.
2. Use `apply_diff` to remove the block from `_data/roadmap.yml`.

## Rules

- Never invent category values not in the allowed list above.
- Never change the `id` of an existing entry — it is the stable key.
- Always read the current `_data/roadmap.yml` with `read_file` before making any edit.
- Dates must be ISO 8601: `YYYY-MM-DD`.
- `distributed` block must always contain all 6 channel keys, even if all `false`.
