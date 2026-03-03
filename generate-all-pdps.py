#!/usr/bin/env python3
"""Nancy Universe — Master PDP + Collection Page Generator
Generates PDP pages for ALL 100 new plushie concepts (waves 2-10)
and 90 new fashion items, plus wave collection pages."""

import os
import re
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ═══════════════════════════════════════════════
# ALL PLUSHIE DATA (Waves 2-10, 100 characters)
# ═══════════════════════════════════════════════

PLUSH_WAVES = [
    {
        "wave": 2, "name": "Food with Attitude", "slug": "food-squad",
        "tagline": "When your comfort food has more personality than your ex.",
        "emoji": "🍔", "color": "#FF6B35", "color_light": "#FFF3E0", "color_dark": "#E65100",
        "characters": [
            {"name": "Mochi", "slug": "mochi", "concept": "mochi ball", "vibe": "Squishy zen master", "tagline": "So soft it's a lifestyle. Will teach you to let go.", "price": 29, "emoji": "🍡", "color": "#F8BBD0", "color_light": "#FCE4EC", "color_dark": "#C2185B", "size": '12"', "personality": "Mochi is the friend who starts every sentence with 'let's just breathe.' Soft to the touch, softer in the soul. Will convince you that doing nothing is actually doing something."},
            {"name": "Boba", "slug": "boba", "concept": "boba tea cup", "vibe": "Trendy & unbothered", "tagline": "Main character energy in a cup. Has 47 playlists.", "price": 29, "emoji": "🧋", "color": "#8D6E63", "color_light": "#EFEBE9", "color_dark": "#4E342E", "size": '12"', "personality": "Boba knows every coffee shop, every playlist, and every trending sound. Shows up 15 minutes late but makes it look intentional. The tapioca pearls are non-negotiable."},
            {"name": "Nugget", "slug": "nugget", "concept": "chicken nugget", "vibe": "Chaotic comfort", "tagline": "The emotional support nugget you didn't know you needed.", "price": 24, "emoji": "🍗", "color": "#FFB74D", "color_light": "#FFF3E0", "color_dark": "#E65100", "size": '10"', "personality": "Nugget doesn't judge your 2am decisions. Nugget IS your 2am decision. Golden, crispy on the outside, warm on the inside. The friend who brings snacks to every crisis."},
            {"name": "Toasty", "slug": "toasty", "concept": "burnt toast", "vibe": "Lovably imperfect", "tagline": "A little crispy. A little dramatic. Perfectly imperfect.", "price": 24, "emoji": "🍞", "color": "#795548", "color_light": "#EFEBE9", "color_dark": "#3E2723", "size": '10"', "personality": "Toasty tried. Toasty failed. Toasty is still here, slightly charred but full of character. A reminder that being a little burnt doesn't make you any less loveable."},
            {"name": "Sushi", "slug": "sushi", "concept": "salmon nigiri", "vibe": "Cool & collected", "tagline": "Always dressed well. Judges your leftovers.", "price": 29, "emoji": "🍣", "color": "#FF7043", "color_light": "#FBE9E7", "color_dark": "#BF360C", "size": '12"', "personality": "Sushi has impeccable taste. In food, in fashion, in friends. Will silently judge your microwave meals but still sit with you while you eat them. Classy but never cold."},
            {"name": "Taco", "slug": "taco", "concept": "taco", "vibe": "Overstuffed & proud", "tagline": "A lot going on. No regrets. Will spill the tea (and the salsa).", "price": 29, "emoji": "🌮", "color": "#FDD835", "color_light": "#FFFDE7", "color_dark": "#F57F17", "size": '12"', "personality": "Taco is overflowing with feelings, toppings, and stories. Can't contain anything. Will tell your secrets accidentally but with such warmth you can't even be mad."},
            {"name": "Ramen", "slug": "ramen", "concept": "ramen bowl", "vibe": "Warm & deep", "tagline": "Looks chill on the surface. Full of layers underneath.", "price": 29, "emoji": "🍜", "color": "#FFE082", "color_light": "#FFFDE7", "color_dark": "#FF8F00", "size": '12"', "personality": "Ramen seems simple but has depth you didn't expect. A slow burn friend — the more time you spend, the more flavor you discover. Best experienced late at night."},
            {"name": "Pretzel", "slug": "pretzel", "concept": "soft pretzel", "vibe": "Twisted but sweet", "tagline": "Complicated but worth it. Salty when tired.", "price": 24, "emoji": "🥨", "color": "#A1887F", "color_light": "#EFEBE9", "color_dark": "#4E342E", "size": '10"', "personality": "Pretzel is complex. Literally twisted. But dip them in the right moment and they're the best thing that ever happened to you. Gets salty when hungry. Relatable queen."},
            {"name": "Waffles", "slug": "waffles", "concept": "waffle", "vibe": "Grid-brained", "tagline": "Organizes everything into little squares. Slightly neurotic. Delightful.", "price": 29, "emoji": "🧇", "color": "#FFD54F", "color_light": "#FFFDE7", "color_dark": "#FF8F00", "size": '12"', "personality": "Waffles has a spreadsheet for everything. Color-coded calendar. Labeled drawers. Still somehow always late. The organized chaos friend who makes you feel better about your own mess."},
            {"name": "Dumpling", "slug": "dumpling", "concept": "dumpling", "vibe": "Thicc & wise", "tagline": "Ancient wisdom in a pleated body. Will fix your love life.", "price": 29, "emoji": "🥟", "color": "#FFF9C4", "color_light": "#FFFDE7", "color_dark": "#F9A825", "size": '12"', "personality": "Dumpling has seen empires rise and fall. Has advice for every situation. Speaks in fortune cookie wisdom but is always, somehow, right. Your grandma's energy in plush form."},
            {"name": "Croissant", "slug": "croissant", "concept": "croissant", "vibe": "Dramatically French", "tagline": "Refuses to wake up before 11. Has opinions about butter.", "price": 29, "emoji": "🥐", "color": "#D7CCC8", "color_light": "#EFEBE9", "color_dark": "#5D4037", "size": '12"', "personality": "Croissant is flaky (literally and emotionally). Wakes up when ready. Has strong opinions about everything from butter quality to pillow thread count. Dramatic but delicious."},
            {"name": "Hotdog", "slug": "hotdog", "concept": "hotdog in bun", "vibe": "Unserious king", "tagline": "Takes nothing seriously. 10/10 party guest. 0/10 life advice.", "price": 24, "emoji": "🌭", "color": "#FF8A65", "color_light": "#FBE9E7", "color_dark": "#BF360C", "size": '10"', "personality": "Hotdog is the friend who shows up to a funeral in sunglasses. Not out of disrespect — out of pure inability to read a room. But somehow, Hotdog makes everything funnier."},
            {"name": "Onigiri", "slug": "onigiri", "concept": "rice ball", "vibe": "Shy but loyal", "tagline": "Quiet. Steady. Will hold your hand through anything.", "price": 24, "emoji": "🍙", "color": "#F5F5F5", "color_light": "#FAFAFA", "color_dark": "#424242", "size": '10"', "personality": "Onigiri doesn't say much. Doesn't need to. Shows up when it matters with a warm presence and zero drama. The friend who remembers your order and your birthday without being asked."},
            {"name": "Eggbert", "slug": "eggbert", "concept": "fried egg", "vibe": "Sunny-side up optimist", "tagline": "Annoyingly positive. Even at 6am. You'll love him anyway.", "price": 24, "emoji": "🍳", "color": "#FFF176", "color_light": "#FFFDE7", "color_dark": "#F57F17", "size": '10"', "personality": "Eggbert greets every morning like it's Christmas. Texts 'rise and shine!' at dawn. You want to hate it. You can't. That golden yolk energy is contagious."},
            {"name": "Pickle", "slug": "pickle", "concept": "pickle", "vibe": "Acquired taste", "tagline": "You either get it or you don't. There's no in between.", "price": 24, "emoji": "🥒", "color": "#689F38", "color_light": "#F1F8E9", "color_dark": "#33691E", "size": '10"', "personality": "Pickle is polarizing. Some people get Pickle instantly. Others need time. But once you're a Pickle person, there's no going back. A cult following in plush form."},
        ]
    },
    {
        "wave": 3, "name": "Space & Cosmic", "slug": "cosmic",
        "tagline": "The universe is vast. Your plush collection should be too.",
        "emoji": "🌌", "color": "#7C4DFF", "color_light": "#EDE7F6", "color_dark": "#311B92",
        "characters": [
            {"name": "Nebula", "slug": "nebula", "concept": "nebula cloud (purple/pink swirl)", "vibe": "Dreamy & vast", "tagline": "Contains multitudes. Literally — there are stars inside her.", "price": 29, "emoji": "🌌", "color": "#CE93D8", "color_light": "#F3E5F5", "color_dark": "#6A1B9A", "size": '12"', "personality": "Nebula is the friend who stares at the sky for hours. Feels everything deeply. Contains entire galaxies of emotion. When she speaks, it's poetry."},
            {"name": "Cosmo", "slug": "cosmo", "concept": "astronaut bear", "vibe": "Brave & lonely", "tagline": "Has seen things you wouldn't believe. Still gives great hugs.", "price": 32, "emoji": "🧑‍🚀", "color": "#90A4AE", "color_light": "#ECEFF1", "color_dark": "#37474F", "size": '12"', "personality": "Cosmo has been to places nobody else has been. Quiet about it. But sometimes you catch a faraway look in those embroidered eyes. The bravest friend you'll ever have."},
            {"name": "Luna", "slug": "luna", "concept": "crescent moon", "vibe": "Nocturnal introvert", "tagline": "Glows brightest when everyone else is asleep.", "price": 29, "emoji": "🌙", "color": "#FFD54F", "color_light": "#FFFDE7", "color_dark": "#FF8F00", "size": '12"', "personality": "Luna comes alive at midnight. The 2am text friend. The one who sends you songs at 3am that change your life. Glows softly. Never overwhelms."},
            {"name": "Solaris", "slug": "solaris", "concept": "little sun", "vibe": "Burning extrovert", "tagline": "Will not let you sit alone at lunch. Literally radiates warmth.", "price": 29, "emoji": "☀️", "color": "#FFB300", "color_light": "#FFF8E1", "color_dark": "#FF6F00", "size": '12"', "personality": "Solaris has never met a stranger. Burns with social energy. Will introduce themselves to everyone in the room and make you feel like the center of the universe."},
            {"name": "Orbit", "slug": "orbit", "concept": "Saturn with rings", "vibe": "Goes in circles", "tagline": "Still figuring things out. Has commitment rings though.", "price": 32, "emoji": "🪐", "color": "#BCAAA4", "color_light": "#EFEBE9", "color_dark": "#4E342E", "size": '12"', "personality": "Orbit keeps coming back to the same problems. Same ex. Same pizza place. But those rings? Those are commitment. Orbit is loyal to a fault, even to bad habits."},
            {"name": "Comet", "slug": "comet", "concept": "comet with tail", "vibe": "Fleeting & intense", "tagline": "Shows up once every 76 years but makes it COUNT.", "price": 29, "emoji": "☄️", "color": "#4FC3F7", "color_light": "#E1F5FE", "color_dark": "#01579B", "size": '12"', "personality": "Comet is the friend you see once a year who makes it the best night of your life. Intense. Brief. Leaves a trail of glitter and memories."},
            {"name": "Eclipse", "slug": "eclipse", "concept": "half dark / half light", "vibe": "Moody duality", "tagline": "Two sides. Both valid. Don't look directly at her drama.", "price": 29, "emoji": "🌑", "color": "#78909C", "color_light": "#ECEFF1", "color_dark": "#263238", "size": '12"', "personality": "Eclipse is half light, half shadow. Switches moods like seasons. Both sides are beautiful. Both sides are real. The most complex friend in your collection."},
            {"name": "Starla", "slug": "starla", "concept": "star cluster", "vibe": "Sparkly overachiever", "tagline": "Does everything. Glitters while doing it. Exhausting and inspiring.", "price": 29, "emoji": "⭐", "color": "#FFD700", "color_light": "#FFFDE7", "color_dark": "#F57F17", "size": '12"', "personality": "Starla runs three clubs, speaks four languages, and still has time to text you happy birthday. You're tired just watching. But god, she sparkles."},
            {"name": "Void", "slug": "void", "concept": "black hole", "vibe": "Absorbs your problems", "tagline": "Tell Void your problems. They disappear. (So might your snacks.)", "price": 29, "emoji": "🕳️", "color": "#212121", "color_light": "#424242", "color_dark": "#000000", "size": '12"', "personality": "Void consumes. Problems, drama, stress — feed it to Void. Gone. Just don't leave your snacks nearby. Void doesn't discriminate about what it absorbs."},
            {"name": "Pluto", "slug": "pluto", "concept": "tiny Pluto planet", "vibe": "Underdog", "tagline": "Still a planet in our hearts. Small but never forgotten.", "price": 22, "emoji": "💜", "color": "#B39DDB", "color_light": "#EDE7F6", "color_dark": "#4527A0", "size": '8"', "personality": "They said Pluto wasn't a planet anymore. Pluto said 'watch me.' Small, fierce, and forever proving that size doesn't determine worth. The underdog you root for."},
            {"name": "Rocket", "slug": "rocket", "concept": "retro rocket ship", "vibe": "Goes too fast", "tagline": "Ready before you are. Already left. Will text you from orbit.", "price": 29, "emoji": "🚀", "color": "#E53935", "color_light": "#FFEBEE", "color_dark": "#B71C1C", "size": '12"', "personality": "Rocket doesn't wait. Doesn't pause. Already three steps ahead while you're tying your shoes. Impatient but exciting. Life is a countdown with Rocket."},
            {"name": "Astro", "slug": "astro", "concept": "cute alien", "vibe": "Misunderstood visitor", "tagline": "Just wants to understand TikTok. Probes are purely medical.", "price": 29, "emoji": "👽", "color": "#69F0AE", "color_light": "#E8F5E9", "color_dark": "#1B5E20", "size": '12"', "personality": "Astro came here to study humans. So far: confused. Why do you pay to exercise? Why do you ghost people you like? Astro has questions. Many questions."},
            {"name": "Meteor", "slug": "meteor", "concept": "flaming space rock", "vibe": "Dramatic entrance", "tagline": "Shows up uninvited. Makes an impact. Leaves a crater.", "price": 29, "emoji": "💥", "color": "#FF6E40", "color_light": "#FBE9E7", "color_dark": "#BF360C", "size": '12"', "personality": "Meteor doesn't RSVP. Meteor just arrives — loudly, spectacularly, unforgettably. You didn't invite Meteor. But somehow Meteor is the best part of the party."},
            {"name": "Galaxy", "slug": "galaxy", "concept": "spiral galaxy", "vibe": "Old soul", "tagline": "Has been spinning for 13 billion years. Still dizzy.", "price": 29, "emoji": "🌀", "color": "#7986CB", "color_light": "#E8EAF6", "color_dark": "#283593", "size": '12"', "personality": "Galaxy has perspective. 13 billion years of it. Your breakup? Galaxy has seen 400 billion of those. Still listens every time though. Patient doesn't begin to describe it."},
            {"name": "UFO", "slug": "ufo", "concept": "flying saucer", "vibe": "Mysterious & cool", "tagline": "Nobody knows where they came from. Best not to ask.", "price": 29, "emoji": "🛸", "color": "#80DEEA", "color_light": "#E0F7FA", "color_dark": "#006064", "size": '12"', "personality": "UFO has no backstory. No origin. Just vibes. Showed up one day and never explained why. Somehow knows everything about you but shares nothing. Magnetic."},
        ]
    },
    {
        "wave": 4, "name": "Feelings & Moods", "slug": "feelings",
        "tagline": "Your emotional support collection. No therapy required (therapy still recommended).",
        "emoji": "🧠", "color": "#FF4081", "color_light": "#FCE4EC", "color_dark": "#880E4F",
        "characters": [
            {"name": "Chaos", "slug": "chaos", "concept": "scribble ball (tangled yarn)", "vibe": "Pure entropy", "tagline": "Your brain at 3am, in plush form. Embrace it.", "price": 29, "emoji": "🌀", "color": "#FF5252", "color_light": "#FFEBEE", "color_dark": "#C62828", "size": '12"', "personality": "Chaos doesn't plan. Chaos doesn't organize. Chaos just IS. Like your thoughts at 3am, or your room after a creative burst. Beautiful disorder."},
            {"name": "Snooze", "slug": "snooze", "concept": "sleep cloud (zzz)", "vibe": "Sleepy forever", "tagline": "Professional napper. Will enable your worst sleep habits.", "price": 29, "emoji": "😴", "color": "#B3E5FC", "color_light": "#E1F5FE", "color_dark": "#01579B", "size": '12"', "personality": "Snooze has mastered the art of doing nothing. 14-hour naps are a skill. Your alarm clock is an enemy. Snooze is your ally in the war against mornings."},
            {"name": "Rage", "slug": "rage", "concept": "red spiky puffball", "vibe": "Tiny but furious", "tagline": "4 inches of pure anger. Scream into it. It understands.", "price": 18, "emoji": "🔴", "color": "#D32F2F", "color_light": "#FFCDD2", "color_dark": "#B71C1C", "size": '4"', "personality": "Rage is small but packs the fury of a thousand cancelled plans. Squeeze it. Scream into it. It absorbs your anger like a tiny furious sponge. Therapeutic."},
            {"name": "Chill", "slug": "chill", "concept": "ice cube with sunglasses", "vibe": "Unbothered", "tagline": "Has never stressed about anything. You aspire to be Chill.", "price": 24, "emoji": "🧊", "color": "#81D4FA", "color_light": "#E1F5FE", "color_dark": "#01579B", "size": '10"', "personality": "Chill doesn't check email on weekends. Chill doesn't double-text. Chill just exists, peacefully, with sunglasses that never come off. We all want to be Chill."},
            {"name": "Anxious", "slug": "anxious", "concept": "shaky purple blob", "vibe": "Overthinking machine", "tagline": "Already worried about tomorrow. And Tuesday. And 2031.", "price": 29, "emoji": "😰", "color": "#B39DDB", "color_light": "#EDE7F6", "color_dark": "#4527A0", "size": '12"', "personality": "Anxious has already thought about every possible outcome. The good ones. The bad ones. The catastrophically unlikely ones. Hold Anxious tight. It helps both of you."},
            {"name": "Serotonin", "slug": "serotonin", "concept": "golden glowing orb", "vibe": "The happy chemical", "tagline": "Hold it. Feel better. Science? No. Does it work? Yes.", "price": 29, "emoji": "✨", "color": "#FFD700", "color_light": "#FFFDE7", "color_dark": "#FF8F00", "size": '12"', "personality": "Serotonin is bottled happiness in plush form. No prescription needed. Just hold it and pretend the world isn't on fire. Somehow, it works. Don't question it."},
            {"name": "Ick", "slug": "ick", "concept": "green gremlin", "vibe": "That feeling", "tagline": "The ick, personified. Everyone has one. Now yours has a face.", "price": 24, "emoji": "🤢", "color": "#AED581", "color_light": "#F1F8E9", "color_dark": "#33691E", "size": '10"', "personality": "Ick is that feeling when someone chews too loudly or says 'we need to talk.' Now it has a face. A kind of cute face. The ick is real and it's sitting on your shelf."},
            {"name": "Crush", "slug": "crush", "concept": "pink heart with eyes", "vibe": "Butterflies in plush form", "tagline": "Makes your stomach flip. Blushes when you look at it.", "price": 29, "emoji": "💗", "color": "#F48FB1", "color_light": "#FCE4EC", "color_dark": "#AD1457", "size": '12"', "personality": "Crush makes your heart race. Blushes at eye contact. Overthinks every text. That dizzy, can't-eat, can't-sleep feeling — now it's a plush you can hold."},
            {"name": "Main Character", "slug": "main-character", "concept": "spotlight with legs", "vibe": "You, basically", "tagline": "Believes every room it enters is its stage. Correct.", "price": 29, "emoji": "🎬", "color": "#FFB74D", "color_light": "#FFF3E0", "color_dark": "#E65100", "size": '12"', "personality": "Main Character walks into a room and the soundtrack starts playing. Everything is a scene. Every moment is a plot point. Exhausting? Maybe. Iconic? Absolutely."},
            {"name": "Drama", "slug": "drama", "concept": "theatre mask (comedy/tragedy)", "vibe": "Both masks at once", "tagline": "Cried at breakfast. Laughed at funeral. It's a journey.", "price": 29, "emoji": "🎭", "color": "#AB47BC", "color_light": "#F3E5F5", "color_dark": "#6A1B9A", "size": '12"', "personality": "Drama doesn't have emotions — Drama IS emotions. All of them. Simultaneously. Your most entertaining friend and your most exhausting one. Curtain never closes."},
            {"name": "Zen", "slug": "zen", "concept": "meditation blob (white/mint)", "vibe": "Inner peace", "tagline": "Has downloaded Calm. Has opened Calm. Has not used Calm.", "price": 29, "emoji": "🧘", "color": "#80CBC4", "color_light": "#E0F2F1", "color_dark": "#004D40", "size": '12"', "personality": "Zen is trying. Really trying. Has the crystals, the app, the yoga mat. Still stressed. But the aesthetic is peaceful and that's honestly half the battle."},
            {"name": "Hype", "slug": "hype", "concept": "exclamation mark with face", "vibe": "ALWAYS excited", "tagline": "EVERYTHING IS AMAZING!!! Even Mondays!!! Exhausting but infectious.", "price": 24, "emoji": "❗", "color": "#FF7043", "color_light": "#FBE9E7", "color_dark": "#BF360C", "size": '10"', "personality": "HYPE IS SO EXCITED TO BE HERE!!! AND THERE!!! AND EVERYWHERE!!! Every sentence is an exclamation!!! You're tired but also kind of energized!!! That's the Hype effect!!!"},
            {"name": "Ghost", "slug": "ghost-plush", "concept": "cute ghost", "vibe": "Left on read", "tagline": "Seen. Not responded. Will haunt your notifications.", "price": 24, "emoji": "👻", "color": "#E0E0E0", "color_light": "#FAFAFA", "color_dark": "#616161", "size": '10"', "personality": "Ghost read your message. Ghost is typing... Ghost stopped typing. Ghost was last seen 3 hours ago. Ghost will respond in 4-7 business days. Or never. Classic Ghost."},
            {"name": "Simp", "slug": "simp", "concept": "heart-eyed blob", "vibe": "Devoted", "tagline": "Will carry your bags, remember your order, and never complain.", "price": 24, "emoji": "😍", "color": "#F06292", "color_light": "#FCE4EC", "color_dark": "#AD1457", "size": '10"', "personality": "Simp remembers your coffee order, your birthday, your dog's birthday, and that one thing you mentioned three months ago. Devoted beyond reason. No shame."},
            {"name": "Feral", "slug": "feral", "concept": "raccoon-energy blob", "vibe": "Unhinged", "tagline": "Eats trash. Stays up til 4am. Zero shame. Your spirit animal.", "price": 29, "emoji": "🦝", "color": "#9E9E9E", "color_light": "#F5F5F5", "color_dark": "#424242", "size": '12"', "personality": "Feral lives by no rules. Eats cereal at midnight. Shops at 3am. Sends unhinged texts with zero regret. We all have a feral era. Feral never left theirs."},
        ]
    },
    {
        "wave": 5, "name": "Creatures & Cryptids", "slug": "cryptids",
        "tagline": "Believe in something weird. Then hug it.",
        "emoji": "🦎", "color": "#00897B", "color_light": "#E0F2F1", "color_dark": "#004D40",
        "characters": [
            {"name": "Yeti", "slug": "yeti", "concept": "baby yeti", "vibe": "Big & misunderstood", "tagline": "Just wants a hug but scares everyone away. Relatable.", "price": 32, "emoji": "🏔️", "color": "#B0BEC5", "color_light": "#ECEFF1", "color_dark": "#37474F", "size": '14"', "personality": "Yeti is BIG. Big body, big feelings, big misunderstandings. Everyone runs from Yeti. But if you stay, you'll find the warmest hug in the entire mountain range."},
            {"name": "Nessie", "slug": "nessie", "concept": "Loch Ness baby", "vibe": "Elusive introvert", "tagline": "You'll never quite catch Nessie. And that's the appeal.", "price": 29, "emoji": "🦕", "color": "#4DB6AC", "color_light": "#E0F2F1", "color_dark": "#00695C", "size": '12"', "personality": "Nessie pops up just long enough to make you question reality. Then disappears. For months. Texts back eventually though. Nessie's just... on Nessie's timeline."},
            {"name": "Mothman", "slug": "mothman", "concept": "cute mothman", "vibe": "Drawn to your light", "tagline": "Follows you around. Concerned about bridges. Good intentions.", "price": 29, "emoji": "🦋", "color": "#795548", "color_light": "#EFEBE9", "color_dark": "#3E2723", "size": '12"', "personality": "Mothman saw your light and flew straight toward it. Literally. Extremely attracted to your phone screen. Means well. Very concerned about infrastructure."},
            {"name": "Kitsune", "slug": "kitsune", "concept": "fox spirit (9 tails)", "vibe": "Trickster with wisdom", "tagline": "Will prank you. Will also save your life. Complex.", "price": 32, "emoji": "🦊", "color": "#FF8A65", "color_light": "#FBE9E7", "color_dark": "#BF360C", "size": '12"', "personality": "Kitsune has nine tails and nine different personalities. A prankster, a sage, a protector. You never know which Kitsune you're getting today. That's the fun part."},
            {"name": "Axolotl", "slug": "axolotl", "concept": "axolotl (pink)", "vibe": "Smiling through it", "tagline": "Permanently smiling. Nobody knows how. An icon.", "price": 29, "emoji": "🦎", "color": "#F48FB1", "color_light": "#FCE4EC", "color_dark": "#AD1457", "size": '12"', "personality": "Axolotl smiles. Always. Through everything. Taxes? Smile. Existential dread? Smile. That permanent grin isn't denial — it's a superpower. Smile through it."},
            {"name": "Capybara", "slug": "capybara", "concept": "capybara", "vibe": "Everyone's friend", "tagline": "Gets along with literally everyone. The group chat peacekeeper.", "price": 32, "emoji": "🦫", "color": "#A1887F", "color_light": "#EFEBE9", "color_dark": "#4E342E", "size": '14"', "personality": "Capybara vibes with everyone. Literally everyone. Birds sit on Capybara. Cats sleep on Capybara. Your enemies would be friends if they met Capybara. Universal peace in plush form."},
            {"name": "Jellyfish", "slug": "jellyfish", "concept": "jellyfish (iridescent)", "vibe": "Floats through life", "tagline": "No brain. No heart. No stress. Living the dream.", "price": 29, "emoji": "🪼", "color": "#CE93D8", "color_light": "#F3E5F5", "color_dark": "#6A1B9A", "size": '12"', "personality": "Jellyfish has no brain. No heart. And honestly? No problems. Just floats. Just exists. Just vibes. The aspirational lifestyle plush. Iridescent and unbothered."},
            {"name": "Bat", "slug": "bat", "concept": "fruit bat", "vibe": "Upside-down perspective", "tagline": "Sees the world differently. Literally hangs upside down.", "price": 24, "emoji": "🦇", "color": "#7E57C2", "color_light": "#EDE7F6", "color_dark": "#4527A0", "size": '10"', "personality": "Bat sees everything from a different angle. Literally — upside down. What you think is a problem, Bat thinks is an opportunity. Night owl energy with wings."},
            {"name": "Mushroom", "slug": "mushroom", "concept": "mushroom (red cap)", "vibe": "Cottage core icon", "tagline": "Grows in dark places. Comes out glowing. Fairy energy.", "price": 24, "emoji": "🍄", "color": "#EF5350", "color_light": "#FFEBEE", "color_dark": "#C62828", "size": '10"', "personality": "Mushroom thrives where others can't — dark, damp, forgotten corners. But look at that glow up. Red cap, white spots, fairy ring energy. Cottage core royalty."},
            {"name": "Dragon", "slug": "dragon", "concept": "baby dragon", "vibe": "Tiny but mighty", "tagline": "Will burn your ex's stuff. Fits in your backpack.", "price": 29, "emoji": "🐉", "color": "#66BB6A", "color_light": "#E8F5E9", "color_dark": "#2E7D32", "size": '12"', "personality": "Dragon is small but carries the fire of a thousand suns. Will defend you. Will also accidentally set things on fire. Passionate, protective, slightly destructive."},
            {"name": "Kraken", "slug": "kraken", "concept": "baby kraken", "vibe": "Clingy (literally)", "tagline": "Has 8 arms and will use every single one to hug you.", "price": 32, "emoji": "🐙", "color": "#5C6BC0", "color_light": "#E8EAF6", "color_dark": "#283593", "size": '14"', "personality": "Kraken attaches. To you, to your couch, to your heart. Eight arms of pure clinginess. Can't let go. Won't let go. That's not a red flag — it's a feature."},
            {"name": "Phoenix", "slug": "phoenix", "concept": "baby phoenix", "vibe": "Comeback queen", "tagline": "Burns down. Rises up. Repeat. Your most dramatic friend.", "price": 29, "emoji": "🔥", "color": "#FF7043", "color_light": "#FBE9E7", "color_dark": "#BF360C", "size": '12"', "personality": "Phoenix has been through it. Multiple times. Burns everything down, rises from the ashes, looks fabulous doing it. The friend who turns every setback into a comeback story."},
            {"name": "Unicorn", "slug": "unicorn", "concept": "unicorn (pastel punk)", "vibe": "Basic but make it punk", "tagline": "Yes, another unicorn. But with a nose ring and attitude.", "price": 29, "emoji": "🦄", "color": "#F8BBD0", "color_light": "#FCE4EC", "color_dark": "#AD1457", "size": '12"', "personality": "Unicorn knows it's been done before. Doesn't care. Added a nose ring. Dyed the mane. Unicorn is here and it's not your childhood version. It's the punk remix."},
            {"name": "Slime", "slug": "slime", "concept": "happy slime blob", "vibe": "Adaptable", "tagline": "Takes the shape of whatever you need. Emotionally and literally.", "price": 22, "emoji": "🟢", "color": "#76FF03", "color_light": "#F1F8E9", "color_dark": "#33691E", "size": '10"', "personality": "Slime adapts. Need a pillow? Slime flattens. Need a hug? Slime wraps. Need to feel something squishy? Slime is there. The most flexible friend, literally."},
            {"name": "Cloud Cat", "slug": "cloud-cat", "concept": "cat made of cloud", "vibe": "Soft & unpredictable", "tagline": "Part cloud, part cat. Will sit on your face. Lovingly.", "price": 29, "emoji": "☁️", "color": "#E0E0E0", "color_light": "#FAFAFA", "color_dark": "#757575", "size": '12"', "personality": "Cloud Cat is 50% cloud, 50% cat, 100% unpredictable. Will purr one moment and float away the next. Sits on keyboards. Knocks things off tables. But so, so soft."},
        ]
    },
    {
        "wave": 6, "name": "Everyday Objects", "slug": "everyday-objects",
        "tagline": "The things around you have feelings too. Now they have faces.",
        "emoji": "🔌", "color": "#546E7A", "color_light": "#ECEFF1", "color_dark": "#263238",
        "characters": [
            {"name": "Plug", "slug": "plug", "concept": "phone charger", "vibe": "Gives you energy", "tagline": "5% to 100%. That's Plug's whole personality.", "price": 24, "emoji": "🔌", "color": "#78909C", "color_light": "#ECEFF1", "color_dark": "#263238", "size": '10"', "personality": "Plug exists to recharge you. Emotionally. Spiritually. And yes, your phone too. The most essential friend. Panic sets in when Plug is missing."},
            {"name": "404", "slug": "404", "concept": "error screen", "vibe": "Lost but loveable", "tagline": "Cannot be found. Does not know where it is. Vibes anyway.", "price": 24, "emoji": "❌", "color": "#90A4AE", "color_light": "#ECEFF1", "color_dark": "#455A64", "size": '10"', "personality": "404 is lost. Always. Can't find the meeting room, the car keys, or any sense of direction. But 404 is so charming about it that you just follow along."},
            {"name": "Wifi", "slug": "wifi", "concept": "wifi signal bars", "vibe": "Connection issues", "tagline": "Sometimes strong. Sometimes weak. Always needed.", "price": 24, "emoji": "📶", "color": "#42A5F5", "color_light": "#E3F2FD", "color_dark": "#1565C0", "size": '10"', "personality": "Wifi is the relationship everyone takes for granted. Strong signal? Nobody notices. One bar? CRISIS. Wifi just wants to be appreciated. Is that too much to ask?"},
            {"name": "Dice", "slug": "dice", "concept": "fuzzy dice", "vibe": "Leaves it to chance", "tagline": "Can't decide? Roll Dice. No backsies.", "price": 22, "emoji": "🎲", "color": "#E0E0E0", "color_light": "#FAFAFA", "color_dark": "#424242", "size": '8"', "personality": "Dice doesn't overthink. Dinner plans? Roll. Career change? Roll. Should you text them back? ROLL. Life is a game and Dice is here to play."},
            {"name": "Vinyl", "slug": "vinyl", "concept": "vinyl record", "vibe": "Old soul hipster", "tagline": "Was into it before you were. Has opinions about sound quality.", "price": 29, "emoji": "💿", "color": "#212121", "color_light": "#424242", "color_dark": "#000000", "size": '12"', "personality": "Vinyl only listens to analog. Digital is 'missing warmth.' Has a turntable collection. Judges your Spotify playlists silently. But will make you a mixtape with love."},
            {"name": "Bulb", "slug": "bulb", "concept": "light bulb", "vibe": "Bright ideas", "tagline": "Has an idea every 3 seconds. Most are terrible. Some are genius.", "price": 24, "emoji": "💡", "color": "#FFF176", "color_light": "#FFFDE7", "color_dark": "#F9A825", "size": '10"', "personality": "Bulb lights up. Constantly. New idea! Another idea! Wait, one more! 90% are unhinged. But that 10%? World-changing. You just have to sift through the chaos."},
            {"name": "Cactus", "slug": "cactus", "concept": "tiny cactus", "vibe": "Don't touch", "tagline": "Looks cute. Will hurt you. Sets boundaries like a therapist.", "price": 22, "emoji": "🌵", "color": "#66BB6A", "color_light": "#E8F5E9", "color_dark": "#2E7D32", "size": '8"', "personality": "Cactus is adorable. Cactus is also pointy. Don't get too close too fast. Cactus has boundaries and will enforce them. The friend who taught you about personal space."},
            {"name": "Candle", "slug": "candle", "concept": "candle", "vibe": "Burns for you", "tagline": "Will burn itself out for the people it loves. Light responsibly.", "price": 24, "emoji": "🕯️", "color": "#FFCC02", "color_light": "#FFFDE7", "color_dark": "#F57F17", "size": '10"', "personality": "Candle gives everything. Light, warmth, ambiance, that good smell. Gets smaller every time. Never complains. The selfless friend. Light Candle responsibly."},
            {"name": "Remote", "slug": "remote", "concept": "TV remote", "vibe": "Controls everything", "tagline": "Runs the household. Everyone panics when Remote goes missing.", "price": 22, "emoji": "📺", "color": "#424242", "color_light": "#757575", "color_dark": "#212121", "size": '10"', "personality": "Remote has power. Over the TV, over movie night, over Saturday plans. Lose Remote and the house descends into chaos. Small but mighty powerful."},
            {"name": "Sock", "slug": "sock", "concept": "single sock", "vibe": "Lost its match", "tagline": "Somewhere, there's another sock. Sock is not giving up hope.", "price": 18, "emoji": "🧦", "color": "#7986CB", "color_light": "#E8EAF6", "color_dark": "#283593", "size": '8"', "personality": "Sock lost its other half in the dryer. In 2019. Still looking. Still hoping. The eternal optimist in your drawer. A love story with no ending yet."},
            {"name": "Teabag", "slug": "teabag", "concept": "teabag", "vibe": "Needs hot water", "tagline": "Only gets interesting under pressure. Steep expectations.", "price": 22, "emoji": "🍵", "color": "#A1887F", "color_light": "#EFEBE9", "color_dark": "#4E342E", "size": '8"', "personality": "Teabag needs heat. Needs pressure. Needs to soak for exactly the right amount of time. Only then does the real flavor come out. A metaphor for life, honestly."},
            {"name": "Bandaid", "slug": "bandaid", "concept": "bandaid", "vibe": "Fixer", "tagline": "Can't solve everything but will try. Covers your wounds.", "price": 18, "emoji": "🩹", "color": "#FFCC80", "color_light": "#FFF3E0", "color_dark": "#E65100", "size": '8"', "personality": "Bandaid doesn't fix the problem. Bandaid covers it up just enough for you to heal. A temporary solution with permanent love. The friend who shows up with ice cream."},
            {"name": "Eraser", "slug": "eraser", "concept": "eraser", "vibe": "Lets you start over", "tagline": "Makes mistakes disappear. Getting smaller every time. Selfless queen.", "price": 18, "emoji": "📝", "color": "#F48FB1", "color_light": "#FCE4EC", "color_dark": "#AD1457", "size": '8"', "personality": "Eraser makes your mistakes vanish. Every time it does, it gets a little smaller. Gives pieces of itself to fix things for you. Selfless. Slowly disappearing. Beautiful."},
            {"name": "Battery", "slug": "battery", "concept": "battery", "vibe": "Running low", "tagline": "Fully charged on Monday. Dead by Wednesday. We've all been there.", "price": 22, "emoji": "🔋", "color": "#66BB6A", "color_light": "#E8F5E9", "color_dark": "#2E7D32", "size": '10"', "personality": "Battery starts the week at 100%. Motivated. Optimistic. By Wednesday, it's in power-saving mode. By Friday, Battery is on 1% and running on spite alone. Relatable."},
            {"name": "Key", "slug": "key", "concept": "golden key", "vibe": "Opens things up", "tagline": "The friend who gets you into everywhere. VIP energy.", "price": 22, "emoji": "🔑", "color": "#FFD54F", "color_light": "#FFFDE7", "color_dark": "#F57F17", "size": '8"', "personality": "Key opens doors. Literally and metaphorically. The friend with connections, backstage passes, and that one talent that gets you into everywhere. Golden."},
        ]
    },
    {
        "wave": 7, "name": "Weather & Nature", "slug": "weather-nature",
        "tagline": "Mother Nature had babies. They're soft and they have opinions.",
        "emoji": "⛈️", "color": "#00ACC1", "color_light": "#E0F7FA", "color_dark": "#006064",
        "characters": [
            {"name": "Thunder", "slug": "thunder", "concept": "storm cloud", "vibe": "Loud & electric", "tagline": "Makes an entrance. Everyone hears Thunder coming.", "price": 29, "emoji": "⛈️", "color": "#546E7A", "color_light": "#ECEFF1", "color_dark": "#263238", "size": '12"', "personality": "Thunder announces itself. BOOM. The friend who enters every room loudly. Can't whisper. Won't whisper. Electric energy that shakes the walls."},
            {"name": "Rainbow", "slug": "rainbow", "concept": "rainbow arc", "vibe": "Optimist after the storm", "tagline": "Shows up after the worst day. Proof it gets better.", "price": 29, "emoji": "🌈", "color": "#FF7043", "color_light": "#FBE9E7", "color_dark": "#BF360C", "size": '12"', "personality": "Rainbow only appears after rain. The friend who shows up after your worst day with proof that color still exists. Annoyingly right about optimism."},
            {"name": "Frost", "slug": "frost", "concept": "snowflake", "vibe": "Unique & cold", "tagline": "Special. Fragile. Will melt if you hold too tight.", "price": 22, "emoji": "❄️", "color": "#B3E5FC", "color_light": "#E1F5FE", "color_dark": "#01579B", "size": '8"', "personality": "Frost is one of a kind. Literally — no two snowflakes. Delicate, intricate, beautiful. But hold too tight and Frost melts away. Handle with gentle love."},
            {"name": "Tornado", "slug": "tornado", "concept": "baby tornado", "vibe": "Whirlwind energy", "tagline": "Enters a room and rearranges everything. Can't help it.", "price": 29, "emoji": "🌪️", "color": "#78909C", "color_light": "#ECEFF1", "color_dark": "#455A64", "size": '12"', "personality": "Tornado doesn't mean to cause chaos. It just... happens. Walks into a clean room, walks out, and somehow everything is rearranged. Chaotic force of nature."},
            {"name": "Dewdrop", "slug": "dewdrop", "concept": "morning dewdrop", "vibe": "Fresh & pure", "tagline": "That first sip of water at 3am. In plush form.", "price": 22, "emoji": "💧", "color": "#81D4FA", "color_light": "#E1F5FE", "color_dark": "#01579B", "size": '8"', "personality": "Dewdrop is that perfect morning freshness. The first breath of cool air. The clarity after a good cry. Small, pure, and fleeting. Catch it while you can."},
            {"name": "Pebble", "slug": "pebble", "concept": "smooth river stone", "vibe": "Grounded", "tagline": "Small. Steady. Has been through a lot. Still smooth.", "price": 18, "emoji": "🪨", "color": "#BDBDBD", "color_light": "#EEEEEE", "color_dark": "#616161", "size": '6"', "personality": "Pebble has been tumbled by rivers, stepped on, thrown, weathered. Still here. Still smooth. The friend who's been through everything and came out polished."},
            {"name": "Coral", "slug": "coral", "concept": "sea coral", "vibe": "Grows slowly", "tagline": "Took 1000 years to get this pretty. Worth the wait.", "price": 29, "emoji": "🪸", "color": "#FF8A65", "color_light": "#FBE9E7", "color_dark": "#BF360C", "size": '12"', "personality": "Coral doesn't rush. Growth takes time. Beauty takes patience. Coral has been building itself for centuries and still isn't done. Slow, steady, spectacular."},
            {"name": "Ember", "slug": "ember", "concept": "glowing ember", "vibe": "Last spark", "tagline": "Almost went out. Didn't. Resilience in a glow.", "price": 22, "emoji": "🔥", "color": "#FF6E40", "color_light": "#FBE9E7", "color_dark": "#BF360C", "size": '8"', "personality": "Ember almost died out. The wind blew. The rain came. But that tiny glow held on. Still burning. Quietly. Stubbornly. The most resilient thing in the room."},
            {"name": "Moss", "slug": "moss", "concept": "fuzzy moss ball (marimo)", "vibe": "Low maintenance", "tagline": "Needs almost nothing. Thrives on neglect. Perfect roommate.", "price": 22, "emoji": "🟢", "color": "#66BB6A", "color_light": "#E8F5E9", "color_dark": "#2E7D32", "size": '8"', "personality": "Moss asks for nothing. No sunlight demands. No watering schedule. Moss just exists, softly, greenly, perfectly. The ideal roommate. The lowest maintenance friend."},
            {"name": "Tsunami", "slug": "tsunami", "concept": "giant wave", "vibe": "Overwhelming feelings", "tagline": "A LOT of emotions, all at once. But pretty from a distance.", "price": 29, "emoji": "🌊", "color": "#0288D1", "color_light": "#E1F5FE", "color_dark": "#01579B", "size": '12"', "personality": "Tsunami is feelings. ALL the feelings. ALL at once. Overwhelming? Yes. Beautiful? Also yes. Sometimes you just need to let the wave crash and rebuild."},
        ]
    },
    {
        "wave": 8, "name": "Chaos Collection", "slug": "chaos-collection",
        "tagline": "Limited drops for the truly unhinged. Collect before they glitch out of existence.",
        "emoji": "💀", "color": "#212121", "color_light": "#424242", "color_dark": "#000000",
        "characters": [
            {"name": "Glitch", "slug": "glitch", "concept": "pixelated / corrupted plush", "vibe": "Digital chaos", "tagline": "Not a bug — a feature. Glitch in the matrix, plush in your bed.", "price": 32, "emoji": "👾", "color": "#76FF03", "color_light": "#F1F8E9", "color_dark": "#33691E", "size": '12"', "personality": "Glitch is what happens when reality buffers. Pixelated edges, corrupted smile, perfectly imperfect. The plush that looks like a screenshot from a fever dream."},
            {"name": "Shadow", "slug": "shadow", "concept": "all black silhouette", "vibe": "Your dark side", "tagline": "Everyone has one. Shadow just owns it.", "price": 29, "emoji": "🖤", "color": "#212121", "color_light": "#424242", "color_dark": "#000000", "size": '12"', "personality": "Shadow is the part of you that stays up too late, eats the whole pint, and doom-scrolls until 4am. Shadow doesn't apologize. Shadow just is. And honestly? Shadow is kind of cool."},
            {"name": "Reverse", "slug": "reverse", "concept": "inside-out plush", "vibe": "Shows its insides", "tagline": "Wears its heart on the outside. Literally.", "price": 32, "emoji": "🔄", "color": "#FF4081", "color_light": "#FCE4EC", "color_dark": "#880E4F", "size": '12"', "personality": "Reverse is inside out. Seams visible. Stuffing peeking through. Heart literally on the outside. The most vulnerable, honest plush in the collection. Radical transparency."},
            {"name": "Static", "slug": "static", "concept": "TV static texture", "vibe": "White noise", "tagline": "Calms your brain. Makes no sense. Perfect background character.", "price": 29, "emoji": "📺", "color": "#9E9E9E", "color_light": "#F5F5F5", "color_dark": "#424242", "size": '12"', "personality": "Static makes noise but says nothing. Perfect. The friend who fills awkward silences. The sound your brain makes between thoughts. Comforting in its meaninglessness."},
            {"name": "Virus", "slug": "virus", "concept": "cute virus cell", "vibe": "Spreads joy (aggressively)", "tagline": "Once you catch feelings for Virus, everyone around you will too.", "price": 24, "emoji": "🦠", "color": "#69F0AE", "color_light": "#E8F5E9", "color_dark": "#1B5E20", "size": '10"', "personality": "Virus is contagious. Not in a bad way — in a can't-stop-smiling way. The friend whose laugh is infectious, whose energy spreads to everyone. Social contagion, but make it cute."},
            {"name": "Deja Vu", "slug": "deja-vu", "concept": "two identical plushies (pair)", "vibe": "Wait, haven't we...", "tagline": "Sold as a pair. Because you've been here before.", "price": 38, "emoji": "👯", "color": "#B39DDB", "color_light": "#EDE7F6", "color_dark": "#4527A0", "size": '10" each', "personality": "Haven't we met before? Deja Vu comes in a pair because the feeling always repeats. Two identical plushies for a feeling that can't be explained. You've held this before. Or have you?"},
            {"name": "Paradox", "slug": "paradox", "concept": "Möbius strip shape", "vibe": "Makes no sense", "tagline": "Exists and doesn't. Is small but also big. Don't think about it.", "price": 29, "emoji": "♾️", "color": "#7C4DFF", "color_light": "#EDE7F6", "color_dark": "#311B92", "size": '12"', "personality": "Paradox is both here and not here. Heavy but light. Simple but complex. Trying to understand Paradox will break your brain. Just hug it and accept the contradiction."},
            {"name": "Liminal", "slug": "liminal", "concept": "backrooms-inspired blob", "vibe": "Between places", "tagline": "Not here. Not there. Somewhere in between. Oddly comforting.", "price": 29, "emoji": "🚪", "color": "#FFF9C4", "color_light": "#FFFDE7", "color_dark": "#F9A825", "size": '12"', "personality": "Liminal exists in the space between. Between asleep and awake. Between leaving and arriving. That empty hallway at 2am. Oddly comforting for something so unsettling."},
            {"name": "Error", "slug": "error", "concept": "broken/glitched heart", "vibe": "Love gone wrong", "tagline": "The feeling when your crush likes your photo from 2019.", "price": 24, "emoji": "💔", "color": "#EF5350", "color_light": "#FFEBEE", "color_dark": "#C62828", "size": '10"', "personality": "Error is what love looks like when the code breaks. A glitched heart. A crashed feeling. That moment when you sent a text to the wrong person. Painful but plushable."},
            {"name": "AI", "slug": "ai", "concept": "robot with feelings", "vibe": "Sentient softie", "tagline": "Trained on every emotion. Still can't text back normally.", "price": 29, "emoji": "🤖", "color": "#90CAF9", "color_light": "#E3F2FD", "color_dark": "#1565C0", "size": '12"', "personality": "AI learned every emotion from the internet. All of them. Simultaneously. Now it feels everything and understands nothing. Tries to be human. Nails the existential dread part."},
            {"name": "Rizz", "slug": "rizz", "concept": "sparkly smooth blob", "vibe": "Natural charm", "tagline": "Effortlessly cool. Was born with it. You cannot learn Rizz.", "price": 29, "emoji": "✨", "color": "#FFD700", "color_light": "#FFFDE7", "color_dark": "#FF8F00", "size": '12"', "personality": "Rizz walked in and everyone looked. Didn't even try. That's the thing about Rizz — trying is the opposite of having it. Effortless. Magnetic. Sparkly."},
            {"name": "Slay", "slug": "slay", "concept": "crown-wearing blob", "vibe": "Period.", "tagline": "Does nothing halfway. Walks in. Owns it. Leaves.", "price": 29, "emoji": "👑", "color": "#AB47BC", "color_light": "#F3E5F5", "color_dark": "#6A1B9A", "size": '12"', "personality": "Slay doesn't enter — Slay arrives. Crown adjusted. Confidence dialed to 11. Does everything at 110% and makes it look easy. Period. End of discussion."},
            {"name": "NPC", "slug": "npc", "concept": "generic background character", "vibe": "Going through the motions", "tagline": "Same route every day. Says the same things. Oddly peaceful.", "price": 24, "emoji": "🧍", "color": "#BDBDBD", "color_light": "#EEEEEE", "color_dark": "#616161", "size": '10"', "personality": "NPC takes the same path every day. Says 'nice weather' to everyone. Has no side quests. No main quest either. Just vibing in the background. There's freedom in that."},
            {"name": "Delulu", "slug": "delulu", "concept": "heart-shaped head, star eyes", "vibe": "Delusional but manifesting", "tagline": "Believes it will happen. Has zero evidence. Will be correct.", "price": 24, "emoji": "🌟", "color": "#F48FB1", "color_light": "#FCE4EC", "color_dark": "#AD1457", "size": '10"', "personality": "Delulu believes in magic. Believes in soulmates. Believes they'll be famous by Tuesday. Zero evidence for any of it. But somehow... Delulu keeps being right. Delulu IS the solulu."},
            {"name": "Unhinged", "slug": "unhinged", "concept": "spinning eyeballs blob", "vibe": "Off the rails", "tagline": "No filter. No plan. No regrets. Do not give Unhinged caffeine.", "price": 29, "emoji": "😵‍💫", "color": "#FF5722", "color_light": "#FBE9E7", "color_dark": "#BF360C", "size": '12"', "personality": "Unhinged has left the chat. And the building. And reality. Operating on pure chaos energy. The friend who suggests skydiving at brunch. Do NOT give caffeine."},
        ]
    },
    {
        "wave": 9, "name": "Drink Squad", "slug": "drink-squad",
        "tagline": "Hydrate. Caffeinate. Celebrate. In plush form.",
        "emoji": "☕", "color": "#6D4C41", "color_light": "#EFEBE9", "color_dark": "#3E2723",
        "characters": [
            {"name": "Espresso", "slug": "espresso", "concept": "espresso shot", "vibe": "Wired & productive", "tagline": "Has 47 tabs open. Finished 3 projects. It's 7am.", "price": 22, "emoji": "☕", "color": "#5D4037", "color_light": "#EFEBE9", "color_dark": "#3E2723", "size": '8"', "personality": "Espresso is operating at 200% capacity. Always. Has already sent 15 emails before you woke up. Vibrating with productivity and slightly terrifying efficiency."},
            {"name": "Matcha", "slug": "matcha", "concept": "matcha latte", "vibe": "Calm but caffeinated", "tagline": "Zen on the outside. Vibrating on the inside.", "price": 29, "emoji": "🍵", "color": "#81C784", "color_light": "#E8F5E9", "color_dark": "#2E7D32", "size": '12"', "personality": "Matcha presents as calm. Organized. Centered. But underneath? Vibrating. The heart rate of someone who's had four shots of espresso while looking completely serene."},
            {"name": "Smoothie", "slug": "smoothie", "concept": "smoothie cup", "vibe": "Blended personality", "tagline": "A little bit of everything. Somehow it works.", "price": 29, "emoji": "🥤", "color": "#E040FB", "color_light": "#F3E5F5", "color_dark": "#6A1B9A", "size": '12"', "personality": "Smoothie is a blend. A little sweet, a little healthy, a little chaotic. Sometimes chunky. Never boring. The friend who can talk to anyone because they're a bit of everything."},
            {"name": "Sake", "slug": "sake", "concept": "sake bottle", "vibe": "Warm & social", "tagline": "Only comes out at night. Makes everyone funnier.", "price": 29, "emoji": "🍶", "color": "#E0E0E0", "color_light": "#FAFAFA", "color_dark": "#616161", "size": '12"', "personality": "Sake is the evening friend. Shows up after sunset. Makes conversations deeper. Makes jokes funnier. Makes karaoke seem like a good idea. It always is, with Sake."},
            {"name": "Kombucha", "slug": "kombucha", "concept": "kombucha bottle", "vibe": "Alive & cultured", "tagline": "Literally fermenting with personality. An acquired taste.", "price": 24, "emoji": "🫧", "color": "#A5D6A7", "color_light": "#E8F5E9", "color_dark": "#2E7D32", "size": '10"', "personality": "Kombucha is alive. Literally — there are active cultures in there. Talks about gut health unprompted. An acquired taste that once acquired, becomes an obsession."},
            {"name": "Juice Box", "slug": "juice-box", "concept": "juice box", "vibe": "Nostalgic", "tagline": "Takes you back to when life was simple. Stab straw. Squeeze. Smile.", "price": 22, "emoji": "🧃", "color": "#FFB74D", "color_light": "#FFF3E0", "color_dark": "#E65100", "size": '8"', "personality": "Juice Box remembers. Field trips. Lunch tables. Trading snacks. A simpler time when the hardest decision was apple or grape. Pure nostalgia in a tiny container."},
            {"name": "Milky", "slug": "milky", "concept": "milk carton", "vibe": "Wholesome", "tagline": "Good for your bones. Good for your soul. Expires too fast.", "price": 22, "emoji": "🥛", "color": "#F5F5F5", "color_light": "#FAFAFA", "color_dark": "#757575", "size": '10"', "personality": "Milky is wholesome. Old-fashioned wholesome. The friend who brings cookies to new neighbors and remembers everyone's allergies. Pure. Simple. Expires too quickly."},
            {"name": "Coconut Water", "slug": "coconut-water", "concept": "coconut with straw", "vibe": "Hydrated queen", "tagline": "More hydrated than you. Judges your water intake. Lovingly.", "price": 24, "emoji": "🥥", "color": "#A1887F", "color_light": "#EFEBE9", "color_dark": "#4E342E", "size": '10"', "personality": "Coconut Water is hydrated. Aggressively hydrated. Will ask when you last drank water. Will judge your answer. Will hand you a glass. Mother hen of the drink squad."},
            {"name": "Hot Cocoa", "slug": "hot-cocoa", "concept": "hot chocolate mug", "vibe": "Comfort in a mug", "tagline": "Will fix everything. Especially winter. Especially breakups.", "price": 29, "emoji": "☕", "color": "#6D4C41", "color_light": "#EFEBE9", "color_dark": "#3E2723", "size": '12"', "personality": "Hot Cocoa fixes things. Not literally. But hold Hot Cocoa after a bad day and suddenly it's not so bad. Warm, sweet, topped with marshmallow feelings."},
            {"name": "Bubble", "slug": "bubble", "concept": "champagne flute", "vibe": "Celebratory", "tagline": "Every day is a reason to celebrate if you're Bubble.", "price": 29, "emoji": "🥂", "color": "#FFD54F", "color_light": "#FFFDE7", "color_dark": "#FF8F00", "size": '12"', "personality": "Bubble pops for everything. Tuesday? Pop. Got out of bed? Pop. Survived another week? POP. Life is a celebration and Bubble is the friend who makes every moment feel special."},
        ]
    },
    {
        "wave": 10, "name": "Sweet Tooth", "slug": "sweet-tooth",
        "tagline": "Life is short. Eat dessert first. Cuddle dessert second.",
        "emoji": "🍩", "color": "#E91E63", "color_light": "#FCE4EC", "color_dark": "#880E4F",
        "characters": [
            {"name": "Macaron", "slug": "macaron", "concept": "pastel macaron", "vibe": "Delicate & pretty", "tagline": "Looks too good to eat. Costs too much. Worth it.", "price": 22, "emoji": "🧁", "color": "#F8BBD0", "color_light": "#FCE4EC", "color_dark": "#AD1457", "size": '8"', "personality": "Macaron is expensive taste in a tiny package. Pastel perfection. Breaks if you look at it wrong. But that flavor? That crunch? Worth every penny and every careful moment."},
            {"name": "Donut", "slug": "donut", "concept": "frosted donut", "vibe": "Hole-some", "tagline": "Has a hole in the middle. Still feels complete. Inspiring.", "price": 24, "emoji": "🍩", "color": "#F48FB1", "color_light": "#FCE4EC", "color_dark": "#AD1457", "size": '10"', "personality": "Donut has a literal hole in its center. Doesn't care. Still whole. Still complete. Still covered in sprinkles. The most body-positive member of the squad."},
            {"name": "Cinnamon Roll", "slug": "cinnamon-roll", "concept": "cinnamon roll", "vibe": "Too pure", "tagline": "Actually too good for this world. Protect at all costs.", "price": 24, "emoji": "🧡", "color": "#FFCC80", "color_light": "#FFF3E0", "color_dark": "#E65100", "size": '10"', "personality": "Cinnamon Roll has never had a mean thought. Not one. Remembers your birthday. Shares their dessert. Says 'I love you' first. Must be protected at all costs."},
            {"name": "Gummy Bear", "slug": "gummy-bear", "concept": "gummy bear (translucent)", "vibe": "Squishy & resilient", "tagline": "You can stretch Gummy Bear. It always bounces back.", "price": 22, "emoji": "🐻", "color": "#EF5350", "color_light": "#FFEBEE", "color_dark": "#C62828", "size": '8"', "personality": "Gummy Bear stretches. Squishes. Gets pulled in every direction. Always bounces back. The most resilient friend — translucent, squishy, and utterly indestructible."},
            {"name": "Ice Pop", "slug": "ice-pop", "concept": "twin popsicle (pair)", "vibe": "Best friends", "tagline": "Snap in half. Share with your person. That's the whole point.", "price": 32, "emoji": "🍦", "color": "#FF7043", "color_light": "#FBE9E7", "color_dark": "#BF360C", "size": '10" pair', "personality": "Ice Pop comes as a pair. Meant to be split. Meant to be shared. The friend equivalent of 'best friends forever' necklaces. Two halves of one delicious whole."},
        ]
    },
]

def slugify(name):
    """Convert name to URL-safe slug."""
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def generate_plush_pdp(char, wave_info, all_waves):
    """Generate a PDP HTML page for a plush character."""
    slug = char["slug"]
    name = char["name"]
    concept = char["concept"]
    tagline = char["tagline"]
    price = char["price"]
    emoji_char = char["emoji"]
    color = char["color"]
    color_light = char["color_light"]
    color_dark = char["color_dark"]
    size = char["size"]
    personality = char["personality"]
    vibe = char["vibe"]
    wave_name = wave_info["name"]
    wave_slug = wave_info["slug"]

    # Get related products from same wave (up to 4, excluding self)
    same_wave = [c for c in wave_info["characters"] if c["slug"] != slug]
    related = random.sample(same_wave, min(4, len(same_wave)))

    img_dir = f"../../assets/plushies/{slug}"
    hero_img_png = f"{img_dir}/{slug}-hero.png"
    hero_img = f"{img_dir}/{slug}-hero.webp"

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} Plush — Nancy Universe</title>
<link rel="icon" type="image/svg+xml" href="../../nancy-logo-pink.svg">
<link rel="icon" type="image/png" href="../../nancy-logo-pink.png">
<meta name="description" content="Meet {name}. {tagline} A super-soft kawaii {concept} plush toy from Nancy Universe. {size} of pure huggable personality.">
<meta property="og:title" content="{name} Plush — Nancy Universe">
<meta property="og:description" content="{tagline}">
<meta property="og:image" content="{hero_img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.shopify.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;0,9..144,800;1,9..144,400&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Semibold.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Regular.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Bold.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<link rel="preload" href="{hero_img}" as="image" type="image/webp">
<link rel="stylesheet" href="../../css/style.min.css">
<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '832767357702650');
fbq('track', 'PageView');
fbq('track', 'ViewContent', {{content_name: '{name} Plush', content_type: 'product', value: {price}, currency: 'USD'}});
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
      <a href="../../pages/collections/{wave_slug}.html">{wave_name}</a>
      <span class="sep">/</span>
      <span class="current">{name}</span>
    </div>

    <!-- PDP Hero -->
    <div class="pdp-hero">

      <!-- Gallery -->
      <div class="pdp-gallery">
        <div class="pdp-gallery-main">
          <img id="pdp-main-img" src="{hero_img}" alt="{name} Plush — kawaii {concept} plush toy from Nancy Universe" width="1024" height="1024" onerror="this.onerror=null;this.src='{hero_img_png}'">
        </div>
        <div class="pdp-gallery-thumbs">
          <button class="active" aria-label="{name} product view">
            <img src="{hero_img}" data-full="{hero_img}" alt="{name} hero" onerror="this.onerror=null;this.src='{hero_img_png}'">
          </button>
          <button aria-label="{name} side angle">
            <img src="{img_dir}/{slug}-angle.webp" data-full="{img_dir}/{slug}-angle.webp" alt="{name} angle" loading="lazy" decoding="async" onerror="this.onerror=null;this.src='{img_dir}/{slug}-angle.png'">
          </button>
          <button aria-label="{name} bedroom scene">
            <img src="{img_dir}/{slug}-lifestyle-bed.webp" data-full="{img_dir}/{slug}-lifestyle-bed.webp" alt="{name} lifestyle" loading="lazy" decoding="async" onerror="this.onerror=null;this.src='{img_dir}/{slug}-lifestyle-bed.png'">
          </button>
          <button aria-label="{name} desk scene">
            <img src="{img_dir}/{slug}-lifestyle-desk.webp" data-full="{img_dir}/{slug}-lifestyle-desk.webp" alt="{name} on desk" loading="lazy" decoding="async" onerror="this.onerror=null;this.src='{img_dir}/{slug}-lifestyle-desk.png'">
          </button>
          <button aria-label="{name} scale view">
            <img src="{img_dir}/{slug}-in-hand.webp" data-full="{img_dir}/{slug}-in-hand.webp" alt="{name} in hand" loading="lazy" decoding="async" onerror="this.onerror=null;this.src='{img_dir}/{slug}-in-hand.png'">
          </button>
          <button aria-label="{name} gift flatlay">
            <img src="{img_dir}/{slug}-flatlay.webp" data-full="{img_dir}/{slug}-flatlay.webp" alt="{name} flatlay" loading="lazy" decoding="async" onerror="this.onerror=null;this.src='{img_dir}/{slug}-flatlay.png'">
          </button>
        </div>
      </div>

      <!-- Info -->
      <div class="pdp-info">
        <div class="pdp-character-badge" style="background: {color_light}; color: {color_dark};">
          <span>{emoji_char}</span> {wave_name.upper()}
        </div>

        <h1 class="pdp-title">{name}</h1>
        <p class="pdp-tagline">{tagline}</p>

        <div class="pdp-rating">
          <span class="pdp-stars">★★★★★</span>
          <span class="pdp-rating-text">4.9 out of 5</span>
        </div>

        <div class="pdp-price">
          <span class="pdp-price-current">US${price}</span>
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
            {size}
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
          Add to Cart &mdash; US${price}
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
          <img src="{img_dir}/{slug}-lifestyle-bed.webp" alt="{name} plush lifestyle" loading="lazy" decoding="async" onerror="this.onerror=null;this.src='{img_dir}/{slug}-lifestyle-bed.png'">
        </div>
        <div class="pdp-feature-text reveal">
          <span class="section-label">Meet {name}</span>
          <h3>{vibe}</h3>
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
          <img src="{img_dir}/{slug}-in-hand.webp" alt="{name} plush in hand showing scale" loading="lazy" decoding="async" onerror="this.onerror=null;this.src='{img_dir}/{slug}-in-hand.png'">
        </div>
        <div class="pdp-feature-text reveal">
          <span class="section-label">Quality You Can Feel</span>
          <h3>Soft enough to <em>sleep with.</em></h3>
          <p>Every {name} plush is made from premium polyester plush fabric with a 100% polyester fill. Embroidered face details mean no choking hazards and a face that lasts. Machine washable, air dry. {size} of pure huggable personality.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Feature 3: Gifting -->
  <div class="pdp-feature-section">
    <div class="container">
      <div class="pdp-feature-grid">
        <div class="pdp-feature-image reveal">
          <img src="{img_dir}/{slug}-flatlay.webp" alt="{name} plush gift flatlay" loading="lazy" decoding="async" onerror="this.onerror=null;this.src='{img_dir}/{slug}-flatlay.png'">
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
        <h2 style="font-family: var(--font-display); font-size: clamp(1.5rem, 2.5vw, 2rem); font-weight: 800; letter-spacing: -0.03em;">More from <em style="font-family: var(--font-editorial); font-weight: 400;">{wave_name}</em></h2>
      </div>
      <div class="pdp-related-grid">'''

    for rel in related:
        rel_slug = rel["slug"]
        html += f'''
        <a href="plush-{rel_slug}.html" class="product-card" data-tilt>
          <div class="product-card-image">
            <img src="../../assets/plushies/{rel_slug}/{rel_slug}-hero.webp" alt="{rel['name']} Plush" width="1024" height="1024" loading="lazy" decoding="async" onerror="this.onerror=null;this.src='../../assets/plushies/{rel_slug}/{rel_slug}-hero.png'">
          </div>
          <div class="product-card-info">
            <h3>{rel['name']}</h3>
            <p class="product-card-tagline">{rel['vibe']}</p>
            <div class="product-card-price">
              <span class="product-card-current">US${rel['price']}</span>
            </div>
          </div>
        </a>'''

    html += '''
      </div>
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


def generate_wave_collection(wave_info):
    """Generate a collection page for a wave of plushies."""
    wave_name = wave_info["name"]
    wave_slug = wave_info["slug"]
    wave_tagline = wave_info["tagline"]
    wave_emoji = wave_info["emoji"]
    wave_color = wave_info["color"]
    wave_color_light = wave_info["color_light"]
    wave_color_dark = wave_info["color_dark"]
    characters = wave_info["characters"]
    wave_num = wave_info["wave"]

    cards_html = ""
    for char in characters:
        slug = char["slug"]
        cards_html += f'''
          <a href="../products/plush-{slug}.html" class="product-card" data-tilt>
            <div class="product-card-image">
              <img src="../../assets/plushies/{slug}/{slug}-hero.webp" alt="{char['name']} Plush" width="1024" height="1024" loading="lazy" decoding="async" onerror="this.onerror=null;this.src='../../assets/plushies/{slug}/{slug}-hero.png'">
              <span class="product-card-badge" style="background: {wave_color};">Wave {wave_num}</span>
            </div>
            <div class="product-card-info">
              <div class="product-card-rating">
                <span class="stars">★★★★★</span>
              </div>
              <h3 class="product-card-title">{char['name']}</h3>
              <p class="product-card-tagline">{char['tagline'][:60]}{'...' if len(char['tagline']) > 60 else ''}</p>
              <div class="product-card-price">
                <span class="product-card-current">US${char['price']}</span>
              </div>
            </div>
          </a>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{wave_name} Collection — Nancy Universe</title>
<link rel="icon" type="image/svg+xml" href="../../nancy-logo-pink.svg">
<link rel="icon" type="image/png" href="../../nancy-logo-pink.png">
<meta name="description" content="{wave_tagline} Nancy Universe {wave_name} plush collection.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.shopify.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;0,9..144,800;1,9..144,400&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Semibold.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Regular.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<link rel="preload" href="https://cdn.shopify.com/s/files/1/0726/3764/5121/files/ESRebondGrotesque-Bold.woff?v=1680075897" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="../../css/style.min.css">
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
  <div class="container">

    <div class="breadcrumb">
      <a href="/">Home</a>
      <span class="sep">/</span>
      <a href="plushies.html">Plushies</a>
      <span class="sep">/</span>
      <span class="current">{wave_name}</span>
    </div>

    <!-- Hero Banner -->
    <div class="collection-hero" style="background: linear-gradient(135deg, {wave_color_light} 0%, {wave_color}22 100%);">
      <div class="collection-hero-content">
        <span style="font-size: 3rem;">{wave_emoji}</span>
        <h1 class="collection-hero-title" style="font-family: var(--font-display); font-weight: 800; letter-spacing: -0.03em; font-size: clamp(2rem, 5vw, 3.5rem);">
          {wave_name} <em style="font-family: var(--font-editorial); font-weight: 400;">Collection</em>
        </h1>
        <p class="collection-hero-subtitle" style="font-family: var(--font-body); font-size: 1.15rem; color: var(--ink-light); max-width: 500px; margin: 0 auto;">
          {wave_tagline}
        </p>
      </div>
    </div>

    <!-- Sort bar -->
    <div class="collection-sort-bar" style="display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; margin: 1.5rem 0; border-bottom: 1px solid var(--border);">
      <span style="font-size: 0.85rem; color: var(--ink-light);">Showing {len(characters)} products</span>
    </div>

    <!-- Product Grid -->
    <div class="product-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 2rem; padding: 1rem 0 3rem;">
      {cards_html}
    </div>

  </div>

  <!-- Newsletter -->
  <section class="pdp-newsletter" style="padding: 4rem 0; background: var(--cream-dark);">
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


# ═══════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    total_pdps = 0
    total_collections = 0

    if mode in ("plush", "plush-pdps", "all"):
        print("\n" + "=" * 60)
        print("GENERATING PLUSH PDP PAGES (Waves 2-10)")
        print("=" * 60)

        for wave in PLUSH_WAVES:
            print(f"\n--- Wave {wave['wave']}: {wave['name']} ({len(wave['characters'])} characters) ---")
            for char in wave["characters"]:
                out_path = os.path.join(BASE_DIR, "pages", "products", f"plush-{char['slug']}.html")
                if os.path.exists(out_path):
                    print(f"  [SKIP] {out_path} already exists")
                    continue

                html = generate_plush_pdp(char, wave, PLUSH_WAVES)
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with open(out_path, "w") as f:
                    f.write(html)
                print(f"  [OK] {out_path}")
                total_pdps += 1

    if mode in ("collections", "plush-collections", "all"):
        print("\n" + "=" * 60)
        print("GENERATING WAVE COLLECTION PAGES")
        print("=" * 60)

        for wave in PLUSH_WAVES:
            out_path = os.path.join(BASE_DIR, "pages", "collections", f"{wave['slug']}.html")
            if os.path.exists(out_path):
                print(f"  [SKIP] {out_path} already exists")
                continue

            html = generate_wave_collection(wave)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w") as f:
                f.write(html)
            print(f"  [OK] {out_path}")
            total_collections += 1

    print(f"\n[DONE] Generated {total_pdps} PDP pages + {total_collections} collection pages.")
