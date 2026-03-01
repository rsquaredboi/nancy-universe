#!/usr/bin/env python3
"""Nancy Universe — Generate hero images for all 100 new plushie characters (Waves 2-10).
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
MODEL = "gemini-2.5-flash-image"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


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
# ALL 100 NEW CHARACTERS — WAVES 2-10
# ═══════════════════════════════════════════════════════════

CHARACTERS = [
    # ── Wave 2: Food (15) ──
    {"name": "Mochi", "concept": "mochi ball", "color": "soft pink", "size": "15cm", "vibe": "squishy and gentle"},
    {"name": "Boba", "concept": "boba tea cup", "color": "brown with colorful tapioca pearls", "size": "20cm", "vibe": "bubbly and social"},
    {"name": "Nugget", "concept": "chicken nugget", "color": "golden crispy", "size": "15cm", "vibe": "cozy comfort-loving"},
    {"name": "Toasty", "concept": "burnt toast slice", "color": "dark brown with charred edges", "size": "18cm", "vibe": "slightly cynical but warm"},
    {"name": "Sushi", "concept": "salmon nigiri sushi", "color": "orange salmon on white rice", "size": "15cm", "vibe": "refined and cultured"},
    {"name": "Taco", "concept": "taco", "color": "yellow shell with colorful fillings", "size": "18cm", "vibe": "party-loving and loud"},
    {"name": "Ramen", "concept": "ramen bowl", "color": "cream and warm yellow broth with toppings", "size": "20cm", "vibe": "comforting and nurturing"},
    {"name": "Pretzel", "concept": "soft pretzel", "color": "warm golden brown with salt crystals", "size": "18cm", "vibe": "twisted and fun"},
    {"name": "Waffles", "concept": "waffle", "color": "golden yellow with grid pattern", "size": "18cm", "vibe": "reliable and sweet"},
    {"name": "Dumpling", "concept": "dumpling", "color": "pale cream white with pleated top", "size": "15cm", "vibe": "shy but delightful"},
    {"name": "Croissant", "concept": "croissant", "color": "buttery tan with flaky layers", "size": "18cm", "vibe": "sophisticated and flaky"},
    {"name": "Hotdog", "concept": "hotdog in a bun", "color": "red sausage in tan bun", "size": "20cm", "vibe": "classic and fun-loving"},
    {"name": "Onigiri", "concept": "rice ball", "color": "white rice with black nori seaweed wrap", "size": "15cm", "vibe": "humble and dependable"},
    {"name": "Eggbert", "concept": "fried egg", "color": "bright yellow yolk on white", "size": "18cm", "vibe": "sunny-side-up optimist"},
    {"name": "Pickle", "concept": "pickle", "color": "bumpy green", "size": "18cm", "vibe": "sour but lovable"},

    # ── Wave 3: Space (15) ──
    {"name": "Nebula", "concept": "nebula cloud", "color": "swirling purple and pink cosmic dust", "size": "20cm", "vibe": "dreamy and mysterious"},
    {"name": "Cosmo", "concept": "astronaut bear", "color": "silver and grey spacesuit", "size": "22cm", "vibe": "brave and curious explorer"},
    {"name": "Luna", "concept": "crescent moon", "color": "golden yellow", "size": "20cm", "vibe": "serene and watchful"},
    {"name": "Solaris", "concept": "little sun", "color": "bright yellow-orange with rays", "size": "20cm", "vibe": "radiantly cheerful"},
    {"name": "Orbit", "concept": "Saturn planet with rings", "color": "tan and beige with ring", "size": "20cm", "vibe": "chill and going in circles"},
    {"name": "Comet", "concept": "comet with a glowing tail", "color": "light blue with white trailing tail", "size": "22cm", "vibe": "fast and fleeting"},
    {"name": "Eclipse", "concept": "eclipse — half dark half light sphere", "color": "half black, half golden", "size": "18cm", "vibe": "mysterious and dramatic"},
    {"name": "Starla", "concept": "star cluster", "color": "shimmering gold", "size": "18cm", "vibe": "sparkly and attention-loving"},
    {"name": "Void", "concept": "black hole", "color": "all black with subtle dark purple edges", "size": "20cm", "vibe": "quiet, absorbing, existential"},
    {"name": "Pluto", "concept": "tiny planet Pluto", "color": "soft lavender purple", "size": "12cm", "vibe": "small but mighty, underdog energy"},
    {"name": "Rocket", "concept": "retro rocket ship", "color": "bright red with silver fins", "size": "25cm", "vibe": "ambitious and ready for launch"},
    {"name": "Astro", "concept": "cute little alien", "color": "lime green with big eyes", "size": "18cm", "vibe": "friendly and curious outsider"},
    {"name": "Meteor", "concept": "flaming space rock", "color": "orange-red with fiery glow", "size": "18cm", "vibe": "hot-headed and impactful"},
    {"name": "Galaxy", "concept": "spiral galaxy", "color": "deep indigo blue with star specks", "size": "22cm", "vibe": "vast and contemplative"},
    {"name": "UFO", "concept": "flying saucer", "color": "teal with silver dome", "size": "20cm", "vibe": "enigmatic and playful"},

    # ── Wave 4: Feelings (15) ──
    {"name": "Chaos", "concept": "tangled yarn scribble ball", "color": "messy red yarn", "size": "18cm", "vibe": "chaotic and unpredictable"},
    {"name": "Snooze", "concept": "sleepy cloud with zzz", "color": "soft light blue", "size": "20cm", "vibe": "perpetually drowsy and peaceful"},
    {"name": "Rage", "concept": "spiky angry puffball", "color": "deep fiery red with spikes", "size": "18cm", "vibe": "furious but cute about it"},
    {"name": "Chill", "concept": "ice cube wearing tiny sunglasses", "color": "translucent ice blue", "size": "15cm", "vibe": "ultra relaxed and cool"},
    {"name": "Anxious", "concept": "shaky wobbly blob", "color": "pale lavender purple", "size": "15cm", "vibe": "nervous and overthinking"},
    {"name": "Serotonin", "concept": "golden glowing orb", "color": "warm glowing gold", "size": "18cm", "vibe": "pure happiness and warmth"},
    {"name": "Ick", "concept": "little green gremlin creature", "color": "slimy green", "size": "15cm", "vibe": "gross but endearing"},
    {"name": "Crush", "concept": "heart with big eyes", "color": "blushing pink", "size": "18cm", "vibe": "lovestruck and flustered"},
    {"name": "Main Character", "concept": "spotlight beam with tiny legs", "color": "bright orange-gold spotlight glow", "size": "22cm", "vibe": "confident and center-of-attention"},
    {"name": "Drama", "concept": "theatre mask — comedy and tragedy combined", "color": "royal purple", "size": "20cm", "vibe": "theatrical and over-the-top"},
    {"name": "Zen", "concept": "meditating blob in lotus position", "color": "soft mint green and white", "size": "18cm", "vibe": "calm, centered, at peace"},
    {"name": "Hype", "concept": "exclamation mark with a face", "color": "vibrant orange", "size": "22cm", "vibe": "extremely excited about everything"},
    {"name": "Ghost", "concept": "cute little ghost", "color": "translucent white with grey tint", "size": "20cm", "vibe": "shy and spooky-cute"},
    {"name": "Simp", "concept": "heart-eyed adoring blob", "color": "hot pink", "size": "15cm", "vibe": "devoted and love-obsessed"},
    {"name": "Feral", "concept": "raccoon-energy chaotic blob", "color": "dark grey with mask markings", "size": "18cm", "vibe": "unhinged and nocturnal"},

    # ── Wave 5: Creatures (15) ──
    {"name": "Yeti", "concept": "baby yeti", "color": "fluffy white with grey accents", "size": "25cm", "vibe": "gentle giant, shy"},
    {"name": "Nessie", "concept": "baby Loch Ness monster", "color": "teal green with long neck", "size": "25cm", "vibe": "elusive and sweet"},
    {"name": "Mothman", "concept": "cute mothman with big red eyes and fuzzy wings", "color": "soft brown and tan", "size": "22cm", "vibe": "cryptid cutie, misunderstood"},
    {"name": "Kitsune", "concept": "fox spirit with multiple fluffy tails", "color": "warm orange with white-tipped tails", "size": "22cm", "vibe": "clever and magical"},
    {"name": "Axolotl", "concept": "baby axolotl with frilly gills", "color": "pastel pink with pink gills", "size": "20cm", "vibe": "permanently smiling and chill"},
    {"name": "Capybara", "concept": "capybara", "color": "warm brown", "size": "22cm", "vibe": "supremely unbothered and friendly"},
    {"name": "Jellyfish", "concept": "jellyfish with trailing tentacles", "color": "iridescent purple and pink", "size": "22cm", "vibe": "graceful and ethereal"},
    {"name": "Bat", "concept": "fruit bat with big ears and tiny wings", "color": "dark purple with pink inner ears", "size": "18cm", "vibe": "nocturnal and cuddly"},
    {"name": "Mushroom", "concept": "mushroom with spotted red cap", "color": "red cap with white spots, beige stem", "size": "18cm", "vibe": "earthy and whimsical"},
    {"name": "Dragon", "concept": "baby dragon with tiny wings", "color": "emerald green with golden belly", "size": "22cm", "vibe": "fierce but adorable"},
    {"name": "Kraken", "concept": "baby kraken with curly tentacles", "color": "deep blue-purple", "size": "22cm", "vibe": "dramatic and cuddly"},
    {"name": "Phoenix", "concept": "baby phoenix bird with flame-like plumage", "color": "orange, red, and golden fire colors", "size": "22cm", "vibe": "resilient and fiery"},
    {"name": "Unicorn", "concept": "pastel punk unicorn with rainbow mane", "color": "pastel pink body with rainbow mane", "size": "22cm", "vibe": "magical and rebellious"},
    {"name": "Slime", "concept": "happy slime blob with dripping edges", "color": "neon green translucent", "size": "15cm", "vibe": "gooey and giggly"},
    {"name": "Cloud Cat", "concept": "cat made entirely of fluffy cloud", "color": "pure white and soft grey", "size": "20cm", "vibe": "floaty and dreamy"},

    # ── Wave 6: Objects (15) ──
    {"name": "Plug", "concept": "phone charger plug", "color": "light grey with white cable", "size": "18cm", "vibe": "always there when you need energy"},
    {"name": "404", "concept": "error screen display", "color": "grey-blue with error text", "size": "18cm", "vibe": "lost and confused"},
    {"name": "Wifi", "concept": "wifi signal bars icon", "color": "bright blue signal waves", "size": "18cm", "vibe": "connecting and reliable (sometimes)"},
    {"name": "Dice", "concept": "pair of fuzzy dice", "color": "white with black dots", "size": "15cm", "vibe": "lucky and risk-taking"},
    {"name": "Vinyl", "concept": "vinyl record", "color": "glossy black with colorful label center", "size": "20cm", "vibe": "retro and soulful"},
    {"name": "Bulb", "concept": "light bulb", "color": "bright yellow glow with clear glass shape", "size": "20cm", "vibe": "bright ideas and aha moments"},
    {"name": "Cactus", "concept": "tiny cactus in pot", "color": "green with tiny flower on top", "size": "18cm", "vibe": "prickly outside, soft inside"},
    {"name": "Candle", "concept": "candle with flickering flame", "color": "cream body with warm yellow flame", "size": "20cm", "vibe": "calming and ambient"},
    {"name": "Remote", "concept": "TV remote control", "color": "dark grey with colorful buttons", "size": "20cm", "vibe": "controlling but comfortable"},
    {"name": "Sock", "concept": "single lonely sock", "color": "blue and purple striped", "size": "18cm", "vibe": "always losing its partner"},
    {"name": "Teabag", "concept": "teabag with string and tag", "color": "warm brown bag with cream tag", "size": "15cm", "vibe": "cozy and comforting"},
    {"name": "Bandaid", "concept": "adhesive bandaid", "color": "beige-peach with little heart on pad", "size": "18cm", "vibe": "healing and caring"},
    {"name": "Eraser", "concept": "rectangular eraser", "color": "classic pink", "size": "12cm", "vibe": "forgiving, lets you start over"},
    {"name": "Battery", "concept": "AA battery", "color": "green and gold", "size": "18cm", "vibe": "energetic until suddenly not"},
    {"name": "Key", "concept": "ornate golden key", "color": "shiny gold", "size": "18cm", "vibe": "mysterious and unlocking potential"},

    # ── Wave 7: Weather (10) ──
    {"name": "Thunder", "concept": "storm cloud with lightning bolt", "color": "dark grey cloud with bright yellow bolt", "size": "20cm", "vibe": "dramatic and powerful"},
    {"name": "Rainbow", "concept": "rainbow arc", "color": "multicolor bands — red, orange, yellow, green, blue, purple", "size": "22cm", "vibe": "optimistic and inclusive"},
    {"name": "Frost", "concept": "snowflake crystal", "color": "icy pale blue with sparkle", "size": "18cm", "vibe": "delicate and unique"},
    {"name": "Tornado", "concept": "baby tornado funnel", "color": "swirling grey", "size": "22cm", "vibe": "chaotic and spinning"},
    {"name": "Dewdrop", "concept": "morning dewdrop", "color": "crystal clear light blue", "size": "12cm", "vibe": "fresh and tiny"},
    {"name": "Pebble", "concept": "smooth river stone", "color": "warm grey with subtle speckles", "size": "12cm", "vibe": "steady and grounding"},
    {"name": "Coral", "concept": "sea coral branch", "color": "warm peach-orange", "size": "18cm", "vibe": "delicate and oceanic"},
    {"name": "Ember", "concept": "glowing ember coal", "color": "deep orange-red with warm glow", "size": "15cm", "vibe": "quietly intense"},
    {"name": "Moss", "concept": "fuzzy marimo moss ball", "color": "deep velvety green", "size": "12cm", "vibe": "low-maintenance and zen"},
    {"name": "Tsunami", "concept": "giant ocean wave", "color": "deep blue curling wave with white foam", "size": "22cm", "vibe": "overwhelming but majestic"},

    # ── Wave 8: Chaos (15) ──
    {"name": "Glitch", "concept": "pixelated corrupted plush with digital artifacts", "color": "neon green and black glitch pattern", "size": "18cm", "vibe": "broken but aesthetic"},
    {"name": "Shadow", "concept": "mysterious all-black silhouette figure", "color": "pure matte black", "size": "20cm", "vibe": "dark and enigmatic"},
    {"name": "Reverse", "concept": "inside-out plush showing inner stuffing", "color": "pink with visible white stuffing poking out", "size": "18cm", "vibe": "vulnerable and exposed"},
    {"name": "Static", "concept": "TV static texture ball", "color": "grey and white noise pattern", "size": "18cm", "vibe": "between channels, liminal"},
    {"name": "Virus", "concept": "cute virus cell with spike proteins", "color": "bright green with colorful spikes", "size": "15cm", "vibe": "contagiously cute"},
    {"name": "Deja Vu", "concept": "two identical small plushies as a pair", "color": "matching soft lavender", "size": "12cm each", "vibe": "eerily familiar"},
    {"name": "Paradox", "concept": "Mobius strip twisted loop shape", "color": "deep purple with impossible geometry", "size": "18cm", "vibe": "mind-bending"},
    {"name": "Liminal", "concept": "pale featureless blob in empty space", "color": "pale sickly yellow", "size": "18cm", "vibe": "uncanny and in-between"},
    {"name": "Error", "concept": "broken glitched heart with crack", "color": "red with digital distortion", "size": "18cm", "vibe": "heartbroken but recovering"},
    {"name": "AI", "concept": "cute robot with a glowing heart", "color": "soft blue with LED-like accents", "size": "20cm", "vibe": "learning to feel"},
    {"name": "Rizz", "concept": "sparkly ultra-smooth blob", "color": "shimmering gold with sparkles", "size": "18cm", "vibe": "irresistibly charming"},
    {"name": "Slay", "concept": "blob wearing a tiny crown", "color": "royal purple with gold crown", "size": "20cm", "vibe": "confident queen energy"},
    {"name": "NPC", "concept": "generic plain background character", "color": "plain grey, deliberately basic", "size": "18cm", "vibe": "blending in, unremarkable on purpose"},
    {"name": "Delulu", "concept": "heart-shaped head with star eyes", "color": "hot pink with sparkling star eyes", "size": "18cm", "vibe": "delusional optimist"},
    {"name": "Unhinged", "concept": "blob with spinning spiral eyes", "color": "chaotic orange-red", "size": "18cm", "vibe": "totally unhinged and loving it"},

    # ── Wave 9: Drinks (10) ──
    {"name": "Espresso", "concept": "espresso shot glass", "color": "rich dark brown with crema foam on top", "size": "12cm", "vibe": "intense and focused"},
    {"name": "Matcha", "concept": "matcha latte cup", "color": "vibrant green with white foam art", "size": "18cm", "vibe": "trendy and balanced"},
    {"name": "Smoothie", "concept": "smoothie cup with straw", "color": "purple and pink berry blend", "size": "22cm", "vibe": "healthy and vibrant"},
    {"name": "Sake", "concept": "sake bottle (tokkuri)", "color": "elegant white and cream ceramic", "size": "20cm", "vibe": "refined and warming"},
    {"name": "Kombucha", "concept": "kombucha bottle", "color": "light green with fizzy bubbles", "size": "22cm", "vibe": "trendy and probiotic"},
    {"name": "Juice Box", "concept": "juice box with tiny straw", "color": "bright orange with straw sticking out", "size": "18cm", "vibe": "nostalgic and sweet"},
    {"name": "Milky", "concept": "milk carton", "color": "white with red and blue stripes", "size": "20cm", "vibe": "wholesome and classic"},
    {"name": "Coconut Water", "concept": "coconut with a straw", "color": "brown coconut shell with white inside, straw", "size": "18cm", "vibe": "tropical and refreshing"},
    {"name": "Hot Cocoa", "concept": "hot chocolate mug with marshmallows", "color": "warm brown in a cozy mug", "size": "18cm", "vibe": "warm and comforting"},
    {"name": "Bubble", "concept": "champagne flute glass", "color": "golden sparkling with tiny bubbles", "size": "22cm", "vibe": "celebratory and bubbly"},

    # ── Wave 10: Sweets (5) ──
    {"name": "Macaron", "concept": "pastel French macaron", "color": "soft pastel pink with cream filling", "size": "12cm", "vibe": "dainty and elegant"},
    {"name": "Donut", "concept": "frosted donut", "color": "pink frosting with rainbow sprinkles", "size": "18cm", "vibe": "fun and indulgent"},
    {"name": "Cinnamon Roll", "concept": "cinnamon roll spiral", "color": "warm brown and orange swirl with white icing", "size": "18cm", "vibe": "sweet and comforting"},
    {"name": "Gummy Bear", "concept": "translucent gummy bear candy", "color": "translucent cherry red", "size": "15cm", "vibe": "bouncy and chewy"},
    {"name": "Ice Pop", "concept": "twin popsicle pair (two sticks together)", "color": "orange and red gradient", "size": "22cm", "vibe": "best friends, meant to be shared"},
]


SHOT_TYPES = ["hero", "angle", "lifestyle-bed", "lifestyle-desk", "in-hand", "flatlay"]


def make_slug(name):
    """Convert character name to URL-safe slug."""
    return name.lower().replace(" ", "-")


def build_prompt(char, shot):
    """Build prompt for a specific shot type."""
    name = char["name"]
    concept = char["concept"]
    color = char["color"]
    size = char["size"]
    vibe = char["vibe"]

    base = (
        f"kawaii {concept} plush toy. The plush is {color}, about {size}, "
        f"with a cute round shape, tiny arms and legs, and an adorable embroidered smiling face "
        f"with rosy cheeks. Super-soft plush fabric with visible texture. "
        f"Named {name} with {vibe} personality."
    )

    if shot == "hero":
        return (
            f"Create a professional e-commerce product photograph of a {base} "
            f"Pure white background. Clean, centered composition with soft even studio lighting "
            f"and a subtle shadow underneath. High-resolution, sharp focus on fabric texture. "
            f"Premium toy brand product photography style."
        )
    elif shot == "angle":
        return (
            f"Create a product photograph of a {base} "
            f"Turned 45 degrees to the right showing the side profile and roundness of the body. "
            f"White background, soft studio lighting. Clean e-commerce product photography."
        )
    elif shot == "lifestyle-bed":
        return (
            f"Create a cozy lifestyle photograph of a {base} "
            f"Sitting on a neatly made bed with white linen sheets and cream pillows. "
            f"Morning sunlight streaming through a window. Warm, aspirational bedroom setting. "
            f"Editorial lifestyle photography, warm tones, soft focus background."
        )
    elif shot == "lifestyle-desk":
        return (
            f"Create a lifestyle photograph of a {base} "
            f"Sitting on a clean modern desk surrounded by a small plant, a candle, and a coffee mug. "
            f"Scandinavian minimal aesthetic. Soft natural side lighting. Warm tones, shallow depth of field."
        )
    elif shot == "in-hand":
        return (
            f"Create a lifestyle photograph of feminine hands gently holding a {base} "
            f"Soft neutral background. Warm natural lighting. The scale looks realistic — "
            f"the plush fits comfortably in two hands. Cozy, inviting feel."
        )
    elif shot == "flatlay":
        return (
            f"Create an overhead flat lay photograph with a {base} "
            f"As the centerpiece, arranged with dried flowers, a cute greeting card, colorful candies, "
            f"and tissue paper — as if someone just received it as a gift. Soft pink background. "
            f"Natural top-down lighting. Premium unboxing moment. Instagram-ready."
        )
    return ""


def main():
    total_chars = len(CHARACTERS)
    total_images = total_chars * len(SHOT_TYPES)
    success = 0
    skipped = 0
    failed = 0

    print("=" * 60)
    print(f"NANCY UNIVERSE — Generating ALL Plushie Assets")
    print(f"{total_chars} characters × {len(SHOT_TYPES)} shots = {total_images} images")
    print("=" * 60)

    for i, char in enumerate(CHARACTERS, 1):
        name = char["name"]
        slug = make_slug(name)
        out_dir = os.path.join(BASE_DIR, "assets", "plushies", slug)
        os.makedirs(out_dir, exist_ok=True)

        for shot in SHOT_TYPES:
            out_file = os.path.join(out_dir, f"{slug}-{shot}.png")

            if os.path.exists(out_file):
                print(f"[{i}/{total_chars}] [SKIP] {name} — {shot} already exists")
                skipped += 1
                continue

            prompt = build_prompt(char, shot)
            print(f"\n[{i}/{total_chars}] [GEN] {name} — {shot}")

            result = generate_image(prompt, out_file)

            if result:
                success += 1
            else:
                failed += 1

            # Rate limit spacing
            time.sleep(5)

    print("\n" + "=" * 60)
    print(f"DONE — {success} generated, {skipped} skipped, {failed} failed (of {total_images} total)")
    print("=" * 60)


if __name__ == "__main__":
    main()
