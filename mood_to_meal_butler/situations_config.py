# situations_config.py
# EXPANSION: 30 Situation Types for Smart Context-Aware Recommendations

"""
SITUATION DETECTION SYSTEM

30 Situations covering: time (breakfast/lunch/dinner), location (office/home),
budget (friendly/moderate), occasions (date/family), fitness (workout),
dietary (keto/vegan), health (diabetic/allergy), and lifestyle.
"""

SITUATIONS = {
    # TIME-BASED (4)
    "breakfast": {
        "keywords": ["breakfast", "morning", "early", "brunch"],
        "emoji": "🌅",
        "greeting": "Good morning! Let's start your day right...",
        "filter_tags": ["quick", "energizing"],
    },
    "lunch": {
        "keywords": ["lunch", "noon", "midday", "afternoon meal"],
        "emoji": "☀️",
        "greeting": "Time for a proper lunch...",
        "filter_tags": ["balanced", "protein"],
    },
    "dinner": {
        "keywords": ["dinner", "supper", "evening"],
        "emoji": "🌙",
        "greeting": "Time for dinner. How about...",
        "filter_tags": ["warm", "comforting"],
    },
    "late-night": {
        "keywords": ["late night", "midnight", "snack before bed"],
        "emoji": "🌃",
        "greeting": "Light snacks that won't keep you up...",
        "filter_tags": ["light", "digestible"],
    },

    # LOCATION-BASED (3)
    "at-office": {
        "keywords": ["office", "work", "desk", "workplace"],
        "emoji": "🏢",
        "greeting": "Lunch at the office? Try these grab-friendly options...",
        "filter_tags": ["portable", "no-smell"],
    },
    "at-home": {
        "keywords": ["home", "kitchen", "house"],
        "emoji": "🏠",
        "greeting": "Cooking at home? Perfect!...",
        "filter_tags": ["comfort", "homemade"],
    },
    "restaurant": {
        "keywords": ["restaurant", "dining out", "eating out"],
        "emoji": "🍽️",
        "greeting": "Out to eat? These are crowd favorites...",
        "filter_tags": ["restaurant-available"],
    },

    # TIME-CONSTRAINT (3)
    "quick-bite": {
        "keywords": ["quick", "5 minutes", "10 minutes", "fast", "rush"],
        "emoji": "⏱️",
        "greeting": "In a rush! Quick meals...",
        "filter_tags": ["quick", "fast"],
    },
    "meal-prep": {
        "keywords": ["meal prep", "batch cooking", "sunday cook"],
        "emoji": "🍳",
        "greeting": "Meal prep time! Batch recipes...",
        "filter_tags": ["freezer-friendly", "batch"],
    },
    "slow-cook": {
        "keywords": ["slow cook", "all day", "crock pot"],
        "emoji": "🍲",
        "greeting": "Slow cooker magic! Set and forget...",
        "filter_tags": ["slow-cook", "comfort"],
    },

    # DIETARY (4)
    "diet-keto": {
        "keywords": ["keto", "low carb", "ketogenic"],
        "emoji": "🥑",
        "greeting": "Keto-friendly options...",
        "filter_tags": ["keto", "low-carb"],
    },
    "diet-vegan": {
        "keywords": ["vegan", "plant-based", "no meat"],
        "emoji": "🌱",
        "greeting": "Plant-based goodness coming up...",
        "filter_tags": ["vegan", "plant-based"],
    },
    "diet-gluten-free": {
        "keywords": ["gluten free", "celiac", "no wheat"],
        "emoji": "🌾",
        "greeting": "Gluten-free options that taste amazing...",
        "filter_tags": ["gluten-free"],
    },
    "diet-low-sodium": {
        "keywords": ["low sodium", "salt-free", "heart health"],
        "emoji": "❤️",
        "greeting": "Heart-healthy, low-sodium meals...",
        "filter_tags": ["low-sodium"],
    },

    # FITNESS (3)
    "high-protein": {
        "keywords": ["protein", "muscle", "gym", "strength"],
        "emoji": "💪",
        "greeting": "Protein-packed meals for muscle building...",
        "filter_tags": ["high-protein"],
    },
    "post-workout": {
        "keywords": ["post workout", "after gym", "recovery"],
        "emoji": "🏋️",
        "greeting": "Post-workout recovery meals...",
        "filter_tags": ["recovery", "protein"],
    },
    "pre-workout": {
        "keywords": ["pre workout", "before gym", "energy boost"],
        "emoji": "⚡",
        "greeting": "Energy-boosting pre-workout meals...",
        "filter_tags": ["energizing"],
    },

    # BUDGET (2)
    "budget-friendly": {
        "keywords": ["budget", "cheap", "affordable", "under $5"],
        "emoji": "💰",
        "greeting": "Budget meals that taste amazing...",
        "filter_tags": ["budget", "affordable"],
    },
    "budget-moderate": {
        "keywords": ["moderate budget", "$10", "reasonable"],
        "emoji": "💵",
        "greeting": "Good quality at a fair price...",
        "filter_tags": ["moderate"],
    },

    # OCCASIONS (3)
    "fine-dining": {
        "keywords": ["fine dining", "special occasion", "date", "anniversary"],
        "emoji": "🍷",
        "greeting": "Something special for tonight...",
        "filter_tags": ["elegant", "impressive"],
    },
    "family-dinner": {
        "keywords": ["family", "kids", "children", "picky eaters"],
        "emoji": "👨‍👩‍👧‍👦",
        "greeting": "Family-friendly meals everyone enjoys...",
        "filter_tags": ["kid-friendly", "mild"],
    },
    "date-night": {
        "keywords": ["date", "romantic", "partner"],
        "emoji": "💕",
        "greeting": "Romantic meal ideas for two...",
        "filter_tags": ["romantic", "elegant"],
    },

    # HEALTH (3)
    "diabetes-friendly": {
        "keywords": ["diabetes", "diabetic", "blood sugar"],
        "emoji": "🩺",
        "greeting": "Blood sugar-friendly options...",
        "filter_tags": ["low-gi", "diabetes-safe"],
    },
    "nut-allergy": {
        "keywords": ["nut allergy", "no nuts", "peanut free"],
        "emoji": "⚠️",
        "greeting": "Safe, nut-free meals...",
        "filter_tags": ["nut-free"],
    },
    "low-calorie": {
        "keywords": ["diet", "lose weight", "low calorie"],
        "emoji": "🧘",
        "greeting": "Light, nutritious meals...",
        "filter_tags": ["low-calorie"],
    },

    # LIFESTYLE (3)
    "comfort-food": {
        "keywords": ["comfort", "cozy", "warm", "soothing"],
        "emoji": "🤗",
        "greeting": "Classic comfort food to soothe the soul...",
        "filter_tags": ["comfort", "warm"],
    },
    "adventure": {
        "keywords": ["adventure", "try new", "exotic", "explore"],
        "emoji": "🌍",
        "greeting": "Let's explore new flavors together...",
        "filter_tags": ["exotic", "international"],
    },
    "nostalgic": {
        "keywords": ["nostalgic", "childhood", "remember", "classic"],
        "emoji": "📸",
        "greeting": "Bring back those favorite memories...",
        "filter_tags": ["classic", "nostalgic"],
    },

    # SOCIAL (3)
    "picnic": {
        "keywords": ["picnic", "outdoor", "park", "portable"],
        "emoji": "🧺",
        "greeting": "Picnic-perfect foods that travel well...",
        "filter_tags": ["portable", "outdoor"],
    },
    "party": {
        "keywords": ["party", "gathering", "appetizer", "sharing"],
        "emoji": "🎉",
        "greeting": "Party foods that impress...",
        "filter_tags": ["shareable", "appetizer"],
    },
    "sick-day": {
        "keywords": ["sick", "cold", "flu", "recovery"],
        "emoji": "🤒",
        "greeting": "Gentle foods to help you recover...",
        "filter_tags": ["gentle", "digestible"],
    },
}

def detect_situation(text: str) -> list:
    """Detect situations from user text"""
    text_lower = text.lower()
    detected = []
    
    # Sort by keyword length (longer first)
    situations_sorted = sorted(
        SITUATIONS.items(),
        key=lambda x: max((len(k) for k in x[1]['keywords']), default=0),
        reverse=True
    )
    
    for situation_key, situation_data in situations_sorted:
        for keyword in situation_data['keywords']:
            if keyword.lower() in text_lower:
                detected.append(situation_key)
                break
    
    return detected

def get_situation_filters(situations: list) -> dict:
    """Get combined filters for detected situations"""
    include_tags = set()
    exclude_tags = set()
    
    for situation in situations:
        if situation in SITUATIONS:
            data = SITUATIONS[situation]
            include_tags.update(data.get("filter_tags", []))
    
    return {"include_tags": list(include_tags), "exclude_tags": list(exclude_tags)}
