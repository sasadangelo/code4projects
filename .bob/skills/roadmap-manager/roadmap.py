#!/usr/bin/env python3
"""
roadmap.py — CLI helper for _data/roadmap.yml
Usage:
  python3 roadmap.py show       # grouped table by status
  python3 roadmap.py calendar   # upcoming posts sorted by scheduled date
  python3 roadmap.py gaps       # published posts with missing distribution
"""

import sys
import yaml
from pathlib import Path

ROADMAP_PATH = Path(__file__).parent.parent.parent.parent / "_data" / "roadmap.yml"
CHANNELS = ["medium", "substack", "twitter", "linkedin", "instagram", "facebook"]
STATUS_ORDER = ["idea", "planned", "draft", "published"]
STATUS_EMOJI = {
    "idea": "💡",
    "planned": "📅",
    "draft": "✏️ ",
    "published": "✅",
}


def load():
    with open(ROADMAP_PATH, "r") as f:
        return yaml.safe_load(f) or []


def truncate(s, n):
    s = str(s) if s else ""
    return s if len(s) <= n else s[: n - 1] + "…"


def cmd_show(entries):
    grouped = {s: [] for s in STATUS_ORDER}
    for e in entries:
        grouped.setdefault(e.get("status", "idea"), []).append(e)

    for status in STATUS_ORDER:
        items = grouped.get(status, [])
        if not items:
            continue
        emoji = STATUS_EMOJI.get(status, "")
        print(f"\n{emoji} {status.upper()} ({len(items)})")
        print(f"  {'ID':<35} {'TITLE':<50} {'CAT':<22} {'SCHEDULED':<12}")
        print(f"  {'-'*35} {'-'*50} {'-'*22} {'-'*12}")
        for e in items:
            print(
                f"  {truncate(e.get('id',''), 35):<35} "
                f"{truncate(e.get('title',''), 50):<50} "
                f"{truncate(e.get('category',''), 22):<22} "
                f"{e.get('scheduled','') or '':<12}"
            )


def cmd_calendar(entries):
    scheduled = [
        e for e in entries if e.get("scheduled") and e.get("status") != "published"
    ]
    scheduled.sort(key=lambda e: str(e.get("scheduled", "")))
    if not scheduled:
        print("No upcoming scheduled posts.")
        return
    print(f"\n📆 CALENDAR ({len(scheduled)} posts)")
    print(f"  {'DATE':<12} {'STATUS':<10} {'TITLE':<55} {'SERIES'}")
    print(f"  {'-'*12} {'-'*10} {'-'*55} {'-'*30}")
    for e in scheduled:
        print(
            f"  {str(e.get('scheduled','')):<12} "
            f"{e.get('status',''):<10} "
            f"{truncate(e.get('title',''), 55):<55} "
            f"{e.get('series','') or ''}"
        )


def cmd_gaps(entries):
    published = [e for e in entries if e.get("status") == "published"]
    if not published:
        print("No published posts found.")
        return

    # filter to posts with at least one missing channel
    gaps = []
    for e in published:
        dist = e.get("distributed") or {}
        missing = [ch for ch in CHANNELS if not dist.get(ch, False)]
        if missing:
            gaps.append((e, missing))

    if not gaps:
        print("✅ All published posts are fully distributed.")
        return

    print(f"\n🔴 DISTRIBUTION GAPS ({len(gaps)} posts)\n")
    header = f"  {'TITLE':<50} " + " ".join(f"{ch[:4]:>6}" for ch in CHANNELS)
    print(header)
    print(f"  {'-'*50} " + " ".join(f"{'------':>6}" for _ in CHANNELS))
    for e, _ in gaps:
        dist = e.get("distributed") or {}
        flags = " ".join(
            f"{'  ✅':>6}" if dist.get(ch) else f"{'  ❌':>6}" for ch in CHANNELS
        )
        print(f"  {truncate(e.get('title',''), 50):<50} {flags}")

    print(f"\n  Channels: " + " | ".join(CHANNELS))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    if not ROADMAP_PATH.exists():
        print(f"ERROR: {ROADMAP_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    entries = load()

    if cmd == "show":
        cmd_show(entries)
    elif cmd == "calendar":
        cmd_calendar(entries)
    elif cmd == "gaps":
        cmd_gaps(entries)
    else:
        print(f"Unknown command: {cmd}. Use: show | calendar | gaps", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
