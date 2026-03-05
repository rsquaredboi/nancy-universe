#!/usr/bin/env python3
"""Generate shop-all.html with all 250 products organized by category."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, 'products-data.json')) as f:
    products = json.load(f)

# Sort into categories
pleasure = [p for p in products if p['category'] == 'pleasure']
plush = [p for p in products if p['category'] == 'plush']
fashion = [p for p in products if p['category'] == 'fashion']

# Sort each alphabetically by name
pleasure.sort(key=lambda p: p['name'])
plush.sort(key=lambda p: p['name'])
fashion.sort(key=lambda p: p['name'])

total = len(products)

def make_card(p, reveal=True):
    """Generate a product card HTML."""
    href = f"../../pages/products/{p['filename']}"
    img = p['image']
    # PNG fallback
    fallback = img.replace('.webp', '.png')
    name = p['name']
    tagline = p['tagline']
    price = p['price']

    # Tag based on category
    if p['category'] == 'pleasure':
        tag = '<span class="product-card-tag">Bestseller</span>'
    elif p['category'] == 'plush':
        tag = '<span class="product-card-tag" style="background: var(--lem-light); color: var(--lem-dark);">Plush</span>'
    else:
        tag = '<span class="product-card-tag" style="background: var(--pink-light); color: var(--pink);">Fashion</span>'

    reveal_cls = ' reveal' if reveal else ''

    return f'''      <a href="{href}" class="product-card{reveal_cls}">
        <div class="product-card-image">
          <img loading="lazy" decoding="async" src="{img}" alt="{name}" onerror="this.onerror=null;this.src='{fallback}'">
          {tag}
        </div>
        <div class="product-card-info">
          <h3>{name}</h3>
          <p class="product-card-tagline">{tagline}</p>
          <div class="product-card-price">
            <span class="product-card-current">{price}</span>
          </div>
        </div>
      </a>'''

def make_section(title, emoji, products_list, cat_id):
    """Generate a category section with all products."""
    cards = '\n'.join(make_card(p) for p in products_list)
    return f'''
    <!-- {title} -->
    <div class="shop-section" id="{cat_id}">
      <h2 class="shop-section-title">{emoji} {title} <span class="shop-section-count">{len(products_list)}</span></h2>
      <div class="collection-grid">
{cards}
      </div>
    </div>'''

# Build page
sections = []
sections.append(make_section('Pleasure Toys', '🍋', pleasure, 'pleasure'))
sections.append(make_section('Plushies', '🧸', plush, 'plushies'))
sections.append(make_section('Fashion & Accessories', '👗', fashion, 'fashion'))

sections_html = '\n'.join(sections)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shop All — Nancy Universe</title>
<link rel="icon" type="image/svg+xml" href="../../nancy-logo-pink.svg">
<link rel="icon" type="image/png" href="../../nancy-logo-pink.png">
<meta name="description" content="Explore the full Nancy collection — {total} products across pleasure toys, plushies, fashion, and accessories.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.shopify.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;0,9..144,800;1,9..144,400&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Semibold.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Regular.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Bold.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="../../css/style.min.css">
<style>
/* Shop All — Category Filter Pills */
.shop-filters {{
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
  padding: 0.5rem 0;
}}
.shop-filter-pill {{
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1.1rem;
  border-radius: 100px;
  font-size: 0.85rem;
  font-weight: 600;
  font-family: var(--font-body);
  cursor: pointer;
  border: 1.5px solid var(--gray-200);
  background: white;
  color: var(--dark);
  transition: all 0.2s ease;
  text-decoration: none;
}}
.shop-filter-pill:hover {{
  border-color: var(--pink);
  color: var(--pink);
}}
.shop-filter-pill.active {{
  background: var(--pink);
  color: white;
  border-color: var(--pink);
}}
/* Section Titles */
.shop-section {{
  margin-bottom: 1rem;
}}
.shop-section-title {{
  font-family: var(--font-display);
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin-bottom: 1.5rem;
  padding-bottom: 0.8rem;
  border-bottom: 2px solid var(--gray-100);
  color: var(--dark);
}}
.shop-section-count {{
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--gray-400);
  margin-left: 0.5rem;
}}
/* Make grid 4-col on wide desktop for this page */
@media (min-width: 1100px) {{
  .shop-all-page .collection-grid {{
    grid-template-columns: repeat(4, 1fr);
    gap: 1.2rem;
  }}
}}
@media (max-width: 1099px) and (min-width: 769px) {{
  .shop-all-page .collection-grid {{
    grid-template-columns: repeat(3, 1fr);
  }}
}}
@media (max-width: 768px) {{
  .shop-all-page .collection-grid {{
    grid-template-columns: repeat(2, 1fr);
    gap: 0.8rem;
  }}
  .shop-section-title {{
    font-size: 1.3rem;
  }}
  .shop-filter-pill {{
    font-size: 0.8rem;
    padding: 0.4rem 0.9rem;
  }}
}}
</style>
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

<main class="shop-all-page">
  <div class="container" style="padding-top: 1.5rem;">

    <div class="breadcrumb">
      <a href="/">Home</a>
      <span class="sep">/</span>
      <span class="current">Shop All</span>
    </div>

    <!-- Collection Hero -->
    <div class="collection-hero">
      <img loading="lazy" decoding="async" src="../../assets/generated/hero-lifestyle-wide.webp" alt="Nancy Universe collection" onerror="this.onerror=null;this.src='../../assets/generated/hero-lifestyle-wide.png'">
      <div class="collection-hero-overlay">
        <h1>Shop <em style="font-family: var(--font-editorial); font-weight: 400;">All</em></h1>
        <p>{total} products. The full Nancy Universe.</p>
      </div>
    </div>

    <!-- Filter Pills -->
    <div class="shop-filters">
      <a href="#" class="shop-filter-pill active" data-filter="all">All Products</a>
      <a href="#pleasure" class="shop-filter-pill" data-filter="pleasure">🍋 Pleasure Toys</a>
      <a href="#plushies" class="shop-filter-pill" data-filter="plushies">🧸 Plushies</a>
      <a href="#fashion" class="shop-filter-pill" data-filter="fashion">👗 Fashion</a>
    </div>

    <!-- Filter Bar -->
    <div class="collection-bar">
      <span class="collection-count" id="product-count">Showing all {total} products</span>
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

    <!-- Product Sections -->
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
          <button type="submit">Join &rarr;</button>
        </form>
      </div>
    </div>
  </section>

</main>

<div id="footer-placeholder"></div>

<script src="../../js/includes.js"></script>
<script src="../../js/main.js"></script>
<script src="../../js/personality.js"></script>
<script>
// Category filter
(function() {{
  const pills = document.querySelectorAll('.shop-filter-pill');
  const sections = document.querySelectorAll('.shop-section');
  const countEl = document.getElementById('product-count');
  const totals = {{}};
  sections.forEach(s => {{
    totals[s.id] = s.querySelectorAll('.product-card').length;
  }});
  const totalAll = Object.values(totals).reduce((a,b) => a+b, 0);

  pills.forEach(pill => {{
    pill.addEventListener('click', (e) => {{
      e.preventDefault();
      const filter = pill.dataset.filter;
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');

      if (filter === 'all') {{
        sections.forEach(s => s.style.display = '');
        countEl.textContent = `Showing all ${{totalAll}} products`;
      }} else {{
        sections.forEach(s => {{
          s.style.display = s.id === filter ? '' : 'none';
        }});
        countEl.textContent = `Showing ${{totals[filter]}} products`;
      }}

      // Smooth scroll to top of products
      document.querySelector('.shop-filters').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }});
  }});
}})();
</script>
</body>
</html>
'''

# Write the shop-all page
out_path = os.path.join(BASE, 'pages', 'collections', 'shop-all.html')
with open(out_path, 'w') as f:
    f.write(html)

print(f"Generated shop-all.html with {total} products")
print(f"  Pleasure: {len(pleasure)}")
print(f"  Plush: {len(plush)}")
print(f"  Fashion: {len(fashion)}")
print(f"  File size: {os.path.getsize(out_path) / 1024:.0f} KB")
