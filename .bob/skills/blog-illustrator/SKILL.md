---
name: blog-illustrator
description: Use when the user wants to generate hero or inline SVG illustrations and diagrams for a blog post (architecture diagrams, sequence diagrams, data flows, and component schemes).
---

# Blog Illustrator — Code4Projects

This skill designs and generates native, high-quality **SVG diagrams and illustrations** for Code4Projects blog posts.

All illustrations are created as clean, standalone, responsive `.svg` files with a standard width of `760px` (or standard `viewBox="0 0 760 H"`), ensuring crisp rendering on any screen, zero external API dependencies, and perfectly accurate technical labeling.

## Why Native SVG Diagrams?

- **Zero API Keys & No Rate Limits:** Completely generated locally with Bob's tools, never fails due to third-party outages or paid tiers.
- **Precise Technical Terminology:** No AI-hallucinated gibberish text or watermarks. Every label, class name, endpoint, and arrow reflects the exact code and architecture.
- **Perfect Responsiveness:** Scalable vector format (`viewBox="0 0 760 H"`), Retina-ready, light payload (~5–20 KB).
- **Consistent Code4Projects Aesthetic:** Clean, professional technical design using the blog's design palette.

---

## Design System & Style Guidelines

Every generated SVG must follow the Code4Projects visual language:

### Dimensions & ViewBox
- **Standard Width:** `760px`
- **Standard Aspect Ratios / ViewBoxes:**
  - Hero image: `viewBox="0 0 760 400"` (or `760x420`)
  - Flow / Sequence / Architecture diagram: `viewBox="0 0 760 400"` to `viewBox="0 0 760 500"`
  - Wide comparison chart: `viewBox="0 0 760 380"`
- **Font Family:** `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"`
- **Monospace Font for Code / Paths:** `ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace`

### Color Palette

| Token | Hex | Usage |
| :--- | :--- | :--- |
| **Canvas Background** | `#ffffff` | Clean white backdrop |
| **Card / Container Surface** | `#f7f8fa` | Subtle gray container panels |
| **Border / Dividers** | `#e5e7eb` or `#d1d5db` | Box borders and dividing rules |
| **Primary Accent (Tech Blue)**| `#3b82d4` / `#2563eb` | Primary layers, active nodes, key badges |
| **Secondary Accent (Purple)** | `#7c5cd8` / `#6d28d9` | Services, transformations, secondary flows |
| **Tertiary Accent (Cyan/Teal)**| `#0ea5e9` / `#0d9488` | Routers, API gateways, incoming requests |
| **Success / Valid** | `#10b981` / `#059669` | Positive states, OK responses, cache hits |
| **Warning / Notice** | `#f59e0b` / `#d97706` | Warnings, intermediate state, cautions |
| **Error / Attention** | `#ef4444` / `#dc2626` | Exceptions, rejected requests, errors |
| **Primary Text** | `#1f2328` | Headings, main labels, strong text |
| **Muted Text / Annotations** | `#57606a` | Subtitles, descriptions, coordinate labels |
| **Badge / Tag Text** | `#ffffff` | Text inside saturated accent badges |

---

## Supported Diagram Types

1. **Layered Architecture & Component Stacks:**
   - Stacked cards for Routers, Services, Repositories, Database with data types crossing boundaries.
2. **Request-Response & Sequence Flows:**
   - Chronological lifelines, HTTP methods (`GET`, `POST`), status codes (`200 OK`, `422 Unprocessable Entity`), middleware chains.
3. **Domain Models & Entity Relationships:**
   - Entities, Value Objects, schemas with typed fields and cardinalities.
4. **Data Pipelines & Concurrency Schemes:**
   - Thread vs Process comparisons, Event loop wheels, async task queues, connection pooling.
5. **Infrastructure & Network Topologies:**
   - Docker containers, bridge networks, volumes, reverse proxies, and Kubernetes pods.

---

## Workflow

### Step 1 — Analyze Post Requirements

1. Inspect the blog post in `_posts/<filename>.md` or `_drafts/<filename>.md`.
2. Extract key architectural concepts, layer interactions, lifecycles, or comparison points.
3. Determine whether you are creating:
   - **Hero Image:** `<slug>-hero.svg` (Overview visual summarizing the core technical premise).
   - **Inline Technical Diagram:** `<slug>-<concept>.svg` (e.g. `<slug>-dependency-injection.svg`, `<slug>-sequence-flow.svg`).

### Step 2 — Generate SVG Code

Write the complete SVG directly to `assets/img/<name>.svg` using the `write_file` or `apply_diff` tool.

**SVG Structure Checklist:**
- [ ] Root element has `xmlns="http://www.w3.org/2000/svg"`, `viewBox="0 0 760 H"`, `width="760"`, `height="H"`.
- [ ] Explicit `<rect width="760" height="H" fill="#ffffff"/>` background.
- [ ] Rounded corners on boxes (`rx="6"` or `rx="8"`).
- [ ] Clean marker arrows defined in `<defs>` (`<marker id="arrow" ... />`).
- [ ] Crisp text alignment using `text-anchor="middle"` or `text-anchor="start"`.
- [ ] Clear typography hierarchy (Title 15–16px bold, section 13–14px bold, labels 11–12px, badges 10–11px).

### Step 3 — Embed in Blog Post

Add or update the illustration reference in the Jekyll markdown file:

**For Hero Image (Front Matter + Top of Body):**
```markdown
---
image: /assets/img/<slug>-hero.svg
---

# Title
_Posted on **{{ page.date | date_to_string }}**_

![Title]({{ site.baseurl }}/assets/img/<slug>-hero.svg){:width="760" height="400" .responsive_img}
```

**For Inline Technical Diagrams:**
```markdown
![Layered Architecture Request Flow]({{ site.baseurl }}/assets/img/<slug>-diagram.svg){:width="760" height="420" .responsive_img}
```
