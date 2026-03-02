#!/usr/bin/env python3
"""Nancy Universe — Generate hero images for 14 new adult toy products.
Uses Gemini 2.5 Flash image generation API."""

import json
import base64
import os
import time
import urllib.request
import urllib.error
import ssl

# Fix macOS Python SSL certificate issue
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "assets", "products")

# Load .env file if present
env_file = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("ERROR: Set GEMINI_API_KEY environment variable or add it to .env file")
    exit(1)

MODEL = "gemini-2.5-flash-image"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"


def generate_image(prompt, output_path, retries=5):
    """Call Gemini API to generate an image and save it."""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120, context=ssl_ctx) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            candidates = result.get("candidates", [])
            if not candidates:
                print(f"  [WARN] No candidates in response (attempt {attempt + 1}/{retries})")
                if attempt < retries - 1:
                    time.sleep(5)
                    continue
                return False

            parts = candidates[0].get("content", {}).get("parts", [])
            for part in parts:
                if "inlineData" in part:
                    img_data = base64.b64decode(part["inlineData"]["data"])
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(img_data)
                    size_kb = len(img_data) / 1024
                    print(f"  [OK] Saved {os.path.basename(output_path)} ({size_kb:.0f} KB)")
                    return True

            print(f"  [WARN] No image data in response parts (attempt {attempt + 1}/{retries})")
            if attempt < retries - 1:
                time.sleep(5)
                continue
            return False

        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            print(f"  [ERR] HTTP {e.code}: {body[:300]}")
            if e.code == 429:
                wait = 15 * (attempt + 1)
                print(f"  [WAIT] Rate limited, waiting {wait}s...")
                time.sleep(wait)
            elif attempt < retries - 1:
                time.sleep(5)
            else:
                return False
        except Exception as e:
            print(f"  [ERR] {e}")
            if attempt < retries - 1:
                time.sleep(5)
            else:
                return False

    return False


# ═══════════════════════════════════════════════════════════
# 14 NEW ADULT TOY PRODUCTS
# ═══════════════════════════════════════════════════════════

PRODUCTS = [
    {
        "slug": "mango",
        "prompt": "Professional product photography of a cute kawaii mango-shaped adult wellness device. Warm sunset orange gradient color. Smooth matte medical-grade silicone surface. Small round suction nozzle at top. Organic rounded mango shape, palm-sized. Clean white background with soft shadow. Studio lighting. No text. No buttons visible."
    },
    {
        "slug": "fig",
        "prompt": "Professional product photography of a cute kawaii fig-shaped smart kegel trainer device. Deep purple with pink accents. Smooth medical-grade silicone. Egg-shaped with a thin retrieval cord. Clean white background with soft shadow. Studio lighting. Minimalist. No text."
    },
    {
        "slug": "cherry",
        "prompt": "Professional product photography of a pair of cute cherry-shaped adult wellness devices. Deep red color, two matching round pieces connected by a green stem accent. Smooth matte silicone. Clean white background with soft shadow. Studio lighting. No text."
    },
    {
        "slug": "plum",
        "prompt": "Professional product photography of a cute kawaii plum-shaped wellness device. Deep plum purple with lavender gradient. Flat smooth pebble shape. Matte medical-grade silicone. Rounded and palm-sized. Clean white background with soft shadow. Studio lighting. No text."
    },
    {
        "slug": "coconut",
        "prompt": "Professional product photography of a cute kawaii coconut-shaped premium adult wellness device. Creamy white color with brown accents. Smooth matte silicone with a small air-pulse nozzle opening. Rounded organic shape. Clean white background with soft shadow. Studio lighting. Premium feel. No text."
    },
    {
        "slug": "grape",
        "prompt": "Professional product photography of a cute kawaii grape-cluster-shaped tiny wearable wellness device. Purple color with a small magnetic clip. Very compact, smaller than a thumb. Smooth matte silicone. Clean white background with soft shadow. Studio lighting. Minimalist. No text."
    },
    {
        "slug": "peach",
        "prompt": "Professional product photography of a cute kawaii peach-shaped squeezable adult wellness device. Soft peach pink color, slightly translucent silicone. Organic peach shape with a subtle crease. No buttons anywhere, completely smooth. Palm-sized. Clean white background with soft shadow. Studio lighting. No text."
    },
    {
        "slug": "melon",
        "prompt": "Professional product photography of a cute kawaii compact honeydew melon-shaped wand massager. Honeydew green with white accents. Small and travel-friendly, about 5 inches long. Rounded head. Matte silicone. Clean white background with soft shadow. Studio lighting. No text."
    },
    {
        "slug": "dragonfruit",
        "prompt": "Professional product photography of a cute kawaii dragonfruit-shaped adult wellness device with a suction cup base. Hot pink with white speckle pattern. The device has a round suction cup at the bottom for mounting. Air-pulse nozzle at top. Clean white background with soft shadow. Studio lighting. No text."
    },
    {
        "slug": "seed",
        "prompt": "Professional product photography of a premium gift box containing 4 miniature colorful fruit-shaped adult wellness devices. Pastel macaron-style packaging. Box is open showing a yellow mini lemon, pink mini peach, rainbow mini lollipop, and green mini avocado device nested in compartments. Clean white background. Studio lighting. Luxurious gifting feel. No text."
    },
    {
        "slug": "fizz",
        "prompt": "Professional product photography of three colorful fruit-shaped bath bombs (lemon yellow, strawberry pink, peach orange) arranged together. Effervescent and sparkling. One is partially dissolved revealing a small metallic bullet device inside. Clean white background with soft shadow. Studio lighting. Self-care aesthetic. No text."
    },
    {
        "slug": "stem",
        "prompt": "Professional product photography of an elegant cherry-shaped pendant necklace that is also an adult wellness device. Rose gold metal chain with a cherry-red enamel pendant. Jewelry box in background. Clean white background with soft shadow. Studio lighting. Luxurious jewelry aesthetic. No text."
    },
    {
        "slug": "berry-set",
        "prompt": "Professional product photography of a set of three graduated pastel-colored silicone anal training plugs. Light pink to deep berry gradient, smallest to largest. Rounded shapes with flared safety bases and T-bar handles. Medical-grade silicone, smooth matte finish. Clean white background with soft shadow. Studio lighting. Welcoming, non-clinical aesthetic. No text."
    },
    {
        "slug": "cozy",
        "prompt": "Professional product photography of a cute kawaii 7-inch lemon-shaped plush stuffed toy sitting on a white surface. The plush has a hidden pocket partially open revealing a small metallic bullet vibrator device inside. Soft yellow fabric, smiling face embroidered. Clean white background with soft shadow. Studio lighting. Cute and playful. No text."
    },
]


def main():
    total = len(PRODUCTS)
    success = 0
    skipped = 0
    failed = 0

    print("=" * 60)
    print(f"NANCY UNIVERSE — Generating Adult Toy Hero Images")
    print(f"{total} products x 1 hero image = {total} images")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, product in enumerate(PRODUCTS, 1):
        slug = product["slug"]
        prompt = product["prompt"]
        out_file = os.path.join(OUTPUT_DIR, f"{slug}-hero.png")

        if os.path.exists(out_file):
            print(f"\n[{i}/{total}] [SKIP] {slug}-hero.png already exists")
            skipped += 1
            continue

        print(f"\n[{i}/{total}] [GEN] {slug}-hero.png")
        result = generate_image(prompt, out_file)

        if result:
            success += 1
        else:
            failed += 1

        # Rate limit spacing between API calls
        if i < total:
            print(f"  [WAIT] 8s cooldown...")
            time.sleep(8)

    print("\n" + "=" * 60)
    print(f"DONE — {success} generated, {skipped} skipped, {failed} failed (of {total} total)")
    print("=" * 60)


if __name__ == "__main__":
    main()
