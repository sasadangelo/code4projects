#!/bin/bash
# =============================================================================
# build-ebook.sh — Generate a PDF ebook from a Jekyll blog post series
#
# Usage:
#   ./build-ebook.sh <post_series_id>
#
# Example:
#   ./build-ebook.sh getting-started-with-docker
#
# The script:
#   1. Reads ebook/series/<post_series_id>/metadata.yml for book settings
#   2. Finds all _posts/*.md whose frontmatter has matching post_series_id
#   3. Sorts them by filename (YYYY-MM-DD prefix = publication order)
#   4. Strips Jekyll frontmatter and Liquid tags from each post
#   5. Assembles: frontmatter/ + chapters + backmatter/
#   6. Runs pandoc + xelatex → PDF
#
# Output:
#   ebook/series/<post_series_id>/build/<output_filename>.pdf
#
# Adding a new series:
#   mkdir -p ebook/series/<new_series_id>/{frontmatter,backmatter,build}
#   cp ebook/series/getting-started-with-docker/metadata.yml \
#      ebook/series/<new_series_id>/metadata.yml
#   # Edit metadata.yml (title, cover-image, dedication, …) and write the
#   # frontmatter/backmatter .md files (preface, glossary, conclusion)
#   ./build-ebook.sh <new_series_id>
# =============================================================================
set -euo pipefail

# ── Colours ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
step()  { echo -e "${CYAN}[STEP]${NC}  $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*" >&2; exit 1; }

# ── Dependency check ─────────────────────────────────────────────────────────
check_deps() {
  local missing=()
  for cmd in pandoc xelatex python3; do
    command -v "$cmd" &>/dev/null || missing+=("$cmd")
  done
  if [[ ${#missing[@]} -gt 0 ]]; then
    error "Missing dependencies: ${missing[*]}\n  pandoc:   brew install pandoc\n  xelatex:  brew install --cask mactex-no-gui\n  python3:  brew install python"
  fi
  info "Dependencies OK  (pandoc $(pandoc --version | head -1 | awk '{print $2}'), xelatex)"
}

# ── Arguments ────────────────────────────────────────────────────────────────
usage() { echo "Usage: $0 <post_series_id>  [e.g. getting-started-with-docker]"; exit 1; }
[[ $# -lt 1 ]] && usage

SERIES_ID="$1"
EBOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$EBOOK_DIR/.." && pwd)"
SERIES_DIR="$EBOOK_DIR/series/$SERIES_ID"
POSTS_DIR="$REPO_ROOT/_posts"
TEMPLATE="$EBOOK_DIR/templates/ebook.latex"
BUILD_DIR="$SERIES_DIR/build"
TMP_DIR="$BUILD_DIR/.tmp"

[[ -d "$SERIES_DIR" ]]              || error "Series folder not found:\n  $SERIES_DIR\nRun with --help for usage."
[[ -f "$SERIES_DIR/metadata.yml" ]] || error "metadata.yml not found in $SERIES_DIR"
[[ -f "$TEMPLATE" ]]                || error "LaTeX template not found: $TEMPLATE"

# Front matter (e.g. cover.md) embeds paths relative to the repo root, so
# pandoc/xelatex must always run from there regardless of the caller's cwd.
cd "$REPO_ROOT"

mkdir -p "$BUILD_DIR" "$TMP_DIR"

# ── YAML helper (no yq dependency) ───────────────────────────────────────────
read_meta() {
  local key="$1"
  python3 - "$SERIES_DIR/metadata.yml" "$key" <<'PY'
import sys, re
key = sys.argv[2]
with open(sys.argv[1]) as f:
    content = re.sub(r'^---\s*\n', '', f.read())
for line in content.splitlines():
    m = re.match(r'^' + re.escape(key) + r'\s*:\s*"?([^"#\n]+?)"?\s*$', line)
    if m:
        print(m.group(1).strip()); sys.exit(0)
print('')
PY
}

# ── Strip Jekyll/Liquid from a post ──────────────────────────────────────────
strip_post() {
  local src="$1" dst="$2" repo_root="$3" img_dir="$4"
  python3 - "$src" "$dst" "$repo_root" "$img_dir" <<'PY'
import os, re, shutil, subprocess, sys, unicodedata

src, dst, repo_root, img_dir = sys.argv[1:5]
SITE_URL = 'https://www.code4projects.org'

with open(src, encoding='utf-8') as f:
    txt = f.read()

# Extract the title, then remove the YAML frontmatter block
title = ''
m = re.match(r'^---\s*\n(.*?)\n---\s*\n', txt, flags=re.DOTALL)
if m:
    t = re.search(r'^title:\s*(.+?)\s*$', m.group(1), flags=re.MULTILINE)
    if t:
        title = t.group(1).strip().strip('"\'')
    txt = txt[m.end():]

# Convert Jekyll highlight tags to fenced code blocks (also when indented)
txt = re.sub(r'^[ \t]*\{%-?\s*highlight\s+(\w+)[^%]*-?%\}[ \t]*$', r'```\1', txt, flags=re.MULTILINE)
txt = re.sub(r'^[ \t]*\{%-?\s*endhighlight\s*-?%\}[ \t]*$', '```', txt, flags=re.MULTILINE)

# Protect fenced code blocks and inline code spans: code examples (HTML in
# particular) must survive the tag/Liquid stripping applied to the prose.
stash = []
def protect(mo):
    stash.append(mo.group(0))
    return f'\x00{len(stash) - 1}\x00'
txt = re.sub(r'^(`{3,}|~{3,})[^\n]*\n.*?^\1[ \t]*$', protect, txt, flags=re.DOTALL | re.MULTILINE)
txt = re.sub(r'`[^`\n]+`', protect, txt)

# Remove all remaining Liquid tags
txt = re.sub(r'\{%-?.*?-?%\}', '', txt, flags=re.DOTALL)

# site.baseurl: images resolve to the repo, links to the published site
txt = re.sub(r'(!\[[^\]]*\]\()\{\{\s*site\.baseurl\s*\}\}/', r'\1' + repo_root + '/', txt)
txt = re.sub(r'\{\{\s*site\.baseurl\s*\}\}/', SITE_URL + '/', txt)
txt = re.sub(r'\{\{[^}]*\}\}', '', txt)

# Remove inline attribute lists {:...} used by kramdown (width, height, class)
txt = re.sub(r'\{:[^}]*\}', '', txt)

# Remove Jekyll "Posted on" line: _Posted on **...**_
txt = re.sub(r'_Posted on \*\*.*?\*\*_\n?', '', txt)

# Remove the blog-only footer (claps/share call to action, AI note)
txt = re.sub(r'\n-{3,}\s*\n+If you enjoyed this article.*\Z', '\n', txt, flags=re.DOTALL)
txt = re.sub(r'^\*\*Note\*\*: English is not my native language.*$', '', txt, flags=re.MULTILINE)

# Images: xelatex only handles png/jpg/pdf. Use a pre-converted PNG next to
# the original when present, otherwise convert into img_dir; drop on failure.
def convert(path):
    os.makedirs(img_dir, exist_ok=True)
    out = os.path.join(img_dir, os.path.splitext(os.path.basename(path))[0] + '.png')
    if os.path.exists(out):
        return out
    ext = os.path.splitext(path)[1].lower()
    cmds = []
    if ext == '.svg' and shutil.which('rsvg-convert'):
        cmds.append(['rsvg-convert', '-z', '2', '-o', out, path])
    if ext == '.webp' and shutil.which('dwebp'):
        cmds.append(['dwebp', '-quiet', path, '-o', out])
    if shutil.which('magick'):
        cmds.append(['magick', '-density', '200', path + ('[0]' if ext == '.gif' else ''), out])
    for cmd in cmds:
        if subprocess.run(cmd, capture_output=True).returncode == 0 and os.path.exists(out):
            return out
    return None

def fix_image(mo):
    alt, path = mo.group(1), mo.group(2)
    base, ext = os.path.splitext(path)
    if ext.lower() not in ('.svg', '.webp', '.gif'):
        return mo.group(0)
    if os.path.exists(base + '.png'):
        return f'![{alt}]({base}.png)'
    out = convert(path) if os.path.exists(path) else None
    if out:
        return f'![{alt}]({out})'
    print(f'  [WARN] image dropped: {path}', file=sys.stderr)
    return ''
txt = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)', fix_image, txt)

# Remove raw HTML blocks (pros-cons tables, divs, etc.) — not supported in PDF
txt = re.sub(r'<div[^>]*>.*?</div>', '', txt, flags=re.DOTALL)
txt = re.sub(r'</?[A-Za-z][^>\n]*>', '', txt)

# Restore protected code
txt = re.sub(r'\x00(\d+)\x00', lambda mo: stash[int(mo.group(1))], txt)
txt = re.sub(r'\x00(\d+)\x00', lambda mo: stash[int(mo.group(1))], txt)

# Remove emoji (not supported by most LaTeX fonts)
# (keep other symbols such as box-drawing characters used in directory trees)
def is_emoji(c):
    cp = ord(c)
    return (unicodedata.category(c) == 'Cs' or cp >= 0x1F000 or 0x2600 <= cp <= 0x27BF
            or 0x2B00 <= cp <= 0x2BFF or cp in (0xFE0F, 0x200D))
txt = ''.join(c for c in txt if not is_emoji(c))

# Clean multiple blank lines left by removals
txt = re.sub(r'\n{3,}', '\n\n', txt).strip()

# Every chapter needs a top-level heading: use the post title when missing
if title and not txt.startswith('# '):
    txt = f'# {title}\n\n' + txt

with open(dst, 'w', encoding='utf-8') as f:
    f.write(txt + '\n\n')
PY
}

# ── Chapter list for the preface (title + excerpt of each post) ──────────────
chapter_list() {
  local out="$1"; shift
  python3 - "$out" "$@" <<'PY'
import re, sys
out, posts = sys.argv[1], sys.argv[2:]
lines = []
for i, path in enumerate(posts, 1):
    fm = re.match(r'^---\s*\n(.*?)\n---', open(path, encoding='utf-8').read(), flags=re.DOTALL)
    meta = {}
    for key in ('title', 'excerpt'):
        m = re.search(r'^' + key + r':\s*(.+?)\s*$', fm.group(1) if fm else '', flags=re.MULTILINE)
        meta[key] = m.group(1).strip().strip('"\'') if m else ''
    item = f'{i}. **{meta["title"]}**'
    if meta['excerpt']:
        item += f' — {meta["excerpt"]}'
    lines.append(item)
open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
PY
}

# ── Read metadata ─────────────────────────────────────────────────────────────
check_deps

POST_SERIES_ID="$(read_meta post_series_id)"
OUTPUT_FILENAME="$(read_meta output_filename)"
[[ -z "$POST_SERIES_ID" ]]  && error "post_series_id not found in metadata.yml"
[[ -z "$OUTPUT_FILENAME" ]] && OUTPUT_FILENAME="${SERIES_ID}.pdf"

echo ""
info "Series        : $SERIES_ID"
info "post_series_id: $POST_SERIES_ID"
info "Output        : $OUTPUT_FILENAME"
echo ""

# ── Collect chapter posts ─────────────────────────────────────────────────────
step "Scanning _posts/ for post_series_id: $POST_SERIES_ID ..."

CHAPTER_FILES=()
while IFS= read -r f; do
  CHAPTER_FILES+=("$f")
done < <(grep -rl "post_series_id:.*${POST_SERIES_ID}" "$POSTS_DIR" 2>/dev/null \
  | grep '\.md$' | sort)

[[ ${#CHAPTER_FILES[@]} -eq 0 ]] && \
  error "No posts found with post_series_id: $POST_SERIES_ID\nCheck metadata.yml and Jekyll frontmatter."

info "Found ${#CHAPTER_FILES[@]} chapter(s)."

# ── Assemble all parts ────────────────────────────────────────────────────────
rm -rf "$TMP_DIR"/*.md "$TMP_DIR/img"
PARTS=()

# 1. Front matter files (sorted: 01-preface, …). Cover and dedication come
#    from metadata.yml and are laid out by the shared template.
#    A "<!-- chapters -->" line is replaced with the generated chapter list.
step "Front matter..."
CHAPTER_LIST="$TMP_DIR/chapter-list.md"
chapter_list "$CHAPTER_LIST" "${CHAPTER_FILES[@]}"
while IFS= read -r -d '' f; do
  base=$(basename "$f")
  dst="$TMP_DIR/00_fm_${base}"
  python3 - "$f" "$dst" "$CHAPTER_LIST" <<'PY'
import re, sys
src, dst, lst = sys.argv[1:4]
txt = open(src, encoding='utf-8').read()
chapters = open(lst, encoding='utf-8').read().rstrip()
txt = re.sub(r'^[ \t]*<!--\s*chapters\s*-->[ \t]*$', lambda m: chapters, txt, flags=re.MULTILINE)
# Front matter is not part of the chapter numbering
txt = re.sub(r'^(#{1,6} (?:(?!\{[.#]).)+?)[ \t]*$', r'\1 {.unnumbered}', txt, flags=re.MULTILINE)
open(dst, 'w', encoding='utf-8').write(txt)
PY
  PARTS+=("$dst")
  info "  + $base"
done < <(find "$SERIES_DIR/frontmatter" -maxdepth 1 -name '*.md' -print0 2>/dev/null | sort -z)

# 2. Chapters
step "Chapters..."
idx=10
for f in "${CHAPTER_FILES[@]}"; do
  base=$(basename "$f")
  dst="$TMP_DIR/$(printf '%02d' $idx)_ch_${base}"
  strip_post "$f" "$dst" "$REPO_ROOT" "$TMP_DIR/img"
  # Force a page break between chapters
  printf '\n\n\\newpage\n\n' >> "$dst"
  PARTS+=("$dst")
  info "  + $base"
  ((idx++))
done

# 3. Back matter files (sorted: 98-glossary, 99-conclusion, …)
step "Back matter..."
while IFS= read -r -d '' f; do
  base=$(basename "$f")
  dst="$TMP_DIR/99_bm_${base}"
  # Add page break before each back matter section
  # Back matter is not part of the chapter numbering
  { printf '\n\n\\newpage\n\n'; sed -E 's/^(#{1,6} [^{]*[^{ ])[[:space:]]*$/\1 {.unnumbered}/' "$f"; } > "$dst"
  PARTS+=("$dst")
  info "  + $base"
done < <(find "$SERIES_DIR/backmatter" -maxdepth 1 -name '*.md' -print0 2>/dev/null | sort -z)

# ── pandoc → PDF ──────────────────────────────────────────────────────────────
OUTPUT_PATH="$BUILD_DIR/$OUTPUT_FILENAME"

# pandoc >= 3.8 renamed --highlight-style to --syntax-highlighting
if pandoc --help | grep -q -- '--syntax-highlighting'; then
  HIGHLIGHT_OPT=(--syntax-highlighting=tango)
else
  HIGHLIGHT_OPT=(--highlight-style=tango)
fi
step "Running pandoc → xelatex  →  $OUTPUT_FILENAME ..."
echo ""

# Cover image: cover-image in metadata.yml is relative to the series folder;
# the template renders it as the first page (or a text title page if absent).
COVER_OPT=()
COVER_IMAGE="$(read_meta cover-image)"
if [[ -n "$COVER_IMAGE" ]]; then
  [[ -f "$SERIES_DIR/$COVER_IMAGE" ]] || error "cover-image not found: $SERIES_DIR/$COVER_IMAGE"
  COVER_OPT=(-V "cover-path=$SERIES_DIR/$COVER_IMAGE")
fi

pandoc \
  "${PARTS[@]}" \
  ${COVER_OPT[@]+"${COVER_OPT[@]}"} \
  --template="$TEMPLATE" \
  --metadata-file="$SERIES_DIR/metadata.yml" \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=2 \
  --number-sections \
  --top-level-division=chapter \
  "${HIGHLIGHT_OPT[@]}" \
  --resource-path="$REPO_ROOT" \
  -V "geometry:a4paper,left=2.5cm,right=2.5cm,top=3cm,bottom=3cm" \
  -V "colorlinks=true" \
  -V "linkcolor=NavyBlue" \
  -V "urlcolor=NavyBlue" \
  -f markdown+smart+pipe_tables+fenced_code_blocks+definition_lists \
  -o "$OUTPUT_PATH"

# ── Result ────────────────────────────────────────────────────────────────────
echo ""
if [[ -f "$OUTPUT_PATH" ]]; then
  SIZE=$(du -h "$OUTPUT_PATH" | cut -f1)
  info "✓  PDF ready: $OUTPUT_PATH  ($SIZE)"
else
  error "PDF not created — check pandoc output above."
fi

rm -rf "$TMP_DIR"
echo ""
info "Done. To add this book to Substack, upload:"
info "  $OUTPUT_PATH"
