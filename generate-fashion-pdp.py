#!/usr/bin/env python3
"""Nancy Universe — Fashion PDP Page Generator
Generates product detail pages for all 10 fashion items."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "pages", "products")

FASHION = [
    {
        "name": "Fruit Club Tee",
        "slug": "fruit-club-tee",
        "type": "t-shirt",
        "color": "white",
        "design": "small 'Fruit Club' text logo with tiny fruit icons on chest",
        "price": 45,
        "tagline": "The everyday essential.",
        "description": "The tee that started it all. A perfectly weighted 220gsm organic cotton tee with a subtle Fruit Club chest logo surrounded by tiny fruit icons. The kind of tee you reach for every morning.",
        "details": "100% GOTS-certified organic cotton. Pre-shrunk. Relaxed unisex fit in sizes XS–XXL. Printed with water-based inks that get softer with every wash.",
        "badge_bg": "#F5F5F5",
        "badge_fg": "#333",
        "badge_text": "ESSENTIALS",
        "emoji": "👕",
        "features": [
            ("100% Organic Cotton", "heart"),
            ("Pre-Shrunk", "wash"),
            ("Unisex XS–XXL", "size"),
            ("Water-Based Inks", "leaf"),
            ("Relaxed Fit", "shirt"),
            ("Machine Washable", "wash2"),
        ],
        "related_exclude": 0,
    },
    {
        "name": "Lem Graphic Tee",
        "slug": "lem-graphic-tee",
        "type": "t-shirt",
        "color": "pale yellow",
        "design": "large Lem character illustration on front",
        "price": 45,
        "tagline": "Bold lemon energy.",
        "description": "Lem takes center stage on this statement tee. A full-size illustration of everyone's favourite sunshine character, screen-printed on soft pale yellow organic cotton.",
        "details": "220gsm organic cotton. Oversized front graphic with premium screen-print. Unisex relaxed fit, XS–XXL. Yellow that actually looks good — trust us.",
        "badge_bg": "#FFF9C4",
        "badge_fg": "#F57F17",
        "badge_text": "LEM COLLECTION",
        "emoji": "🍋",
        "features": [
            ("100% Organic Cotton", "heart"),
            ("Screen-Printed", "print"),
            ("Unisex XS–XXL", "size"),
            ("Statement Graphic", "star"),
            ("Pre-Shrunk", "wash"),
            ("Machine Washable", "wash2"),
        ],
        "related_exclude": 1,
    },
    {
        "name": "Berri Crop Top",
        "slug": "berri-crop-top",
        "type": "crop top",
        "color": "pink",
        "design": "small embroidered strawberry on chest, cropped fit",
        "price": 38,
        "tagline": "Sweet & cropped.",
        "description": "A cropped silhouette with a tiny hand-embroidered strawberry on the chest. Made from soft pink organic cotton with a relaxed, boxy cut that pairs with everything.",
        "details": "200gsm organic cotton. Cropped length hits at natural waist. Boxy relaxed fit in XS–XL. Hand-embroidered Berri character on chest.",
        "badge_bg": "#FCE4EC",
        "badge_fg": "#C62828",
        "badge_text": "BERRI COLLECTION",
        "emoji": "🍓",
        "features": [
            ("100% Organic Cotton", "heart"),
            ("Hand-Embroidered", "needle"),
            ("Cropped Length", "crop"),
            ("Boxy Fit XS–XL", "size"),
            ("Pre-Shrunk", "wash"),
            ("Machine Washable", "wash2"),
        ],
        "related_exclude": 2,
    },
    {
        "name": "Avo Hoodie",
        "slug": "avo-hoodie",
        "type": "oversized hoodie",
        "color": "sage green",
        "design": "embroidered avocado character on chest, kangaroo pocket",
        "price": 85,
        "tagline": "Cozy avocado vibes.",
        "description": "The hoodie you'll cancel plans for. 380gsm heavyweight organic cotton fleece with a tiny embroidered Avo on the chest, kangaroo pocket, and the kind of softness that makes everything better.",
        "details": "380gsm heavyweight organic cotton fleece. Pre-washed for zero shrinkage. Raglan sleeves, kangaroo pocket, ribbed cuffs. Oversized unisex fit XS–XXL.",
        "badge_bg": "#E8F5E9",
        "badge_fg": "#2E7D32",
        "badge_text": "AVO COLLECTION",
        "emoji": "🥑",
        "features": [
            ("380gsm Heavyweight", "weight"),
            ("Organic Cotton Fleece", "heart"),
            ("Embroidered Detail", "needle"),
            ("Kangaroo Pocket", "pocket"),
            ("Oversized Fit", "size"),
            ("Pre-Washed", "wash"),
        ],
        "related_exclude": 3,
    },
    {
        "name": "Squad Goals Sweatshirt",
        "slug": "squad-sweatshirt",
        "type": "crewneck sweatshirt",
        "color": "cream/off-white",
        "design": "all 5 original fruit characters in a row across chest",
        "price": 75,
        "tagline": "The whole crew on your chest.",
        "description": "All five OG fruit characters in a row — Lem, Berri, Avo, Pixie, and Lolly — screen-printed across the chest of a premium cream crewneck. The ultimate squad flex.",
        "details": "340gsm organic cotton fleece. Brushed interior for extra softness. Ribbed collar, cuffs, and hem. Relaxed unisex fit XS–XXL.",
        "badge_bg": "#FFF8E1",
        "badge_fg": "#E65100",
        "badge_text": "SQUAD COLLECTION",
        "emoji": "🍇",
        "features": [
            ("340gsm Premium Weight", "weight"),
            ("Organic Cotton Fleece", "heart"),
            ("Screen-Printed Squad", "print"),
            ("Brushed Interior", "soft"),
            ("Ribbed Cuffs & Hem", "detail"),
            ("Unisex XS–XXL", "size"),
        ],
        "related_exclude": 4,
    },
    {
        "name": "Pixie Bucket Hat",
        "slug": "pixie-bucket-hat",
        "type": "bucket hat",
        "color": "lavender purple",
        "design": "small embroidered grape character on front, short brim",
        "price": 35,
        "tagline": "Grape shade.",
        "description": "Sun protection with personality. A lavender bucket hat with a tiny embroidered Pixie grape character on the front and a perfectly proportioned short brim.",
        "details": "100% organic cotton twill. Embroidered Pixie character. Short brim with topstitched edge. One size fits most (adjustable inner drawstring).",
        "badge_bg": "#EDE7F6",
        "badge_fg": "#6A1B9A",
        "badge_text": "PIXIE COLLECTION",
        "emoji": "🍇",
        "features": [
            ("Organic Cotton Twill", "heart"),
            ("Embroidered Pixie", "needle"),
            ("UPF 30+ Protection", "sun"),
            ("One Size Fits Most", "size"),
            ("Inner Drawstring", "adjust"),
            ("Short Brim", "hat"),
        ],
        "related_exclude": 5,
    },
    {
        "name": "Lolly Socks Set",
        "slug": "lolly-socks-set",
        "type": "crew socks 3-pack",
        "color": "multicolor — pink, yellow, green pairs",
        "design": "each pair has a different fruit character knitted into the ankle",
        "price": 22,
        "tagline": "Sweet feet trio.",
        "description": "Three pairs of crew socks, each featuring a different fruit character knitted into the ankle. Pink (Berri), yellow (Lem), and green (Avo). The gift that actually gets worn.",
        "details": "80% organic cotton, 18% nylon, 2% elastane. Cushioned sole. Reinforced heel and toe. Fits US 6–12 / EU 39–46.",
        "badge_bg": "#FFF3E0",
        "badge_fg": "#E65100",
        "badge_text": "LOLLY COLLECTION",
        "emoji": "🍭",
        "features": [
            ("3-Pack Set", "pack"),
            ("80% Organic Cotton", "heart"),
            ("Cushioned Sole", "comfort"),
            ("Reinforced Heel & Toe", "durable"),
            ("Fits US 6–12", "size"),
            ("Character Knit Detail", "detail"),
        ],
        "related_exclude": 6,
    },
    {
        "name": "Nancy Logo Cap",
        "slug": "nancy-logo-cap",
        "type": "dad cap / baseball cap",
        "color": "black",
        "design": "embroidered Nancy logo in pink on front, adjustable strap",
        "price": 32,
        "tagline": "Classic Nancy.",
        "description": "The cap that goes with everything. A classic dad cap silhouette in black with the Nancy logo embroidered in signature pink. Adjustable buckle strap for the perfect fit.",
        "details": "100% organic cotton twill. Six-panel construction. Pre-curved brim. Embroidered Nancy logo. Adjustable metal buckle strap. One size.",
        "badge_bg": "#212121",
        "badge_fg": "#F48FB1",
        "badge_text": "NANCY CLASSICS",
        "emoji": "🧢",
        "features": [
            ("Organic Cotton Twill", "heart"),
            ("Embroidered Logo", "needle"),
            ("Adjustable Strap", "adjust"),
            ("Pre-Curved Brim", "hat"),
            ("Six-Panel", "detail"),
            ("One Size", "size"),
        ],
        "related_exclude": 7,
    },
    {
        "name": "Tropical Shorts",
        "slug": "tropical-shorts",
        "type": "casual shorts",
        "color": "pastel tie-dye (pink, yellow, green)",
        "design": "all-over fruit pattern print, elastic waist, relaxed fit",
        "price": 45,
        "tagline": "Fruit print paradise.",
        "description": "Summer in a pair of shorts. A pastel tie-dye base covered in an all-over fruit character print. Elastic waist, side pockets, and a relaxed fit that works for beach days and lazy Sundays.",
        "details": "100% organic cotton poplin. All-over digital print. Elastic waistband with internal drawstring. Side pockets. Relaxed fit XS–XXL.",
        "badge_bg": "#F3E5F5",
        "badge_fg": "#7B1FA2",
        "badge_text": "TROPICAL COLLECTION",
        "emoji": "🩳",
        "features": [
            ("100% Organic Cotton", "heart"),
            ("All-Over Print", "print"),
            ("Elastic Waist", "comfort"),
            ("Side Pockets", "pocket"),
            ("Relaxed Fit", "size"),
            ("Digital Printed", "detail"),
        ],
        "related_exclude": 8,
    },
    {
        "name": "Fruit Tote Bag",
        "slug": "fruit-tote-bag",
        "type": "canvas tote bag",
        "color": "natural canvas / cream",
        "design": "printed fruit characters scattered across bag, cotton handles",
        "price": 28,
        "tagline": "Carry the squad.",
        "description": "A heavyweight canvas tote with the full fruit squad scattered across both sides. Long cotton handles for comfortable over-the-shoulder carry. Roomy enough for groceries, gym, or life.",
        "details": "12oz organic cotton canvas. Screen-printed both sides. Internal pocket. Long handles (26\" drop). 15\" W × 16\" H × 4\" D.",
        "badge_bg": "#FFF8E1",
        "badge_fg": "#F57F17",
        "badge_text": "ACCESSORIES",
        "emoji": "👜",
        "features": [
            ("12oz Cotton Canvas", "weight"),
            ("Printed Both Sides", "print"),
            ("Internal Pocket", "pocket"),
            ("Long Handles", "carry"),
            ("Roomy Interior", "size"),
            ("Machine Washable", "wash"),
        ],
        "related_exclude": 9,
    },
]

# SVG icons for features
FEATURE_SVGS = {
    "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    "wash": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"/></svg>',
    "wash2": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"/></svg>',
    "size": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.9C15.5 4.9 17 3.5 17 3.5s1.5 4.5-.5 10.5c-1.3 3.8-5 6-5.5 6z"/><path d="M10 21.5c0-2.5 1.5-5 3-7"/></svg>',
    "shirt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.38 3.46L16 2 12 5 8 2 3.62 3.46a2 2 0 0 0-1.34 1.47l-.38 1.57 4.1 2 V22h12V8.5l4.1-2-.38-1.57a2 2 0 0 0-1.34-1.47z"/></svg>',
    "print": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>',
    "star": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    "needle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "crop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6.13 1L6 16a2 2 0 0 0 2 2h15"/><path d="M1 6.13L16 6a2 2 0 0 1 2 2v15"/></svg>',
    "weight": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>',
    "pocket": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 7V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v3"/></svg>',
    "soft": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    "detail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    "sun": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>',
    "adjust": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/></svg>',
    "hat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "pack": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/></svg>',
    "comfort": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    "durable": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "carry": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 7V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v3"/></svg>',
}


def get_svg(key):
    return FEATURE_SVGS.get(key, FEATURE_SVGS["heart"])


def get_related(items, exclude_idx):
    """Get 4 related fashion items, excluding the current one."""
    related = []
    for i, item in enumerate(items):
        if i != exclude_idx:
            related.append(item)
        if len(related) == 4:
            break
    return related


def generate_page(item, all_items):
    slug = item["slug"]
    name = item["name"]
    price = item["price"]
    emoji = item["emoji"]
    asset_dir = f"../../assets/fashion/{slug}"
    hero_img = f"{asset_dir}/{slug}-hero.png"

    # Gallery shots for fashion: hero, flatlay, model-front, detail, lifestyle-street, lifestyle
    gallery_shots = [
        ("hero", f"{name} product view", f"{name} hero"),
        ("flatlay", f"{name} flat lay", f"{name} flatlay"),
        ("model-front", f"{name} on model", f"{name} model"),
        ("detail", f"{name} detail close-up", f"{name} detail"),
        ("lifestyle-street", f"{name} street style", f"{name} street"),
        ("lifestyle", f"{name} lifestyle", f"{name} lifestyle"),
    ]

    features_html = ""
    for feat_name, feat_icon in item["features"]:
        features_html += f"""          <div class="pdp-feature">
            {get_svg(feat_icon)}
            {feat_name}
          </div>\n"""

    thumbs_html = ""
    for i, (shot, label, alt) in enumerate(gallery_shots):
        active = ' class="active"' if i == 0 else ""
        img_src = f"{asset_dir}/{slug}-{shot}.png"
        thumbs_html += f"""          <button{active} aria-label="{label}">
            <img src="{img_src}" data-full="{img_src}" alt="{alt}" onerror="this.src='{hero_img}'">
          </button>\n"""

    related = get_related(all_items, item["related_exclude"])
    related_html = ""
    for r in related:
        r_slug = r["slug"]
        related_html += f"""        <a href="fashion-{r_slug}.html" class="product-card" data-tilt>
          <div class="product-card-image">
            <img src="../../assets/fashion/{r_slug}/{r_slug}-hero.png" alt="{r['name']}">
          </div>
          <div class="product-card-info">
            <h3>{r['name']}</h3>
            <p class="product-card-tagline">{r['tagline']}</p>
            <div class="product-card-price">
              <span class="product-card-current">US${r['price']}</span>
            </div>
          </div>
        </a>\n"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} — Nancy Universe</title>
<link rel="icon" type="image/svg+xml" href="../../nancy-logo-pink.svg">
<link rel="icon" type="image/png" href="../../nancy-logo-pink.png">
<meta name="description" content="{item['tagline']} {item['description'][:100]}">
<meta property="og:title" content="{name} — Nancy Universe">
<meta property="og:description" content="{item['tagline']} Nancy Universe fashion.">
<meta property="og:image" content="{hero_img}">
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
<link rel="stylesheet" href="../../css/page-pdp.css">
<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '832767357702650');
fbq('track', 'PageView');
fbq('track', 'ViewContent', {{content_name: '{name}', content_type: 'product', value: {price}, currency: 'USD'}});
</script>
</head>
<body class="loading">
<script src="../../js/loader.js"></script>

<div id="loader-placeholder"></div>
<div id="topbar-placeholder"></div>
<div id="nav-placeholder"></div>

<main>
  <div class="container">

    <div class="breadcrumb">
      <a href="/">Home</a>
      <span class="sep">/</span>
      <a href="../../pages/collections/fashion.html">Fashion</a>
      <span class="sep">/</span>
      <span class="current">{name}</span>
    </div>

    <!-- PDP Hero -->
    <div class="pdp-hero">

      <!-- Gallery -->
      <div class="pdp-gallery">
        <div class="pdp-gallery-main">
          <img id="pdp-main-img" src="{hero_img}" alt="{name} — {item['type']} from Nancy Universe">
        </div>
        <div class="pdp-gallery-thumbs">
{thumbs_html}        </div>
      </div>

      <!-- Info -->
      <div class="pdp-info">
        <div class="pdp-character-badge" style="background: {item['badge_bg']}; color: {item['badge_fg']};">
          <span>{emoji}</span> {item['badge_text']}
        </div>

        <h1 class="pdp-title">{name}</h1>
        <p class="pdp-tagline">{item['tagline']}</p>

        <div class="pdp-rating">
          <span class="pdp-stars">&starf;&starf;&starf;&starf;&starf;</span>
          <span class="pdp-rating-text">New — be the first to review</span>
        </div>

        <div class="pdp-price">
          <span class="pdp-price-current">US${price}</span>
        </div>

        <div class="pdp-features">
{features_html}        </div>

        <button class="pdp-add-to-cart">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
          Add to Cart &mdash; US${price}
        </button>

        <div class="pdp-trust">
          <div class="pdp-trust-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="22" height="18" rx="2"/><line x1="1" y1="9" x2="23" y2="9"/></svg>
            Free shipping over $89
          </div>
          <div class="pdp-trust-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            100% organic cotton
          </div>
          <div class="pdp-trust-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            30-day returns
          </div>
        </div>
      </div>
    </div>

  </div>

  <!-- Feature 1: Product Story -->
  <div class="pdp-feature-section">
    <div class="container">
      <div class="pdp-feature-grid">
        <div class="pdp-feature-image reveal">
          <img src="{asset_dir}/{slug}-hero.png" alt="{name}" onerror="this.src='{hero_img}'">
        </div>
        <div class="pdp-feature-text reveal">
          <span class="section-label">The Details</span>
          <h3>{item['tagline'].rstrip('.')}</h3>
          <p>{item['description']}</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Feature 2: Materials -->
  <div class="pdp-feature-section" style="background: var(--cream-dark);">
    <div class="container">
      <div class="pdp-feature-grid reverse">
        <div class="pdp-feature-image reveal">
          <img src="{asset_dir}/{slug}-hero.png" alt="{name} materials detail" onerror="this.src='{hero_img}'">
        </div>
        <div class="pdp-feature-text reveal">
          <span class="section-label">Materials &amp; Fit</span>
          <h3>Made to <em>last.</em></h3>
          <p>{item['details']}</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Feature 3: Sustainability -->
  <div class="pdp-feature-section">
    <div class="container">
      <div class="pdp-feature-grid">
        <div class="pdp-feature-image reveal">
          <img src="{asset_dir}/{slug}-hero.png" alt="{name} sustainable fashion" onerror="this.src='{hero_img}'">
        </div>
        <div class="pdp-feature-text reveal">
          <span class="section-label">Sustainability</span>
          <h3>Fashion that feels <em>good.</em></h3>
          <p>Every Nancy fashion piece uses GOTS-certified organic cotton, water-based inks, and responsible manufacturing. Because looking good shouldn&rsquo;t cost the planet.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Related Products -->
  <section class="pdp-related">
    <div class="container">
      <div class="section-header" style="text-align: center;">
        <h2 style="font-family: var(--font-display); font-size: clamp(1.5rem, 2.5vw, 2rem); font-weight: 800; letter-spacing: -0.03em;">More from <em style="font-family: var(--font-editorial); font-weight: 400;">Fashion</em></h2>
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
          <button type="submit">Join &rarr;</button>
        </form>
      </div>
    </div>
  </section>

</main>

<div id="footer-placeholder"></div>

<script src="../../js/includes.js"></script>
<script src="../../js/gallery.js"></script>
<script src="../../js/main.js"></script>
<script src="../../js/personality.js"></script>
</body>
</html>"""

    return html


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for item in FASHION:
        filename = f"fashion-{item['slug']}.html"
        filepath = os.path.join(OUT_DIR, filename)
        html = generate_page(item, FASHION)
        with open(filepath, "w") as f:
            f.write(html)
        print(f"[OK] {filename}")
    print(f"\n[DONE] Generated {len(FASHION)} fashion PDP pages.")
