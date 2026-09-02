---
name: blog
description: "Full-lifecycle blog engine with 9 sub-skills. Routes requests to the right sub-skill: glog-advisor, idea-evaluator,
medium-importer, post-planner, post-reviewer, post-writer, roadmap-manager, social-content, style-guide."
metadata:
  disable-model-invocation: true
  argument-hint: [write|idea|medium-importer|planner|reviewer|roadmap-manager|social|style|writer]
---

# Blog: Engine for Content Management

Full-lifecycle blog management: idea, medium-importer, planner, reviewer, roadmap-manager, social, style, writer.

## Quick Reference

| Command                       | What it does                                        |
| ----------------------------- | --------------------------------------------------- |
| /blog idea <topic>            | Evaluate an idea for blog post                      |
| /blog planner <topic>         | When an idea is approved it plans the new blog post |
| /blog medium-importer <topic> | Import an article from Medium.com                   |
| /blog write <topic>           | Write a new blog post as draft                      |
| /blog review <topic>          | Evaluate a new blog post before publish it          |
| /blog roadmap-manager         | Define a roadmap for blog content                   |
| /blog social                  | Write social content to promote a blog post         |
| /blog style                   | Define the style of blog post                       |

## Orchestration Logic

### Command Routing

1. Parse the user's command to determine the sub-skill
2. If no sub-command given, ask which action they need
3. Route to the appropriate sub-skill:
   idea -> blog-idea (Evaluate an idea for blog post)
   planner -> blog-planner (When an idea is approved it plans the new blog post)
   medium-importer → blog-medium-importer (Import an article from Medium.com )
   write → blog-write (Write a new blog post as draft )
   review → blog-review (Evaluate a new blog post before publish it)
   roadmap-manager → blog-roadmap-manager (Define a roadmap for blog content )
   social → blog-social (Write social content to promote a blog post)
   style → blog-style (Define the style of blog post)

## Platform Detection

Detect blog platform from file extension and project structure:

| Signal                  | Platform Format                                 |
| ----------------------- | ----------------------------------------------- |
| .md files, \_config.yml | Jekyll Standard markdown with YAML front matter |

## Content Pillars

Every post must respect these 6 pillars, derived from the existing corpus:

| Pillar | What it means | How to apply it |
| ---------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1. Problem-First Opening** | Every post starts with the pain point the reader is already feeling, not with abstract definitions. | First paragraph states the specific problem or goal. Avoid opening with history, theory, or author biography. |
| **2. Series Architecture & Cross-Linking** | Content is organised in intentional multi-part series with explicit navigation. | Use `post_series_id` front matter. Open with a breadcrumb ("This is Part N of the [X series](link)"). Close by pointing forward to the next article. |
| **3. Hands-On Build with Real Code** | Posts teach by doing: every concept is demonstrated with a working, copy-pasteable code example drawn from a real project. | Include 5–12 code blocks per technical post. Prefer complete, runnable snippets over fragments. Link to the source GitHub repository. Use "Good / Avoid" comparisons where relevant. |
| **4. Visual Clarity** | Every post has a featured image plus at least one diagram or screenshot that replaces prose a reader would otherwise have to imagine. | Front matter must include `image:`. Use architecture diagrams for concept posts, UI screenshots for step-by-step tutorials, SVG/inline charts where data is compared. |
| **5. Hierarchical Structure with a Conclusion** | Headers create a scannable skeleton; the conclusion distils what was learned and bridges to the next step. | Use H2 for major sections, H3 for subsections, H4 only when a sub-subsection is genuinely distinct. End every post with a `## Conclusion` that bullet-lists key takeaways and names the next article in the series. |
| **6. Consistent Front Matter & Reader Contract** | Every post declares its intent, audience, and series membership in a uniform way so readers and tools can rely on it. | Required fields: `layout`, `title`, `slug`, `image`, `excerpt`, `categories`, `post_series_id` (all except standalone posts). `excerpt` must be 1–2 sentences, 150–200 characters, written as a value proposition. |
