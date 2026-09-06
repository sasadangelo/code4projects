#!/usr/bin/env python3
"""
generate_ai_image.py — Generate AI images for a blog post using Gemini REST API.

Generates:
  - 1 hero image  (saved as ai_hero.jpg)
  - 3 content images (saved as ai_content_1.jpg, ai_content_2.jpg, ai_content_3.jpg)

All images are center-cropped and resized to exactly 760x400 px.

Requires:
  - GOOGLE_AI_API_KEY environment variable (free tier at https://aistudio.google.com/apikey)
  - Pillow:  pip install pillow
  - requests: pip install requests

Usage:
  python3 .bob/skills/blog-research/generate_ai_image.py <slug> "<topic>" "<hero_prompt>" "<content_prompt_1>" "<content_prompt_2>" "<content_prompt_3>"

Example:
  python3 .bob/skills/blog-research/generate_ai_image.py \
    understanding-mcp-protocol \
    "Understanding MCP Protocol" \
    "A photorealistic editorial hero image showing AI agents connected by glowing network lines in a futuristic server room, 16:9, blog cover" \
    "A clean technical diagram of the MCP request-response cycle with labeled components, flat illustration style" \
    "A developer working at a terminal with MCP tool calls visualized as floating panels, editorial style" \
    "An infographic showing the three MCP primitives: tools, resources, and prompts, with icons, minimal clean design"
"""

import base64
import io
import json
import os
import sys

import requests
from PIL import Image

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, fall back to os.environ only

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"
TARGET_SIZE = (760, 400)


def get_api_key() -> str:
    key = os.environ.get("GOOGLE_AI_API_KEY", "").strip()
    if not key:
        print("❌ GOOGLE_AI_API_KEY is not set.", file=sys.stderr)
        print("   Get a free key at: https://aistudio.google.com/apikey", file=sys.stderr)
        sys.exit(1)
    return key


def generate_image(prompt: str, api_key: str) -> bytes:
    """Call Gemini REST API and return raw PNG bytes."""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    response = requests.post(
        API_URL,
        headers={"Content-Type": "application/json"},
        params={"key": api_key},
        json=payload,
        timeout=120,
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"Gemini API error {response.status_code}: {response.text[:300]}"
        )
    data = response.json()
    try:
        b64 = data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Unexpected response structure: {json.dumps(data)[:400]}") from exc
    return base64.b64decode(b64)


def save_standardized(image_bytes: bytes, filepath: str) -> None:
    """Center-crop and resize to 760x400, save as JPEG."""
    with Image.open(io.BytesIO(image_bytes)) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        target_aspect = TARGET_SIZE[0] / TARGET_SIZE[1]
        img_aspect = img.width / img.height
        if img_aspect > target_aspect:
            new_width = int(img.height * target_aspect)
            left = (img.width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img.height))
        elif img_aspect < target_aspect:
            new_height = int(img.width / target_aspect)
            top = (img.height - new_height) // 2
            img = img.crop((0, top, img.width, top + new_height))
        img = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
        img.save(filepath, "JPEG", quality=90)


def main() -> None:
    if len(sys.argv) != 7:
        print(__doc__)
        sys.exit(1)

    slug = sys.argv[1]
    _topic = sys.argv[2]
    hero_prompt = sys.argv[3]
    content_prompts = [sys.argv[4], sys.argv[5], sys.argv[6]]

    images_dir = f".bob/tmp/blog-research/{slug}/images"
    os.makedirs(images_dir, exist_ok=True)

    api_key = get_api_key()

    jobs = [
        ("hero", f"{images_dir}/ai_hero.jpg", hero_prompt),
        ("content_1", f"{images_dir}/ai_content_1.jpg", content_prompts[0]),
        ("content_2", f"{images_dir}/ai_content_2.jpg", content_prompts[1]),
        ("content_3", f"{images_dir}/ai_content_3.jpg", content_prompts[2]),
    ]

    for label, filepath, prompt in jobs:
        print(f"🎨 Generating {label}...")
        try:
            raw = generate_image(prompt, api_key)
            save_standardized(raw, filepath)
            print(f"   ✅ Saved: {filepath}")
        except Exception as exc:
            print(f"   ❌ Failed ({label}): {exc}", file=sys.stderr)

    print("🎉 AI image generation complete!")


if __name__ == "__main__":
    main()
