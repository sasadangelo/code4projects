# eBook Build System

This folder contains everything needed to generate PDF ebooks from the blog post series.

## Structure

```
ebook/
├── README.md                  ← this file
├── build-ebook.sh             ← main build script (parametric)
├── templates/
│   └── ebook.latex            ← LaTeX template (shared by all series)
└── series/
    ├── getting-started-with-docker/
    │   ├── metadata.yml       ← book title, author, description
    │   ├── post_series_id     ← maps to post_series_id in Jekyll frontmatter
    │   ├── frontmatter/
    │   │   ├── 00-cover.md
    │   │   ├── 01-dedication.md
    │   │   └── 02-preface.md
    │   └── backmatter/
    │       ├── 98-glossary.md
    │       └── 99-conclusion.md
    └── getting-started-with-kubernetes/   ← future series, same structure
        ├── metadata.yml
        └── ...
```

## How to build an ebook

```bash
# Build a specific series
./build-ebook.sh getting-started-with-docker

# The output PDF will be in:
# ebook/series/getting-started-with-docker/build/getting-started-with-docker.pdf
```

## How to add a new series

1. Create the folder: `ebook/series/<post_series_id>/`
2. Copy the structure from an existing series
3. Edit `metadata.yml` with the book details
4. Write the frontmatter and backmatter Markdown files
5. Run `./build-ebook.sh <post_series_id>`

The script automatically picks up all `_posts/*.md` files whose frontmatter
contains `post_series_id: <series>`, strips Jekyll frontmatter, and assembles
them in date order between the front and back matter.

## Prerequisites

- `pandoc` >= 3.0  (`brew install pandoc`)
- `xelatex`  (`brew install --cask mactex-no-gui`)
- DejaVu fonts or any system font you configure in `metadata.yml`
