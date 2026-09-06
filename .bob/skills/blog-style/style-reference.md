# Code4Projects — Style Reference

Annotated excerpts from the post corpus. Use these as the ground truth when generating or reviewing content.

---

## Voice: Practitioner-to-practitioner

**Good** (from `2026-07-25-getting-started-with-docker.md`):
> "Before diving into commands, it is worth spending a minute on the problem Docker actually solves."

Why it works: gets to the point, assumes the reader knows what commands are, frames the value before asking for attention.

**Good** (from `2026-02-23-build-your-own-llm-chatbot-with-python-and-langchain-part-1.md`):
> "Everyone says building a chatbot with LLMs is easy. Just call an API, send a prompt, and get a response. That illusion lasts exactly until you try to turn it into something real."

Why it works: short declarative sentences. Starts with shared experience, immediately subverts the expectation. No warm-up fluff.

**Avoid** (from `2023-06-03-demystifying-agile-unleashing-flexibility-project-management.md` — older post, style diverged):
> "By adhering to these guiding principles, organizations can unleash the true potential of Agile and achieve better outcomes for their projects and customers."

Why it fails: corporate HR-speak. "Unleash the true potential" is filler. The newer posts never write like this.

---

## Tone: Analogies that resolve immediately

**Good** (from `2026-04-30-understanding-a2a-the-protocol-for-agent-collaboration.md`):
> "Imagine you need to plan a complex trip abroad … Each of these tasks is complex enough to require specialized expertise … But here's the challenge: how do these agents communicate and coordinate with each other? This is exactly the problem that A2A … solves."

Pattern: scenario → roles → problem question → answer in the same paragraph. The analogy is never abandoned; it resolves immediately.

**Good** — contrast metaphor (same post):
> "Think of it like the early days of the web, before HTTP became the standard. A2A aims to be the HTTP for AI agents."

Pattern: historical parallel → direct mapping. One sentence each.

---

## Structure: Introduction block

Template used consistently in recent (2026) posts:

```markdown
## Introduction

[1–2 sentences framing the problem / referencing the previous article in series]

[1–2 sentences on what this article delivers]

You should read this article if:

- [criterion 1]
- [criterion 2]
- [criterion 3]
```

The "You should read this" list is a commitment contract with the reader. It should be honest and specific — not "if you want to learn about X" (too vague) but "if you want to move beyond basic LLM API calls" (specific skill gap).

---

## Structure: Conclusion block

Always a bullet summary + bridge sentence + CTA separator. Template:

```markdown
## Conclusion

In this article we covered:

- [item 1]
- [item 2]
- [item N]

The [next article]({{ site.baseurl }}/slug/) [one sentence on what's next].

---

If you enjoyed this article, don't forget to **give it a clap 👏**, **share it with your friends 🔗**, and **follow me for more tips and tutorials on software development 📘**. Your support helps me create more content like this — thank you! 🙌
```

The CTA line is fixed. Do not rephrase it.

---

## Structure: Series opener — "How This Series Is Structured"

From `2026-07-25-getting-started-with-docker.md`:

```markdown
## How This Series Is Structured

This first article introduced the core concepts and got you running immediately. In the upcoming articles we will progressively build on this foundation:

- **Containers vs Virtual Machines** — deep dive into isolation mechanisms ...
- **Dockerfile & Building Custom Images** — write your own `Dockerfile`, build and tag a custom image ...
- ...
```

Rules:
- Bold article title, em-dash, brief description. One line per article.
- Always written in the *first* article of the series only.
- Describes the series arc, not just a table of contents.

---

## Code blocks: flag breakdown pattern

From `2026-07-25-getting-started-with-docker.md`:

```markdown
```shell
docker run -d -p 8080:80 --name my-nginx nginx:alpine
```

Breaking down the options:

- `-d` — runs the container in detached mode (in the background, shell does not hang)
- `-p 8080:80` — maps port 8080 on your host to port 80 inside the container
- `--name my-nginx` — gives the container a friendly name instead of a random one
- `nginx:alpine` — the image to use
```

This pattern is mandatory for any command with more than two options. Each flag on its own bullet, em-dash separator, plain English explanation.

---

## Comparison tables

From `2026-07-25-getting-started-with-docker.md`:

```markdown
| | Docker | Podman |
|---|---|---|
| **Architecture** | Requires a background daemon (`dockerd`) | Daemonless — runs containers directly |
| **Privileges** | Daemon runs as root | Rootless by default — more secure |
```

Rules:
- First column is the property name, in bold.
- Use backticks for technical terms inside cells.
- Em-dash for supplementary notes within a cell.
- No more than 5–6 rows; if more, split into multiple tables or use a prose list.

---

## Blockquotes for key take-aways

From `2026-02-23-build-your-own-llm-chatbot-with-python-and-langchain-part-1.md`:

```markdown
> Input text → Output text
```

```markdown
> The combination of URL + API Key determines which provider you connect to.
```

Blockquotes are used for:
1. A one-line summary of a concept the reader must remember.
2. Simulated terminal/user interaction (short inputs/outputs).
3. Literal quotations from specs or documentation.

Not used for: lengthy explanatory paragraphs (use normal prose).

---

## Depth vs. length

The Docker security article (`2026-07-31-docker-security-best-practices.md`) demonstrates the right balance: the explanation of "pinned digest vs floating tag" runs 8 detailed paragraphs because the concept genuinely requires it. No padding — every paragraph adds information.

Contrast this with the Agile article (`2023-06-03`) which is long but thin: many section headings, each with only 2–3 sentences. The newer style packs more substance per section, fewer sections overall.

**Rule of thumb**: prefer fewer, deeper sections over many shallow ones.

---

## Categories in use (from post corpus)

| Category | Topic area |
|---|---|
| `Virtualization` | Docker, Kubernetes, containers |
| `Artificial Intelligence` | LLMs, LangChain, A2A, MCP |
| `Cloud` | AWS, IBM Cloud |
| `Project Management` | Agile, DevOps |
| `Software Architecture` | Layered, Hexagonal, Clean, Event-Driven, Hybrid architectures |
| `Android` | Android game development |

Always use the exact string shown above. Do not invent new categories without confirming with the author.

---

## Front matter checklist

```yaml
layout: post                          # always "post"
title: "Title in Title Case"         # quoted, title case
post_series_id: series-slug          # only if part of a series
slug: exact-slug-no-trailing-slash   # must match the URL
image: /assets/img/filename.svg      # relative from site root
excerpt: One or two sentence SEO summary without markdown.
categories:
  - "Category Name"
```

- `slug` must NOT have a trailing slash (breaking change introduced in 2021-era posts; fixed in 2026 posts).
- `excerpt` is used by SEO tag and social cards — must be readable without context, no markdown.
- `image` path starts with `/assets/img/` (not `/wp-content/` — that path is legacy 2021 only).
