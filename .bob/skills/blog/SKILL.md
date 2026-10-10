---
name: blog
description: "Full-lifecycle blog engine with 11 sub-skills. Routes requests to the right sub-skill: blog-advisor, blog-idea, blog-illustrator, blog-medium-importer, blog-planner, blog-research, blog-review, blog-roadmap-manager, blog-social, blog-style, blog-writer."
metadata:
  disable-model-invocation: true
  argument-hint: [illustrate|write|idea|medium-importer|planner|research|reviewer|roadmap-manager|social|style|writer]
---

# Blog: Engine for Content Management

Full-lifecycle blog management: idea, illustrator, medium-importer, planner, research, reviewer, roadmap-manager, social, style, writer.

## Quick Reference

| Command                       | What it does                                        |
| ----------------------------- | --------------------------------------------------- |
| /blog idea <topic>            | Evaluate an idea for blog post                      |
| /blog planner <topic>         | When an idea is approved it plans the new blog post |
| /blog research <topic>        | Research references, statistics, and images for the post |
| /blog write <topic>           | Write a new blog post as draft                      |
| /blog illustrator <topic>     | Generate the hero SVG + inline diagrams after writing |
| /blog review <topic>          | Evaluate a new blog post before publish it          |
| /blog medium-importer <topic> | Import an article from Medium.com                   |
| /blog roadmap-manager         | Define a roadmap for blog content                   |
| /blog social                  | Write social content to promote a blog post         |
| /blog style                   | Define the style of blog post                       |

## Standard Post Pipeline

For every new post, follow this exact sequence:

```
idea → planner → research → writer → illustrator → review → (roadmap-manager) → social
```

| Step | Command | Output |
| ---- | ------- | ------ |
| 1. Evaluate idea | `/blog idea <topic>` | approve / reject / transform decision |
| 2. Plan the post | `/blog planner <topic>` | outline, front matter, series context |
| 3. Research | `/blog research <topic>` | notes + references in `.bob/tmp/blog-research/<slug>/` |
| 4. Write draft | `/blog write <topic>` | `_drafts/<slug>.md` |
| 5. Illustrate | `/blog illustrator <slug>` | hero `<slug>-hero.svg` + inline `<slug>-<concept>.svg` → `assets/img/` |
| 6. Review | `/blog review <topic>` | prioritised fix list; apply fixes |
| 7. Publish | `/blog roadmap-manager` | update roadmap status to `published` |
| 8. Promote | `/blog social` | Twitter/X, LinkedIn, Instagram, Facebook, Substack copy |

> **Illustrator note:** Step 5 is mandatory for every post. It generates at minimum a **hero image** (`<slug>-hero.svg`) and adds as many inline diagrams as are needed to replace prose the reader would otherwise have to imagine. The goal is ≥1 inline diagram per major concept.

## Orchestration Logic

### Command Routing

1. Parse the user's command to determine the sub-skill
2. If no sub-command given, ask which action they need
3. Route to the appropriate sub-skill:
   idea -> blog-idea (Evaluate an idea for blog post)
   planner -> blog-planner (When an idea is approved it plans the new blog post)
   research -> blog-research (Research references and statistics for the post)
   write → blog-writer (Write a new blog post as draft)
   illustrate | illustrator -> blog-illustrator (Generate hero SVG and inline diagrams after writing)
   medium-importer → blog-medium-importer (Import an article from Medium.com)
   review → blog-review (Evaluate a new blog post before publish it)
   roadmap-manager → blog-roadmap-manager (Define a roadmap for blog content)
   social → blog-social (Write social content to promote a blog post)
   style → blog-style (Define the style of blog post)

## Platform Detection

Detect blog platform from file extension and project structure:

| Signal                  | Platform Format                                 |
| ----------------------- | ----------------------------------------------- |
| .md files, \_config.yml | Jekyll Standard markdown with YAML front matter |

## Content Pillars

Every post must respect these 6 pillars, derived from the existing corpus:

| Pillar                                           | What it means                                                                                                                         | How to apply it                                                                                                                                                                                                     |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Problem-First Opening**                     | Every post starts with the pain point the reader is already feeling, not with abstract definitions.                                   | First paragraph states the specific problem or goal. Avoid opening with history, theory, or author biography.                                                                                                       |
| **2. Series Architecture & Cross-Linking**       | Content is organised in intentional multi-part series with explicit navigation.                                                       | Use `post_series_id` front matter. Open with a breadcrumb ("This is Part N of the series..."). Close by pointing forward to the next article.                                                                |
| **3. Hands-On Build with Real Code**             | Posts teach by doing: every concept is demonstrated with a working, copy-pasteable code example drawn from a real project.            | Include 5–12 code blocks per technical post. Prefer complete, runnable snippets over fragments. Link to the source GitHub repository. Use "Good / Avoid" comparisons where relevant.                                |
| **4. Visual Clarity**                            | Every post has a featured image plus at least one diagram or screenshot that replaces prose a reader would otherwise have to imagine. | Front matter must include `image:`. Use architecture diagrams for concept posts, UI screenshots for step-by-step tutorials, SVG/inline charts where data is compared.                                               |
| **5. Hierarchical Structure with a Conclusion**  | Headers create a scannable skeleton; the conclusion distils what was learned and bridges to the next step.                            | Use H2 for major sections, H3 for subsections, H4 only when a sub-subsection is genuinely distinct. End every post with a `## Conclusion` that bullet-lists key takeaways and names the next article in the series. |
| **6. Consistent Front Matter & Reader Contract** | Every post declares its intent, audience, and series membership in a uniform way so readers and tools can rely on it.                 | Required fields: `layout`, `title`, `slug`, `image`, `excerpt`, `categories`, `post_series_id` (all except standalone posts). `excerpt` must be 1–2 sentences, 150–200 characters, written as a value proposition.  |

## Agents

| Agent | Role |
| :--- | :--- |
| **blog-researcher** | Research specialist: finds statistics, sources, competitive data |

## Reference Files

Load on-demand as needed (1 references, load only what the task needs):

skills/blog-review/references/quality-scoring.md: Full 5-category scoring checklist (100 points)
