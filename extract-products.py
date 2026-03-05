#!/usr/bin/env python3
"""
Extract product data from all PDP HTML files in pages/products/
and output a JSON array to products-data.json.
"""

import os
import re
import json
from html.parser import HTMLParser

PRODUCTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages", "products")
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products-data.json")


def classify(filename):
    """Determine product category from filename."""
    if filename.startswith("plush-"):
        return "plush"
    elif filename.startswith("fashion-"):
        return "fashion"
    else:
        return "pleasure"


def extract_from_html(filepath):
    """Extract product data from a single HTML file using regex."""
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # Product name from <h1 class="pdp-title">
    name_match = re.search(r'class="pdp-title"[^>]*>([^<]+)</h1>', html)
    name = name_match.group(1).strip() if name_match else None

    # Tagline from <p class="pdp-tagline">
    tagline_match = re.search(r'class="pdp-tagline"[^>]*>([^<]+)</p>', html)
    tagline = tagline_match.group(1).strip() if tagline_match else None

    # Price from <span class="pdp-price-current">
    price_match = re.search(r'class="pdp-price-current"[^>]*>([^<]+)</span>', html)
    price = price_match.group(1).strip() if price_match else None

    # Hero image from id="pdp-main-img" src="..."
    img_match = re.search(r'id="pdp-main-img"\s+src="([^"]+)"', html)
    if not img_match:
        # Some files have loading/decoding attributes before id
        img_match = re.search(r'id="pdp-main-img"[^>]*\ssrc="([^"]+)"', html)
    image = img_match.group(1).strip() if img_match else None

    return name, tagline, price, image


def main():
    products = []
    errors = []

    files = sorted(f for f in os.listdir(PRODUCTS_DIR) if f.endswith(".html"))

    for filename in files:
        filepath = os.path.join(PRODUCTS_DIR, filename)
        category = classify(filename)

        try:
            name, tagline, price, image = extract_from_html(filepath)

            if not name:
                errors.append(f"  WARN: No name found in {filename}")

            products.append({
                "filename": filename,
                "name": name or filename.replace(".html", "").replace("-", " ").title(),
                "tagline": tagline or "",
                "price": price or "",
                "image": image or "",
                "category": category
            })
        except Exception as e:
            errors.append(f"  ERROR: {filename}: {e}")

    # Write JSON output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    # Summary
    print(f"Extracted {len(products)} products to {OUTPUT_FILE}")
    cats = {}
    for p in products:
        cats[p["category"]] = cats.get(p["category"], 0) + 1
    for cat, count in sorted(cats.items()):
        print(f"  {cat}: {count}")

    if errors:
        print(f"\n{len(errors)} warnings/errors:")
        for e in errors:
            print(e)

    # Print sample entries
    print("\n--- Sample entries ---")
    # One from each category
    samples = {}
    for p in products:
        if p["category"] not in samples:
            samples[p["category"]] = p
    for cat in sorted(samples):
        print(json.dumps(samples[cat], indent=2))
        print()


if __name__ == "__main__":
    main()
