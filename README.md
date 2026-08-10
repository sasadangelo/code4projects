# Code4Projects

**Code4Projects** is a technical blog by [Salvatore D'Angelo](https://www.linkedin.com/in/salvatore-d-angelo-0321851/) — a software professional with 30+ years of experience. The blog covers Cloud, Virtualization, AI/LLM, DevOps, Programming, and Software Engineering, written from hands-on practice rather than theory.

🌐 **Live site:** [sasadangelo.github.io/code4projects](https://sasadangelo.github.io/code4projects/)

---

## About

The blog is built with [Jekyll](https://jekyllrb.com/) and hosted on GitHub Pages. Every post is written in Markdown, versioned here, and automatically deployed on push to `main`.

Topics covered:
- **Cloud** — AWS, IBM Cloud, Kubernetes
- **Virtualization** — Docker, containers, Podman
- **Artificial Intelligence** — LLMs, LangChain, agent protocols (A2A, MCP)
- **Programming** — Python, HTML, CSS, YAML
- **DevOps & Project Management** — Agile, DevOps practices
- **Android** — game programming series

---

## Running Locally

**Requirements:** Ruby 3+, Bundler

```bash
# Install dependencies
bundle install

# Serve with live reload
bundle exec jekyll serve --config _config.yml,_config.dev.yml

# Open in browser
open http://localhost:4000/code4projects/
```

---

## Project Structure

```
_posts/          ← published articles (Markdown)
_drafts/         ← work-in-progress drafts (not published)
_data/           ← YAML data files (navigation, roadmap, newsletter, etc.)
_layouts/        ← Jekyll page templates
_includes/       ← reusable HTML partials
_sass/           ← stylesheets
assets/          ← images, fonts, CSS, JS
_authors/        ← author profile pages
docs/            ← project documentation
```

---

## Writing & Publishing Workflow

This repository uses a **Bob AI skill system** to automate the editorial workflow — from idea to multi-channel distribution.

The full workflow:

```
💡 Idea → evaluate → plan → write → review → publish → distribute
```

Each step is handled by a dedicated Bob skill:

| Skill | Purpose |
|-------|---------|
| `blog-advisor` | Strategic review, gap analysis, content direction |
| `idea-evaluator` | Evaluate a new idea (rubric + duplicate check) |
| `roadmap-manager` | Manage `_data/roadmap.yml` — pipeline, scheduling, distribution tracking |
| `post-planner` | Turn an approved idea into a full outline and front matter |
| `post-writer` | Write the complete draft in `_drafts/` |
| `post-reviewer` | Review a draft against the style guide |
| `social-content` | Generate Twitter thread, LinkedIn, Instagram, Facebook, Substack content |
| `style-guide` | Voice, tone, structure, and technical conventions |

📖 **Full documentation:** [docs/BLOG_AUTOMATION.md](docs/BLOG_AUTOMATION.md)

---

## Roadmap

Post ideas, drafts, and distribution status are tracked in [`_data/roadmap.yml`](_data/roadmap.yml).

View the pipeline from the terminal:

```bash
python3 .bob/skills/roadmap-manager/roadmap.py show      # full pipeline by status
python3 .bob/skills/roadmap-manager/roadmap.py calendar  # upcoming scheduled posts
python3 .bob/skills/roadmap-manager/roadmap.py gaps      # published but not distributed
```

---

## Channels

Published posts are distributed to:
- [Medium](https://medium.com/@sasadangelo) — mirror of all posts
- [Substack](https://code4projects.substack.com) — newsletter
- Twitter / X — [@code4projects](https://twitter.com/code4projects)
- LinkedIn
- Instagram
- Facebook

---

## Release History

### 0.0.2
- Contact Form with FormSpree
- CSS Print
- W3C Syntax Validation
- RSS Feed

### 0.0.1
- Posts and pages support
- Home page with hero image
- Sitemaps (posts and pages)
- Robots.txt, SEO tags, Google Analytics
- Social buttons, Categories, Pagination
- Newsletter, Post series, Draft posts
- 404 page, Favicon, Privacy Policy
