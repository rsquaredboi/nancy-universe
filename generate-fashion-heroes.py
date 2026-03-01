#!/usr/bin/env python3
"""Nancy Universe — Generate hero images for all 100 fashion items.
Uses Gemini 2.0 Flash image generation API."""

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

                    os.makedirs(os.path.dirname(output_path), exist_ok=True)

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


# ═══════════════════════════════════════════════════════════
# ALL 100 FASHION ITEMS
# ═══════════════════════════════════════════════════════════

FASHION_ITEMS = [
    # ── Tees & Tops (25) ──
    {"name": "Fruit Club Tee", "slug": "fruit-club-tee", "type": "white t-shirt", "design": "small 'Fruit Club' text logo with tiny fruit icons on chest"},
    {"name": "Lem Graphic Tee", "slug": "lem-graphic-tee", "type": "pale yellow graphic t-shirt", "design": "large kawaii lemon character illustration on the front"},
    {"name": "Berri Crop Top", "slug": "berri-crop-top", "type": "pink cropped t-shirt", "design": "embroidered strawberry on chest, boxy cropped fit"},
    {"name": "Squad Goals Tee", "slug": "squad-goals-tee", "type": "white graphic t-shirt", "design": "five cute fruit characters in a row across the chest"},
    {"name": "Emotionally Attached Tee", "slug": "emotionally-attached-tee", "type": "off-white t-shirt", "design": "back print reading 'Emotionally Attached to a Plush Toy' in elegant serif font"},
    {"name": "Chaos Fairy Tee", "slug": "chaos-fairy-tee", "type": "black graphic t-shirt", "design": "pixie fairy illustration with 'Chaos' in gothic dripping font"},
    {"name": "404 Not Found Tee", "slug": "404-not-found-tee", "type": "dark grey t-shirt", "design": "glitched distorted text reading '404: Feelings Not Found'"},
    {"name": "Nugget Appreciation Tee", "slug": "nugget-appreciation-tee", "type": "golden yellow t-shirt", "design": "cute chicken nugget character with 'Emotional Support Nugget' text"},
    {"name": "Void Tee", "slug": "void-tee", "type": "all black minimal t-shirt", "design": "tiny white 'Void' text embroidered on chest, very minimal"},
    {"name": "Delulu Manifesting Tee", "slug": "delulu-manifesting-tee", "type": "light pink t-shirt", "design": "'Delulu is the Solulu' in handwritten cursive script"},
    {"name": "Avo Cropped Tank", "slug": "avo-cropped-tank", "type": "sage green ribbed cropped tank top", "design": "small avocado embroidery on left chest"},
    {"name": "Boba Ringer Tee", "slug": "boba-ringer-tee", "type": "white ringer t-shirt with brown trim", "design": "cute boba tea character on front, contrast collar and sleeve trim"},
    {"name": "Space Squad Tee", "slug": "space-squad-tee", "type": "navy blue graphic t-shirt", "design": "cosmic characters arranged in constellation map pattern with glow details"},
    {"name": "Feelings Forecast Tee", "slug": "feelings-forecast-tee", "type": "light blue t-shirt", "design": "weather emoji characters with 'Today\\'s Forecast: Chaotic' text"},
    {"name": "NPC Mode Tee", "slug": "npc-mode-tee", "type": "grey t-shirt", "design": "'NPC Mode: Activated' in retro pixel font"},
    {"name": "Moth to a Flame Tank", "slug": "moth-flame-tank", "type": "brown tank top", "design": "cute mothman character illustration with 'Drawn to Your Light' text"},
    {"name": "Dragon Energy Tee", "slug": "dragon-energy-tee", "type": "emerald green t-shirt", "design": "baby dragon breathing fire with 'Tiny but Mighty' text"},
    {"name": "Unhinged & Thriving Tee", "slug": "unhinged-thriving-tee", "type": "orange t-shirt", "design": "spinning spiral eyes graphic with 'Unhinged & Thriving' bold text"},
    {"name": "Cinnamon Roll Tee", "slug": "cinnamon-roll-tee", "type": "warm cream t-shirt", "design": "cute cinnamon roll character with 'Too Pure for This World' text"},
    {"name": "Serotonin Dealer Tee", "slug": "serotonin-dealer-tee", "type": "golden yellow t-shirt", "design": "golden glow orb graphic with 'Serotonin Dealer' in metallic print"},
    {"name": "Cryptid Club Tee", "slug": "cryptid-club-tee", "type": "forest green t-shirt", "design": "Yeti, Nessie, and Mothman lineup in vintage illustration style with 'Believe'"},
    {"name": "Jellyfish Mesh Top", "slug": "jellyfish-mesh-top", "type": "iridescent sheer mesh top", "design": "iridescent jellyfish print on semi-transparent mesh fabric"},
    {"name": "Main Character Tee", "slug": "main-character-tee", "type": "bright orange t-shirt", "design": "spotlight beam graphic with 'Supporting Characters DNI' text"},
    {"name": "Axolotl Smile Tee", "slug": "axolotl-smile-tee", "type": "pastel pink t-shirt", "design": "large axolotl face filling the front with 'Smile Through It' text"},
    {"name": "Reverse Crop", "slug": "reverse-crop", "type": "inside-out pink crop top", "design": "exposed seams and raw edges, Reverse character print"},

    # ── Hoodies & Sweatshirts (20) ──
    {"name": "Avo Hoodie", "slug": "avo-hoodie", "type": "sage green oversized hoodie", "design": "embroidered avocado character on chest, kangaroo pocket"},
    {"name": "Chaos Hoodie", "slug": "chaos-hoodie", "type": "red oversized hoodie", "design": "'Chaos' in dripping text on back, scribble yarn character on chest pocket"},
    {"name": "Void Hoodie", "slug": "void-hoodie", "type": "all black heavyweight hoodie", "design": "glow-in-the-dark Void character printed on the back"},
    {"name": "Nebula Hoodie", "slug": "nebula-hoodie", "type": "purple and pink tie-dye hoodie", "design": "nebula cosmic tie-dye pattern with embroidered space character"},
    {"name": "Cozy Era Crewneck", "slug": "cozy-era-crewneck", "type": "cream crewneck sweatshirt", "design": "'Entering My Cozy Era' in varsity athletic font"},
    {"name": "Cryptid Crewneck", "slug": "cryptid-crewneck", "type": "dark green crewneck sweatshirt", "design": "all cryptid characters (yeti, nessie, mothman) in vintage illustration style"},
    {"name": "Glitch Hoodie", "slug": "glitch-hoodie", "type": "black and neon green hoodie", "design": "distorted glitched Nancy logo with pixelated artifacts"},
    {"name": "Mushroom Hoodie", "slug": "mushroom-hoodie", "type": "brown oversized hoodie", "design": "cottage core mushroom village illustration on the back, earth tones"},
    {"name": "Weather Report Crewneck", "slug": "weather-report-crewneck", "type": "light blue crewneck sweatshirt", "design": "all weather characters arranged in a forecast layout grid"},
    {"name": "Espresso Yourself Hoodie", "slug": "espresso-yourself-hoodie", "type": "coffee brown hoodie", "design": "'Espresso Yourself' text with cute coffee cup characters"},
    {"name": "Dragon Fire Hoodie", "slug": "dragon-fire-hoodie", "type": "dark red hoodie", "design": "baby dragon breathing fire on the back, 'Handle With Care' text"},
    {"name": "Eclipse Half-Zip", "slug": "eclipse-half-zip", "type": "half-zip pullover split black and white", "design": "left half black, right half white, eclipse character embroidered"},
    {"name": "Emotional Baggage Hoodie", "slug": "emotional-baggage-hoodie", "type": "grey oversized hoodie", "design": "suitcase illustration filled with cute feeling characters"},
    {"name": "Feral Hours Crewneck", "slug": "feral-hours-crewneck", "type": "dark grey crewneck sweatshirt", "design": "'Feral Hours: 12am-5am' in scratchy distressed font"},
    {"name": "Capybara Zen Hoodie", "slug": "capybara-zen-hoodie", "type": "warm brown oversized hoodie", "design": "capybara in hot spring on front, 'Unbothered' on the back"},
    {"name": "Static Noise Hoodie", "slug": "static-noise-hoodie", "type": "grey and white all-over print hoodie", "design": "TV static all-over print pattern with small Static character"},
    {"name": "Phoenix Rising Crewneck", "slug": "phoenix-rising-crewneck", "type": "orange-red crewneck sweatshirt", "design": "phoenix illustration in flame gradient, 'Burn it Down. Rise Up.'"},
    {"name": "Matcha State of Mind", "slug": "matcha-state-of-mind", "type": "matcha green hoodie", "design": "'Calm but Caffeinated' embroidered text"},
    {"name": "Deja Vu Crewneck", "slug": "deja-vu-crewneck", "type": "lavender crewneck sweatshirt", "design": "same design printed twice overlapping deliberately, double-vision effect"},
    {"name": "Rizz Academy Hoodie", "slug": "rizz-academy-hoodie", "type": "navy blue varsity hoodie", "design": "'Rizz Academy Est. 2024' in collegiate font with chenille patch"},

    # ── Bottoms (10) ──
    {"name": "Tropical Shorts", "slug": "tropical-shorts", "type": "pastel tie-dye casual shorts", "design": "all-over fruit pattern print on pink, yellow, green tie-dye base"},
    {"name": "Chaos Sweats", "slug": "chaos-sweats", "type": "black jogger sweatpants", "design": "'Chaos' text running down the leg with splatter paint accents"},
    {"name": "Cosmic Sweats", "slug": "cosmic-sweats", "type": "dark navy jogger sweatpants", "design": "galaxy print panels on sides with embroidered star details"},
    {"name": "NPC Cargo Pants", "slug": "npc-cargo-pants", "type": "grey cargo pants", "design": "pixel art patches on cargo pockets, 'Quest Accepted' label"},
    {"name": "Jellyfish Mesh Shorts", "slug": "jellyfish-mesh-shorts", "type": "iridescent mesh basketball shorts", "design": "iridescent jellyfish print pattern on mesh fabric"},
    {"name": "Dragon Scale Leggings", "slug": "dragon-scale-leggings", "type": "emerald green leggings", "design": "scale texture pattern across fabric, tiny dragon on waistband"},
    {"name": "Feral Sweatpants", "slug": "feral-sweatpants", "type": "dark grey sweatpants", "design": "'Do Not Disturb: Feral' text on thigh, elastic cuffs"},
    {"name": "Mushroom Pajama Pants", "slug": "mushroom-pajama-pants", "type": "cozy flannel pajama pants", "design": "all-over mushroom village print pattern on cream flannel"},
    {"name": "Boba Float Skirt", "slug": "boba-float-skirt", "type": "pleated mini skirt", "design": "boba pearl print on brown pleated fabric"},
    {"name": "Eclipse Split Shorts", "slug": "eclipse-split-shorts", "type": "split-color cotton shorts", "design": "left leg entirely black, right leg entirely white"},

    # ── Headwear (10) ──
    {"name": "Pixie Bucket Hat", "slug": "pixie-bucket-hat", "type": "lavender purple bucket hat", "design": "embroidered grape character on the front panel"},
    {"name": "Nancy Logo Cap", "slug": "nancy-logo-cap", "type": "black dad cap baseball hat", "design": "pink Nancy logo embroidered on front, adjustable back strap"},
    {"name": "Void Beanie", "slug": "void-beanie", "type": "all black knit beanie", "design": "tiny 'Void' woven patch, double-layer cuff style"},
    {"name": "Chaos Bucket Hat", "slug": "chaos-bucket-hat", "type": "multicolor bucket hat", "design": "splatter paint pattern with 'Chaos' woven label"},
    {"name": "Mushroom Beret", "slug": "mushroom-beret", "type": "red wool beret", "design": "red with white spots mimicking a mushroom cap"},
    {"name": "Dragon Horns Beanie", "slug": "dragon-horns-beanie", "type": "green knit beanie", "design": "3D knitted dragon horn details protruding from top"},
    {"name": "Boba Trucker Hat", "slug": "boba-trucker-hat", "type": "trucker hat with mesh back", "design": "cute boba tea character woven patch on cotton front, mesh back"},
    {"name": "Feral Headband", "slug": "feral-headband", "type": "cotton stretch headband", "design": "raccoon ear details with 'Feral' embroidered"},
    {"name": "Axolotl Ear Flap Hat", "slug": "axolotl-ear-flap-hat", "type": "pink winter hat with ear flaps", "design": "pink gradient with axolotl gill-shaped ear flaps"},
    {"name": "Nebula Bucket Hat", "slug": "nebula-bucket-hat", "type": "purple/pink tie-dye bucket hat", "design": "cosmic tie-dye pattern with small space characters printed"},

    # ── Accessories (20) ──
    {"name": "Fruit Tote Bag", "slug": "fruit-tote-bag", "type": "natural canvas tote bag", "design": "all fruit characters scattered across the bag, cotton handles"},
    {"name": "Lolly Socks Set", "slug": "lolly-socks-set", "type": "three pairs of crew socks — pink, yellow, green", "design": "each pair has a different fruit character knitted at the ankle"},
    {"name": "Void Crossbody Bag", "slug": "void-crossbody-bag", "type": "all black mini crossbody bag", "design": "reflective Void logo, vegan leather, slim profile"},
    {"name": "Chaos Fanny Pack", "slug": "chaos-fanny-pack", "type": "nylon belt bag fanny pack", "design": "splatter paint print with multiple zip pockets"},
    {"name": "Emotional Baggage Duffle", "slug": "emotional-baggage-duffle", "type": "canvas weekender duffle bag", "design": "'Emotional Baggage' embroidered with iron-on feeling character patches"},
    {"name": "Cryptid Keychain Set", "slug": "cryptid-keychain-set", "type": "three PVC rubber keychains", "design": "mini Yeti, Nessie, and Mothman characters with lobster clasps"},
    {"name": "Dragon Enamel Pin Set", "slug": "dragon-enamel-pin-set", "type": "five gold-plated hard enamel pins", "design": "baby dragon in five different expressions — happy, angry, sleepy, love, fire"},
    {"name": "Jellyfish Phone Case", "slug": "jellyfish-phone-case", "type": "holographic iridescent phone case", "design": "jellyfish print on holographic material, slim fit"},
    {"name": "Serotonin Sticker Pack", "slug": "serotonin-sticker-pack", "type": "fifteen waterproof vinyl die-cut stickers", "design": "all feeling characters — cute expressive sticker designs"},
    {"name": "Space Squad Laptop Sleeve", "slug": "space-squad-laptop-sleeve", "type": "padded neoprene laptop sleeve", "design": "cosmic characters in constellation map pattern, fits 13-15 inch"},
    {"name": "Mushroom Canvas Pouch", "slug": "mushroom-canvas-pouch", "type": "canvas zipper pouch", "design": "cottage core mushroom village print pattern"},
    {"name": "Boba Airpods Case", "slug": "boba-airpods-case", "type": "silicone airpods case shaped like a boba cup", "design": "boba tea cup shape with straw detail, carabiner clip"},
    {"name": "NPC Name Badge Lanyard", "slug": "npc-name-badge-lanyard", "type": "polyester lanyard with ID holder", "design": "'NPC' repeated in pixel font, badge template holder"},
    {"name": "Glitch Wristband Set", "slug": "glitch-wristband-set", "type": "three silicone wristbands", "design": "pixelated text: 'Error', 'Glitch', 'Reboot' on each band"},
    {"name": "Capybara Sleep Mask", "slug": "capybara-sleep-mask", "type": "silk satin sleep mask", "design": "capybara face printed on front, 'Unbothered' on the strap"},
    {"name": "Phoenix Enamel Pin", "slug": "phoenix-enamel-pin", "type": "single gold-plated hard enamel pin", "design": "flame-gradient phoenix bird design"},
    {"name": "Axolotl Water Bottle", "slug": "axolotl-water-bottle", "type": "pink gradient stainless steel water bottle", "design": "axolotl face molded lid, pink gradient body, 500ml"},
    {"name": "Espresso Shot Glass Set", "slug": "espresso-shot-glass-set", "type": "two ceramic espresso cups", "design": "espresso character on each cup, '47 Tabs Open' text"},
    {"name": "Chaos Scarf", "slug": "chaos-scarf", "type": "multicolor knit scarf with fringe", "design": "chaotic scribble pattern in multiple colors, fringe ends"},
    {"name": "Rizz Mirror Keychain", "slug": "rizz-mirror-keychain", "type": "gold metal compact mirror keychain", "design": "'Check Your Rizz' engraved on the back, mirror inside"},

    # ── Home & Lifestyle (15) ──
    {"name": "Nancy Throw Blanket", "slug": "nancy-throw-blanket", "type": "cream fleece throw blanket", "design": "all Nancy characters scattered across in colorful pattern"},
    {"name": "Snooze Pillowcase Set", "slug": "snooze-pillowcase-set", "type": "two cotton sateen pillowcases", "design": "Snooze cloud character with 'Do Not Disturb' text"},
    {"name": "Mushroom Mug", "slug": "mushroom-mug", "type": "ceramic mug with mushroom-shaped handle", "design": "mushroom character design, handle shaped like a mushroom stem"},
    {"name": "Dragon Incense Holder", "slug": "dragon-incense-holder", "type": "ceramic incense holder shaped like a baby dragon", "design": "dragon design where incense smoke comes out of the dragon's mouth"},
    {"name": "Void Candle", "slug": "void-candle", "type": "black glass jar soy candle", "design": "black vessel with minimal 'Void' label, cedar and patchouli scent"},
    {"name": "Capybara Desk Organizer", "slug": "capybara-desk-organizer", "type": "resin desk organizer shaped like a capybara", "design": "capybara shape with pen holder opening and phone stand groove"},
    {"name": "Chill Ice Cube Tray", "slug": "chill-ice-cube-tray", "type": "blue silicone ice cube tray", "design": "ice cube molds shaped like the Chill character wearing sunglasses"},
    {"name": "Nebula Poster Set", "slug": "nebula-poster-set", "type": "three 8x10 art prints on premium cardstock", "design": "cosmic characters in galaxy scenes, nebula and star art"},
    {"name": "Feral Hours Clock", "slug": "feral-hours-clock", "type": "round wall clock", "design": "'Feral Hours' text replacing the 12-5 numbers on the clock face"},
    {"name": "Serotonin Desk Light", "slug": "serotonin-desk-light", "type": "golden orb-shaped LED desk lamp", "design": "warm glowing golden orb shape, USB-C powered, touch dimmer"},
    {"name": "Weather Mood Board", "slug": "weather-mood-board", "type": "metal magnetic board with character magnets", "design": "eight weather character magnets to set daily mood on a 30x20cm board"},
    {"name": "Emotional Baggage Tags", "slug": "emotional-baggage-tags", "type": "three PVC luggage tags", "design": "labeled 'Emotional', 'Heavy', and 'Carry-On' with ID windows"},
    {"name": "Jellyfish Night Light", "slug": "jellyfish-night-light", "type": "silicone LED night light shaped like a jellyfish", "design": "color-changing jellyfish silhouette, touch control, USB-C powered"},
    {"name": "Boba Coaster Set", "slug": "boba-coaster-set", "type": "four natural cork coasters", "design": "each coaster features a different drink character print"},
    {"name": "The Full Nancy Box", "slug": "full-nancy-box", "type": "premium gift box set", "design": "curated box containing a plush, tee, sticker pack, tote, and pin set in branded tissue paper"},
]


SHOT_TYPES = ["hero", "flatlay", "model-front", "detail", "lifestyle-street", "lifestyle"]


def build_prompt(item, shot):
    """Build prompt for a specific shot type."""
    name = item["name"]
    item_type = item["type"]
    design = item["design"]

    if shot == "hero":
        return (
            f"Create a clean, professional flat lay product photograph of a {item_type} "
            f"on a pure white background. The item features {design}. "
            f"Laid out neatly showing the full front design. Soft overhead studio lighting, "
            f"no harsh shadows. Modern streetwear meets cute kawaii style — premium product "
            f"photography for a trendy Gen-Z fashion brand called Nancy Universe. "
            f"High-resolution, sharp details on fabric texture and prints/embroidery."
        )
    elif shot == "flatlay":
        return (
            f"Create a styled flat lay photograph of a {item_type} arranged neatly with "
            f"accessories — sunglasses, a coffee cup, a phone, and a small plant. "
            f"The {item_type} features {design}. Shot from directly above on a light wooden "
            f"surface. Warm natural lighting. Lifestyle editorial for a Gen-Z fashion brand. "
            f"Instagram-ready styling."
        )
    elif shot == "model-front":
        return (
            f"Create a fashion editorial photograph of a young woman (mid-20s, natural look) "
            f"wearing a {item_type} featuring {design}. Standing against a simple warm cream "
            f"studio background, relaxed natural pose. Relaxed/oversized fit. Soft warm lighting. "
            f"Modern streetwear brand photography. Focus on the fit and design."
        )
    elif shot == "detail":
        return (
            f"Create a macro close-up photograph of a {item_type}'s main design detail — "
            f"{design}. Tight crop showing fabric texture, print quality or embroidery stitching. "
            f"Sharp focus. Warm soft lighting. Premium quality craftsmanship feel."
        )
    elif shot == "lifestyle-street":
        return (
            f"Create a street-style photograph of a young woman wearing a {item_type} "
            f"featuring {design}, paired with casual bottoms and white sneakers. Urban setting — "
            f"sunny sidewalk or coffee shop background. Natural daylight. Candid feel like a "
            f"real street-style photo. Vibrant but natural colors."
        )
    elif shot == "lifestyle":
        return (
            f"Create a cozy lifestyle photograph of someone wearing a {item_type} "
            f"featuring {design} while relaxing at home — sitting on a couch or at a kitchen "
            f"counter with coffee. Warm interior with natural window light. Relaxed, "
            f"aspirational weekend-at-home vibe. Soft focus background."
        )
    return ""


def main():
    total_items = len(FASHION_ITEMS)
    total_images = total_items * len(SHOT_TYPES)
    success = 0
    skipped = 0
    failed = 0

    print("=" * 60)
    print(f"NANCY UNIVERSE — Generating ALL Fashion Assets")
    print(f"{total_items} items × {len(SHOT_TYPES)} shots = {total_images} images")
    print("=" * 60)

    for i, item in enumerate(FASHION_ITEMS, 1):
        slug = item["slug"]
        out_dir = os.path.join(BASE_DIR, "assets", "fashion", slug)
        os.makedirs(out_dir, exist_ok=True)

        for shot in SHOT_TYPES:
            out_file = os.path.join(out_dir, f"{slug}-{shot}.png")

            if os.path.exists(out_file):
                print(f"[{i}/{total_items}] [SKIP] {item['name']} — {shot} already exists")
                skipped += 1
                continue

            prompt = build_prompt(item, shot)
            print(f"\n[{i}/{total_items}] [GEN] {item['name']} — {shot}")

            result = generate_image(prompt, out_file)

            if result:
                success += 1
            else:
                failed += 1

            # Rate limit spacing
            time.sleep(2)

    print("\n" + "=" * 60)
    print(f"DONE — {success} generated, {skipped} skipped, {failed} failed (of {total_images} total)")
    print("=" * 60)


if __name__ == "__main__":
    main()
