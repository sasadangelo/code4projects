#!/opt/homebrew/bin/bash
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
#   # Edit metadata.yml and write frontmatter/backmatter .md files
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
  local src="$1" dst="$2" repo_root="$3"
  python3 - "$src" "$dst" "$repo_root" <<'PY'
import sys, re

with open(sys.argv[1], encoding='utf-8') as f:
    txt = f.read()

repo_root = sys.argv[3]

# Remove YAML frontmatter block
txt = re.sub(r'^---\s*\n.*?\n---\s*\n', '', txt, count=1, flags=re.DOTALL)

# Convert Jekyll highlight tags to fenced code blocks
txt = re.sub(r'\{%[-\s]*highlight\s+(\w+)\s*[-\s]*%\}', r'```\1', txt)
txt = re.sub(r'\{%[-\s]*endhighlight\s*[-\s]*%\}', '```', txt)

# Remove all remaining Liquid tags
txt = re.sub(r'\{%-?.*?-?%\}', '', txt, flags=re.DOTALL)

# Strip Jekyll Liquid output {{ ... }}, replacing site.baseurl with repo root
txt = re.sub(r'\{\{\s*site\.baseurl\s*\}\}/', repo_root + '/', txt)
txt = re.sub(r'\{\{[^}]*\}\}', '', txt)

# Remove inline attribute lists {:...} used by kramdown (width, height, class)
txt = re.sub(r'\{:[^}]*\}', '', txt)

# Remove Jekyll "Posted on" line: _Posted on **...**_
txt = re.sub(r'_Posted on \*\*.*?\*\*_\n?', '', txt)

# Replace SVG images with their PNG counterpart (pre-converted with rsvg-convert)
txt = re.sub(r'(!\[[^\]]*\]\([^)]*?)\.svg(\))', r'\1.png\2', txt)

# Remove image references with remaining unsupported formats for xelatex (webp, gif)
txt = re.sub(r'!\[[^\]]*\]\([^)]*\.(webp|gif)\)', '', txt)

# Remove raw HTML blocks (pros-cons tables, divs, etc.) — not supported in PDF
txt = re.sub(r'<div[^>]*>.*?</div>', '', txt, flags=re.DOTALL)
txt = re.sub(r'<[^>]+>', '', txt)

# Remove emoji (not supported by most LaTeX fonts)
import unicodedata
txt = ''.join(c for c in txt if unicodedata.category(c) not in ('So', 'Cs'))

# Clean multiple blank lines left by removals
txt = re.sub(r'\n{3,}', '\n\n', txt)

with open(sys.argv[2], 'w', encoding='utf-8') as f:
    f.write(txt.strip() + '\n\n')
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
rm -f "$TMP_DIR"/*.md
PARTS=()
COVER_FILE=""

# 1. Front matter files (sorted: 01-dedication, 02-preface, …)
#    00-cover.md is handled separately via --include-before-body
step "Front matter..."
while IFS= read -r -d '' f; do
  base=$(basename "$f")
  if [[ "$base" == "00-cover.md" ]]; then
    COVER_FILE="$f"
    info "  + $base (cover — injected before body)"
  else
    dst="$TMP_DIR/00_fm_${base}"
    cp "$f" "$dst"
    PARTS+=("$dst")
    info "  + $base"
  fi
done < <(find "$SERIES_DIR/frontmatter" -maxdepth 1 -name '*.md' -print0 2>/dev/null | sort -z)

# 2. Chapters
step "Chapters..."
idx=10
for f in "${CHAPTER_FILES[@]}"; do
  base=$(basename "$f")
  dst="$TMP_DIR/$(printf '%02d' $idx)_ch_${base}"
  strip_post "$f" "$dst" "$REPO_ROOT"
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
  { printf '\n\n\\newpage\n\n'; cat "$f"; } > "$dst"
  PARTS+=("$dst")
  info "  + $base"
done < <(find "$SERIES_DIR/backmatter" -maxdepth 1 -name '*.md' -print0 2>/dev/null | sort -z)

# ── pandoc → PDF ──────────────────────────────────────────────────────────────
OUTPUT_PATH="$BUILD_DIR/$OUTPUT_FILENAME"
step "Running pandoc → xelatex  →  $OUTPUT_FILENAME ..."
echo ""

# Build cover injection option: if a cover file was found, use --include-before-body
# and suppress pandoc's automatic title page with -V title=""
COVER_OPT=()
if [[ -n "$COVER_FILE" ]]; then
  COVER_OPT=(--include-before-body="$COVER_FILE" -V "title=")
fi

pandoc \
  "${PARTS[@]}" \
  "${COVER_OPT[@]}" \
  --metadata-file="$SERIES_DIR/metadata.yml" \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=2 \
  --number-sections \
  --highlight-style=tango \
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
