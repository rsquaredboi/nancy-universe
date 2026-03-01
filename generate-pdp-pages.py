#!/usr/bin/env python3
"""Generate PDP pages for all 15 plush characters from a template."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "pages", "products")

PLUSHIES = [
    {"name": "Lem", "slug": "lem", "fruit": "lemon", "emoji": "🍋", "tagline": "Your sunshine sidekick.", "color_bg": "var(--lem-light)", "color_fg": "var(--lem-dark)", "badge_class": "lem", "personality": "Bold, sunny, and always the first to cheer you up. Lem is pure golden energy — the friend who texts you good morning every day and means it.", "reviews": 1247, "rating": "4.9"},
    {"name": "Berri", "slug": "berri", "fruit": "strawberry", "emoji": "🍓", "tagline": "Sweet and fierce.", "color_bg": "var(--berri-light)", "color_fg": "var(--berri-dark)", "badge_class": "berri", "personality": "Don't let the sweetness fool you — Berri has opinions and isn't afraid to share them. Loyal, fierce, and always ready for adventure.", "reviews": 983, "rating": "4.8"},
    {"name": "Avo", "slug": "avo", "fruit": "avocado", "emoji": "🥑", "tagline": "Calm and grounding.", "color_bg": "var(--avo-light)", "color_fg": "var(--avo-dark)", "badge_class": "avo", "personality": "The zen master of the fruit family. Avo brings calm to chaos, wisdom to uncertainty, and the best hugs in the universe.", "reviews": 712, "rating": "4.9"},
    {"name": "Pixie", "slug": "pixie", "fruit": "grape", "emoji": "🍇", "tagline": "Tiny but mighty.", "color_bg": "#F3E8FF", "color_fg": "#7C3AED", "badge_class": "pixie", "personality": "Small but mighty, Pixie packs more personality per centimeter than anyone. Mischievous, playful, and always up to something.", "reviews": 534, "rating": "4.8"},
    {"name": "Lolly", "slug": "lolly", "fruit": "lollipop", "emoji": "🍭", "tagline": "Sweet on everyone.", "color_bg": "#FFF0E0", "color_fg": "#EA580C", "badge_class": "lolly", "personality": "The social butterfly of the crew. Lolly is warm, bubbly, and makes everyone feel like the most important person in the room.", "reviews": 421, "rating": "4.7"},
    {"name": "Mango", "slug": "mango", "fruit": "mango", "emoji": "🥭", "tagline": "Tropical adventurer.", "color_bg": "#FFF3E0", "color_fg": "#E65100", "badge_class": "mango", "personality": "Always dreaming of the next adventure. Mango brings tropical warmth and a can-do attitude to everything. The friend who says yes to everything.", "reviews": 0, "rating": "—"},
    {"name": "Kiwi", "slug": "kiwi", "fruit": "kiwi", "emoji": "🥝", "tagline": "Quirky and surprising.", "color_bg": "#E8F5E9", "color_fg": "#2E7D32", "badge_class": "kiwi", "personality": "Fuzzy on the outside, full of surprises on the inside. Kiwi is the friend who always has the most interesting take on everything.", "reviews": 0, "rating": "—"},
    {"name": "Peachy", "slug": "peachy", "fruit": "peach", "emoji": "🍑", "tagline": "Warm and affectionate.", "color_bg": "#FFF0F0", "color_fg": "#D84315", "badge_class": "peachy", "personality": "Soft-spoken but deeply caring. Peachy gives the warmest hugs and remembers every little thing about you. The emotional heart of the group.", "reviews": 0, "rating": "—"},
    {"name": "Coco", "slug": "coco", "fruit": "coconut", "emoji": "🥥", "tagline": "Tough outside, sweet inside.", "color_bg": "#EFEBE9", "color_fg": "#4E342E", "badge_class": "coco", "personality": "Hard shell, soft heart. Coco takes a while to open up, but once you're in, you've got a friend for life. Tough love, real love.", "reviews": 0, "rating": "—"},
    {"name": "Cherry", "slug": "cherry", "fruit": "cherry", "emoji": "🍒", "tagline": "Inseparable best friends.", "color_bg": "#FFEBEE", "color_fg": "#C62828", "badge_class": "cherry", "personality": "Two cherries, one stem — the ultimate duo. Cherry represents the bonds that can't be broken. Always better together.", "reviews": 0, "rating": "—"},
    {"name": "Melon", "slug": "melon", "fruit": "watermelon", "emoji": "🍉", "tagline": "Refreshing and laid-back.", "color_bg": "#E8F5E9", "color_fg": "#1B5E20", "badge_class": "melon", "personality": "Cool as a slice on a summer day. Melon is the chill friend who never stresses, always refreshes, and makes everything feel easy.", "reviews": 0, "rating": "—"},
    {"name": "Figgy", "slug": "figgy", "fruit": "fig", "emoji": "🫐", "tagline": "Wise and mysterious.", "color_bg": "#EDE7F6", "color_fg": "#4527A0", "badge_class": "figgy", "personality": "Old soul energy in a tiny plush body. Figgy is the philosopher of the group — deep, mysterious, and somehow always right.", "reviews": 0, "rating": "—"},
    {"name": "Plummy", "slug": "plummy", "fruit": "plum", "emoji": "🫐", "tagline": "Elegant and sophisticated.", "color_bg": "#F3E5F5", "color_fg": "#6A1B9A", "badge_class": "plummy", "personality": "Grace, poise, and a hint of drama. Plummy brings elegance to the fruit family — the one who always looks put together.", "reviews": 0, "rating": "—"},
    {"name": "Papaya", "slug": "papaya", "fruit": "papaya", "emoji": "🍈", "tagline": "Exotic and free-spirited.", "color_bg": "#FFF3E0", "color_fg": "#BF360C", "badge_class": "papaya", "personality": "Free spirit who dances to their own beat. Papaya is exotic, expressive, and brings a little bit of paradise wherever they go.", "reviews": 0, "rating": "—"},
    {"name": "Guava", "slug": "guava", "fruit": "guava", "emoji": "🍏", "tagline": "Vibrant and energetic.", "color_bg": "#F1F8E9", "color_fg": "#33691E", "badge_class": "guava", "personality": "Bursting with energy from the moment they wake up. Guava is the hype friend — vibrant, positive, and impossible to ignore.", "reviews": 0, "rating": "—"},
]

def get_related(current_slug):
    """Get 4 related plushies (not the current one)."""
    others = [p for p in PLUSHIES if p["slug"] != current_slug]
    # Pick first 4
    return others[:4]

def generate_pdp(plush):
    slug = plush["slug"]
    name = plush["name"]
    emoji = plush["emoji"]
    tagline = plush["tagline"]
    color_bg = plush["color_bg"]
    color_fg = plush["color_fg"]
    badge_class = plush["badge_class"]
    personality = plush["personality"]
    reviews = plush["reviews"]
    rating = plush["rating"]

    # Image paths
    hero_img = f"../../assets/plushies/{slug}/{slug}-hero.png"

    # Gallery thumbs — hero + 5 lifestyle/angle shots
    shot_types = ["hero", "angle", "lifestyle-bed", "lifestyle-desk", "in-hand", "flatlay"]
    gallery_thumbs = ""
    for i, shot in enumerate(shot_types):
        img_path = f"../../assets/plushies/{slug}/{slug}-{shot}.png"
        active = ' class="active"' if i == 0 else ""
        label = {"hero": "product view", "angle": "side angle", "lifestyle-bed": "bedroom scene", "lifestyle-desk": "desk scene", "in-hand": "scale view", "flatlay": "gift flatlay"}
        gallery_thumbs += f"""          <button{active} aria-label="{name} {label.get(shot, shot)}">
            <img src="{img_path}" data-full="{img_path}" alt="{name} {shot}" onerror="this.src='{hero_img}'">
          </button>
"""

    # Reviews section
    review_text = f'<span class="pdp-rating-text">{rating} out of 5 · {reviews:,} reviews</span>' if reviews > 0 else '<span class="pdp-rating-text">New arrival — be the first to review</span>'
    stars = "★★★★★" if reviews > 0 else "☆☆☆☆☆"

    # Related products
    related = get_related(slug)
    related_html = ""
    for r in related:
        related_html += f"""        <a href="plush-{r['slug']}.html" class="product-card" data-tilt>
          <div class="product-card-image">
            <img src="../../assets/plushies/{r['slug']}/{r['slug']}-hero.png" alt="{r['name']} Plush" onerror="this.src='../../assets/generated/plush-{r['slug']}.png'">
          </div>
          <div class="product-card-info">
            <h3>{r['name']}</h3>
            <p class="product-card-tagline">{r['tagline']}</p>
            <div class="product-card-price">
              <span class="product-card-current">US$29</span>
            </div>
          </div>
        </a>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} Plush — Nancy Universe</title>
<link rel="icon" type="image/svg+xml" href="../../nancy-logo-pink.svg">
<link rel="icon" type="image/png" href="../../nancy-logo-pink.png">
<meta name="description" content="Meet {name}. {tagline} A super-soft, machine-washable kawaii {plush['fruit']} plush toy from Nancy Universe. 25cm of pure huggable joy.">
<meta property="og:title" content="{name} Plush — Nancy Universe">
<meta property="og:description" content="{tagline} Kawaii {plush['fruit']} plush from Nancy.">
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
fbq('track', 'ViewContent', {{content_name: '{name} Plush', content_type: 'product', value: 29, currency: 'USD'}});
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
      <a href="../../pages/collections/plushies.html">Plushies</a>
      <span class="sep">/</span>
      <span class="current">{name}</span>
    </div>

    <!-- PDP Hero -->
    <div class="pdp-hero">

      <!-- Gallery -->
      <div class="pdp-gallery">
        <div class="pdp-gallery-main">
          <img id="pdp-main-img" src="{hero_img}" alt="{name} Plush — kawaii {plush['fruit']} plush toy from Nancy Universe">
        </div>
        <div class="pdp-gallery-thumbs">
{gallery_thumbs}        </div>
      </div>

      <!-- Info -->
      <div class="pdp-info">
        <div class="pdp-character-badge" style="background: {color_bg}; color: {color_fg};">
          <span>{emoji}</span> {name} Collection
        </div>

        <h1 class="pdp-title">{name}</h1>
        <p class="pdp-tagline">{tagline}</p>

        <div class="pdp-rating">
          <span class="pdp-stars">{stars}</span>
          {review_text}
        </div>

        <div class="pdp-price">
          <span class="pdp-price-current">US$29</span>
        </div>

        <div class="pdp-features">
          <div class="pdp-feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            Super Soft Plush
          </div>
          <div class="pdp-feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"/></svg>
            Machine Washable
          </div>
          <div class="pdp-feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
            25cm / 9.8&Prime;
          </div>
          <div class="pdp-feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg>
            Gift-Ready Box
          </div>
          <div class="pdp-feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            100% Polyester Fill
          </div>
          <div class="pdp-feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 12s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>
            Embroidered Face
          </div>
        </div>

        <button class="pdp-add-to-cart">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
          Add to Cart &mdash; US$29
        </button>

        <div class="pdp-trust">
          <div class="pdp-trust-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="22" height="18" rx="2"/><line x1="1" y1="9" x2="23" y2="9"/></svg>
            Free shipping over $89
          </div>
          <div class="pdp-trust-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            Gift wrapping available
          </div>
          <div class="pdp-trust-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            Join 50K+ collectors
          </div>
        </div>
      </div>
    </div>

  </div>

  <!-- Feature 1: Character Personality -->
  <div class="pdp-feature-section">
    <div class="container">
      <div class="pdp-feature-grid">
        <div class="pdp-feature-image reveal">
          <img src="../../assets/plushies/{slug}/{slug}-lifestyle-bed.png" alt="{name} plush lifestyle" onerror="this.src='{hero_img}'">
        </div>
        <div class="pdp-feature-text reveal">
          <span class="section-label">Meet {name}</span>
          <h3>{tagline.rstrip('.')}</h3>
          <p>{personality}</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Feature 2: Quality -->
  <div class="pdp-feature-section" style="background: var(--cream-dark);">
    <div class="container">
      <div class="pdp-feature-grid reverse">
        <div class="pdp-feature-image reveal">
          <img src="../../assets/plushies/{slug}/{slug}-in-hand.png" alt="{name} plush in hand showing scale" onerror="this.src='{hero_img}'">
        </div>
        <div class="pdp-feature-text reveal">
          <span class="section-label">Quality You Can Feel</span>
          <h3>Soft enough to <em>sleep with.</em></h3>
          <p>Every {name} plush is made from premium polyester plush fabric with a 100% polyester fill. Embroidered face details mean no choking hazards and a face that lasts. Machine washable, air dry. 25cm of pure huggable joy.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Feature 3: Gifting -->
  <div class="pdp-feature-section">
    <div class="container">
      <div class="pdp-feature-grid">
        <div class="pdp-feature-image reveal">
          <img src="../../assets/plushies/{slug}/{slug}-flatlay.png" alt="{name} plush gift flatlay" onerror="this.src='{hero_img}'">
        </div>
        <div class="pdp-feature-text reveal">
          <span class="section-label">The Perfect Gift</span>
          <h3>Arrives <em>gift-ready.</em></h3>
          <p>Each {name} comes in its own character box with a personality card. From birthdays to &ldquo;just because&rdquo; — it&rsquo;s the kind of gift that gets an instant smile. Add a message at checkout.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Related Products -->
  <section class="pdp-related">
    <div class="container">
      <div class="section-header" style="text-align: center;">
        <h2 style="font-family: var(--font-display); font-size: clamp(1.5rem, 2.5vw, 2rem); font-weight: 800; letter-spacing: -0.03em;">More fruit <em style="font-family: var(--font-editorial); font-weight: 400;">friends</em></h2>
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
    for plush in PLUSHIES:
        filename = f"plush-{plush['slug']}.html"
        filepath = os.path.join(OUT_DIR, filename)
        html = generate_pdp(plush)
        with open(filepath, "w") as f:
            f.write(html)
        print(f"[OK] Generated {filename}")
    print(f"\n[DONE] Generated {len(PLUSHIES)} PDP pages in {OUT_DIR}")
