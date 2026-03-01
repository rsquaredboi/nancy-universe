#!/usr/bin/env python3
"""
Nancy Universe — Fashion PDP + Collection Page Generator
Generates product detail pages for all 90 new fashion items
and 6 category collection pages.
"""

import os
import sys

# ============================================================
# FASHION ITEM DATA — All 100 items from PRODUCT-IDEAS.md
# Items that already have pages will be skipped during generation
# ============================================================

EXISTING_SLUGS = {
    'fruit-club-tee', 'lem-graphic-tee', 'berri-crop-top',
    'squad-sweatshirt', 'avo-hoodie', 'tropical-shorts',
    'pixie-bucket-hat', 'nancy-logo-cap', 'fruit-tote-bag', 'lolly-socks-set'
}

FASHION_CATEGORIES = [
    {
        'name': 'Tees & Tops',
        'slug': 'tees-tops',
        'emoji': '👕',
        'tagline': 'Statement pieces for everyday rebels.',
        'color': '#FF6B6B',
        'color_light': '#FFE0E0',
        'color_dark': '#C62828',
        'items': [
            {'name': 'Fruit Club Tee', 'slug': 'fruit-club-tee', 'type': 'Basic tee', 'price': 45, 'concept': 'Small "Fruit Club" text logo + tiny icons on chest', 'tagline': 'The everyday essential.', 'features': ['100% Cotton', 'Screen Printed', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': 'Lem Graphic Tee', 'slug': 'lem-graphic-tee', 'type': 'Graphic tee', 'price': 45, 'concept': 'Large Lem character illustration, oversized front print', 'tagline': 'Bold lemon energy.', 'features': ['100% Cotton', 'Oversized Print', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Relaxed Fit']},
            {'name': 'Berri Crop Top', 'slug': 'berri-crop-top', 'type': 'Crop top', 'price': 38, 'concept': 'Embroidered strawberry on chest, boxy cropped fit', 'tagline': 'Sweet & cropped.', 'features': ['100% Cotton', 'Embroidered', 'Boxy Fit', 'Cropped Length', 'Pre-Washed', 'Ribbed Neckline']},
            {'name': 'Squad Goals Tee', 'slug': 'squad-goals-tee', 'type': 'Graphic tee', 'price': 45, 'concept': 'All 5 OGs in a row across chest', 'tagline': 'The whole crew on your chest.', 'features': ['100% Cotton', 'Full Front Print', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': 'Emotionally Attached Tee', 'slug': 'emotionally-attached-tee', 'type': 'Slogan tee', 'price': 42, 'concept': 'Back print: "Emotionally Attached to a Plush Toy" in serif font', 'tagline': 'Wear your feelings.', 'features': ['100% Cotton', 'Back Print', 'Serif Typography', 'Unisex Fit', 'Pre-Washed', 'Regular Fit']},
            {'name': 'Chaos Fairy Tee', 'slug': 'chaos-fairy-tee', 'type': 'Graphic tee', 'price': 45, 'concept': 'Pixie illustration with "Chaos" in gothic font', 'tagline': 'Tiny but terrifying.', 'features': ['100% Cotton', 'Gothic Typography', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': '404 Not Found Tee', 'slug': '404-not-found-tee', 'type': 'Slogan tee', 'price': 42, 'concept': 'Glitched text: "404: Feelings Not Found"', 'tagline': 'Error: too real.', 'features': ['100% Cotton', 'Distressed Print', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': 'Nugget Appreciation Tee', 'slug': 'nugget-appreciation-tee', 'type': 'Graphic tee', 'price': 45, 'concept': 'Nugget character with "Emotional Support Nugget" text', 'tagline': 'Everyone needs a nugget.', 'features': ['100% Cotton', 'Screen Printed', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': 'Void Tee', 'slug': 'void-tee', 'type': 'Minimal tee', 'price': 45, 'concept': 'All black, tiny white "Void" embroidered on chest', 'tagline': 'Stare into it.', 'features': ['100% Cotton', 'Embroidered', 'All Black', 'Unisex Fit', 'Pre-Washed', 'Regular Fit']},
            {'name': 'Delulu Manifesting Tee', 'slug': 'delulu-manifesting-tee', 'type': 'Slogan tee', 'price': 42, 'concept': '"Delulu is the Solulu" in handwritten script', 'tagline': 'Manifesting greatness.', 'features': ['100% Cotton', 'Script Typography', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': 'Avo Cropped Tank', 'slug': 'avo-cropped-tank', 'type': 'Tank top', 'price': 35, 'concept': 'Avo embroidery on left chest, ribbed cotton', 'tagline': 'Cool & calm energy.', 'features': ['Ribbed Cotton', 'Embroidered', 'Cropped Length', 'Slim Fit', 'Pre-Washed', 'Tagless']},
            {'name': 'Boba Ringer Tee', 'slug': 'boba-ringer-tee', 'type': 'Ringer tee', 'price': 45, 'concept': 'Boba character with contrast collar/sleeves', 'tagline': 'Retro boba vibes.', 'features': ['100% Cotton', 'Contrast Trim', 'Unisex Fit', 'Pre-Washed', 'Retro Style', 'Regular Fit']},
            {'name': 'Space Squad Tee', 'slug': 'space-squad-tee', 'type': 'Graphic tee', 'price': 48, 'concept': 'Cosmic characters (Nebula, Cosmo, Luna) constellation map', 'tagline': 'Lost in space.', 'features': ['Premium Cotton', 'Full Front Print', 'Unisex Fit', 'Pre-Washed', 'Glow Detail', 'Relaxed Fit']},
            {'name': 'Feelings Forecast Tee', 'slug': 'feelings-forecast-tee', 'type': 'Graphic tee', 'price': 45, 'concept': 'Weather emoji characters with "Today\'s Forecast: Chaotic"', 'tagline': 'Today: chaotic.', 'features': ['100% Cotton', 'Screen Printed', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': 'NPC Mode Tee', 'slug': 'npc-mode-tee', 'type': 'Slogan tee', 'price': 42, 'concept': '"NPC Mode: Activated" in pixel font', 'tagline': 'Activated.', 'features': ['100% Cotton', 'Pixel Typography', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': 'Moth to a Flame Tank', 'slug': 'moth-flame-tank', 'type': 'Tank top', 'price': 35, 'concept': 'Mothman character, "Drawn to Your Light"', 'tagline': 'Drawn to your light.', 'features': ['100% Cotton', 'Screen Printed', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': 'Dragon Energy Tee', 'slug': 'dragon-energy-tee', 'type': 'Graphic tee', 'price': 45, 'concept': 'Baby Dragon breathing fire, "Tiny but Mighty"', 'tagline': 'Tiny but mighty.', 'features': ['100% Cotton', 'Full Front Print', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': 'Unhinged & Thriving Tee', 'slug': 'unhinged-thriving-tee', 'type': 'Slogan tee', 'price': 42, 'concept': 'Spinning eyes graphic, "Unhinged & Thriving"', 'tagline': 'No filter. No plan.', 'features': ['100% Cotton', 'Screen Printed', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': 'Cinnamon Roll Tee', 'slug': 'cinnamon-roll-tee', 'type': 'Graphic tee', 'price': 45, 'concept': 'Cinnamon Roll character, "Too Pure for This World"', 'tagline': 'Too pure.', 'features': ['100% Cotton', 'Screen Printed', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': 'Serotonin Dealer Tee', 'slug': 'serotonin-dealer-tee', 'type': 'Slogan tee', 'price': 42, 'concept': 'Golden glow graphic, "Serotonin Dealer"', 'tagline': 'Your daily dose.', 'features': ['100% Cotton', 'Metallic Print', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': 'Cryptid Club Tee', 'slug': 'cryptid-club-tee', 'type': 'Graphic tee', 'price': 48, 'concept': 'Yeti, Nessie, Mothman lineup, "Believe"', 'tagline': 'Believe.', 'features': ['Premium Cotton', 'Vintage Print', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Relaxed Fit']},
            {'name': 'Jellyfish Mesh Top', 'slug': 'jellyfish-mesh-top', 'type': 'Mesh/sheer top', 'price': 55, 'concept': 'Iridescent jellyfish print on sheer mesh', 'tagline': 'Ethereal flow.', 'features': ['Mesh Fabric', 'Iridescent Print', 'Relaxed Fit', 'Layering Piece', 'Hand Wash', 'Semi-Sheer']},
            {'name': 'Main Character Tee', 'slug': 'main-character-tee', 'type': 'Slogan tee', 'price': 42, 'concept': 'Spotlight graphic, "Supporting Characters DNI"', 'tagline': 'Main character energy.', 'features': ['100% Cotton', 'Screen Printed', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': 'Axolotl Smile Tee', 'slug': 'axolotl-smile-tee', 'type': 'Graphic tee', 'price': 45, 'concept': 'Axolotl face full front, "Smile Through It"', 'tagline': 'Smile through it.', 'features': ['100% Cotton', 'Full Front Print', 'Unisex Fit', 'Pre-Washed', 'Tagless', 'Regular Fit']},
            {'name': 'Reverse Crop', 'slug': 'reverse-crop', 'type': 'Crop top', 'price': 38, 'concept': 'Inside-out seams exposed, Reverse character print', 'tagline': 'Inside out & proud.', 'features': ['100% Cotton', 'Exposed Seams', 'Boxy Fit', 'Cropped Length', 'Raw Edge', 'Unisex']},
        ]
    },
    {
        'name': 'Hoodies & Sweatshirts',
        'slug': 'hoodies-sweatshirts',
        'emoji': '🧥',
        'tagline': 'Cozy chaos. Heavyweight comfort.',
        'color': '#7C3AED',
        'color_light': '#EDE9FE',
        'color_dark': '#4C1D95',
        'items': [
            {'name': 'Avo Hoodie', 'slug': 'avo-hoodie', 'type': 'Oversized hoodie', 'price': 85, 'concept': 'Embroidered Avo on chest, sage green, kangaroo pocket', 'tagline': 'Cozy avocado vibes.', 'features': ['380gsm Heavyweight', 'Organic Cotton Fleece', 'Embroidered Detail', 'Kangaroo Pocket', 'Oversized Fit', 'Pre-Washed']},
            {'name': 'Chaos Hoodie', 'slug': 'chaos-hoodie', 'type': 'Oversized hoodie', 'price': 89, 'concept': '"Chaos" in dripping text on back, scribble character on chest', 'tagline': 'Embrace the chaos.', 'features': ['380gsm Heavyweight', 'Organic Cotton Fleece', 'Drip Typography', 'Kangaroo Pocket', 'Oversized Fit', 'Pre-Washed']},
            {'name': 'Void Hoodie', 'slug': 'void-hoodie', 'type': 'Heavyweight hoodie', 'price': 89, 'concept': 'All black, glow-in-the-dark Void character on back', 'tagline': 'Disappear into it.', 'features': ['400gsm Heavyweight', 'Glow-in-the-Dark', 'All Black', 'Kangaroo Pocket', 'Oversized Fit', 'Pre-Washed']},
            {'name': 'Nebula Hoodie', 'slug': 'nebula-hoodie', 'type': 'Tie-dye hoodie', 'price': 95, 'concept': 'Purple/pink nebula tie-dye, Nebula character embroidered', 'tagline': 'Cosmic comfort.', 'features': ['380gsm Heavyweight', 'Hand-Dyed Tie-Dye', 'Embroidered Detail', 'Kangaroo Pocket', 'Oversized Fit', 'One-of-a-Kind']},
            {'name': 'Cozy Era Crewneck', 'slug': 'cozy-era-crewneck', 'type': 'Crewneck sweatshirt', 'price': 75, 'concept': '"Entering My Cozy Era" in varsity font, cream', 'tagline': 'Entering my cozy era.', 'features': ['350gsm French Terry', 'Varsity Typography', 'Cream Colorway', 'Ribbed Cuffs', 'Relaxed Fit', 'Pre-Washed']},
            {'name': 'Cryptid Crewneck', 'slug': 'cryptid-crewneck', 'type': 'Crewneck sweatshirt', 'price': 78, 'concept': 'All cryptid characters in vintage illustration style', 'tagline': 'Believers only.', 'features': ['350gsm French Terry', 'Vintage Illustration', 'Full Front Print', 'Ribbed Cuffs', 'Relaxed Fit', 'Pre-Washed']},
            {'name': 'Glitch Hoodie', 'slug': 'glitch-hoodie', 'type': 'Hoodie', 'price': 89, 'concept': 'Distorted/glitched Nancy logo, pixelated details', 'tagline': 'Not a bug.', 'features': ['380gsm Heavyweight', 'Distorted Print', 'Pixel Details', 'Kangaroo Pocket', 'Oversized Fit', 'Pre-Washed']},
            {'name': 'Mushroom Hoodie', 'slug': 'mushroom-hoodie', 'type': 'Hoodie', 'price': 85, 'concept': 'Cottage core mushroom village on back, brown/green', 'tagline': 'Forest floor vibes.', 'features': ['380gsm Heavyweight', 'Back Print', 'Earth Tones', 'Kangaroo Pocket', 'Oversized Fit', 'Pre-Washed']},
            {'name': 'Weather Report Crewneck', 'slug': 'weather-report-crewneck', 'type': 'Crewneck sweatshirt', 'price': 75, 'concept': 'All weather characters in forecast layout', 'tagline': "Today's forecast: cozy.", 'features': ['350gsm French Terry', 'Full Front Print', 'Forecast Layout', 'Ribbed Cuffs', 'Relaxed Fit', 'Pre-Washed']},
            {'name': 'Espresso Yourself Hoodie', 'slug': 'espresso-yourself-hoodie', 'type': 'Hoodie', 'price': 85, 'concept': '"Espresso Yourself" + coffee characters', 'tagline': 'Caffeinated comfort.', 'features': ['380gsm Heavyweight', 'Screen Printed', 'Coffee Brown', 'Kangaroo Pocket', 'Oversized Fit', 'Pre-Washed']},
            {'name': 'Dragon Fire Hoodie', 'slug': 'dragon-fire-hoodie', 'type': 'Hoodie', 'price': 89, 'concept': 'Dragon breathing fire on back, "Handle With Care"', 'tagline': 'Handle with care.', 'features': ['380gsm Heavyweight', 'Full Back Print', 'Fire Detail', 'Kangaroo Pocket', 'Oversized Fit', 'Pre-Washed']},
            {'name': 'Eclipse Half-Zip', 'slug': 'eclipse-half-zip', 'type': 'Half-zip pullover', 'price': 95, 'concept': 'Half black/half white split, Eclipse character', 'tagline': 'Light meets dark.', 'features': ['380gsm Heavyweight', 'Half-Zip Design', 'Split Colorblock', 'Stand Collar', 'Relaxed Fit', 'Pre-Washed']},
            {'name': 'Emotional Baggage Hoodie', 'slug': 'emotional-baggage-hoodie', 'type': 'Oversized hoodie', 'price': 89, 'concept': 'Suitcase graphic filled with feeling characters', 'tagline': 'Unpacking feelings.', 'features': ['380gsm Heavyweight', 'Full Front Print', 'Illustrated Detail', 'Kangaroo Pocket', 'Oversized Fit', 'Pre-Washed']},
            {'name': 'Feral Hours Crewneck', 'slug': 'feral-hours-crewneck', 'type': 'Crewneck sweatshirt', 'price': 75, 'concept': '"Feral Hours: 12am-5am" in scratchy font', 'tagline': 'After midnight.', 'features': ['350gsm French Terry', 'Scratchy Typography', 'Distressed Print', 'Ribbed Cuffs', 'Relaxed Fit', 'Pre-Washed']},
            {'name': 'Capybara Zen Hoodie', 'slug': 'capybara-zen-hoodie', 'type': 'Oversized hoodie', 'price': 85, 'concept': 'Capybara in hot spring, "Unbothered" on back', 'tagline': 'Unbothered.', 'features': ['380gsm Heavyweight', 'Front + Back Print', 'Warm Brown', 'Kangaroo Pocket', 'Oversized Fit', 'Pre-Washed']},
            {'name': 'Static Noise Hoodie', 'slug': 'static-noise-hoodie', 'type': 'Hoodie', 'price': 89, 'concept': 'TV static all-over print, small Static character', 'tagline': 'White noise.', 'features': ['380gsm Heavyweight', 'All-Over Print', 'Static Pattern', 'Kangaroo Pocket', 'Oversized Fit', 'Pre-Washed']},
            {'name': 'Phoenix Rising Crewneck', 'slug': 'phoenix-rising-crewneck', 'type': 'Crewneck sweatshirt', 'price': 78, 'concept': 'Phoenix illustration, "Burn it Down. Rise Up."', 'tagline': 'Rise up.', 'features': ['350gsm French Terry', 'Flame Gradient', 'Full Front Print', 'Ribbed Cuffs', 'Relaxed Fit', 'Pre-Washed']},
            {'name': 'Matcha State of Mind', 'slug': 'matcha-state-of-mind', 'type': 'Hoodie', 'price': 85, 'concept': 'Matcha green, "Calm but Caffeinated"', 'tagline': 'Calm but caffeinated.', 'features': ['380gsm Heavyweight', 'Embroidered Text', 'Matcha Green', 'Kangaroo Pocket', 'Oversized Fit', 'Pre-Washed']},
            {'name': 'Deja Vu Crewneck', 'slug': 'deja-vu-crewneck', 'type': 'Crewneck sweatshirt', 'price': 75, 'concept': 'Same design printed twice, overlapping. On purpose.', 'tagline': 'Wait, haven\'t we...', 'features': ['350gsm French Terry', 'Double-Print Effect', 'Intentional Overlap', 'Ribbed Cuffs', 'Relaxed Fit', 'Pre-Washed']},
            {'name': 'Rizz Academy Hoodie', 'slug': 'rizz-academy-hoodie', 'type': 'Varsity hoodie', 'price': 95, 'concept': '"Rizz Academy Est. 2024" in collegiate font', 'tagline': 'Enrolled.', 'features': ['400gsm Heavyweight', 'Collegiate Typography', 'Chenille Patch', 'Kangaroo Pocket', 'Oversized Fit', 'Pre-Washed']},
        ]
    },
    {
        'name': 'Bottoms',
        'slug': 'bottoms',
        'emoji': '👖',
        'tagline': 'From sweats to skirts. All vibes welcome.',
        'color': '#059669',
        'color_light': '#D1FAE5',
        'color_dark': '#064E3B',
        'items': [
            {'name': 'Tropical Shorts', 'slug': 'tropical-shorts', 'type': 'Casual shorts', 'price': 45, 'concept': 'All-over fruit pattern, pastel tie-dye base', 'tagline': 'Summer on your legs.', 'features': ['100% Cotton', 'All-Over Print', 'Elastic Waist', 'Deep Pockets', 'Relaxed Fit', 'Pre-Washed']},
            {'name': 'Chaos Sweats', 'slug': 'chaos-sweats', 'type': 'Joggers', 'price': 65, 'concept': '"Chaos" down the leg, splatter paint details', 'tagline': 'Chaos from the waist down.', 'features': ['350gsm French Terry', 'Leg Print', 'Splatter Detail', 'Deep Pockets', 'Tapered Fit', 'Drawstring Waist']},
            {'name': 'Cosmic Sweats', 'slug': 'cosmic-sweats', 'type': 'Joggers', 'price': 68, 'concept': 'Galaxy print panels, star embroidery', 'tagline': 'Lost in space.', 'features': ['350gsm French Terry', 'Galaxy Panels', 'Embroidered Stars', 'Deep Pockets', 'Tapered Fit', 'Drawstring Waist']},
            {'name': 'NPC Cargo Pants', 'slug': 'npc-cargo-pants', 'type': 'Cargo pants', 'price': 72, 'concept': 'Pixel art patches on pockets, "Quest Accepted"', 'tagline': 'Quest accepted.', 'features': ['Cotton Twill', 'Pixel Patches', 'Cargo Pockets', 'Adjustable Ankle', 'Relaxed Fit', 'Pre-Washed']},
            {'name': 'Jellyfish Mesh Shorts', 'slug': 'jellyfish-mesh-shorts', 'type': 'Basketball shorts', 'price': 48, 'concept': 'Iridescent print, jellyfish characters', 'tagline': 'Float on.', 'features': ['Mesh Fabric', 'Iridescent Print', 'Elastic Waist', 'Deep Pockets', 'Relaxed Fit', 'Quick-Dry']},
            {'name': 'Dragon Scale Leggings', 'slug': 'dragon-scale-leggings', 'type': 'Leggings', 'price': 55, 'concept': 'Scale-texture fabric, tiny dragon on waistband', 'tagline': 'Scale up.', 'features': ['4-Way Stretch', 'Scale Texture', 'High Waist', 'Hidden Pocket', 'Squat-Proof', 'Moisture-Wicking']},
            {'name': 'Feral Sweatpants', 'slug': 'feral-sweatpants', 'type': 'Sweatpants', 'price': 62, 'concept': '"Do Not Disturb: Feral" on thigh', 'tagline': 'Do not disturb.', 'features': ['350gsm French Terry', 'Thigh Print', 'Elastic Cuffs', 'Deep Pockets', 'Relaxed Fit', 'Drawstring Waist']},
            {'name': 'Mushroom Pajama Pants', 'slug': 'mushroom-pajama-pants', 'type': 'PJ pants', 'price': 42, 'concept': 'All-over mushroom village print, cozy flannel', 'tagline': 'Cottage core bedtime.', 'features': ['Cotton Flannel', 'All-Over Print', 'Elastic Waist', 'Side Pockets', 'Relaxed Fit', 'Brushed Interior']},
            {'name': 'Boba Float Skirt', 'slug': 'boba-float-skirt', 'type': 'Mini skirt', 'price': 48, 'concept': 'Pleated, boba pearl print', 'tagline': 'Pearl power.', 'features': ['Cotton Blend', 'Pleated Design', 'Boba Print', 'Hidden Zip', 'A-Line Fit', 'Lined Interior']},
            {'name': 'Eclipse Split Shorts', 'slug': 'eclipse-split-shorts', 'type': 'Shorts', 'price': 45, 'concept': 'Left leg black, right leg white', 'tagline': 'Light meets dark.', 'features': ['100% Cotton', 'Split Colorblock', 'Elastic Waist', 'Deep Pockets', 'Relaxed Fit', 'Pre-Washed']},
        ]
    },
    {
        'name': 'Headwear',
        'slug': 'headwear',
        'emoji': '🧢',
        'tagline': 'Top off your look. Literally.',
        'color': '#D97706',
        'color_light': '#FEF3C7',
        'color_dark': '#92400E',
        'items': [
            {'name': 'Pixie Bucket Hat', 'slug': 'pixie-bucket-hat', 'type': 'Bucket hat', 'price': 35, 'concept': 'Lavender, embroidered Pixie grape on front', 'tagline': 'Grape expectations.', 'features': ['100% Cotton', 'Embroidered', 'Lavender', 'One Size', 'Packable', 'UPF 30+']},
            {'name': 'Nancy Logo Cap', 'slug': 'nancy-logo-cap', 'type': 'Dad cap', 'price': 32, 'concept': 'Black, pink Nancy logo embroidered', 'tagline': 'The classic.', 'features': ['Cotton Twill', 'Embroidered Logo', 'Adjustable Strap', 'One Size', 'Pre-Curved Brim', 'Brass Buckle']},
            {'name': 'Void Beanie', 'slug': 'void-beanie', 'type': 'Beanie', 'price': 28, 'concept': 'All black, tiny "Void" patch', 'tagline': 'Into the void.', 'features': ['Acrylic Knit', 'Woven Patch', 'All Black', 'One Size', 'Double-Layer', 'Cuff Style']},
            {'name': 'Chaos Bucket Hat', 'slug': 'chaos-bucket-hat', 'type': 'Bucket hat', 'price': 35, 'concept': 'Splatter paint pattern, "Chaos" label', 'tagline': 'Controlled chaos.', 'features': ['100% Cotton', 'Splatter Print', 'Woven Label', 'One Size', 'Packable', 'Wide Brim']},
            {'name': 'Mushroom Beret', 'slug': 'mushroom-beret', 'type': 'Beret', 'price': 38, 'concept': 'Red with white spots, mushroom cap shape', 'tagline': 'Fungi fashion.', 'features': ['Wool Blend', 'Mushroom Design', 'Red & White', 'One Size', 'Lined Interior', 'Adjustable']},
            {'name': 'Dragon Horns Beanie', 'slug': 'dragon-horns-beanie', 'type': 'Novelty beanie', 'price': 35, 'concept': 'Knit beanie with dragon horn details', 'tagline': 'Horns up.', 'features': ['Acrylic Knit', '3D Horn Details', 'Novelty Design', 'One Size', 'Double-Layer', 'Fleece Lined']},
            {'name': 'Boba Trucker Hat', 'slug': 'boba-trucker-hat', 'type': 'Trucker hat', 'price': 32, 'concept': 'Mesh back, Boba character patch on front', 'tagline': 'Sip & style.', 'features': ['Cotton Front', 'Mesh Back', 'Woven Patch', 'Snapback', 'One Size', 'Pre-Curved Brim']},
            {'name': 'Feral Headband', 'slug': 'feral-headband', 'type': 'Headband', 'price': 22, 'concept': 'Raccoon ears, "Feral" embroidered', 'tagline': 'Unleashed.', 'features': ['Cotton Stretch', 'Raccoon Ears', 'Embroidered', 'One Size', 'Elastic Back', 'Machine Washable']},
            {'name': 'Axolotl Ear Flap Hat', 'slug': 'axolotl-ear-flap-hat', 'type': 'Winter hat', 'price': 38, 'concept': 'Pink with axolotl gill flaps', 'tagline': 'Gill-ty pleasure.', 'features': ['Acrylic Knit', 'Gill Flap Design', 'Pink Gradient', 'One Size', 'Fleece Lined', 'Chin Ties']},
            {'name': 'Nebula Bucket Hat', 'slug': 'nebula-bucket-hat', 'type': 'Bucket hat', 'price': 38, 'concept': 'Purple/pink tie-dye, cosmic characters', 'tagline': 'Cosmic crown.', 'features': ['100% Cotton', 'Tie-Dye', 'Cosmic Print', 'One Size', 'Packable', 'Wide Brim']},
        ]
    },
    {
        'name': 'Accessories',
        'slug': 'accessories',
        'emoji': '🎒',
        'tagline': 'The little things that make it.',
        'color': '#EC4899',
        'color_light': '#FCE7F3',
        'color_dark': '#9D174D',
        'items': [
            {'name': 'Fruit Tote Bag', 'slug': 'fruit-tote-bag', 'type': 'Canvas tote', 'price': 28, 'concept': 'All fruit characters scattered, cotton handles', 'tagline': 'Carry your crew.', 'features': ['12oz Canvas', 'Cotton Handles', 'Full Print', 'Inner Pocket', 'Machine Washable', 'Roomy 15L']},
            {'name': 'Lolly Socks Set', 'slug': 'lolly-socks-set', 'type': '3-pack crew socks', 'price': 22, 'concept': 'Pink/yellow/green pairs, character knit at ankle', 'tagline': 'Sweet feet.', 'features': ['Combed Cotton', '3-Pack', 'Character Knit', 'Cushioned Sole', 'Reinforced Toe', 'Fits 6-12']},
            {'name': 'Void Crossbody Bag', 'slug': 'void-crossbody-bag', 'type': 'Mini crossbody', 'price': 45, 'concept': 'All black, reflective Void logo', 'tagline': 'Dark essentials.', 'features': ['Vegan Leather', 'Reflective Logo', 'All Black', 'Adjustable Strap', 'Zip Closure', 'Card Slots']},
            {'name': 'Chaos Fanny Pack', 'slug': 'chaos-fanny-pack', 'type': 'Belt bag', 'price': 38, 'concept': 'Splatter paint, multiple pockets', 'tagline': 'Organized chaos.', 'features': ['Nylon', 'Splatter Print', '3 Zip Pockets', 'Adjustable Belt', 'Quick-Release', 'Water-Resistant']},
            {'name': 'Emotional Baggage Duffle', 'slug': 'emotional-baggage-duffle', 'type': 'Weekender bag', 'price': 78, 'concept': '"Emotional Baggage" embroidered, feeling patches', 'tagline': 'Pack your feelings.', 'features': ['Canvas', 'Embroidered', 'Iron-On Patches', 'Shoe Compartment', 'Shoulder Strap', 'Water-Resistant']},
            {'name': 'Cryptid Keychain Set', 'slug': 'cryptid-keychain-set', 'type': '3-pack keychains', 'price': 18, 'concept': 'Mini Yeti, Nessie, Mothman', 'tagline': 'Pocket-sized legends.', 'features': ['PVC Rubber', '3-Pack', 'Lobster Clasp', 'Durable', 'Collectible', '3cm Each']},
            {'name': 'Dragon Enamel Pin Set', 'slug': 'dragon-enamel-pin-set', 'type': '5-pack enamel pins', 'price': 25, 'concept': 'Baby dragon in 5 expressions', 'tagline': 'Five moods.', 'features': ['Hard Enamel', '5-Pack', 'Butterfly Clutch', 'Gold Plated', 'Collectible', '2.5cm Each']},
            {'name': 'Jellyfish Phone Case', 'slug': 'jellyfish-phone-case', 'type': 'Phone case', 'price': 28, 'concept': 'Iridescent holographic, jellyfish print', 'tagline': 'Glow up your phone.', 'features': ['TPU + PC', 'Holographic', 'MagSafe Compatible', 'Drop Protection', 'Wireless Charging', 'Slim Profile']},
            {'name': 'Serotonin Sticker Pack', 'slug': 'serotonin-sticker-pack', 'type': '15-pack stickers', 'price': 12, 'concept': 'All feeling characters, waterproof vinyl', 'tagline': 'Stick your mood.', 'features': ['Vinyl', '15-Pack', 'Waterproof', 'UV-Resistant', 'Die-Cut', 'Laptop-Safe']},
            {'name': 'Space Squad Laptop Sleeve', 'slug': 'space-squad-laptop-sleeve', 'type': 'Laptop sleeve', 'price': 35, 'concept': 'Cosmic characters constellation, padded neoprene', 'tagline': 'Protect your portal.', 'features': ['Neoprene', 'Padded Interior', 'Full Print', 'Zip Closure', 'Fits 13-15"', 'Water-Resistant']},
            {'name': 'Mushroom Canvas Pouch', 'slug': 'mushroom-canvas-pouch', 'type': 'Zipper pouch', 'price': 22, 'concept': 'Cottage core mushroom print, canvas', 'tagline': 'Tiny treasures.', 'features': ['12oz Canvas', 'Zip Closure', 'Full Print', 'Lined Interior', 'Machine Washable', '20x15cm']},
            {'name': 'Boba Airpods Case', 'slug': 'boba-airpods-case', 'type': 'Airpods case', 'price': 18, 'concept': 'Silicone boba cup shape', 'tagline': 'Sip your beats.', 'features': ['Silicone', 'Boba Cup Shape', 'Carabiner Clip', 'Charging Compatible', 'Shockproof', 'Fits Gen 1-3']},
            {'name': 'NPC Name Badge Lanyard', 'slug': 'npc-name-badge-lanyard', 'type': 'Lanyard', 'price': 15, 'concept': '"NPC" badge template, pixel font', 'tagline': 'Badge equipped.', 'features': ['Polyester', 'Pixel Font', 'ID Holder', 'Safety Breakaway', 'Swivel Hook', '45cm Length']},
            {'name': 'Glitch Wristband Set', 'slug': 'glitch-wristband-set', 'type': '3-pack wristbands', 'price': 16, 'concept': 'Pixelated text: "Error" "Glitch" "Reboot"', 'tagline': 'System overload.', 'features': ['Silicone', '3-Pack', 'Pixel Text', 'Adjustable', 'Waterproof', 'One Size']},
            {'name': 'Capybara Sleep Mask', 'slug': 'capybara-sleep-mask', 'type': 'Sleep mask', 'price': 18, 'concept': 'Capybara face, "Unbothered" on strap', 'tagline': 'Sleep unbothered.', 'features': ['Silk Satin', 'Padded', 'Capybara Face', 'Adjustable Strap', 'Light Blocking', 'Travel Pouch']},
            {'name': 'Phoenix Enamel Pin', 'slug': 'phoenix-enamel-pin', 'type': 'Single pin', 'price': 12, 'concept': 'Flame-gradient phoenix, gold plating', 'tagline': 'Rise from the ashes.', 'features': ['Hard Enamel', 'Gold Plated', 'Flame Gradient', 'Butterfly Clutch', 'Collectible', '3cm']},
            {'name': 'Axolotl Water Bottle', 'slug': 'axolotl-water-bottle', 'type': 'Reusable bottle', 'price': 32, 'concept': 'Pink gradient, axolotl face lid', 'tagline': 'Stay hydrated, stay cute.', 'features': ['Stainless Steel', '500ml', 'Double Wall', 'Axolotl Lid', 'Keeps Cold 24hr', 'BPA-Free']},
            {'name': 'Espresso Shot Glass Set', 'slug': 'espresso-shot-glass-set', 'type': '2-pack ceramic', 'price': 28, 'concept': 'Espresso character on each, "47 Tabs Open"', 'tagline': '47 tabs open.', 'features': ['Ceramic', '2-Pack', 'Espresso Character', 'Microwave Safe', 'Dishwasher Safe', '90ml Each']},
            {'name': 'Chaos Scarf', 'slug': 'chaos-scarf', 'type': 'Knit scarf', 'price': 35, 'concept': 'Scribble pattern, multicolor', 'tagline': 'Wrap up the chaos.', 'features': ['Acrylic Knit', 'Scribble Pattern', 'Multicolor', 'Fringe Ends', '180cm Length', 'Machine Washable']},
            {'name': 'Rizz Mirror Keychain', 'slug': 'rizz-mirror-keychain', 'type': 'Compact mirror', 'price': 15, 'concept': '"Check Your Rizz" engraved', 'tagline': 'Check your rizz.', 'features': ['Metal', 'Engraved', 'Compact Mirror', 'Keyring Attached', 'Scratch-Proof', '5cm Diameter']},
        ]
    },
    {
        'name': 'Home & Lifestyle',
        'slug': 'home-lifestyle',
        'emoji': '🏠',
        'tagline': 'Make your space a Nancy space.',
        'color': '#0EA5E9',
        'color_light': '#E0F2FE',
        'color_dark': '#075985',
        'items': [
            {'name': 'Nancy Throw Blanket', 'slug': 'nancy-throw-blanket', 'type': 'Fleece blanket', 'price': 55, 'concept': 'All characters scattered, cream base', 'tagline': 'Wrap up in the whole squad.', 'features': ['Fleece', 'All Characters', 'Cream Base', '150x200cm', 'Machine Washable', 'Double-Sided']},
            {'name': 'Snooze Pillowcase Set', 'slug': 'snooze-pillowcase-set', 'type': '2-pack pillowcases', 'price': 35, 'concept': 'Snooze cloud character, "Do Not Disturb"', 'tagline': 'Do not disturb.', 'features': ['Cotton Sateen', '2-Pack', 'Snooze Character', 'Envelope Closure', 'Standard Size', 'Machine Washable']},
            {'name': 'Mushroom Mug', 'slug': 'mushroom-mug', 'type': 'Ceramic mug', 'price': 22, 'concept': 'Mushroom-shaped handle, 12oz', 'tagline': 'Sip among the fungi.', 'features': ['Ceramic', 'Mushroom Handle', '12oz / 350ml', 'Microwave Safe', 'Dishwasher Safe', 'Gift Boxed']},
            {'name': 'Dragon Incense Holder', 'slug': 'dragon-incense-holder', 'type': 'Ceramic holder', 'price': 28, 'concept': 'Baby dragon, smoke comes from mouth', 'tagline': 'Breathe fire & incense.', 'features': ['Ceramic', 'Dragon Design', 'Smoke Effect', 'Ash Catcher', 'Hand-Painted', 'Gift Boxed']},
            {'name': 'Void Candle', 'slug': 'void-candle', 'type': 'Soy candle', 'price': 25, 'concept': 'Black vessel, "Void" label, cedar/patchouli scent', 'tagline': 'Smells like the void.', 'features': ['Soy Wax', 'Cedar/Patchouli', '40hr Burn', 'Black Vessel', 'Cotton Wick', 'Reusable Jar']},
            {'name': 'Capybara Desk Organizer', 'slug': 'capybara-desk-organizer', 'type': 'Desk organizer', 'price': 32, 'concept': 'Capybara-shaped pen/phone holder', 'tagline': 'Organized & unbothered.', 'features': ['Resin', 'Capybara Shape', 'Pen Holder', 'Phone Stand', 'Weighted Base', 'Hand-Painted']},
            {'name': 'Chill Ice Cube Tray', 'slug': 'chill-ice-cube-tray', 'type': 'Silicone tray', 'price': 15, 'concept': 'Makes ice cubes shaped like Chill character', 'tagline': 'Keep it chill.', 'features': ['Food-Grade Silicone', 'Character Shape', '6 Cubes', 'BPA-Free', 'Dishwasher Safe', 'Stackable']},
            {'name': 'Nebula Poster Set', 'slug': 'nebula-poster-set', 'type': '3-pack art prints', 'price': 38, 'concept': 'Cosmic characters, 8x10, premium cardstock', 'tagline': 'Gallery-worthy cosmos.', 'features': ['Premium Cardstock', '3-Pack', '8x10 Each', 'Cosmic Characters', 'Unframed', 'Archival Ink']},
            {'name': 'Feral Hours Clock', 'slug': 'feral-hours-clock', 'type': 'Wall clock', 'price': 35, 'concept': '"Feral Hours" replaces 12-5 on the clock face', 'tagline': 'Feral time zone.', 'features': ['ABS Frame', 'Quartz Movement', '25cm Diameter', 'Custom Face', 'Silent Tick', 'AA Battery']},
            {'name': 'Serotonin Desk Light', 'slug': 'serotonin-desk-light', 'type': 'LED light', 'price': 42, 'concept': 'Golden orb shape, warm glow, USB powered', 'tagline': 'Glow from within.', 'features': ['LED', 'Golden Orb', 'USB-C Powered', 'Warm Glow', 'Touch Dimmer', '3 Brightness Levels']},
            {'name': 'Weather Mood Board', 'slug': 'weather-mood-board', 'type': 'Magnetic board', 'price': 28, 'concept': 'Weather character magnets to set your daily mood', 'tagline': "Today's mood: variable.", 'features': ['Metal Board', '8 Magnets', 'Weather Characters', '30x20cm', 'Wall Mount', 'Gift Boxed']},
            {'name': 'Emotional Baggage Tags', 'slug': 'emotional-baggage-tags', 'type': '3-pack luggage tags', 'price': 18, 'concept': '"Emotional" "Heavy" "Carry-On"', 'tagline': 'Travel with feelings.', 'features': ['PVC', '3-Pack', 'ID Window', 'Buckle Strap', 'Durable', 'Waterproof']},
            {'name': 'Jellyfish Night Light', 'slug': 'jellyfish-night-light', 'type': 'LED night light', 'price': 32, 'concept': 'Color-changing, jellyfish silhouette', 'tagline': 'Glow with the flow.', 'features': ['LED', 'Color-Changing', 'USB-C Powered', 'Silicone', 'Touch Control', 'Auto-Off Timer']},
            {'name': 'Boba Coaster Set', 'slug': 'boba-coaster-set', 'type': '4-pack cork coasters', 'price': 18, 'concept': 'Each features a different drink character', 'tagline': 'Drip protection.', 'features': ['Natural Cork', '4-Pack', 'Character Prints', '10cm Diameter', 'Heat Resistant', 'Gift Boxed']},
            {'name': 'The Full Nancy Box', 'slug': 'full-nancy-box', 'type': 'Gift box set', 'price': 149, 'concept': 'Curated: 1 plush + 1 tee + sticker pack + tote + pin set', 'tagline': 'The ultimate starter kit.', 'features': ['Curated Gift Set', 'Plush + Tee + Stickers', 'Tote + Pin Set', 'Gift Boxed', 'Tissue Paper', 'Greeting Card']},
        ]
    },
]

# ============================================================
# SVG ICONS (reused across all PDPs)
# ============================================================
SVG_ICONS = {
    'box': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>',
    'heart': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    'bag': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 7V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v3"/></svg>',
    'star': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"/></svg>',
    'card': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="22" height="18" rx="2"/><line x1="1" y1="9" x2="23" y2="9"/></svg>',
    'check': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    'users': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    'cart': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>',
}

ICON_ORDER = ['box', 'heart', 'shield', 'bag', 'star', 'box']


def generate_fashion_pdp(item, category, all_categories):
    """Generate a full fashion PDP HTML page."""
    slug = item['slug']
    name = item['name']
    asset_dir = f'../../assets/fashion/{slug}'
    hero_img = f'{asset_dir}/{slug}-hero.png'

    # Build gallery thumbnails
    gallery_shots = ['hero', 'flatlay', 'model-front', 'detail', 'lifestyle-street', 'lifestyle']
    gallery_labels = ['product view', 'flat lay', 'on model', 'detail close-up', 'street style', 'lifestyle']

    thumb_html = ''
    for i, (shot, label) in enumerate(zip(gallery_shots, gallery_labels)):
        active = ' class="active"' if i == 0 else ''
        img_path = f'{asset_dir}/{slug}-{shot}.png'
        thumb_html += f'''          <button{active} aria-label="{name} {label}">
            <img src="{img_path}" data-full="{img_path}" alt="{name} {label}" onerror="this.src='{hero_img}'">
          </button>\n'''

    # Build features list
    features_html = ''
    for i, feat in enumerate(item.get('features', [])[:6]):
        icon = SVG_ICONS[ICON_ORDER[i % len(ICON_ORDER)]]
        features_html += f'''          <div class="pdp-feature">
            {icon}
            {feat}
          </div>\n'''

    # Build related products (from same category, excluding self)
    related_html = ''
    others = [it for it in category['items'] if it['slug'] != slug][:4]
    for other in others:
        other_hero = f'../../assets/fashion/{other["slug"]}/{other["slug"]}-hero.png'
        related_html += f'''        <a href="fashion-{other['slug']}.html" class="product-card" data-tilt>
          <div class="product-card-image">
            <img src="{other_hero}" alt="{other['name']}">
          </div>
          <div class="product-card-info">
            <h3>{other['name']}</h3>
            <p class="product-card-tagline">{other['tagline']}</p>
            <div class="product-card-price">
              <span class="product-card-current">US${other['price']}</span>
            </div>
          </div>
        </a>\n'''

    # Material/composition description based on category
    material_desc = get_material_desc(item, category)
    sustainability_desc = "Every Nancy fashion piece uses GOTS-certified organic cotton, water-based inks, and responsible manufacturing. Because looking good shouldn&rsquo;t cost the planet."

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} &mdash; Nancy Universe</title>
<link rel="icon" type="image/svg+xml" href="../../nancy-logo-pink.svg">
<link rel="icon" type="image/png" href="../../nancy-logo-pink.png">
<meta name="description" content="{item['tagline']} {item['concept']}">
<meta property="og:title" content="{name} &mdash; Nancy Universe">
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
fbq('track', 'ViewContent', {{content_name: '{name}', content_type: 'product', value: {item['price']}, currency: 'USD'}});
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
      <a href="../../pages/collections/{category['slug']}.html">{category['name']}</a>
      <span class="sep">/</span>
      <span class="current">{name}</span>
    </div>

    <!-- PDP Hero -->
    <div class="pdp-hero">

      <!-- Gallery -->
      <div class="pdp-gallery">
        <div class="pdp-gallery-main">
          <img id="pdp-main-img" src="{hero_img}" alt="{name} &mdash; {item['type']} from Nancy Universe">
        </div>
        <div class="pdp-gallery-thumbs">
{thumb_html}        </div>
      </div>

      <!-- Info -->
      <div class="pdp-info">
        <div class="pdp-character-badge" style="background: {category['color_light']}; color: {category['color_dark']};">
          <span>{category['emoji']}</span> {category['name'].upper()}
        </div>

        <h1 class="pdp-title">{name}</h1>
        <p class="pdp-tagline">{item['tagline']}</p>

        <div class="pdp-rating">
          <span class="pdp-stars">&starf;&starf;&starf;&starf;&starf;</span>
          <span class="pdp-rating-text">New &mdash; be the first to review</span>
        </div>

        <div class="pdp-price">
          <span class="pdp-price-current">US${item['price']}</span>
        </div>

        <div class="pdp-features">
{features_html}        </div>

        <button class="pdp-add-to-cart">
          {SVG_ICONS['cart']}
          Add to Cart &mdash; US${item['price']}
        </button>

        <div class="pdp-trust">
          <div class="pdp-trust-item">
            {SVG_ICONS['card']}
            Free shipping over $89
          </div>
          <div class="pdp-trust-item">
            {SVG_ICONS['check']}
            Ethically made
          </div>
          <div class="pdp-trust-item">
            {SVG_ICONS['users']}
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
          <img src="{hero_img}" alt="{name}" onerror="this.src='{hero_img}'">
        </div>
        <div class="pdp-feature-text reveal">
          <span class="section-label">The Details</span>
          <h3>{item['tagline']}</h3>
          <p>{item['concept']}. Designed for the Nancy Universe community &mdash; because your wardrobe should be as expressive as your personality.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Feature 2: Materials -->
  <div class="pdp-feature-section" style="background: var(--cream-dark);">
    <div class="container">
      <div class="pdp-feature-grid reverse">
        <div class="pdp-feature-image reveal">
          <img src="{hero_img}" alt="{name} materials detail" onerror="this.src='{hero_img}'">
        </div>
        <div class="pdp-feature-text reveal">
          <span class="section-label">Materials &amp; Fit</span>
          <h3>Made to <em>last.</em></h3>
          <p>{material_desc}</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Feature 3: Sustainability -->
  <div class="pdp-feature-section">
    <div class="container">
      <div class="pdp-feature-grid">
        <div class="pdp-feature-image reveal">
          <img src="{hero_img}" alt="{name} sustainable fashion" onerror="this.src='{hero_img}'">
        </div>
        <div class="pdp-feature-text reveal">
          <span class="section-label">Sustainability</span>
          <h3>Fashion that feels <em>good.</em></h3>
          <p>{sustainability_desc}</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Related Products -->
  <section class="pdp-related">
    <div class="container">
      <div class="section-header" style="text-align: center;">
        <h2 style="font-family: var(--font-display); font-size: clamp(1.5rem, 2.5vw, 2rem); font-weight: 800; letter-spacing: -0.03em;">More from <em style="font-family: var(--font-editorial); font-weight: 400;">{category['name']}</em></h2>
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
</html>'''

    return html


def get_material_desc(item, category):
    """Generate material/fit description based on item type."""
    item_type = item['type'].lower()

    if 'hoodie' in item_type or 'pullover' in item_type or 'half-zip' in item_type:
        return f"380gsm heavyweight organic cotton fleece. Pre-washed for zero shrinkage. Raglan sleeves, kangaroo pocket, ribbed cuffs. Oversized unisex fit XS&ndash;XXL."
    elif 'crewneck' in item_type or 'sweatshirt' in item_type:
        return f"350gsm French terry organic cotton. Pre-washed, brushed interior for instant softness. Ribbed cuffs and hem. Relaxed unisex fit XS&ndash;XXL."
    elif 'tee' in item_type or 'graphic' in item_type or 'slogan' in item_type or 'basic' in item_type or 'minimal' in item_type or 'ringer' in item_type:
        return f"200gsm premium combed cotton. Pre-washed for that broken-in feel from day one. Tagless for comfort. Unisex fit XS&ndash;XXL."
    elif 'crop' in item_type or 'tank' in item_type:
        return f"180gsm ribbed cotton. Pre-washed, boxy cropped fit. Sits perfectly at the waist. Unisex sizing XS&ndash;XL."
    elif 'mesh' in item_type or 'sheer' in item_type:
        return f"Lightweight mesh fabric with iridescent print. Designed as a layering piece. Semi-sheer, relaxed fit. Hand wash recommended. XS&ndash;XL."
    elif 'jogger' in item_type or 'sweats' in item_type or 'sweatpants' in item_type:
        return f"350gsm French terry with elastic cuffs and drawstring waist. Deep side pockets. Pre-washed for zero shrinkage. Tapered unisex fit XS&ndash;XXL."
    elif 'cargo' in item_type:
        return f"Cotton twill with reinforced cargo pockets. Adjustable ankle. Relaxed fit with drawstring waist. Unisex sizing XS&ndash;XXL."
    elif 'legging' in item_type:
        return f"4-way stretch fabric with scale texture. High waist with hidden pocket. Squat-proof and moisture-wicking. XS&ndash;XL."
    elif 'shorts' in item_type:
        return f"Lightweight cotton with elastic waist and deep pockets. Relaxed fit, 7-inch inseam. Pre-washed. Unisex XS&ndash;XXL."
    elif 'skirt' in item_type:
        return f"Cotton blend with pleated design. Hidden side zip, lined interior. A-line fit. XS&ndash;XL."
    elif 'pajama' in item_type or 'pj' in item_type:
        return f"Cotton flannel with brushed interior for extra coziness. Elastic waist, side pockets. Relaxed fit XS&ndash;XXL."
    elif 'bucket' in item_type or 'hat' in item_type or 'cap' in item_type or 'beanie' in item_type or 'beret' in item_type or 'trucker' in item_type:
        return f"Premium materials with embroidered/woven details. One size fits most with adjustable fit. Packable design."
    elif 'headband' in item_type:
        return f"Stretchy cotton with elastic back. One size fits most. Machine washable."
    elif 'tote' in item_type or 'bag' in item_type or 'crossbody' in item_type or 'fanny' in item_type or 'duffle' in item_type:
        return f"Durable construction with quality hardware. Designed to carry your essentials (and your emotional baggage). Machine washable where applicable."
    elif 'blanket' in item_type:
        return f"Ultra-soft fleece, double-sided print. 150x200cm. Machine washable, tumble dry low. Gets softer with every wash."
    elif 'pillowcase' in item_type:
        return f"300 thread count cotton sateen. Envelope closure for a clean look. Standard size. Machine washable."
    elif 'mug' in item_type or 'ceramic' in item_type:
        return f"Hand-finished ceramic with unique design details. Microwave and dishwasher safe. Gift boxed."
    elif 'candle' in item_type:
        return f"100% soy wax with cotton wick. 40-hour burn time. Reusable vessel after burning. Hand-poured."
    elif 'pin' in item_type:
        return f"Hard enamel with gold plating. Butterfly clutch backing. Collectible quality, perfect for jackets, bags, and lanyards."
    elif 'sticker' in item_type:
        return f"Waterproof vinyl, UV-resistant. Die-cut for clean application. Laptop, water bottle, and phone safe."
    elif 'phone case' in item_type:
        return f"Dual-layer TPU + PC construction. Drop protection up to 6ft. MagSafe compatible. Supports wireless charging."
    elif 'bottle' in item_type:
        return f"Double-wall stainless steel. Keeps drinks cold 24hr, hot 12hr. BPA-free. 500ml capacity."
    else:
        return f"Premium materials, thoughtfully designed. Every Nancy product is made with care, built to last, and designed to make you smile."


def generate_fashion_collection(category):
    """Generate a collection page for a fashion category."""
    items = category['items']

    # Build product grid
    grid_html = ''
    for item in items:
        hero_img = f'../../assets/fashion/{item["slug"]}/{item["slug"]}-hero.png'
        grid_html += f'''        <a href="../products/fashion-{item['slug']}.html" class="product-card" data-tilt>
          <div class="product-card-image">
            <img src="{hero_img}" alt="{item['name']}" loading="lazy">
          </div>
          <div class="product-card-info">
            <h3>{item['name']}</h3>
            <p class="product-card-tagline">{item['tagline']}</p>
            <div class="product-card-price">
              <span class="product-card-current">US${item['price']}</span>
            </div>
          </div>
        </a>\n'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{category['name']} &mdash; Nancy Universe Fashion</title>
<link rel="icon" type="image/svg+xml" href="../../nancy-logo-pink.svg">
<link rel="icon" type="image/png" href="../../nancy-logo-pink.png">
<meta name="description" content="{category['tagline']} Shop the Nancy Universe {category['name']} collection.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.shopify.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;0,9..144,800;1,9..144,400&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Semibold.woff?v=1680075897" as="font" type="font/woff" crossorigin>
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
  <!-- Hero -->
  <section class="collection-hero" style="background: linear-gradient(135deg, {category['color_light']} 0%, white 50%, {category['color_light']} 100%);">
    <div class="container">
      <div style="text-align: center; padding: 4rem 1rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">{category['emoji']}</div>
        <h1 style="font-family: var(--font-display); font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 800; letter-spacing: -0.03em; color: {category['color_dark']};">
          {category['name']}
        </h1>
        <p style="font-family: var(--font-body); font-size: 1.2rem; color: #666; max-width: 500px; margin: 1rem auto 0;">
          {category['tagline']}
        </p>
        <p style="font-family: var(--font-body); font-size: 0.9rem; color: #999; margin-top: 0.5rem;">
          {len(items)} items
        </p>
      </div>
    </div>
  </section>

  <!-- Breadcrumb -->
  <div class="container">
    <div class="breadcrumb" style="margin-top: 1rem;">
      <a href="/">Home</a>
      <span class="sep">/</span>
      <a href="fashion.html">Fashion</a>
      <span class="sep">/</span>
      <span class="current">{category['name']}</span>
    </div>
  </div>

  <!-- Product Grid -->
  <section style="padding: 2rem 0 4rem;">
    <div class="container">
      <div class="product-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 2rem;">
{grid_html}      </div>
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
<script src="../../js/main.js"></script>
<script src="../../js/personality.js"></script>
</body>
</html>'''

    return html


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'

    base_dir = os.path.dirname(os.path.abspath(__file__))
    products_dir = os.path.join(base_dir, 'pages', 'products')
    collections_dir = os.path.join(base_dir, 'pages', 'collections')
    assets_dir = os.path.join(base_dir, 'assets', 'fashion')

    os.makedirs(products_dir, exist_ok=True)
    os.makedirs(collections_dir, exist_ok=True)

    if mode in ('fashion', 'all'):
        count = 0
        skipped = 0
        for cat in FASHION_CATEGORIES:
            for item in cat['items']:
                filepath = os.path.join(products_dir, f'fashion-{item["slug"]}.html')
                if item['slug'] in EXISTING_SLUGS and os.path.exists(filepath):
                    skipped += 1
                    continue

                # Create asset directory
                item_asset_dir = os.path.join(assets_dir, item['slug'])
                os.makedirs(item_asset_dir, exist_ok=True)

                html = generate_fashion_pdp(item, cat, FASHION_CATEGORIES)
                with open(filepath, 'w') as f:
                    f.write(html)
                count += 1
                print(f"  Created: fashion-{item['slug']}.html")

        print(f"\n  {count} fashion PDP pages created, {skipped} skipped (already exist)")

    if mode in ('collections', 'all'):
        count = 0
        for cat in FASHION_CATEGORIES:
            filepath = os.path.join(collections_dir, f'{cat["slug"]}.html')
            html = generate_fashion_collection(cat)
            with open(filepath, 'w') as f:
                f.write(html)
            count += 1
            print(f"  Created collection: {cat['slug']}.html")

        print(f"\n  {count} fashion collection pages created")

    print("\nDone!")


if __name__ == '__main__':
    main()
