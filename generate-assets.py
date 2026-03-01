#!/usr/bin/env python3
"""Nancy Universe — Gemini API Image Generator (Nano Banana 2)
Generates product images for plushies and fashion items via Gemini 2.0 Flash."""

import json
import base64
import os
import sys
import time
import urllib.request
import urllib.error
import ssl

# Fix macOS Python SSL certificate issue
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

API_KEY = "AIzaSyCrUHz0oQ8V9EAMiqA6KMXzTMA_IFjiKP8"
MODEL = "gemini-2.0-flash-exp-image-generation"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_image(prompt, output_path, retries=2):
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

    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=120, context=ssl_ctx) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            # Extract image from response
            candidates = result.get("candidates", [])
            if not candidates:
                print(f"  [WARN] No candidates in response for {output_path}")
                if attempt < retries:
                    time.sleep(2)
                    continue
                return False

            parts = candidates[0].get("content", {}).get("parts", [])
            for part in parts:
                if "inlineData" in part:
                    img_data = base64.b64decode(part["inlineData"]["data"])
                    mime = part["inlineData"].get("mimeType", "image/png")
                    ext = ".png" if "png" in mime else ".jpg" if "jpeg" in mime or "jpg" in mime else ".webp"

                    # Ensure directory exists
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)

                    # If output_path doesn't have right extension, adjust
                    if not output_path.endswith(ext) and not output_path.endswith(".png"):
                        output_path = os.path.splitext(output_path)[0] + ext

                    with open(output_path, "wb") as f:
                        f.write(img_data)
                    size_kb = len(img_data) / 1024
                    print(f"  [OK] Saved {output_path} ({size_kb:.0f} KB)")
                    return True

            print(f"  [WARN] No image data in response parts for {output_path}")
            if attempt < retries:
                time.sleep(2)
                continue
            return False

        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            print(f"  [ERR] HTTP {e.code}: {body[:200]}")
            if e.code == 429:
                wait = 15 * (attempt + 1)
                print(f"  [WAIT] Rate limited, waiting {wait}s...")
                time.sleep(wait)
            elif attempt < retries:
                time.sleep(3)
            else:
                return False
        except Exception as e:
            print(f"  [ERR] {e}")
            if attempt < retries:
                time.sleep(3)
            else:
                return False

    return False


# ═══════════════════════════════════════════════
# PRODUCT DEFINITIONS
# ═══════════════════════════════════════════════

PLUSHIES = [
    # Existing 5
    {"name": "Lem", "fruit": "lemon", "color": "bright yellow", "emoji": "🍋", "personality": "bold and sunny"},
    {"name": "Berri", "fruit": "strawberry", "color": "pink-red", "emoji": "🍓", "personality": "sweet and fierce"},
    {"name": "Avo", "fruit": "avocado", "color": "sage green", "emoji": "🥑", "personality": "calm and grounding"},
    {"name": "Pixie", "fruit": "grape bunch", "color": "purple", "emoji": "🍇", "personality": "mischievous and playful"},
    {"name": "Lolly", "fruit": "lollipop", "color": "orange and rainbow swirl", "emoji": "🍭", "personality": "bubbly and sweet"},
    # New 10
    {"name": "Mango", "fruit": "mango", "color": "golden orange-yellow", "emoji": "🥭", "personality": "tropical and adventurous"},
    {"name": "Kiwi", "fruit": "kiwi fruit", "color": "fuzzy brown outside, bright green inside", "emoji": "🥝", "personality": "quirky and surprising"},
    {"name": "Peachy", "fruit": "peach", "color": "soft blush pink-orange", "emoji": "🍑", "personality": "warm and affectionate"},
    {"name": "Coco", "fruit": "coconut", "color": "brown and white", "emoji": "🥥", "personality": "tough on outside, sweet inside"},
    {"name": "Cherry", "fruit": "pair of cherries", "color": "deep red with green stem", "emoji": "🍒", "personality": "inseparable best friends (twin)"},
    {"name": "Melon", "fruit": "watermelon slice", "color": "green rind with pink-red inside", "emoji": "🍉", "personality": "refreshing and laid-back"},
    {"name": "Figgy", "fruit": "fig", "color": "deep purple-brown", "emoji": "🫐", "personality": "wise and mysterious"},
    {"name": "Plummy", "fruit": "plum", "color": "deep indigo-purple", "emoji": "🫐", "personality": "elegant and sophisticated"},
    {"name": "Papaya", "fruit": "papaya", "color": "orange with pink-salmon center", "emoji": "🍈", "personality": "exotic and free-spirited"},
    {"name": "Guava", "fruit": "guava", "color": "green outside, pink inside", "emoji": "🍏", "personality": "vibrant and energetic"},
]

FASHION = [
    {"name": "Fruit Club Tee", "slug": "fruit-club-tee", "type": "t-shirt", "color": "white", "design": "small 'Fruit Club' text logo with tiny fruit icons on chest"},
    {"name": "Lem Graphic Tee", "slug": "lem-graphic-tee", "type": "t-shirt", "color": "pale yellow", "design": "large Lem character illustration on front"},
    {"name": "Berri Crop Top", "slug": "berri-crop-top", "type": "crop top", "color": "pink", "design": "small embroidered strawberry on chest, cropped fit"},
    {"name": "Avo Hoodie", "slug": "avo-hoodie", "type": "oversized hoodie", "color": "sage green", "design": "embroidered avocado character on chest, kangaroo pocket"},
    {"name": "Squad Goals Sweatshirt", "slug": "squad-sweatshirt", "type": "crewneck sweatshirt", "color": "cream/off-white", "design": "all 5 original fruit characters in a row across chest"},
    {"name": "Pixie Bucket Hat", "slug": "pixie-bucket-hat", "type": "bucket hat", "color": "lavender purple", "design": "small embroidered grape character on front, short brim"},
    {"name": "Lolly Socks Set", "slug": "lolly-socks-set", "type": "crew socks 3-pack", "color": "multicolor — pink, yellow, green pairs", "design": "each pair has a different fruit character knitted into the ankle"},
    {"name": "Nancy Logo Cap", "slug": "nancy-logo-cap", "type": "dad cap / baseball cap", "color": "black", "design": "embroidered Nancy logo in pink on front, adjustable strap"},
    {"name": "Tropical Shorts", "slug": "tropical-shorts", "type": "casual shorts", "color": "pastel tie-dye (pink, yellow, green)", "design": "all-over fruit pattern print, elastic waist, relaxed fit"},
    {"name": "Fruit Tote Bag", "slug": "fruit-tote-bag", "type": "canvas tote bag", "color": "natural canvas / cream", "design": "printed fruit characters scattered across bag, cotton handles"},
]


def generate_plush_images(plushies, shot_types=None):
    """Generate product images for each plush character."""
    if shot_types is None:
        shot_types = ["hero"]  # Start with hero shots

    for plush in plushies:
        name = plush["name"]
        slug = name.lower()
        fruit = plush["fruit"]
        color = plush["color"]
        personality = plush["personality"]

        out_dir = os.path.join(BASE_DIR, "assets", "plushies", slug)
        os.makedirs(out_dir, exist_ok=True)

        for shot in shot_types:
            out_file = os.path.join(out_dir, f"{slug}-{shot}.png")
            if os.path.exists(out_file):
                print(f"  [SKIP] {out_file} already exists")
                continue

            if shot == "hero":
                prompt = f"""Create a professional e-commerce product photograph of a kawaii {fruit} plush toy on a pure white background. The plush is {color}, about 25cm tall, with a cute round shape, tiny arms and legs, and an adorable embroidered smiling face with rosy cheeks. It's made of super-soft plush fabric with visible soft texture. The character's name is {name} and it has a {personality} personality — the expression should reflect this. Clean, centered composition with soft even studio lighting and a subtle shadow underneath. High-resolution, sharp focus on fabric texture. Premium toy brand product photography style."""
            elif shot == "lifestyle-bed":
                prompt = f"""Create a cozy lifestyle photograph of a kawaii {color} {fruit} plush toy sitting on a neatly made bed with white linen sheets and cream pillows. Morning sunlight streaming through a window. The plush has a cute embroidered smiling face. Warm, aspirational bedroom setting. The plush is about 25cm tall. Editorial lifestyle photography, warm tones, soft focus background."""
            elif shot == "lifestyle-desk":
                prompt = f"""Create a lifestyle photograph of a kawaii {color} {fruit} plush toy sitting on a clean modern desk. Surrounded by a small plant, a candle, and a coffee mug. Scandinavian minimal aesthetic. Soft natural side lighting. The plush adds personality to a grown-up space. Warm tones, shallow depth of field."""
            elif shot == "in-hand":
                prompt = f"""Create a lifestyle photograph of feminine hands gently holding a kawaii {color} {fruit} plush toy. The plush is about 25cm tall with a cute embroidered face. Soft neutral background. Warm natural lighting. The scale should look realistic — the plush fits comfortably in two hands. Cozy, inviting feel."""
            elif shot == "flatlay":
                prompt = f"""Create an overhead flat lay photograph with a kawaii {color} {fruit} plush toy as the centerpiece. Arranged around it: dried flowers, a cute greeting card, colorful candies, and tissue paper — as if someone just received it as a gift. Soft pink background. Natural top-down lighting. Styled like a premium unboxing moment. Instagram-ready."""
            elif shot == "angle":
                prompt = f"""Create a product photograph of a kawaii {color} {fruit} plush toy turned 45 degrees to the right. White background, soft studio lighting. Show the side profile and the roundness of the body. The plush has a cute embroidered face, tiny arms, about 25cm tall. Clean e-commerce product photography."""
            else:
                continue

            print(f"\n[GEN] {name} — {shot}")
            generate_image(prompt, out_file)
            time.sleep(2)  # Rate limit spacing


def generate_fashion_images(items):
    """Generate product images for each fashion item."""
    for item in items:
        name = item["name"]
        slug = item["slug"]
        item_type = item["type"]
        color = item["color"]
        design = item["design"]

        out_dir = os.path.join(BASE_DIR, "assets", "fashion", slug)
        os.makedirs(out_dir, exist_ok=True)

        out_file = os.path.join(out_dir, f"{slug}-hero.png")
        if os.path.exists(out_file):
            print(f"  [SKIP] {out_file} already exists")
            continue

        prompt = f"""Create a clean, professional flat lay product photograph of a {color} {item_type} on a pure white background. The item has {design}. It's laid neatly showing the full front design. Soft overhead studio lighting, no harsh shadows. The style is modern streetwear meets cute — premium quality like a Shopify product listing for a trendy Gen-Z fashion brand called Nancy. High-resolution, sharp details on fabric texture and any prints/embroidery."""

        print(f"\n[GEN] Fashion: {name}")
        generate_image(prompt, out_file)
        time.sleep(2)


def generate_fashion_lifestyle(items):
    """Generate lifestyle/detail images for each fashion item."""
    shot_types = ["flatlay", "model-front", "detail", "lifestyle-street", "lifestyle"]

    for item in items:
        name = item["name"]
        slug = item["slug"]
        item_type = item["type"]
        color = item["color"]
        design = item["design"]

        out_dir = os.path.join(BASE_DIR, "assets", "fashion", slug)
        os.makedirs(out_dir, exist_ok=True)

        for shot in shot_types:
            out_file = os.path.join(out_dir, f"{slug}-{shot}.png")
            if os.path.exists(out_file):
                print(f"  [SKIP] {out_file} already exists")
                continue

            if shot == "flatlay":
                prompt = f"""Create a styled flat lay photograph of a {color} {item_type} arranged neatly with accessories — sunglasses, a coffee cup, a phone, and a small plant. The {item_type} has {design}. Shot from directly above on a light wooden surface. Warm natural lighting. Lifestyle editorial for a Gen-Z fashion brand. Instagram-ready styling."""
            elif shot == "model-front":
                prompt = f"""Create a fashion editorial photograph of a young woman (mid-20s, natural look) wearing a {color} {item_type} with {design}. She's standing against a simple warm cream studio background, relaxed natural pose. The {item_type} fits oversized/relaxed. Soft warm lighting. Modern streetwear brand photography. Focus on the fit and design."""
            elif shot == "detail":
                prompt = f"""Create a macro close-up photograph of the {item_type}'s main design detail — {design}. Tight crop showing fabric texture, any print quality or embroidery stitching. Sharp focus. Warm soft lighting. Premium quality craftsmanship feel. The fabric is {color}."""
            elif shot == "lifestyle-street":
                prompt = f"""Create a street-style photograph of a young woman wearing the {color} {item_type} with {design}, paired with casual bottoms and white sneakers. Urban setting — sunny sidewalk, coffee shop, or minimal mural background. Natural daylight. Candid feel, like a real street-style blog photo. Vibrant but natural colors."""
            elif shot == "lifestyle":
                prompt = f"""Create a cozy lifestyle photograph of someone wearing the {color} {item_type} with {design} while relaxing at home — sitting on a couch or at a kitchen counter with a coffee. Warm interior with natural window light. Relaxed, aspirational weekend-at-home vibe. Soft focus background."""
            else:
                continue

            print(f"\n[GEN] Fashion: {name} — {shot}")
            generate_image(prompt, out_file)
            time.sleep(2)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("plush", "plushies", "all"):
        print("\n" + "=" * 60)
        print("GENERATING PLUSH HERO IMAGES")
        print("=" * 60)
        # Generate hero shots for all 15 plushies
        generate_plush_images(PLUSHIES, shot_types=["hero"])

    if mode in ("plush-lifestyle", "all-lifestyle"):
        print("\n" + "=" * 60)
        print("GENERATING PLUSH LIFESTYLE IMAGES")
        print("=" * 60)
        generate_plush_images(PLUSHIES, shot_types=["lifestyle-bed", "lifestyle-desk", "in-hand", "flatlay", "angle"])

    if mode in ("fashion", "all"):
        print("\n" + "=" * 60)
        print("GENERATING FASHION HERO IMAGES")
        print("=" * 60)
        generate_fashion_images(FASHION)

    if mode in ("fashion-lifestyle", "all-lifestyle"):
        print("\n" + "=" * 60)
        print("GENERATING FASHION LIFESTYLE IMAGES")
        print("=" * 60)
        generate_fashion_lifestyle(FASHION)

    print("\n[DONE] Image generation complete.")
