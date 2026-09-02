#!/usr/bin/env python3
"""
evaluate.py — Duplicate/similarity checker for blog post ideas.
Usage:
  python3 evaluate.py "your idea title or description"

Prints existing posts sorted by keyword overlap with the idea.
"""

import sys
import re
import yaml
from pathlib import Path
from collections import Counter

ROADMAP_PATH = Path(__file__).parent.parent.parent.parent / "_data" / "roadmap.yml"

# Words to ignore in matching
STOPWORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "in",
    "on",
    "to",
    "of",
    "for",
    "with",
    "how",
    "what",
    "why",
    "when",
    "is",
    "are",
    "was",
    "your",
    "my",
    "its",
    "it",
    "be",
    "do",
    "does",
    "by",
    "from",
    "at",
    "up",
    "as",
    "into",
    "getting",
    "started",
    "introduction",
    "guide",
    "tutorial",
    "beginners",
    "step",
    "using",
    "part",
    "vs",
    "build",
    "create",
    "make",
    "use",
}


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 2}


def load_roadmap() -> list[dict]:
    if not ROADMAP_PATH.exists():
        print(f"ERROR: {ROADMAP_PATH} not found.", file=sys.stderr)
        sys.exit(1)
    with open(ROADMAP_PATH) as f:
        return yaml.safe_load(f) or []


def similarity(tokens_a: set, tokens_b: set) -> float:
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union)  # Jaccard


def main():
    if len(sys.argv) < 2:
        print("Usage: evaluate.py '<idea description>'", file=sys.stderr)
        sys.exit(1)

    idea = " ".join(sys.argv[1:])
    idea_tokens = tokenize(idea)

    entries = load_roadmap()

    scores = []
    for e in entries:
        combined = f"{e.get('title', '')} {e.get('id', '')} {e.get('category', '')} {e.get('series', '')}"
        entry_tokens = tokenize(combined)
        score = similarity(idea_tokens, entry_tokens)
        shared = idea_tokens & entry_tokens
        scores.append((score, e, shared))

    scores.sort(key=lambda x: x[0], reverse=True)
    top = [s for s in scores if s[0] > 0.0][:10]

    print(f'\n🔍 Similarity check for: "{idea}"')
    print(f"   Idea keywords: {', '.join(sorted(idea_tokens))}\n")

    if not top or top[0][0] == 0.0:
        print("✅ No similar posts found in the roadmap.")
        return

    print(f"  {'SCORE':>6}  {'STATUS':<10} {'TITLE':<55} {'SHARED KEYWORDS'}")
    print(f"  {'------':>6}  {'-'*10} {'-'*55} {'-'*30}")
    for score, e, shared in top:
        bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
        shared_str = ", ".join(sorted(shared)[:5])
        title = e.get("title", "")
        title = title if len(title) <= 55 else title[:54] + "…"
        print(
            f"  {score:>5.0%}  [{bar}]  {e.get('status',''):<10} {title:<55}  {shared_str}"
        )

    # Highlight high-risk overlaps
    high = [(s, e, sh) for s, e, sh in top if s >= 0.35]
    if high:
        print(f"\n⚠️  HIGH OVERLAP (≥35%) — review before approving:")
        for score, e, shared in high:
            print(
                f"   - [{score:.0%}] {e.get('title','')}  (status: {e.get('status','')})"
            )
    else:
        print(f"\n✅ No high-overlap posts detected (all scores < 35%).")


if __name__ == "__main__":
    main()
