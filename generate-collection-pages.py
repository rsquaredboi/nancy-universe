#!/usr/bin/env python3
"""Nancy Universe — Collection Page Generator
Generates the master plushies.html and fashion.html collection pages
showing ALL products in a long scrollable grid, organized by wave/category.

Imports data from:
  - generate-all-pdps.py (PLUSH_WAVES)
  - generate-fashion-pdps.py (FASHION_CATEGORIES)
"""

import os
import sys
import importlib.util
import html as html_mod

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────
# Import data from sibling generator files
# ─────────────────────────────────────────────

def import_module_from_file(module_name, file_path):
    """Import a Python module from an arbitrary file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

plush_mod = import_module_from_file("generate_all_pdps", os.path.join(BASE_DIR, "generate-all-pdps.py"))
fashion_mod = import_module_from_file("generate_fashion_pdps", os.path.join(BASE_DIR, "generate-fashion-pdps.py"))

PLUSH_WAVES = plush_mod.PLUSH_WAVES
FASHION_CATEGORIES = fashion_mod.FASHION_CATEGORIES

# ─────────────────────────────────────────────
# OG Five plushies — special treatment
# ─────────────────────────────────────────────

OG_FIVE = [
    {"name": "Lem",   "slug": "lem",   "tagline": "Your sunshine sidekick",  "reviews": 1247, "tag": "Bestseller", "price": 29, "tag_bg": "var(--lem-light)",   "tag_color": "var(--lem-dark)"},
    {"name": "Berri", "slug": "berri", "tagline": "Sweet &amp; fierce",      "reviews": 983,  "tag": "Bestseller", "price": 29, "tag_bg": "var(--berri-light)", "tag_color": "var(--berri-dark)"},
    {"name": "Avo",   "slug": "avo",   "tagline": "Calm &amp; grounding",    "reviews": 712,  "tag": "OG",         "price": 29, "tag_bg": "var(--avo-light)",   "tag_color": "var(--avo-dark)"},
    {"name": "Pixie", "slug": "pixie", "tagline": "Tiny but mighty",         "reviews": 534,  "tag": "OG",         "price": 29, "tag_bg": "#F3E8FF",           "tag_color": "#7C3AED"},
    {"name": "Lolly", "slug": "lolly", "tagline": "Sweet on everyone",       "reviews": 621,  "tag": "OG",         "price": 29, "tag_bg": "#FFF0E0",           "tag_color": "#EA580C"},
]

# ─────────────────────────────────────────────
# Shared HTML head template
# ─────────────────────────────────────────────

def build_head(title, meta_desc):
    """Build the HTML head section with title and meta description."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} &mdash; Nancy Universe</title>
<link rel="icon" type="image/svg+xml" href="../../nancy-logo-pink.svg">
<link rel="icon" type="image/png" href="../../nancy-logo-pink.png">
<meta name="description" content="{meta_desc}">
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
</head>'''

BODY_OPEN = '''
<body class="loading">
<script src="../../js/loader.js"></script>

<div id="loader-placeholder"></div>
<div id="topbar-placeholder"></div>
<div id="nav-placeholder"></div>

<main>
  <div class="container" style="padding-top: 1.5rem;">
'''

NEWSLETTER = '''
  <!-- NEWSLETTER CTA -->
  <section class="pdp-newsletter" style="padding: var(--space-lg) 0 var(--space-xl);">
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
'''

FOOTER = '''
</main>

<div id="footer-placeholder"></div>

<script src="../../js/includes.js"></script>
<script src="../../js/main.js"></script>
<script src="../../js/personality.js"></script>
</body>
</html>'''


# ═══════════════════════════════════════════════
#  PLUSHIES COLLECTION PAGE
# ═══════════════════════════════════════════════

def generate_plushies_page():
    """Generate pages/collections/plushies.html with ALL plushies by wave."""

    # Count total plushies
    new_plush_count = sum(len(w["characters"]) for w in PLUSH_WAVES)
    total_count = 5 + new_plush_count  # OG Five + new waves

    parts = []

    # Head
    parts.append(build_head(
        title="Plushies",
        meta_desc=f"Nancy Universe plushies — {total_count} kawaii characters across 10 waves. Super soft, machine washable, gift-ready. Lem, Berri, Avo and {total_count - 3} more. Collect them all.",
    ))

    # Body open
    parts.append(BODY_OPEN)

    # Breadcrumb
    parts.append('''    <div class="breadcrumb">
      <a href="/">Home</a>
      <span class="sep">/</span>
      <span class="current">Plushies</span>
    </div>
''')

    # Hero banner
    parts.append(f'''    <!-- HERO BANNER -->
    <div class="collection-hero">
      <img src="../../assets/generated/v2/cat-plushies.png" alt="Nancy Plushies collection — all fruit characters">
      <div class="collection-hero-overlay">
        <h1><em style="font-family: var(--font-editorial); font-weight: 400;">Plushies</em></h1>
        <p>{total_count} kawaii characters. Collect them all.</p>
      </div>
    </div>
''')

    # Feature trust strip
    parts.append(f'''    <!-- FEATURE TRUST STRIP -->
    <div class="collection-features">
      <div class="collection-feature-item">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
        <h4>Super Soft</h4>
        <p>100% polyester fill</p>
      </div>
      <div class="collection-feature-item">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"></path><circle cx="12" cy="12" r="3"></circle></svg>
        <h4>Machine Washable</h4>
        <p>Easy care, always fresh</p>
      </div>
      <div class="collection-feature-item">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
        <h4>{total_count} Characters</h4>
        <p>A friend for everyone</p>
      </div>
      <div class="collection-feature-item">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 12 20 22 4 22 4 12"></polyline><rect x="2" y="7" width="20" height="5"></rect><line x1="12" y1="22" x2="12" y2="7"></line><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"></path><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"></path></svg>
        <h4>Gift-Ready</h4>
        <p>Arrives in character box</p>
      </div>
    </div>
''')

    # Sort bar
    parts.append(f'''    <!-- SORT BAR -->
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
''')

    # ── WAVE 1: The OG Five ──
    parts.append('''    <!-- ═══════════════════════════════════════════════
         WAVE 1: THE OG FIVE
         ═══════════════════════════════════════════════ -->
    <div class="collection-section-header">
      <h2>The OG <em style="font-family: var(--font-editorial); font-weight: 400;">Five</em></h2>
      <p>The original fruit squad. Where it all started.</p>
    </div>

    <div class="collection-grid">
''')

    for og in OG_FIVE:
        parts.append(f'''      <a href="../products/plush-{og["slug"]}.html" class="product-card reveal" data-tilt>
        <div class="product-card-image">
          <img src="../../assets/plushies/{og["slug"]}/{og["slug"]}-hero.png" alt="{og["name"]} Plush" onerror="this.src='../../assets/generated/plush-{og["slug"]}.png'">
          <span class="product-card-tag" style="background: {og["tag_bg"]}; color: {og["tag_color"]};">{og["tag"]}</span>
        </div>
        <div class="product-card-info">
          <div class="product-card-badge">
            <span class="product-card-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
            <span class="product-card-reviews">{og["reviews"]:,} reviews</span>
          </div>
          <h3>{og["name"]}</h3>
          <p class="product-card-tagline">{og["tagline"]}</p>
          <div class="product-card-price">
            <span class="product-card-current">US${og["price"]}</span>
          </div>
        </div>
      </a>

''')

    parts.append('    </div>\n\n')

    # ── Waves 2-10 ──
    for wave in PLUSH_WAVES:
        wave_num = wave["wave"]
        wave_name = wave["name"]
        wave_tagline = wave["tagline"]
        chars = wave["characters"]

        parts.append(f'''    <!-- ═══════════════════════════════════════════════
         WAVE {wave_num}: {wave_name.upper()}
         ═══════════════════════════════════════════════ -->
    <div class="collection-section-header">
      <h2>Wave {wave_num}: <em style="font-family: var(--font-editorial); font-weight: 400;">{wave_name}</em></h2>
      <p>{html_mod.escape(wave_tagline)}</p>
    </div>

    <div class="collection-grid">
''')

        for char in chars:
            slug = char["slug"]
            name = char["name"]
            tagline = html_mod.escape(char.get("tagline", char.get("vibe", "")))
            price = char.get("price", 29)
            wave_tag = wave_name

            parts.append(f'''      <a href="../products/plush-{slug}.html" class="product-card reveal" data-tilt>
        <div class="product-card-image">
          <img src="../../assets/plushies/{slug}/{slug}-hero.png" alt="{name} Plush" onerror="this.src='../../assets/generated/plush-{slug}.png'">
          <span class="product-card-tag">{wave_tag}</span>
        </div>
        <div class="product-card-info">
          <h3>{name}</h3>
          <p class="product-card-tagline">{tagline}</p>
          <div class="product-card-price">
            <span class="product-card-current">US${price}</span>
          </div>
        </div>
      </a>

''')

        parts.append('    </div>\n\n')

    # Close container
    parts.append('  </div><!-- end .container -->\n')

    # Newsletter
    parts.append(NEWSLETTER)

    # Footer
    parts.append(FOOTER)

    return ''.join(parts)


# ═══════════════════════════════════════════════
#  FASHION COLLECTION PAGE
# ═══════════════════════════════════════════════

def generate_fashion_page():
    """Generate pages/collections/fashion.html with ALL fashion items by category."""

    # Count total fashion items
    total_count = sum(len(cat["items"]) for cat in FASHION_CATEGORIES)

    parts = []

    # Head
    parts.append(build_head(
        title="Fashion",
        meta_desc=f"Nancy Universe fashion — {total_count} items across 6 categories. Tees, hoodies, bottoms, headwear, accessories, and home goods. Wear the universe.",
    ))

    # Body open
    parts.append(BODY_OPEN)

    # Breadcrumb
    parts.append('''    <div class="breadcrumb">
      <a href="/">Home</a>
      <span class="sep">/</span>
      <span class="current">Fashion</span>
    </div>
''')

    # Hero banner
    parts.append(f'''    <!-- HERO BANNER -->
    <div class="collection-hero">
      <img src="../../assets/generated/v2/cat-fashion.png" alt="Nancy Fashion collection — apparel and accessories">
      <div class="collection-hero-overlay">
        <h1><em style="font-family: var(--font-editorial); font-weight: 400;">Fashion</em></h1>
        <p>{total_count} items across 6 categories. Wear the universe.</p>
      </div>
    </div>
''')

    # Feature trust strip
    parts.append(f'''    <!-- FEATURE TRUST STRIP -->
    <div class="collection-features">
      <div class="collection-feature-item">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
        <h4>Premium Materials</h4>
        <p>Organic cotton &amp; more</p>
      </div>
      <div class="collection-feature-item">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"></path><circle cx="12" cy="12" r="3"></circle></svg>
        <h4>Pre-Washed</h4>
        <p>No shrinkage surprises</p>
      </div>
      <div class="collection-feature-item">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
        <h4>{total_count} Products</h4>
        <p>6 categories</p>
      </div>
      <div class="collection-feature-item">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 12 20 22 4 22 4 12"></polyline><rect x="2" y="7" width="20" height="5"></rect><line x1="12" y1="22" x2="12" y2="7"></line><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"></path><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"></path></svg>
        <h4>Unisex Fit</h4>
        <p>Designed for everyone</p>
      </div>
    </div>
''')

    # Sort bar
    parts.append(f'''    <!-- SORT BAR -->
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
''')

    # ── Each category ──
    for cat in FASHION_CATEGORIES:
        cat_name = cat["name"]
        cat_tagline = cat.get("tagline", "")
        items = cat["items"]

        parts.append(f'''    <!-- ═══════════════════════════════════════════════
         {cat_name.upper()}
         ═══════════════════════════════════════════════ -->
    <div class="collection-section-header">
      <h2><em style="font-family: var(--font-editorial); font-weight: 400;">{cat_name}</em></h2>
      <p>{html_mod.escape(cat_tagline)}</p>
    </div>

    <div class="collection-grid">
''')

        for item in items:
            slug = item["slug"]
            name = item["name"]
            tagline = html_mod.escape(item.get("tagline", ""))
            price = item.get("price", 0)
            category_tag = cat_name

            parts.append(f'''      <a href="../products/fashion-{slug}.html" class="product-card reveal" data-tilt>
        <div class="product-card-image">
          <img src="../../assets/fashion/{slug}/{slug}-hero.png" alt="{name}" onerror="this.src='../../assets/generated/fashion-{slug}.png'">
          <span class="product-card-tag">{category_tag}</span>
        </div>
        <div class="product-card-info">
          <h3>{name}</h3>
          <p class="product-card-tagline">{tagline}</p>
          <div class="product-card-price">
            <span class="product-card-current">US${price}</span>
          </div>
        </div>
      </a>

''')

        parts.append('    </div>\n\n')

    # Close container
    parts.append('  </div><!-- end .container -->\n')

    # Newsletter
    parts.append(NEWSLETTER)

    # Footer
    parts.append(FOOTER)

    return ''.join(parts)


# ═══════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════

def main():
    collections_dir = os.path.join(BASE_DIR, "pages", "collections")
    os.makedirs(collections_dir, exist_ok=True)

    # Generate plushies page
    plushies_path = os.path.join(collections_dir, "plushies.html")
    plushies_html = generate_plushies_page()
    with open(plushies_path, "w", encoding="utf-8") as f:
        f.write(plushies_html)

    # Count plushies
    new_count = sum(len(w["characters"]) for w in PLUSH_WAVES)
    total_plush = 5 + new_count
    print(f"[OK] Generated plushies.html — {total_plush} total products ({len(PLUSH_WAVES)} waves + OG Five)")
    print(f"     -> {plushies_path}")

    # Generate fashion page
    fashion_path = os.path.join(collections_dir, "fashion.html")
    fashion_html = generate_fashion_page()
    with open(fashion_path, "w", encoding="utf-8") as f:
        f.write(fashion_html)

    # Count fashion
    total_fashion = sum(len(cat["items"]) for cat in FASHION_CATEGORIES)
    print(f"[OK] Generated fashion.html — {total_fashion} total products ({len(FASHION_CATEGORIES)} categories)")
    print(f"     -> {fashion_path}")

    print(f"\nDone. {total_plush + total_fashion} total product cards generated across 2 collection pages.")


if __name__ == "__main__":
    main()
