#!/usr/bin/env python3
"""
import_medium.py — Convert a Medium article (HTML from RSS content:encoded)
into a Jekyll Markdown draft for Code4Projects.

Usage:
  python3 import_medium.py --html "<html fragment>" --title "..." --date "2026-01-05" \
      --slug "my-slug" --category "Programming" [--series "series-id"] \
      [--excerpt "..."] [--image "filename.png"] [--out _drafts/]

  All args except --html and --title are optional.
  If --slug is omitted, it is derived from --title.
  If --date is omitted, today's date is used.

Outputs:
  - _drafts/<slug>.md        (Jekyll post)
  - assets/img/<images>      (downloaded hero + inline images)
  Prints a JSON summary to stdout.
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.parse
from datetime import date
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print(
        "ERROR: beautifulsoup4 is required. Run: pip install beautifulsoup4",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BLOG_SLUG_BASE = "https://sasadangelo.github.io/code4projects"
MEDIUM_DOMAINS = (
    "medium.com",
    "plainenglish.io",
    "towardsdatascience.com",
    "betterprogramming.pub",
    "itnext.io",
    "stackademic.com",
    "python.plainenglish.io",
    "levelup.gitconnected.com",
)

ALLOWED_CATEGORIES = [
    "Virtualization",
    "Artificial Intelligence",
    "Cloud",
    "Programming",
    "Networking",
    "Android",
    "Multimedia",
    "Project Management",
    "Design Patterns",
]

CTA_BLOCK = (
    "\n---\n\n"
    "If you enjoyed this article, don't forget to **give it a clap 👏**, "
    "**share it with your friends 🔗**, and "
    "**follow me for more tips and tutorials on software development 📘**. "
    "Your support helps me create more content like this — thank you! 🙌\n"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def download_image(
    url: str, dest_dir: Path, rename_as: str | None = None
) -> str | None:
    """
    Download an image to dest_dir and return the local filename, or None on failure.
    If rename_as is provided, the file is saved with that name (extension preserved
    from the original URL). rename_as should be the stem only, e.g. 'my-post-hero'.
    """
    try:
        parsed = urllib.parse.urlparse(url)
        # Derive extension from the original URL path
        original_name = Path(parsed.path).name
        suffix = Path(original_name).suffix if "." in original_name else ".png"
        if suffix.lower() not in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"):
            suffix = ".png"

        if rename_as:
            name = re.sub(r"[^a-zA-Z0-9._-]", "-", rename_as) + suffix
        else:
            name = (
                re.sub(r"[^a-zA-Z0-9._-]", "_", original_name)
                if original_name
                else "image.png"
            )

        dest = dest_dir / name
        if not dest.exists():
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                dest.write_bytes(resp.read())
        return name
    except Exception as e:
        print(f"  [warn] Could not download {url}: {e}", file=sys.stderr)
        return None


def is_medium_link(href: str) -> bool:
    return any(d in href for d in MEDIUM_DOMAINS)


def load_roadmap_slugs(roadmap_path: Path) -> set[str]:
    """Return set of slugs already in the blog roadmap."""
    if not roadmap_path.exists():
        return set()
    try:
        import yaml

        with open(roadmap_path) as f:
            entries = yaml.safe_load(f) or []
        return {e.get("slug", "") for e in entries if e.get("slug")}
    except Exception:
        return set()


# ---------------------------------------------------------------------------
# HTML → Markdown converter (no external markdownify dependency)
# ---------------------------------------------------------------------------


def _heading_shift(soup_node) -> int:
    """
    Compute how many levels to shift headings so the minimum heading in the
    article body maps to H2 (Jekyll convention: H1 = post title only).

    Medium typically uses H3 as the top section level → shift = -1 (H3→H2).
    If the article uses H2 as top level → shift = 0.
    If it uses H4 as top level → shift = -2.
    """
    levels = set()
    for tag in soup_node.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        levels.add(int(tag.name[1]))
    if not levels:
        return 0
    min_level = min(levels)
    # We want min_level to become 2 (H2)
    return 2 - min_level  # e.g. min=3 → shift=-1; min=2 → shift=0; min=4 → shift=-2


def html_to_markdown(
    soup_node,
    assets_dir: Path,
    blog_slugs: set[str],
    downloaded_images: list,
    slug: str = "article",
) -> str:
    """Recursively convert a BeautifulSoup node tree to Markdown."""

    shift = _heading_shift(soup_node)
    inline_img_counter = [0]  # mutable counter accessible inside convert()

    def convert(node) -> str:
        from bs4 import NavigableString, Tag

        if isinstance(node, NavigableString):
            return str(node)

        if not isinstance(node, Tag):
            return ""

        tag = node.name
        children_md = "".join(convert(c) for c in node.children)

        # --- Block elements ---
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            # Shift so the minimum heading in the article maps to H2.
            # H1 is reserved for the post title — floor at 2, cap at 4.
            jekyll_level = max(2, min(4, level + shift))
            return f"\n\n{'#' * jekyll_level} {children_md.strip()}\n\n"

        if tag == "p":
            text = children_md.strip()
            if not text:
                return ""
            return f"\n\n{text}\n\n"

        if tag in ("ul", "ol"):
            items = []
            for i, li in enumerate(node.find_all("li", recursive=False)):
                li_md = "".join(convert(c) for c in li.children).strip()
                if tag == "ol":
                    items.append(f"{i+1}. {li_md}")
                else:
                    items.append(f"- {li_md}")
            return "\n\n" + "\n".join(items) + "\n\n"

        if tag == "li":
            return children_md  # handled by ul/ol

        if tag == "blockquote":
            lines = children_md.strip().splitlines()
            return "\n\n" + "\n".join(f"> {l}" for l in lines) + "\n\n"

        if tag == "pre":
            # Detect language hint from a nested <code class="language-X">
            code_tag = node.find("code")
            lang = ""
            if code_tag:
                cls = " ".join(code_tag.get("class", []))
                m = re.search(r"language-(\w+)", cls)
                if m:
                    lang = m.group(1)
            # Medium RSS uses <br/> as newlines inside <pre> — fix before get_text
            for br in node.find_all("br"):
                br.replace_with("\n")
            code_text = node.get_text()
            # Unescape HTML entities
            code_text = (
                code_text.replace("&lt;", "<")
                .replace("&gt;", ">")
                .replace("&amp;", "&")
                .replace("&quot;", '"')
                .replace("&#39;", "'")
                .replace("&nbsp;", " ")
            )
            return f"\n\n```{lang}\n{code_text.rstrip()}\n```\n\n"

        if tag == "code" and node.parent.name != "pre":
            text = node.get_text()
            return f"`{text}`"

        if tag == "hr":
            return "\n\n---\n\n"

        if tag == "br":
            return "\n"

        # --- Inline formatting ---
        if tag in ("strong", "b"):
            text = children_md.strip()
            return f"**{text}**" if text else ""

        if tag in ("em", "i"):
            text = children_md.strip()
            return f"*{text}*" if text else ""

        if tag == "a":
            href = node.get("href", "").strip()
            text = children_md.strip() or href

            # Strip Medium tracking suffixes
            href = re.sub(r"\?source=.*$", "", href)

            if not href or href.startswith("#"):
                return text

            # Internal Medium link — check if we have it in blog
            if is_medium_link(href):
                m = re.search(r"/([a-z0-9-]+)-[a-f0-9]{8,}$", href)
                if m:
                    candidate = m.group(1)
                    if candidate in blog_slugs:
                        return f"[{text}]({{{{ site.baseurl }}}}/{candidate}/)"
                # Not in blog — keep medium link as-is
                return f"[{text}]({href})"

            return f"[{text}]({href})"

        if tag == "img":
            src = node.get("src", "")
            alt = node.get("alt", "")

            # Skip tracking pixels
            if "stat?event" in src or (
                node.get("width") == "1" and node.get("height") == "1"
            ):
                return ""

            inline_img_counter[0] += 1
            rename = f"{slug}-fig-{inline_img_counter[0]}"
            local_name = download_image(src, assets_dir, rename_as=rename)
            if local_name:
                downloaded_images.append(local_name)
                return (
                    f"\n\n![{alt}]({{{{ site.baseurl }}}}/assets/img/{local_name})"
                    f'{{:width="760" height="400" .responsive_img}}\n\n'
                )
            return f"\n\n![{alt}]({src})\n\n"

        if tag == "figure":
            img_tag = node.find("img")
            caption_tag = node.find("figcaption")
            img_md = convert(img_tag) if img_tag else ""
            caption = caption_tag.get_text().strip() if caption_tag else ""
            if img_md and caption:
                return img_md.rstrip() + f"\n*{caption}*\n\n"
            return img_md

        if tag == "figcaption":
            return ""  # handled by figure

        # --- Skip noise tags ---
        if tag in (
            "script",
            "style",
            "nav",
            "footer",
            "button",
            "form",
            "input",
            "noscript",
            "svg",
        ):
            return ""

        # Default: recurse
        return children_md

    return convert(soup_node)


# ---------------------------------------------------------------------------
# Main conversion
# ---------------------------------------------------------------------------


def convert_medium_html(
    html_content: str,
    title: str,
    slug: str,
    pub_date: str,
    category: str,
    series: str | None,
    excerpt: str,
    hero_image_hint: str | None,
    assets_dir: Path,
    blog_slugs: set[str],
) -> tuple[str, list[str]]:
    """
    Convert Medium HTML content to Jekyll Markdown.
    Returns (markdown_string, list_of_downloaded_image_filenames).
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove the "originally published in..." footer Medium appends
    for hr in soup.find_all("hr"):
        for sibling in list(hr.find_next_siblings()):
            sibling.decompose()
        hr.decompose()

    # Remove Medium tracking pixel
    for img in soup.find_all("img"):
        if "stat?event" in img.get("src", ""):
            img.decompose()

    # Extract hero image from the FIRST <figure> before converting body
    # (Medium RSS always puts the hero as the first element)
    hero_src_from_content = None
    first_figure = soup.find("figure")
    if first_figure:
        first_img = first_figure.find("img")
        if first_img:
            hero_src_from_content = first_img.get("src", "")
        first_figure.decompose()

    downloaded_images: list[str] = []
    body_md = html_to_markdown(
        soup, assets_dir, blog_slugs, downloaded_images, slug=slug
    )

    # Clean up excessive blank lines
    body_md = re.sub(r"\n{3,}", "\n\n", body_md).strip()

    # Remove duplicate CTA if the article body already contained it from Medium
    if "give it a clap" in body_md:
        # Match any variant: ASCII apostrophe, Unicode right-single-quote, or HTML entity
        cta_pattern = re.compile(
            r"\n\n(?:---\n\n)?If you enjoyed this article[,.]? don[\u2019']t forget",
            re.IGNORECASE,
        )
        m = list(cta_pattern.finditer(body_md))
        if m:
            body_md = body_md[: m[-1].start()].rstrip()

    # --- Hero image ---
    hero_filename = None
    if hero_src_from_content:
        hero_filename = download_image(
            hero_src_from_content, assets_dir, rename_as=f"{slug}-hero"
        )

    hero_line = ""
    if hero_filename:
        hero_line = (
            f"\n![{title}]({{{{ site.baseurl }}}}/assets/img/{hero_filename})"
            f'{{:width="760" height="400" .responsive_img}}\n'
        )
    elif downloaded_images:
        hero_line = (
            f"\n![{title}]({{{{ site.baseurl }}}}/assets/img/{downloaded_images[0]})"
            f'{{:width="760" height="400" .responsive_img}}\n'
        )
    elif hero_image_hint:
        hero_line = (
            f"\n![{title}]({{{{ site.baseurl }}}}/assets/img/{hero_image_hint})"
            f'{{:width="760" height="400" .responsive_img}}\n'
        )

    # --- Front matter ---
    hero_img_filename = (
        hero_filename
        or (downloaded_images[0] if downloaded_images else None)
        or hero_image_hint
        or "placeholder.png"
    )
    fm_lines = [
        "---",
        "layout: post",
        f'title: "{title}"',
    ]
    if series:
        fm_lines.append(f"post_series_id: {series}")
    fm_lines += [
        f"slug: {slug}",
        f"image: /assets/img/{hero_img_filename}",
        f"excerpt: {excerpt or title}",
        "categories:",
        f'  - "{category}"',
        "---",
    ]
    front_matter = "\n".join(fm_lines)

    # --- Assemble post ---
    post = (
        f"{front_matter}\n\n"
        f"# {title}\n"
        f"_Posted on **{{{{ page.date | date_to_string }}}}**_\n"
        f"{hero_line}\n"
        f"{body_md}\n"
        f"{CTA_BLOCK}"
    )

    return post, ([hero_filename] if hero_filename else []) + downloaded_images


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Convert Medium HTML to Jekyll draft")
    parser.add_argument(
        "--html",
        required=True,
        help="Medium article HTML (content:encoded from RSS, or pasted HTML)",
    )
    parser.add_argument("--title", required=True, help="Article title")
    parser.add_argument(
        "--date", default=str(date.today()), help="Publication date YYYY-MM-DD"
    )
    parser.add_argument(
        "--slug", default="", help="Post slug (derived from title if omitted)"
    )
    parser.add_argument(
        "--category",
        default="Programming",
        help=f"One of: {', '.join(ALLOWED_CATEGORIES)}",
    )
    parser.add_argument("--series", default="", help="post_series_id (optional)")
    parser.add_argument("--excerpt", default="", help="SEO excerpt (optional)")
    parser.add_argument(
        "--image", default="", help="Hero image filename hint (optional)"
    )
    parser.add_argument(
        "--out", default="_drafts", help="Output directory for the .md file"
    )
    parser.add_argument(
        "--assets", default="assets/img", help="Directory to download images into"
    )
    parser.add_argument(
        "--roadmap",
        default="_data/roadmap.yml",
        help="Path to roadmap.yml for internal link resolution",
    )
    args = parser.parse_args()

    if args.category not in ALLOWED_CATEGORIES:
        print(
            f"WARNING: '{args.category}' not in allowed categories. Using 'Programming'.",
            file=sys.stderr,
        )
        args.category = "Programming"

    slug = args.slug or slugify(args.title)
    assets_dir = Path(args.assets)
    assets_dir.mkdir(parents=True, exist_ok=True)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    blog_slugs = load_roadmap_slugs(Path(args.roadmap))

    post_md, images = convert_medium_html(
        html_content=args.html,
        title=args.title,
        slug=slug,
        pub_date=args.date,
        category=args.category,
        series=args.series or None,
        excerpt=args.excerpt,
        hero_image_hint=args.image or None,
        assets_dir=assets_dir,
        blog_slugs=blog_slugs,
    )

    out_file = out_dir / f"{slug}.md"
    out_file.write_text(post_md, encoding="utf-8")

    result = {
        "draft": str(out_file),
        "slug": slug,
        "title": args.title,
        "date": args.date,
        "category": args.category,
        "images_downloaded": images,
        "images_count": len(images),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
