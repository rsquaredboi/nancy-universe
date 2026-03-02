#!/usr/bin/env python3
"""
generate-new-toys.py
====================
Generates 14 new Nancy Universe adult toy PDP pages + updated toys collection page.
Matches the exact HTML structure of lem.html and plushies.html collection format.

Usage:
    python3 generate-new-toys.py
"""

import os
import math

# ═══════════════════════════════════════════════════════════════════
# BASE DIRECTORY
# ═══════════════════════════════════════════════════════════════════
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_DIR = os.path.join(BASE_DIR, "pages", "products")
COLLECTIONS_DIR = os.path.join(BASE_DIR, "pages", "collections")

os.makedirs(PRODUCTS_DIR, exist_ok=True)
os.makedirs(COLLECTIONS_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════
# EMOJI MAP — fruit emoji for each product
# ═══════════════════════════════════════════════════════════════════
EMOJI_MAP = {
    "mango": "\U0001F96D",      # mango
    "fig": "\U0001FAD0",         # fig (blueberries as proxy)
    "cherry": "\U0001F352",      # cherries
    "plum": "\U0001FAD0",        # plum (blueberries proxy)
    "coconut": "\U0001F965",     # coconut
    "grape": "\U0001F347",       # grapes
    "peach": "\U0001F351",       # peach
    "melon": "\U0001F348",       # melon
    "dragonfruit": "\U0001F432", # dragon face (proxy)
    "seed": "\U0001F331",        # seedling
    "fizz": "\U0001F9CB",        # bubble tea (proxy)
    "stem": "\U0001F352",        # cherries (pendant)
    "berry-set": "\U0001FAD0",   # berries
    "cozy": "\U0001F9F8",        # teddy bear
}

# ═══════════════════════════════════════════════════════════════════
# SVG ICON LIBRARY — reusable SVGs for feature icons
# ═══════════════════════════════════════════════════════════════════
SVG = {
    "warmth": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>',
    "airpulse": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"/></svg>',
    "waterproof": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/></svg>',
    "quiet": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.5 0 10-4.5 10-10S17.5 2 12 2 2 6.5 2 12s4.5 10 10 10z"/><path d="M8 12s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>',
    "battery": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="6" width="18" height="12" rx="2"/><line x1="23" y1="13" x2="23" y2="11"/></svg>',
    "silicone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    "bluetooth": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6.5 6.5 17.5 17.5 12 23 12 1 17.5 6.5 6.5 17.5"/></svg>',
    "app": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>',
    "vibration": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h2m16 0h2M7 12h10"/><path d="M12 2v4m0 12v4"/><circle cx="12" cy="12" r="3"/></svg>',
    "wifi": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>',
    "magnetic": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2v6a6 6 0 0 0 12 0V2"/><line x1="6" y1="2" x2="6" y2="6"/><line x1="18" y1="2" x2="18" y2="6"/></svg>',
    "squeeze": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0"/><path d="M14 10V4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v2"/><path d="M10 10.5V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.9-5.9-2.5L3.3 16a2 2 0 0 1 3-2.6L8 15"/></svg>',
    "compact": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
    "suction": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><line x1="4.93" y1="4.93" x2="9.17" y2="9.17"/><line x1="14.83" y1="14.83" x2="19.07" y2="19.07"/><line x1="14.83" y1="9.17" x2="19.07" y2="4.93"/><line x1="4.93" y1="19.07" x2="9.17" y2="14.83"/></svg>',
    "gift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg>',
    "bath": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h16a1 1 0 0 1 1 1v3a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4v-3a1 1 0 0 1 1-1z"/><path d="M6 12V5a2 2 0 0 1 2-2h3"/></svg>',
    "jewelry": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="16" r="4"/><path d="M8 2l4 6 4-6"/><line x1="12" y1="8" x2="12" y2="12"/></svg>',
    "graduated": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>',
    "plush": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    "tens": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
    "handsfree": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg>',
    "wireless": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>',
}

# ═══════════════════════════════════════════════════════════════════
# PRODUCT DATA — All 14 new products
# ═══════════════════════════════════════════════════════════════════
PRODUCTS = [
    # ─── TIER 1: HERO UPGRADES ───
    {
        "slug": "mango",
        "name": "Mango",
        "subtitle": "The Warm One",
        "category": "Clitoral Suction + Warming",
        "tagline": "Warmth meets air-pulse. The hug your body's been waiting for.",
        "description": "Everything you love about Lem, now with a warming embrace. Mango heats to body temperature in 60 seconds while delivering 10 levels of air-pulse suction. The gentle warmth increases blood flow and sensitivity, making every pulse feel more alive. Medical-grade silicone. Waterproof. Whisper-quiet.",
        "price": 99,
        "compare_price": 179,
        "stars": 4.9,
        "review_count": "Preview",
        "badge_text": "NEW \u00b7 WARMING",
        "badge_style": 'style="background: #FFF3E0; color: #E65100;"',
        "color_desc": "Warm sunset orange gradient",
        "features": [
            (SVG["warmth"], "Warming to 104\u00b0F"),
            (SVG["airpulse"], "10 Air-Pulse Levels"),
            (SVG["waterproof"], "IPX7 Waterproof"),
            (SVG["quiet"], "Whisper Quiet"),
            (SVG["battery"], "USB-C \u00b7 90min Battery"),
            (SVG["silicone"], "Medical-Grade Silicone"),
        ],
        "feature_sections": [
            {
                "label": "The Technology",
                "heading": "Warmth that <em>awakens</em>.",
                "text": "Mango's PTC ceramic heating element warms to a comfortable 104\u00b0F in just 60 seconds. Combined with Nancy's signature air-pulse technology, the gentle warmth increases blood flow and sensitivity \u2014 making every pulse feel deeper, richer, more alive. It's the difference between a cold touch and a warm embrace.",
                "image_num": "1",
                "bg": "",
            },
            {
                "label": "Designed to Delight",
                "heading": "Sunset in your <em>palm</em>.",
                "text": "Mango's warm orange gradient fades from golden sunrise to deep sunset. The ergonomic shape sits naturally in your hand, while the soft-touch silicone warms to body temperature. Every detail was designed by our all-female Hong Kong team to feel as good as it looks.",
                "image_num": "2",
                "bg": ' style="background: var(--cream-dark);"',
                "reverse": True,
            },
            {
                "label": "Go Anywhere",
                "heading": "Waterproof. Warm. <em>Worry-free.</em>",
                "text": "IPX7 waterproof means Mango loves the bath as much as you do. The warming element is fully sealed and safe for full submersion. USB-C magnetic charging gives you 90 minutes of warm, pulsing playtime on a single charge.",
                "image_num": "3",
                "bg": "",
            },
        ],
    },
    {
        "slug": "fig",
        "name": "Fig",
        "subtitle": "The Smart Trainer",
        "category": "Smart Kegel Trainer",
        "tagline": "Grow your strength. Grow your garden.",
        "description": "A kegel trainer that actually makes you want to train. Fig's pressure sensors connect to the Nancy app where your squeezes grow a virtual fruit garden. 5 minutes a day, 3x per week. Watch your pelvic floor strength bloom alongside your digital orchard. Biofeedback visualization. Progress tracking. Personalized programs.",
        "price": 99,
        "compare_price": 199,
        "stars": 4.8,
        "review_count": "Preview",
        "badge_text": "NEW \u00b7 SMART",
        "badge_style": 'style="background: #F3E8FF; color: #7C3AED;"',
        "color_desc": "Deep purple with pink accents",
        "features": [
            (SVG["bluetooth"], "Bluetooth 5.0"),
            (SVG["app"], "Nancy App + Gamification"),
            (SVG["squeeze"], "Dual Pressure Sensors"),
            (SVG["waterproof"], "IPX7 Waterproof"),
            (SVG["battery"], "USB-C \u00b7 4hr Battery"),
            (SVG["silicone"], "Medical-Grade Silicone"),
        ],
        "feature_sections": [
            {
                "label": "The Technology",
                "heading": "Biofeedback meets <em>fun</em>.",
                "text": "Fig's dual pressure sensors detect the strength and duration of every squeeze, sending real-time data to the Nancy app via Bluetooth 5.0. Watch your efforts visualized as growing fruit \u2014 each squeeze blooms a new bud. It turns the most important exercise you're probably not doing into a game you actually want to play.",
                "image_num": "1",
                "bg": "",
            },
            {
                "label": "Your Digital Garden",
                "heading": "5 minutes. 3 days. <em>Real results.</em>",
                "text": "The Nancy app creates personalized training programs that adapt to your progress. Start gentle, build strength gradually. Track your improvement over weeks and months with clear metrics. Your virtual fruit garden grows as your pelvic floor strengthens \u2014 a beautiful, private record of your journey.",
                "image_num": "2",
                "bg": ' style="background: var(--cream-dark);"',
                "reverse": True,
            },
            {
                "label": "Designed for Life",
                "heading": "Wear it. Forget it. <em>Feel it.</em>",
                "text": "Fig's smooth, ergonomic shape in deep purple silicone is comfortable for extended wear during your training sessions. IPX7 waterproof for easy cleaning. The 4-hour battery means you'll never run out mid-session. USB-C charging because it's 2026.",
                "image_num": "3",
                "bg": "",
            },
        ],
    },
    {
        "slug": "cherry",
        "name": "Cherry",
        "subtitle": "The Pair",
        "category": "Couples Toy",
        "tagline": "Two halves. One connection. Zero distance.",
        "description": "Cherry comes in pairs \u2014 just like real cherries. Each partner holds one half. Squeeze yours, and theirs responds. Works across the room or across the world via WiFi. 12 shared patterns. Real-time touch mirroring. The first couples toy designed to feel like holding hands, not reading a manual.",
        "price": 129,
        "compare_price": 229,
        "stars": 4.7,
        "review_count": "Preview",
        "badge_text": "NEW \u00b7 COUPLES",
        "badge_style": 'style="background: #FEE2E2; color: #DC2626;"',
        "color_desc": "Deep red pair with green stem accent",
        "features": [
            (SVG["wifi"], "WiFi + Bluetooth"),
            (SVG["squeeze"], "Bidirectional Haptics"),
            (SVG["app"], "Partner App Control"),
            (SVG["waterproof"], "IPX7 Waterproof"),
            (SVG["battery"], "2hr Battery Each"),
            (SVG["magnetic"], "Magnetic Charging Dock"),
        ],
        "feature_sections": [
            {
                "label": "The Connection",
                "heading": "Touch them <em>here</em>, they feel it <em>there</em>.",
                "text": "Cherry's bidirectional haptic motors create a real-time feedback loop between two devices. Squeeze yours gently, and your partner's Cherry responds with matching pressure \u2014 whether they're in the next room or another timezone. 12 shared patterns let you communicate through touch in ways words can't.",
                "image_num": "1",
                "bg": "",
            },
            {
                "label": "Designed for Two",
                "heading": "Two cherries. One <em>stem</em>.",
                "text": "Each Cherry is identical \u2014 no 'his' or 'hers.' The deep red silicone with green stem accent sits beautifully in the magnetic charging dock. Pair once via the Nancy app, and they'll remember each other forever. Just like you.",
                "image_num": "2",
                "bg": ' style="background: var(--cream-dark);"',
                "reverse": True,
            },
            {
                "label": "No Distance Too Far",
                "heading": "WiFi means <em>anywhere</em>.",
                "text": "Bluetooth for close range. WiFi for long distance. Cherry works seamlessly across both \u2014 switching automatically based on proximity. IPX7 waterproof. 2 hours of battery each. The magnetic dock charges both simultaneously. Distance was never the problem.",
                "image_num": "3",
                "bg": "",
            },
        ],
    },
    # ─── TIER 2: MARKET GAP FILLERS ───
    {
        "slug": "plum",
        "name": "Plum",
        "subtitle": "The Cycle Companion",
        "category": "Period Comfort + Pleasure",
        "tagline": "For every day of your cycle. Yes, those days too.",
        "description": "Mode 1: Gentle TENS pulses + warming heat to melt period cramps away. Mode 2: Reposition for targeted vibration pleasure. One device, two purposes, zero shame. Plum is the first toy that acknowledges your whole cycle \u2014 the painful parts and the pleasurable parts.",
        "price": 89,
        "compare_price": 169,
        "stars": 4.8,
        "review_count": "Preview",
        "badge_text": "NEW \u00b7 WELLNESS",
        "badge_style": 'style="background: #F3E8FF; color: #7C3AED;"',
        "color_desc": "Deep plum with lavender gradient",
        "features": [
            (SVG["tens"], "TENS Mode \u00b7 4 Patterns"),
            (SVG["warmth"], "Warming to 107\u00b0F"),
            (SVG["vibration"], "Vibration \u00b7 8 Patterns"),
            (SVG["waterproof"], "IPX6 Splash-Proof"),
            (SVG["battery"], "USB-C \u00b7 3hr Battery"),
            (SVG["silicone"], "Medical-Grade Silicone"),
        ],
        "feature_sections": [
            {
                "label": "Two Modes, One Device",
                "heading": "Comfort <em>and</em> pleasure.",
                "text": "Plum's flat pebble shape houses both TENS electrodes and a vibration motor. Mode 1 delivers gentle electrical pulses combined with warming heat \u2014 clinically proven to reduce menstrual cramp pain. Mode 2 repositions for targeted vibration pleasure. Your cycle has many days. Plum is for all of them.",
                "image_num": "1",
                "bg": "",
            },
            {
                "label": "The Warmth",
                "heading": "Heat that <em>melts</em> the pain.",
                "text": "Plum's PTC heater warms to 107\u00b0F \u2014 the therapeutic sweet spot for cramp relief. Combined with 4 TENS pulse patterns, it creates a warm, tingling sensation that relaxes uterine muscles and increases blood flow. No pills. No hot water bottle. Just relief that fits in your pocket.",
                "image_num": "2",
                "bg": ' style="background: var(--cream-dark);"',
                "reverse": True,
            },
            {
                "label": "Zero Shame",
                "heading": "Your cycle. Your <em>rules</em>.",
                "text": "Plum's deep plum-to-lavender gradient is as beautiful as it is functional. The smooth pebble shape doesn't look like a medical device or a toy \u2014 it looks like Plum. IPX6 splash-proof. 3-hour battery. USB-C charging. Because your body deserves good design every day of the month.",
                "image_num": "3",
                "bg": "",
            },
        ],
    },
    {
        "slug": "coconut",
        "name": "Coconut",
        "subtitle": "The Connected One",
        "category": "App-Connected Suction",
        "tagline": "Your pleasure, your patterns, your rules.",
        "description": "Lem's air-pulse technology meets the Nancy app. Create custom patterns. Let your partner control from anywhere. Track what works. Coconut learns your preferences and builds a personalized pleasure profile over time. The premium, connected evolution of everything Nancy does best.",
        "price": 129,
        "compare_price": 249,
        "stars": 4.9,
        "review_count": "Preview",
        "badge_text": "PREMIUM",
        "badge_style": 'style="background: #1a1a1a; color: #fff;"',
        "color_desc": "Creamy white with brown accents",
        "features": [
            (SVG["bluetooth"], "Bluetooth 5.0"),
            (SVG["app"], "Nancy App \u00b7 Custom Patterns"),
            (SVG["airpulse"], "12 Preset + Unlimited Custom"),
            (SVG["waterproof"], "IPX7 Waterproof"),
            (SVG["battery"], "USB-C \u00b7 2hr Battery"),
            (SVG["silicone"], "Premium Silicone"),
        ],
        "feature_sections": [
            {
                "label": "The Evolution",
                "heading": "Air-pulse meets <em>intelligence</em>.",
                "text": "Coconut takes Nancy's proven air-pulse technology and adds a brain. Connect via Bluetooth 5.0 to the Nancy app and unlock custom pattern creation, partner remote control, and preference tracking. 12 curated presets to start \u2014 then build unlimited patterns of your own. Coconut learns what you love.",
                "image_num": "1",
                "bg": "",
            },
            {
                "label": "Your Pleasure Profile",
                "heading": "It <em>remembers</em>.",
                "text": "Over time, Coconut builds a personalized pleasure profile based on your usage patterns. Favorite intensities. Preferred rhythms. Session durations. The Nancy app visualizes your journey in beautiful, private charts. No two Coconuts are the same \u2014 because no two people are.",
                "image_num": "2",
                "bg": ' style="background: var(--cream-dark);"',
                "reverse": True,
            },
            {
                "label": "Premium Everything",
                "heading": "The <em>finest</em> we've made.",
                "text": "Creamy white premium silicone with warm brown accents. IPX7 waterproof. 2-hour battery. USB-C charging. Partner control from anywhere in the world. Coconut is the premium flagship of the Nancy fruit bowl \u2014 for those who want the very best.",
                "image_num": "3",
                "bg": "",
            },
        ],
    },
    {
        "slug": "grape",
        "name": "Grape",
        "subtitle": "The Invisible One",
        "category": "Wearable Panty Vibrator",
        "tagline": "Your secret. Anywhere. Anytime.",
        "description": "Slip Grape into your underwear and forget it's there \u2014 until you don't want to. Magnetic clip keeps it in place. App-controlled by you or a partner. So quiet you could wear it to brunch. (We're not saying you should. We're not saying you shouldn't.)",
        "price": 79,
        "compare_price": 149,
        "stars": 4.6,
        "review_count": "Preview",
        "badge_text": "NEW \u00b7 DISCREET",
        "badge_style": 'style="background: #F3E8FF; color: #7C3AED;"',
        "color_desc": "Purple grape cluster shape",
        "features": [
            (SVG["magnetic"], "Magnetic Underwear Clip"),
            (SVG["vibration"], "10 Vibration Modes"),
            (SVG["app"], "App-Controlled"),
            (SVG["quiet"], "Whisper Quiet (<25dB)"),
            (SVG["waterproof"], "IPX7 Waterproof"),
            (SVG["battery"], "USB-C \u00b7 3hr Battery"),
        ],
        "feature_sections": [
            {
                "label": "The Secret",
                "heading": "Wear it. <em>Forget it.</em> Remember it.",
                "text": "Grape's flat, contoured profile and magnetic underwear clip hold it securely in place without any straps or harnesses. At under 25 decibels, it's quieter than your breathing. Slip it in, go about your day, and let the anticipation build. Your secret, your schedule.",
                "image_num": "1",
                "bg": "",
            },
            {
                "label": "App Control",
                "heading": "Your hand. Or <em>theirs</em>.",
                "text": "Connect Grape to the Nancy app via Bluetooth and control 10 vibration modes from your phone \u2014 or hand control to a partner anywhere in the world. The app's discreet mode means no one will know what that notification is. Except you.",
                "image_num": "2",
                "bg": ' style="background: var(--cream-dark);"',
                "reverse": True,
            },
            {
                "label": "All Day, Every Day",
                "heading": "3 hours. <em>Waterproof.</em> Ready for anything.",
                "text": "Grape's 3-hour battery means it outlasts your longest brunch, your entire commute, or your most boring meeting. IPX7 waterproof for easy cleaning. USB-C charging. Medical-grade purple silicone that's as body-safe as it is beautiful.",
                "image_num": "3",
                "bg": "",
            },
        ],
    },
    # ─── TIER 3: INNOVATION/EDGY ───
    {
        "slug": "peach",
        "name": "Peach",
        "subtitle": "The Squeeze",
        "category": "Pressure-Adaptive Vibrator",
        "tagline": "No buttons. No app. Just squeeze.",
        "description": "The world's first squeeze-to-control vibrator. Grip Peach gently for a whisper. Squeeze harder for thunder. Your hand IS the interface. Pressure sensors across the body translate your grip into intensity in real-time. It's the most intuitive toy ever made \u2014 because your body already knows what it wants.",
        "price": 99,
        "compare_price": 179,
        "stars": 4.8,
        "review_count": "Preview",
        "badge_text": "INNOVATION",
        "badge_style": 'style="background: #FFF0E0; color: #EA580C;"',
        "color_desc": "Soft peach pink, slightly translucent",
        "features": [
            (SVG["squeeze"], "Pressure-Sensitive Array"),
            (SVG["vibration"], "Real-Time Grip Mapping"),
            (SVG["quiet"], "No Buttons Needed"),
            (SVG["waterproof"], "IPX7 Waterproof"),
            (SVG["battery"], "USB-C \u00b7 2hr Battery"),
            (SVG["silicone"], "Body-Safe Silicone"),
        ],
        "feature_sections": [
            {
                "label": "The Innovation",
                "heading": "Your grip is the <em>interface</em>.",
                "text": "Peach's force-sensitive resistor array detects pressure across its entire surface and translates your grip into vibration intensity in real-time. No buttons to fumble with. No app to navigate. No learning curve. Grip gently for a whisper. Squeeze firmly for thunder. Your body already knows what it wants \u2014 Peach just listens.",
                "image_num": "1",
                "bg": "",
            },
            {
                "label": "Pure Intuition",
                "heading": "Zero friction. <em>Maximum</em> feeling.",
                "text": "Every other toy makes you think \u2014 which button? which mode? which app screen? Peach removes all of that. The soft peach-pink silicone body has no visible controls, no seams, no distractions. Just a smooth, warm shape that responds to the most natural gesture in the world: your squeeze.",
                "image_num": "2",
                "bg": ' style="background: var(--cream-dark);"',
                "reverse": True,
            },
            {
                "label": "Beautifully Simple",
                "heading": "Waterproof. Quiet. <em>Perfect.</em>",
                "text": "IPX7 waterproof. 2-hour battery. USB-C charging. Whisper-quiet motor. The slightly translucent peach-pink silicone glows softly in warm light. Peach proves that the most advanced technology should feel like no technology at all.",
                "image_num": "3",
                "bg": "",
            },
        ],
    },
    {
        "slug": "melon",
        "name": "Melon",
        "subtitle": "The Power Wand",
        "category": "Compact Warming Wand",
        "tagline": "Big energy. Small footprint. Warm vibes.",
        "description": "Lolly's power in a travel-friendly body. Melon packs a deep-rumble motor with body-temperature warming into a form factor that fits in your makeup bag. 8 patterns from gentle flutter to deep thunder. The head warms in 30 seconds. Passes as a skincare device at TSA.",
        "price": 89,
        "compare_price": 169,
        "stars": 4.7,
        "review_count": "Preview",
        "badge_text": "NEW \u00b7 TRAVEL",
        "badge_style": 'style="background: #ECFDF5; color: #059669;"',
        "color_desc": "Honeydew green with white accents",
        "features": [
            (SVG["warmth"], "Warming Head"),
            (SVG["vibration"], "Deep-Rumble Motor"),
            (SVG["compact"], "Compact 5.5\u201d"),
            (SVG["waterproof"], "IPX7 Waterproof"),
            (SVG["battery"], "USB-C \u00b7 90min Battery"),
            (SVG["silicone"], "Body-Safe Silicone"),
        ],
        "feature_sections": [
            {
                "label": "The Power",
                "heading": "Wand power. Travel <em>size</em>.",
                "text": "Melon's weighted vibration motor delivers the deep, rumbly vibrations you expect from a full-size wand \u2014 compressed into a 5.5-inch body that fits in your makeup bag. 8 patterns from gentle flutter to deep thunder. The difference between Melon and a 'mini' wand? Melon doesn't compromise.",
                "image_num": "1",
                "bg": "",
            },
            {
                "label": "The Warmth",
                "heading": "30 seconds to <em>warm</em>.",
                "text": "Melon's flexible head heats to body temperature in 30 seconds. The warmth loosens muscles and increases sensitivity before the motor even kicks in. Combined with 8 vibration patterns, it's like a warm-up and a workout in one beautiful green package.",
                "image_num": "2",
                "bg": ' style="background: var(--cream-dark);"',
                "reverse": True,
            },
            {
                "label": "Travel Ready",
                "heading": "TSA-friendly. <em>Doubt-free.</em>",
                "text": "Melon looks like a skincare device. At 5.5 inches, it slides into your toiletry bag without a second glance. IPX7 waterproof. 90-minute battery. USB-C charging. Honeydew green with white accents \u2014 because your travel companion should be as cute as your passport holder.",
                "image_num": "3",
                "bg": "",
            },
        ],
    },
    {
        "slug": "dragonfruit",
        "name": "Dragonfruit",
        "subtitle": "The Hands-Free",
        "category": "Shower Suction-Mount Toy",
        "tagline": "Stick it. Forget your hands. Remember yourself.",
        "description": "A suction-cup-mounted air-pulse device designed for the shower. Stick Dragonfruit to any smooth surface, adjust the angle, and go completely hands-free. The industrial-grade suction cup holds firm on wet tile. IPX8 fully submersible. Combines the relaxation of a hot shower with Nancy's signature air-pulse sensation.",
        "price": 89,
        "compare_price": 159,
        "stars": 4.6,
        "review_count": "Preview",
        "badge_text": "NEW \u00b7 HANDS-FREE",
        "badge_style": 'style="background: #FCE7F3; color: #DB2777;"',
        "color_desc": "Hot pink with white speckle pattern",
        "features": [
            (SVG["suction"], "Industrial Suction Cup"),
            (SVG["handsfree"], "360\u00b0 Angle Adjustment"),
            (SVG["airpulse"], "Air-Pulse + Vibration"),
            (SVG["waterproof"], "IPX8 Fully Submersible"),
            (SVG["battery"], "90min Battery"),
            (SVG["silicone"], "Body-Safe Silicone"),
        ],
        "feature_sections": [
            {
                "label": "The Freedom",
                "heading": "Hands-free means <em>mind-free</em>.",
                "text": "Dragonfruit's industrial-grade suction cup grips any smooth surface \u2014 tile, glass, metal \u2014 and holds firm even on wet surfaces. The 360-degree ball joint lets you adjust the angle precisely. Stick it, position it, and forget about it. Your hands are free to do\u2026 whatever they want.",
                "image_num": "1",
                "bg": "",
            },
            {
                "label": "Shower-Proof",
                "heading": "IPX8. Fully <em>submersible</em>.",
                "text": "Not just waterproof \u2014 fully submersible. Dragonfruit is rated IPX8, meaning it can handle direct water streams, full submersion, and everything in between. The combination of a hot shower and Nancy's air-pulse technology creates a sensation that's uniquely, wonderfully Dragonfruit.",
                "image_num": "2",
                "bg": ' style="background: var(--cream-dark);"',
                "reverse": True,
            },
            {
                "label": "Bold by Design",
                "heading": "Hot pink. White speckle. <em>Unapologetic.</em>",
                "text": "Dragonfruit doesn't hide. Its hot pink body with white speckle pattern is inspired by the real fruit \u2014 bold, exotic, and impossible to ignore. 10 modes combining air-pulse and vibration. 90-minute battery. Because your shower time should be as exciting as you want it to be.",
                "image_num": "3",
                "bg": "",
            },
        ],
    },
    # ─── TIER 4: GIFT/ENTRY PRODUCTS ───
    {
        "slug": "seed",
        "name": "Seed",
        "subtitle": "The Fruit Basket",
        "category": "Sampler Kit",
        "tagline": "Try everything. Commit to nothing. (Yet.)",
        "description": "A premium gift box with mini versions of Nancy's hero toys: Mini Lem, Mini Pixie, Mini Lolly, and Mini Avo \u2014 plus a sachet of Nancy lube. Each mini is fully functional with 3 intensity levels. Packaged like a macaron box. The most giftable thing in pleasure.",
        "price": 149,
        "compare_price": 299,
        "stars": 4.9,
        "review_count": "Preview",
        "badge_text": "GIFT SET",
        "badge_style": 'style="background: #FEF3C7; color: #D97706;"',
        "color_desc": "Pastel rainbow box, each mini in its fruit color",
        "features": [
            (SVG["gift"], "4 Mini Toys (Functional)"),
            (SVG["vibration"], "3 Intensity Levels Each"),
            (SVG["silicone"], "Medical-Grade Silicone"),
            (SVG["battery"], "Individual USB-C Chargers"),
            (SVG["bath"], "Nancy Lube Sachet"),
            (SVG["compact"], "Premium Gift Box"),
        ],
        "feature_sections": [
            {
                "label": "The Collection",
                "heading": "Four icons. One <em>beautiful</em> box.",
                "text": "Seed contains fully functional mini versions of Nancy's four hero products: Mini Lem (air-pulse), Mini Pixie (bullet), Mini Lolly (tongue), and Mini Avo (couples). Each has 3 intensity levels and its own USB-C charger. Plus a generous sachet of Nancy's water-based lube. It's a greatest hits album in a macaron box.",
                "image_num": "1",
                "bg": "",
            },
            {
                "label": "The Gift",
                "heading": "The most giftable thing in <em>pleasure</em>.",
                "text": "Seed's pastel rainbow gift box is designed to make someone's day. Each mini sits in its own velvet cradle, color-matched to its character. The unboxing experience is half the gift. Perfect for birthdays, anniversaries, Valentine's, holidays, or just because someone deserves to try everything.",
                "image_num": "2",
                "bg": ' style="background: var(--cream-dark);"',
                "reverse": True,
            },
            {
                "label": "No Commitment",
                "heading": "Try everything. Then <em>choose</em>.",
                "text": "Not sure which Nancy is right for you? Seed lets you experiment with four different sensation types without committing to a full-size purchase. Each mini is powerful enough for real use \u2014 these aren't samples, they're travel companions. Fall in love with one, then upgrade to the full-size version.",
                "image_num": "3",
                "bg": "",
            },
        ],
    },
    {
        "slug": "fizz",
        "name": "Fizz",
        "subtitle": "The Bath Ritual",
        "category": "Bath Bomb + Bullet Set",
        "tagline": "Dissolve the day. Discover what's inside.",
        "description": "Three fruit-shaped bath bombs (lemon, strawberry, peach) that fizz away in your tub to reveal a waterproof bullet vibrator inside. Essential oils turn your bath into a spa. The bullet turns your bath into\u2026 something more. Sold as a 3-pack self-care ritual. The ultimate 'treat yourself' moment.",
        "price": 49,
        "compare_price": 89,
        "stars": 4.7,
        "review_count": "Preview",
        "badge_text": "NEW \u00b7 SELF-CARE",
        "badge_style": 'style="background: #FCE7F3; color: #DB2777;"',
        "color_desc": "Pastel fruit trio (yellow, pink, peach)",
        "features": [
            (SVG["bath"], "3 Bath Bombs + Essential Oils"),
            (SVG["vibration"], "Waterproof Bullet (10 Modes)"),
            (SVG["waterproof"], "IPX7 Waterproof"),
            (SVG["battery"], "USB-C \u00b7 60min Battery"),
            (SVG["gift"], "Perfect Gift Set"),
            (SVG["silicone"], "Body-Safe Materials"),
        ],
        "feature_sections": [
            {
                "label": "The Ritual",
                "heading": "Bath time, <em>elevated</em>.",
                "text": "Three fruit-shaped bath bombs in lemon, strawberry, and peach. Each releases essential oils (citrus, berry, floral) as it fizzes away, turning your bath into a spa-grade self-care experience. And as the bomb dissolves, it reveals a surprise: a waterproof bullet vibrator sealed inside. Your bath just got a lot more interesting.",
                "image_num": "1",
                "bg": "",
            },
            {
                "label": "The Bullet",
                "heading": "10 modes. Fully <em>waterproof</em>.",
                "text": "The bullet inside Fizz isn't a novelty \u2014 it's a properly powerful vibrator with 10 modes, IPX7 waterproof rating, and USB-C charging. 60 minutes of battery life means it outlasts even your longest soak. Use it in the bath, out of the bath, wherever the mood takes you.",
                "image_num": "2",
                "bg": ' style="background: var(--cream-dark);"',
                "reverse": True,
            },
            {
                "label": "The Gift",
                "heading": "Self-care in a <em>box</em>.",
                "text": "Fizz is the ultimate 'treat yourself' moment \u2014 or the most memorable gift you'll ever give. Three bath bombs, one reusable bullet, and a whole evening of relaxation. The pastel fruit trio packaging looks like it belongs in a luxury spa. Because it does.",
                "image_num": "3",
                "bg": "",
            },
        ],
    },
    {
        "slug": "stem",
        "name": "Stem",
        "subtitle": "The Pendant",
        "category": "Jewelry Vibrator Necklace",
        "tagline": "Wear your pleasure. Literally.",
        "description": "A cherry-shaped pendant necklace in anodized metal that doubles as a discreet clitoral vibrator. Wear it to dinner. Use it after. The 18-inch chain is surgical steel. The pendant houses a powerful mini motor with 5 modes. Comes in a jewelry box because that's exactly what it is.",
        "price": 79,
        "compare_price": 149,
        "stars": 4.5,
        "review_count": "Preview",
        "badge_text": "NEW \u00b7 WEARABLE",
        "badge_style": 'style="background: #FEF3C7; color: #D97706;"',
        "color_desc": "Rose gold with cherry-red enamel",
        "features": [
            (SVG["jewelry"], "Surgical Steel Chain (18\u201d)"),
            (SVG["vibration"], "5 Vibration Modes"),
            (SVG["magnetic"], "Magnetic USB Charging"),
            (SVG["waterproof"], "IPX6 Splash-Proof"),
            (SVG["battery"], "45min Battery"),
            (SVG["compact"], "Jewelry Box Packaging"),
        ],
        "feature_sections": [
            {
                "label": "The Disguise",
                "heading": "Jewelry that <em>vibrates</em>.",
                "text": "Stem is a cherry-shaped pendant in anodized aluminum with cherry-red enamel and rose gold accents. On the outside, it's a beautiful, fashionable necklace. On the inside, it houses a powerful miniaturized motor with 5 vibration modes. The 18-inch surgical steel chain is hypoallergenic and skin-safe. Wear it anywhere.",
                "image_num": "1",
                "bg": "",
            },
            {
                "label": "Double Life",
                "heading": "Dinner to <em>dessert</em>.",
                "text": "Wear Stem to dinner, to work, to brunch. No one will know. The pendant detaches from the chain with a gentle twist, transforming from jewelry to pleasure tool in seconds. The smooth anodized surface is body-safe and easy to clean. Magnetic USB charging means no visible port \u2014 it's seamless in every way.",
                "image_num": "2",
                "bg": ' style="background: var(--cream-dark);"',
                "reverse": True,
            },
            {
                "label": "The Gift",
                "heading": "Comes in a <em>jewelry box</em>. Because it is.",
                "text": "Stem arrives in a premium velvet jewelry box that you'd be proud to give as a gift. IPX6 splash-proof. 45-minute battery. 5 discreet vibration modes. It's the most intimate piece of jewelry you'll ever own \u2014 and the most beautiful toy you'll ever use.",
                "image_num": "3",
                "bg": "",
            },
        ],
    },
    # ─── TIER 5: BOUNDARY-PUSHING ───
    {
        "slug": "berry-set",
        "name": "Berry Set",
        "subtitle": "The Explorer Set",
        "category": "Beginner Anal Training Set",
        "tagline": "New territory deserves a gentle guide.",
        "description": "Three graduated sizes in the softest medical-grade silicone. Berry Set is the first anal training kit that doesn't look like it belongs in a doctor's office. Pastel colors. Rounded shapes. Flared bases. T-bar handles. Designed with beginners in mind \u2014 because everyone starts somewhere, and it should feel welcoming, not clinical.",
        "price": 59,
        "compare_price": 109,
        "stars": 4.6,
        "review_count": "Preview",
        "badge_text": "NEW \u00b7 BEGINNER",
        "badge_style": 'style="background: #FCE7F3; color: #DB2777;"',
        "color_desc": "Pastel berry gradient (light pink to deep berry)",
        "features": [
            (SVG["graduated"], "3 Graduated Sizes (S/M/L)"),
            (SVG["silicone"], "Ultra-Soft Silicone"),
            (SVG["handsfree"], "Flared Safety Bases"),
            (SVG["squeeze"], "T-Bar Handles"),
            (SVG["bath"], "Dishwasher-Safe"),
            (SVG["gift"], "Velvet Storage Pouch"),
        ],
        "feature_sections": [
            {
                "label": "Designed for Beginners",
                "heading": "Start small. Go at <em>your pace</em>.",
                "text": "Berry Set's three graduated sizes (Small, Medium, Large) let you progress at your own pace. Each piece features a gently tapered tip, flared safety base, and T-bar handle for confident, comfortable use. The ultra-soft medical-grade silicone is the most flexible in the Nancy range \u2014 because comfort is non-negotiable for new experiences.",
                "image_num": "1",
                "bg": "",
            },
            {
                "label": "Beautiful, Not Clinical",
                "heading": "Pastel colors. <em>Zero</em> intimidation.",
                "text": "Berry Set graduates from light pink (Small) through rose (Medium) to deep berry (Large). The rounded, organic shapes look like abstract art, not medical equipment. Nancy designed this set to live proudly on your nightstand \u2014 because shame has no place in your bedroom.",
                "image_num": "2",
                "bg": ' style="background: var(--cream-dark);"',
                "reverse": True,
            },
            {
                "label": "Easy Care",
                "heading": "Dishwasher-safe. <em>Really.</em>",
                "text": "Berry Set is made from 100% body-safe, non-porous medical-grade silicone that's dishwasher-safe for effortless hygiene. Each set comes with a velvet storage pouch. No batteries, no charging, no complexity \u2014 just beautifully simple design that lets you focus on what matters.",
                "image_num": "3",
                "bg": "",
            },
        ],
    },
    {
        "slug": "cozy",
        "name": "Cozy",
        "subtitle": "The Secret Plushie",
        "category": "Plushie with Hidden Vibrator",
        "tagline": "Cute on the outside. Powerful on the inside. Just like you.",
        "description": "A kawaii 7-inch fruit plushie with a secret: a hidden magnetic pocket that holds a powerful removable bullet vibrator. The plushie sits cute on your bed. The bullet detaches for solo play. Inductive charging through the plushie's base \u2014 just set it on the wireless pad. The most discreet toy Nancy's ever made.",
        "price": 69,
        "compare_price": 119,
        "stars": 4.8,
        "review_count": "Preview",
        "badge_text": "NEW \u00b7 STEALTH",
        "badge_style": 'style="background: var(--lem-light); color: var(--lem-dark);"',
        "color_desc": "Lemon yellow plush (Lem character)",
        "features": [
            (SVG["plush"], '7" Plush Exterior'),
            (SVG["vibration"], "Removable Bullet (10 Modes)"),
            (SVG["magnetic"], "Magnetic Hidden Pocket"),
            (SVG["wireless"], "Inductive/Wireless Charging"),
            (SVG["waterproof"], "IPX6 Bullet"),
            (SVG["battery"], "90min Battery"),
        ],
        "feature_sections": [
            {
                "label": "The Secret",
                "heading": "Cute on the shelf. <em>Powerful</em> in your hand.",
                "text": "Cozy looks like a regular Nancy plushie \u2014 a cute 7-inch Lem character that sits sweetly on your bed. But hidden inside is a magnetic pocket containing a powerful removable bullet vibrator with 10 intensity modes. Pop it out, play, pop it back. No one will ever know.",
                "image_num": "1",
                "bg": "",
            },
            {
                "label": "Wireless Charging",
                "heading": "Just set it <em>down</em>.",
                "text": "No visible ports. No cables plugged into your plushie. Cozy charges inductively through its base \u2014 just set the plushie on the included wireless charging pad. The bullet charges inside the plushie. When the base glows gently, it's ready. The most seamless charging experience in the Nancy range.",
                "image_num": "2",
                "bg": ' style="background: var(--cream-dark);"',
                "reverse": True,
            },
            {
                "label": "Maximum Stealth",
                "heading": "The most discreet toy <em>ever</em>.",
                "text": "Roommates? Parents visiting? Cozy sits on your bed looking like an adorable plushie \u2014 because it IS an adorable plushie. The removable bullet is IPX6 splash-proof with 90 minutes of battery. 10 modes from gentle purr to powerful rumble. Your secret is safe with Lem.",
                "image_num": "3",
                "bg": "",
            },
        ],
    },
]

# ═══════════════════════════════════════════════════════════════════
# EXISTING OG PRODUCTS — for the collection page
# ═══════════════════════════════════════════════════════════════════
OG_PRODUCTS = [
    {
        "slug": "lem",
        "name": "Lem",
        "tagline": "Air-pulse lemon sensation",
        "price": 89,
        "compare_price": 149,
        "stars": "2,847 reviews",
        "tag_text": "#1 Bestseller",
        "tag_style": "",
        "hero_ext": "webp",
    },
    {
        "slug": "berri",
        "name": "Berri",
        "tagline": "Dual-motor strawberry bliss",
        "price": 99,
        "compare_price": 159,
        "stars": "1,923 reviews",
        "tag_text": "Bestseller",
        "tag_style": "",
        "hero_ext": "png",
    },
    {
        "slug": "avo",
        "name": "Avo",
        "tagline": "Couples' avocado vibrator",
        "price": 79,
        "compare_price": 129,
        "stars": "1,247 reviews",
        "tag_text": "For Two",
        "tag_style": ' style="background: var(--avo-light); color: var(--avo-dark);"',
        "hero_ext": "webp",
    },
    {
        "slug": "pixie",
        "name": "Pixie",
        "tagline": "Tiny but mighty",
        "price": 69,
        "compare_price": 109,
        "stars": "834 reviews",
        "tag_text": "New",
        "tag_style": ' style="background: #F3E8FF; color: #7C3AED;"',
        "hero_ext": "png",
    },
    {
        "slug": "lolly",
        "name": "Lolly",
        "tagline": "Lollipop tongue vibrator",
        "price": 59,
        "compare_price": 99,
        "stars": "612 reviews",
        "tag_text": "New",
        "tag_style": ' style="background: #FFF0E0; color: #EA580C;"',
        "hero_ext": "png",
    },
]

# ═══════════════════════════════════════════════════════════════════
# COLLECTION TIER DEFINITIONS
# ═══════════════════════════════════════════════════════════════════
COLLECTION_TIERS = [
    {
        "title": 'The <em style="font-family: var(--font-editorial); font-weight: 400;">Originals</em>',
        "subtitle": "The fruit squad that started it all.",
        "slugs": ["lem", "berri", "avo", "pixie", "lolly"],
        "is_og": True,
    },
    {
        "title": 'Hero <em style="font-family: var(--font-editorial); font-weight: 400;">Upgrades</em>',
        "subtitle": "Customer-validated evolutions of what you already love.",
        "slugs": ["mango", "fig", "cherry"],
        "is_og": False,
    },
    {
        "title": 'Market <em style="font-family: var(--font-editorial); font-weight: 400;">Innovators</em>',
        "subtitle": "Filling the gaps no one else saw.",
        "slugs": ["plum", "coconut", "grape"],
        "is_og": False,
    },
    {
        "title": 'Pushing <em style="font-family: var(--font-editorial); font-weight: 400;">Boundaries</em>',
        "subtitle": "New interactions. New sensations. New everything.",
        "slugs": ["peach", "melon", "dragonfruit"],
        "is_og": False,
    },
    {
        "title": 'Gift &amp; <em style="font-family: var(--font-editorial); font-weight: 400;">Entry</em>',
        "subtitle": "Perfect for first-timers and gift-givers.",
        "slugs": ["seed", "fizz", "stem"],
        "is_og": False,
    },
    {
        "title": 'The Bold <em style="font-family: var(--font-editorial); font-weight: 400;">Ones</em>',
        "subtitle": "For the curious, the adventurous, the unapologetic.",
        "slugs": ["berry-set", "cozy"],
        "is_og": False,
    },
]


# ═══════════════════════════════════════════════════════════════════
# HELPER: Generate PDP HTML
# ═══════════════════════════════════════════════════════════════════
def generate_pdp(product):
    """Generate a full PDP HTML page matching lem.html structure exactly."""
    p = product
    slug = p["slug"]
    name = p["name"]
    emoji = EMOJI_MAP.get(slug, "\U0001F351")
    save_pct = round((1 - p["price"] / p["compare_price"]) * 100)
    price_int = p["price"]

    # Build star display
    full_stars = int(p["stars"])
    has_half = (p["stars"] - full_stars) >= 0.5
    star_display = "\u2605" * full_stars
    if has_half:
        star_display += "\u2605"  # use full star for .5+ rounding up visually

    # Build features HTML
    features_html = ""
    for icon_svg, label in p["features"]:
        features_html += f"""          <div class="pdp-feature">
            {icon_svg}
            {label}
          </div>
"""

    # Build feature sections HTML
    feature_sections_html = ""
    for i, fs in enumerate(p["feature_sections"]):
        bg = fs.get("bg", "")
        reverse = fs.get("reverse", False)
        grid_class = "pdp-feature-grid reverse" if reverse else "pdp-feature-grid"
        feature_sections_html += f"""
  <!-- Feature {i+1}: {fs["label"]} -->
  <div class="pdp-feature-section"{bg}>
    <div class="container">
      <div class="{grid_class}">
        <div class="pdp-feature-image reveal">
          <img src="../../assets/products/{slug}-{fs["image_num"]}.png" alt="{name} {fs["label"].lower()}" onerror="this.src='../../assets/products/{slug}-hero.png'">
        </div>
        <div class="pdp-feature-text reveal">
          <span class="section-label">{fs["label"]}</span>
          <h3>{fs["heading"]}</h3>
          <p>{fs["text"]}</p>
        </div>
      </div>
    </div>
  </div>
"""

    # Build related products (pick 4 from the other products + OGs)
    all_slugs = [og["slug"] for og in OG_PRODUCTS] + [pr["slug"] for pr in PRODUCTS]
    related_slugs = [s for s in all_slugs if s != slug][:4]
    related_html = ""
    for rs in related_slugs:
        # find product data
        rp = None
        for og in OG_PRODUCTS:
            if og["slug"] == rs:
                rp = og
                break
        if rp is None:
            for pr in PRODUCTS:
                if pr["slug"] == rs:
                    rp = pr
                    break
        if rp is None:
            continue

        rname = rp["name"]
        rtagline = rp.get("tagline", "")
        rprice = rp["price"]
        rhero_ext = rp.get("hero_ext", "png")
        rtag_text = rp.get("tag_text", rp.get("badge_text", "New"))
        rtag_style = rp.get("tag_style", rp.get("badge_style", ""))

        related_html += f"""        <!-- {rname} -->
        <a href="../../pages/products/{rs}.html" class="product-card" data-tilt>
          <div class="product-card-image">
            <img src="../../assets/products/{rs}-hero.{rhero_ext}" alt="{rname} by Nancy" onerror="this.src='../../assets/products/{rs}-hero.png'">
            <span class="product-card-tag"{rtag_style}>{rtag_text}</span>
          </div>
          <div class="product-card-info">
            <h3>{rname}</h3>
            <p class="product-card-tagline">{rtagline}</p>
            <div class="product-card-price">
              <span class="product-card-current">US${rprice}</span>
            </div>
          </div>
        </a>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} \u2014 {p["subtitle"]} | Nancy</title>
<link rel="icon" type="image/svg+xml" href="../../nancy-logo-pink.svg">
<link rel="icon" type="image/png" href="../../nancy-logo-pink.png">
<meta name="description" content="Meet {name}. {p["tagline"]} {p["category"]}. Designed in Hong Kong. Loved in 50+ countries.">
<meta property="og:title" content="{name} \u2014 {p["subtitle"]} | Nancy">
<meta property="og:description" content="{p["tagline"]}">
<meta property="og:image" content="../../assets/products/{slug}-hero.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.shopify.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;0,9..144,800;1,9..144,400&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Semibold.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Regular.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Bold.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<!-- Nancy Universe CSS -->
<link rel="stylesheet" href="../../css/variables.css">
<link rel="stylesheet" href="../../css/base.css">
<link rel="stylesheet" href="../../css/animations.css">
<link rel="stylesheet" href="../../css/nav.css">
<link rel="stylesheet" href="../../css/components.css">
<link rel="stylesheet" href="../../css/cards.css">
<link rel="stylesheet" href="../../css/sections.css">
<link rel="stylesheet" href="../../css/footer.css">
<link rel="stylesheet" href="../../css/responsive.css">
<link rel="stylesheet" href="../../css/personality.css">
<link rel="stylesheet" href="../../css/loader.css">
<link rel="stylesheet" href="../../css/page-pdp.css">
<!-- Meta Pixel -->
<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '832767357702650');
fbq('track', 'PageView');
fbq('track', 'ViewContent', {{content_name: '{name}', content_type: 'product', value: {price_int}, currency: 'USD'}});
</script>
</head>
<body class="loading">
<script src="../../js/loader.js"></script>

<!-- Shared Partials -->
<div id="loader-placeholder"></div>
<div id="topbar-placeholder"></div>
<div id="nav-placeholder"></div>

<main>
  <div class="container">

    <!-- Breadcrumb -->
    <div class="breadcrumb">
      <a href="/">Home</a>
      <span class="sep">/</span>
      <a href="../../pages/collections/toys.html">Pleasure Toys</a>
      <span class="sep">/</span>
      <span class="current">{name}</span>
    </div>

    <!-- PDP Hero -->
    <div class="pdp-hero">

      <!-- Gallery Column -->
      <div class="pdp-gallery">
        <div class="pdp-gallery-main">
          <img id="pdp-main-img" src="../../assets/products/{slug}-hero.png" alt="{name} by Nancy \u2014 {p["category"].lower()}" onerror="this.style.background='linear-gradient(135deg, #f0f0f0, #e0e0e0)'; this.alt='Image coming soon';">
        </div>
        <div class="pdp-gallery-thumbs">
          <button class="active" aria-label="{name} hero image">
            <img src="../../assets/products/{slug}-hero.png" data-full="../../assets/products/{slug}-hero.png" alt="{name} hero" onerror="this.src='../../assets/products/{slug}-hero.png'">
          </button>
          <button aria-label="{name} product angle 1">
            <img src="../../assets/products/{slug}-1.png" data-full="../../assets/products/{slug}-1.png" alt="{name} angle 1" onerror="this.src='../../assets/products/{slug}-hero.png'">
          </button>
          <button aria-label="{name} product angle 2">
            <img src="../../assets/products/{slug}-2.png" data-full="../../assets/products/{slug}-2.png" alt="{name} angle 2" onerror="this.src='../../assets/products/{slug}-hero.png'">
          </button>
          <button aria-label="{name} product angle 3">
            <img src="../../assets/products/{slug}-3.png" data-full="../../assets/products/{slug}-3.png" alt="{name} angle 3" onerror="this.src='../../assets/products/{slug}-hero.png'">
          </button>
          <button aria-label="{name} product angle 4">
            <img src="../../assets/products/{slug}-4.png" data-full="../../assets/products/{slug}-4.png" alt="{name} angle 4" onerror="this.src='../../assets/products/{slug}-hero.png'">
          </button>
          <button aria-label="{name} lifestyle">
            <img src="../../assets/products/{slug}-5.png" data-full="../../assets/products/{slug}-5.png" alt="{name} lifestyle" onerror="this.src='../../assets/products/{slug}-hero.png'">
          </button>
        </div>
      </div>

      <!-- Info Column -->
      <div class="pdp-info">
        <div class="pdp-character-badge" {p["badge_style"]}>
          <span>{emoji}</span> {p["badge_text"]}
        </div>

        <h1 class="pdp-title">{name}</h1>
        <p class="pdp-tagline">{p["tagline"]}</p>

        <!-- Rating -->
        <div class="pdp-rating">
          <span class="pdp-stars">{star_display}</span>
          <span class="pdp-rating-text">{p["stars"]} out of 5 \u00b7 {p["review_count"]}</span>
        </div>

        <!-- Price -->
        <div class="pdp-price">
          <span class="pdp-price-current">US${p["price"]}</span>
          <span class="pdp-price-compare">US${p["compare_price"]}</span>
          <span class="pdp-price-save">Save {save_pct}%</span>
        </div>

        <!-- Description -->
        <div class="pdp-description" style="margin-bottom: 1.5rem;">
          <p style="font-size: 0.95rem; line-height: 1.7; color: var(--gray-600);">{p["description"]}</p>
        </div>

        <!-- Key Features -->
        <div class="pdp-features">
{features_html}        </div>

        <!-- Add to Cart -->
        <button class="pdp-add-to-cart" onclick="window.open('https://hellonancy.co', '_blank')">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
          Add to Cart \u2014 US${p["price"]}
        </button>

        <!-- Trust Badges -->
        <div class="pdp-trust">
          <div class="pdp-trust-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="22" height="18" rx="2"/><line x1="1" y1="9" x2="23" y2="9"/></svg>
            Free shipping over $89
          </div>
          <div class="pdp-trust-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            1-year warranty
          </div>
          <div class="pdp-trust-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            Discreet packaging
          </div>
        </div>
      </div>
    </div>

  </div><!-- /container -->

  <!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
       FEATURE SECTIONS
       \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 -->
{feature_sections_html}
  <!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
       RELATED PRODUCTS
       \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 -->
  <section class="pdp-related">
    <div class="container">
      <div class="section-header" style="text-align: center;">
        <h2 style="font-family: var(--font-display); font-size: clamp(1.5rem, 2.5vw, 2rem); font-weight: 800; letter-spacing: -0.03em;">You might also <em style="font-family: var(--font-editorial); font-weight: 400;">love</em></h2>
      </div>
      <div class="pdp-related-grid">
{related_html}      </div>
    </div>
  </section>

  <!-- Newsletter -->
  <section class="pdp-newsletter">
    <div class="container">
      <div class="newsletter-box">
        <div class="newsletter-text">
          <h3 style="font-family: var(--font-display); font-size: 1.8rem; font-weight: 800; letter-spacing: -0.02em;">Join the <em style="font-family: var(--font-editorial); font-weight: 400;">Fruit Club</em></h3>
          <p>Get 10% off your first order, early access to drops, and content that actually matters.</p>
        </div>
        <form class="newsletter-form" onsubmit="event.preventDefault();">
          <input type="email" placeholder="Your email" required>
          <button type="submit">Join \u2192</button>
        </form>
      </div>
    </div>
  </section>

</main>

<!-- Footer -->
<div id="footer-placeholder"></div>

<!-- Scripts -->
<script src="../../js/includes.js"></script>
<script src="../../js/gallery.js"></script>
<script src="../../js/main.js"></script>
<script src="../../js/personality.js"></script>
</body>
</html>
"""
    return html


# ═══════════════════════════════════════════════════════════════════
# HELPER: Generate collection card HTML for a product
# ═══════════════════════════════════════════════════════════════════
def generate_collection_card_og(og):
    """Generate a product card for an OG product."""
    return f"""      <!-- {og["name"]} -->
      <a href="../../pages/products/{og["slug"]}.html" class="product-card reveal" data-tilt>
        <div class="product-card-image">
          <img src="../../assets/products/{og["slug"]}-hero.{og["hero_ext"]}" alt="{og["name"]} by Nancy">
          <span class="product-card-tag"{og["tag_style"]}>{og["tag_text"]}</span>
        </div>
        <div class="product-card-info">
          <div class="product-card-badge">
            <span class="product-card-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
            <span class="product-card-reviews">{og["stars"]}</span>
          </div>
          <h3>{og["name"]}</h3>
          <p class="product-card-tagline">{og["tagline"]}</p>
          <div class="product-card-price">
            <span class="product-card-current">US${og["price"]}</span>
            <span class="product-card-compare">US${og["compare_price"]}</span>
          </div>
        </div>
      </a>
"""


def generate_collection_card_new(product):
    """Generate a product card for a new product."""
    p = product
    return f"""      <!-- {p["name"]} -->
      <a href="../../pages/products/{p["slug"]}.html" class="product-card reveal" data-tilt>
        <div class="product-card-image">
          <img src="../../assets/products/{p["slug"]}-hero.png" alt="{p["name"]} by Nancy" onerror="this.src='../../assets/products/{p["slug"]}-hero.png'">
          <span class="product-card-tag" {p["badge_style"]}>{p["badge_text"]}</span>
        </div>
        <div class="product-card-info">
          <div class="product-card-badge">
            <span class="product-card-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
            <span class="product-card-reviews">{p["stars"]}/5 Preview</span>
          </div>
          <h3>{p["name"]}</h3>
          <p class="product-card-tagline">{p["tagline"]}</p>
          <div class="product-card-price">
            <span class="product-card-current">US${p["price"]}</span>
            <span class="product-card-compare">US${p["compare_price"]}</span>
          </div>
        </div>
      </a>
"""


# ═══════════════════════════════════════════════════════════════════
# HELPER: Generate toys collection page
# ═══════════════════════════════════════════════════════════════════
def generate_toys_collection():
    """Generate the toys.html collection page with all 19 products in tiered sections."""

    # Build product lookup by slug
    new_product_map = {p["slug"]: p for p in PRODUCTS}
    og_product_map = {p["slug"]: p for p in OG_PRODUCTS}

    total_count = len(OG_PRODUCTS) + len(PRODUCTS)

    # Build tier sections
    sections_html = ""
    for tier in COLLECTION_TIERS:
        sections_html += f"""
    <!-- ═══════════════════════════════════════════════ -->
    <div class="collection-section-header">
      <h2>{tier["title"]}</h2>
      <p>{tier["subtitle"]}</p>
    </div>

    <div class="collection-grid">
"""
        for slug in tier["slugs"]:
            if slug in og_product_map:
                sections_html += generate_collection_card_og(og_product_map[slug])
            elif slug in new_product_map:
                sections_html += generate_collection_card_new(new_product_map[slug])

        sections_html += """    </div>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pleasure Toys \u2014 Nancy Universe</title>
<link rel="icon" type="image/svg+xml" href="../../nancy-logo-pink.svg">
<link rel="icon" type="image/png" href="../../nancy-logo-pink.png">
<meta name="description" content="Shop Nancy's full range of fruit-shaped pleasure toys. 19 products across 6 collections. Air-pulse, warming, smart, couples, wearable, and more. Designed in Hong Kong, loved in 50+ countries.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.shopify.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;0,9..144,800;1,9..144,400&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Semibold.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Regular.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Bold.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="../../css/variables.css">
<link rel="stylesheet" href="../../css/base.css">
<link rel="stylesheet" href="../../css/animations.css">
<link rel="stylesheet" href="../../css/nav.css">
<link rel="stylesheet" href="../../css/components.css">
<link rel="stylesheet" href="../../css/cards.css">
<link rel="stylesheet" href="../../css/sections.css">
<link rel="stylesheet" href="../../css/footer.css">
<link rel="stylesheet" href="../../css/responsive.css">
<link rel="stylesheet" href="../../css/personality.css">
<link rel="stylesheet" href="../../css/loader.css">
<link rel="stylesheet" href="../../css/page-collection.css">
<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '832767357702650');
fbq('track', 'PageView');
</script>
</head>
<body class="loading">
<script src="../../js/loader.js"></script>

<div id="loader-placeholder"></div>
<div id="topbar-placeholder"></div>
<div id="nav-placeholder"></div>

<main>
  <div class="container" style="padding-top: 1.5rem;">

    <div class="breadcrumb">
      <a href="/">Home</a>
      <span class="sep">/</span>
      <span class="current">Pleasure Toys</span>
    </div>

    <!-- Collection Hero -->
    <div class="collection-hero">
      <img src="../../assets/generated/v2/cat-pleasure-toys.png" alt="Nancy Pleasure Toys collection">
      <div class="collection-hero-overlay">
        <h1>Pleasure <em style="font-family: var(--font-editorial); font-weight: 400;">Toys</em></h1>
        <p>19 fruit-shaped toys. 6 collections. Infinite possibilities.</p>
      </div>
    </div>

    <!-- Feature Trust Strip -->
    <div class="collection-features">
      <div class="collection-feature-item">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
        <h4>Body-Safe</h4>
        <p>Medical-grade silicone</p>
      </div>
      <div class="collection-feature-item">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"></path></svg>
        <h4>Waterproof</h4>
        <p>IPX6\u2013IPX8 rated</p>
      </div>
      <div class="collection-feature-item">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
        <h4>1-Year Warranty</h4>
        <p>Hassle-free guarantee</p>
      </div>
      <div class="collection-feature-item">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 12 20 22 4 22 4 12"></polyline><rect x="2" y="7" width="20" height="5"></rect><line x1="12" y1="22" x2="12" y2="7"></line><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"></path><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"></path></svg>
        <h4>Discreet Shipping</h4>
        <p>Plain box, no labels</p>
      </div>
    </div>

    <!-- Sort Bar -->
    <div class="collection-bar">
      <span class="collection-count">Showing {total_count} products</span>
      <div class="collection-sort">
        <label for="sort-select">Sort by:</label>
        <select id="sort-select">
          <option>Bestselling</option>
          <option>Price: Low to High</option>
          <option>Price: High to Low</option>
          <option>Newest</option>
        </select>
      </div>
    </div>
{sections_html}
  </div>

  <!-- Newsletter -->
  <section class="pdp-newsletter" style="padding: var(--space-lg) 0 var(--space-xl);">
    <div class="container">
      <div class="newsletter-box">
        <div class="newsletter-text">
          <h3 style="font-family: var(--font-display); font-size: 1.8rem; font-weight: 800; letter-spacing: -0.02em;">Join the <em style="font-family: var(--font-editorial); font-weight: 400;">Fruit Club</em></h3>
          <p>Get 10% off your first order, early access to drops, and content that actually matters.</p>
        </div>
        <form class="newsletter-form" onsubmit="event.preventDefault();">
          <input type="email" placeholder="Your email" required>
          <button type="submit">Join \u2192</button>
        </form>
      </div>
    </div>
  </section>

</main>

<div id="footer-placeholder"></div>

<script src="../../js/includes.js"></script>
<script src="../../js/main.js"></script>
<script src="../../js/personality.js"></script>
</body>
</html>
"""
    return html


# ═══════════════════════════════════════════════════════════════════
# MAIN — Generate all files
# ═══════════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("Nancy Universe — New Toys Generator")
    print("=" * 60)

    # 1. Generate PDP pages for each new product
    print("\n--- Generating PDP pages ---")
    for product in PRODUCTS:
        html = generate_pdp(product)
        filepath = os.path.join(PRODUCTS_DIR, f"{product['slug']}.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  [OK] {product['name']:15s} -> pages/products/{product['slug']}.html")

    # 2. Generate updated toys collection page
    print("\n--- Generating toys collection page ---")
    html = generate_toys_collection()
    filepath = os.path.join(COLLECTIONS_DIR, "toys.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [OK] toys.html -> pages/collections/toys.html")

    # Summary
    print("\n" + "=" * 60)
    print(f"Generated {len(PRODUCTS)} PDP pages + 1 collection page")
    print(f"Total products in collection: {len(OG_PRODUCTS) + len(PRODUCTS)}")
    print("=" * 60)
    print("\nAll files written to:")
    print(f"  PDPs:       {PRODUCTS_DIR}/")
    print(f"  Collection: {COLLECTIONS_DIR}/toys.html")
    print("\nDone!")


if __name__ == "__main__":
    main()
