#!/usr/bin/env python3
"""
image_downloader.py — Permanent script to parse notes.md, download hero image candidates,
and standardize them to exactly 760x400 px using center cropping.

Usage:
  python3 .bob/skills/blog-research/image_downloader.py <slug>
"""

import os
import sys
import re
import urllib.request
from PIL import Image

TARGET_SIZE = (760, 400)


def parse_image_urls(notes_path):
    """
    Parses notes.md and extracts candidate hero image Unsplash/Pixabay/Pexels CDN URLs.
    Looks for the Hero Image Candidates table.
    """
    if not os.path.exists(notes_path):
        print(f"❌ Error: {notes_path} not found.", file=sys.stderr)
        sys.exit(1)

    with open(notes_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the Hero Image table by looking for rows with URLs
    # Matches URLs starting with http/https inside markdown tables or text
    urls = re.findall(r"https://images\.unsplash\.com/[^\s`|)\"\']+", content)
    # Also find Pixabay/Pexels patterns if any
    pixabay_urls = re.findall(
        r"https://cdn\.pixabay\.com/[^\s`|)\"\']+", content
    )
    pexels_urls = re.findall(
        r"https://images\.pexels\.com/[^\s`|)\"\']+", content
    )

    all_urls = urls + pixabay_urls + pexels_urls
    # Deduplicate while preserving order
    seen = set()
    unique_urls = []
    for u in all_urls:
        # Strip trailing characters that might be caught
        clean_url = u.split("?")[0]
        # Append parameters for higher quality resolution
        if "unsplash.com" in clean_url:
            clean_url = f"{clean_url}?w=1200&fit=crop&q=80"
        elif "pexels.com" in clean_url:
            clean_url = f"{clean_url}?auto=compress&cs=tinysrgb&w=1200"

        if clean_url not in seen:
            seen.add(clean_url)
            unique_urls.append(clean_url)

    # Return up to 5 URLs
    return unique_urls[:5]


def download_and_standardize(url, filepath):
    """
    Downloads an image from URL and standardizes it to exactly TARGET_SIZE (760x400) via center-cropping.
    """
    try:
        # Download file
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
        )
        with urllib.request.urlopen(req) as response:
            data = response.read()

        # Temporary write
        temp_path = filepath + ".tmp"
        with open(temp_path, "wb") as f:
            f.write(data)

        # Open image with Pillow to process
        with Image.open(temp_path) as img:
            # Convert to RGB
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Aspect ratio crop
            target_aspect = TARGET_SIZE[0] / TARGET_SIZE[1]
            img_aspect = img.size[0] / img.size[1]

            if img_aspect > target_aspect:
                # Too wide, crop sides
                new_width = int(img.size[1] * target_aspect)
                left = (img.size[0] - new_width) // 2
                img = img.crop((left, 0, left + new_width, img.size[1]))
            elif img_aspect < target_aspect:
                # Too tall, crop top and bottom
                new_height = int(img.size[0] / target_aspect)
                top = (img.size[1] - new_height) // 2
                img = img.crop((0, top, img.size[0], top + new_height))

            # Resize to exactly 760x400
            img = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
            img.save(filepath, "JPEG", quality=90)

        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

        print(f"   ✅ Downloaded and standardized: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(
            f"   ❌ Failed downloading/processing {url}: {e}", file=sys.stderr
        )
        return False


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python3 image_downloader.py <slug-name>", file=sys.stderr
        )
        sys.exit(1)

    slug = sys.argv[1]
    research_dir = f".bob/tmp/blog-research/{slug}"
    notes_path = os.path.join(research_dir, "notes.md")
    images_dir = os.path.join(research_dir, "images")

    os.makedirs(images_dir, exist_ok=True)

    print(f"🔍 Parsing image URLs from: {notes_path}")
    urls = parse_image_urls(notes_path)

    if not urls:
        print(
            "⚠️ No candidate image URLs found in notes.md table.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"📥 Found {len(urls)} image URLs. Downloading and cropping...")
    for index, url in enumerate(urls, 1):
        filepath = os.path.join(images_dir, f"hero_{index}.jpg")
        download_and_standardize(url, filepath)

    print("🎉 Image downloader task complete!")


if __name__ == "__main__":
    main()
