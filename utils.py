import random
import cv2
import numpy as np
from pathlib import Path

# ── Category detection ──────────────────────────────────────────────────────

CATEGORY_KEYWORDS = {
    "shirt":       ["shirt", "tee", "top", "blouse", "polo", "tshirt", "t-shirt"],
    "hoodie":      ["hoodie", "sweatshirt", "pullover", "sweater", "jumper"],
    "jacket":      ["jacket", "coat", "blazer", "windbreaker", "parka"],
    "pants":       ["pants", "jeans", "trousers", "chinos", "shorts", "denim", "cargo"],
    "shoes":       ["shoes", "sneakers", "boots", "loafers", "heels", "sandals", "trainers"],
    "dress":       ["dress", "skirt", "gown", "frock"],
    "accessory":   ["hat", "cap", "scarf", "belt", "bag", "watch", "glasses"],
}

CATEGORY_LIST = list(CATEGORY_KEYWORDS.keys())

def detect_category(filename: str) -> str:
    name = filename.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in name for kw in keywords):
            return category
    return random.choice(CATEGORY_LIST)


# ── Color detection via OpenCV ───────────────────────────────────────────────

COLOR_RANGES_HSV = {
    "red":    [((0, 70, 50), (10, 255, 255)), ((170, 70, 50), (180, 255, 255))],
    "orange": [((11, 70, 50), (25, 255, 255))],
    "yellow": [((26, 70, 50), (34, 255, 255))],
    "green":  [((35, 40, 40), (85, 255, 255))],
    "blue":   [((86, 40, 40), (130, 255, 255))],
    "purple": [((131, 40, 40), (160, 255, 255))],
    "pink":   [((161, 40, 100), (169, 255, 255))],
}

def detect_color(filepath: str) -> str:
    try:
        img = cv2.imread(filepath)
        if img is None:
            return _fallback_color()

        # Resize for speed
        img = cv2.resize(img, (100, 100))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Check brightness for white/black/grey
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mean_brightness = float(gray.mean())
        if mean_brightness > 200:
            return "white"
        if mean_brightness < 40:
            return "black"

        best_color, best_count = "grey", 0
        total_pixels = img.shape[0] * img.shape[1]

        for color_name, ranges in COLOR_RANGES_HSV.items():
            mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
            for lo, hi in ranges:
                mask |= cv2.inRange(hsv, np.array(lo), np.array(hi))
            count = int(np.sum(mask > 0))
            if count > best_count:
                best_count = count
                best_color = color_name

        # Only trust if ≥8% of pixels match
        if best_count / total_pixels < 0.08:
            if mean_brightness < 90:
                return "dark grey"
            return "grey"

        return best_color

    except Exception:
        return _fallback_color()

def _fallback_color():
    return random.choice(["black", "white", "blue", "grey", "red", "navy", "beige"])


# ── Outfit generator ─────────────────────────────────────────────────────────

STYLE_TEMPLATES = {
    "casual":     {"shirt": 1, "pants": 1, "shoes": 1},
    "formal":     {"shirt": 1, "pants": 1, "shoes": 1, "jacket": 1},
    "streetwear": {"hoodie": 1, "pants": 1, "shoes": 1},
    "classic":    {"shirt": 1, "pants": 1, "shoes": 1},
    "sporty":     {"shirt": 1, "pants": 1, "shoes": 1},
    "chic":       {"dress": 1, "shoes": 1, "accessory": 1},
    "smart":      {"shirt": 1, "pants": 1, "shoes": 1, "jacket": 1},
}

# Fallbacks if an exact category is missing
CATEGORY_FALLBACKS = {
    "hoodie": ["jacket", "shirt"],
    "dress":  ["shirt", "pants"],
    "jacket": ["hoodie"],
}

# Preferred colors per style for color-matching bonus sort
STYLE_COLOR_PREFS = {
    "casual":     ["blue", "white", "grey"],
    "formal":     ["black", "white", "navy", "dark grey"],
    "streetwear": ["black", "grey", "white"],
    "classic":    ["navy", "white", "beige", "grey"],
    "sporty":     ["black", "white", "red", "blue"],
    "chic":       ["black", "white", "pink"],
    "smart":      ["navy", "white", "grey"],
}

def generate_outfit(style: str, wardrobe_items: list) -> dict:
    style = style.lower().strip()

    # Find closest matching style
    template = STYLE_TEMPLATES.get(style)
    if not template:
        for key in STYLE_TEMPLATES:
            if key in style or style in key:
                template = STYLE_TEMPLATES[key]
                style = key
                break
    if not template:
        template = STYLE_TEMPLATES["casual"]
        style = "casual"

    preferred_colors = STYLE_COLOR_PREFS.get(style, [])

    # Group wardrobe by category
    by_category: dict[str, list] = {}
    for item in wardrobe_items:
        cat = item["category"]
        by_category.setdefault(cat, []).append(item)

    outfit = []
    missing = []

    for needed_cat in template:
        candidates = by_category.get(needed_cat, [])

        # Try fallbacks
        if not candidates:
            for fb in CATEGORY_FALLBACKS.get(needed_cat, []):
                candidates = by_category.get(fb, [])
                if candidates:
                    break

        if candidates:
            # Sort: preferred colors first, then shuffle rest
            preferred = [c for c in candidates if c["color"] in preferred_colors]
            others    = [c for c in candidates if c["color"] not in preferred_colors]
            random.shuffle(preferred)
            random.shuffle(others)
            pool = (preferred + others)
            # Avoid duplicates
            used_ids = {i["id"] for i in outfit}
            pick = next((c for c in pool if c["id"] not in used_ids), None)
            if pick:
                outfit.append(pick)
            else:
                missing.append(needed_cat)
        else:
            missing.append(needed_cat)

    return {
        "style": style,
        "items": outfit,
        "missing_categories": missing,
        "complete": len(missing) == 0,
    }
