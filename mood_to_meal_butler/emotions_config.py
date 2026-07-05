# emotions_config.py
# Comprehensive emotion keywords and situation detection
# Easily extensible for developers to add more emotions

EMOTION_KEYWORDS = {
    # SADNESS FAMILY (15 keywords)
    "sad": "sadness",
    "down": "sadness",
    "depressed": "sadness",
    "upset": "sadness",
    "unhappy": "sadness",
    "blue": "sadness",
    "heartbroken": "sadness",
    "devastated": "sadness",
    "miserable": "sadness",
    "gloomy": "sadness",
    "sorrowful": "sadness",
    "melancholy": "sadness",
    "grief": "sadness",
    "mourning": "sadness",
    "lonesome": "sadness",
    
    # TIREDNESS FAMILY (12 keywords)
    "tired": "exhaustion",
    "exhausted": "exhaustion",
    "fatigue": "exhaustion",
    "sleepy": "exhaustion",
    "drained": "exhaustion",
    "worn-out": "exhaustion",
    "weary": "exhaustion",
    "bushed": "exhaustion",
    "burned-out": "exhaustion",
    "depleted": "exhaustion",
    "fatigued": "exhaustion",
    "sluggish": "exhaustion",
    
    # HAPPINESS FAMILY (18 keywords)
    "happy": "joy",
    "excited": "joy",
    "celebrating": "joy",
    "celebration": "joy",
    "celebrate": "joy",
    "thrilled": "joy",
    "delighted": "joy",
    "ecstatic": "joy",
    "elated": "joy",
    "joyful": "joy",
    "cheerful": "joy",
    "wonderful": "joy",
    "great": "joy",
    "fantastic": "joy",
    "amazing": "joy",
    "accomplished": "joy",
    "proud": "joy",
    "triumphant": "joy",
    
    # STRESS FAMILY (14 keywords)
    "stressed": "stress",
    "anxious": "stress",
    "nervous": "stress",
    "worried": "stress",
    "tense": "stress",
    "pressured": "stress",
    "overwhelmed": "stress",
    "uneasy": "stress",
    "restless": "stress",
    "frazzled": "stress",
    "on edge": "stress",
    "jumpy": "stress",
    "apprehensive": "stress",
    "troubled": "stress",
    
    # ANGER FAMILY (12 keywords)
    "angry": "anger",
    "frustrated": "anger",
    "annoyed": "anger",
    "irritated": "anger",
    "furious": "anger",
    "livid": "anger",
    "enraged": "anger",
    "resentful": "anger",
    "bitter": "anger",
    "cross": "anger",
    "vexed": "anger",
    "exasperated": "anger",
    
    # ILLNESS/RECOVERY FAMILY (8 keywords)
    "sick": "illness",
    "unwell": "illness",
    "ill": "illness",
    "under-the-weather": "illness",
    "flu": "illness",
    "cold": "illness",
    "nauseous": "illness",
    "recovering": "illness",
    
    # BOREDOM FAMILY (10 keywords)
    "bored": "boredom",
    "unmotivated": "boredom",
    "meh": "boredom",
    "uninterested": "boredom",
    "disinterested": "boredom",
    "lazy": "boredom",
    "procrastinating": "boredom",
    "apathetic": "boredom",
    "listless": "boredom",
    "indifferent": "boredom",
    
    # LONELINESS FAMILY (8 keywords)
    "lonely": "loneliness",
    "alone": "loneliness",
    "isolated": "loneliness",
    "solitary": "loneliness",
    "disconnected": "loneliness",
    "excluded": "loneliness",
    "abandoned": "loneliness",
    "left-out": "loneliness",
    
    # CALM FAMILY (8 keywords)
    "calm": "calm",
    "peaceful": "calm",
    "serene": "calm",
    "meditative": "calm",
    "tranquil": "calm",
    "relaxed": "calm",
    "composed": "calm",
    "zen": "calm",
    
    # ENERGY FAMILY (10 keywords)
    "energetic": "energy",
    "pumped": "energy",
    "vibrant": "energy",
    "hyped": "energy",
    "charged": "energy",
    "active": "energy",
    "motivated": "energy",
    "invigorated": "energy",
    "alive": "energy",
    "spirited": "energy",
    
    # ROMANTIC FAMILY (8 keywords)
    "romantic": "romance",
    "in-love": "romance",
    "affectionate": "romance",
    "intimate": "romance",
    "tender": "romance",
    "amorous": "romance",
    "passionate": "romance",
    "enamored": "romance",
    
    # ADVENTUROUS FAMILY (8 keywords)
    "adventurous": "adventure",
    "curious": "adventure",
    "exploring": "adventure",
    "experimental": "adventure",
    "daring": "adventure",
    "bold": "adventure",
    "venturesome": "adventure",
    "thrilled": "adventure",
    
    # HOMESICK FAMILY (6 keywords)
    "homesick": "nostalgia",
    "nostalgic": "nostalgia",
    "missing-home": "nostalgia",
    "sentimental": "nostalgia",
    "wistful": "nostalgia",
    "yearning": "nostalgia",
    
    # CONFIDENT FAMILY (8 keywords)
    "confident": "confidence",
    "assured": "confidence",
    "self-assured": "confidence",
    "poised": "confidence",
    "fearless": "confidence",
    "capable": "confidence",
    "empowered": "confidence",
    "strong": "confidence",
}

# EMOTION METADATA: responses, emojis, meal tags
EMOTION_METADATA = {
    "sadness": {
        "emoji": "💙",
        "greeting": "I hear you... that's tough. Let me suggest some comfort foods to lift your spirits.",
        "meal_filters": ["comfort", "warmth", "mood-booster"],
        "response_style": "empathetic",
        "temperature": "warm",
    },
    "exhaustion": {
        "emoji": "😴",
        "greeting": "You sound exhausted. Here are some restorative foods to help you recover.",
        "meal_filters": ["energy-boost", "recovery", "rejuvenation"],
        "response_style": "supportive",
        "temperature": "warm",
    },
    "joy": {
        "emoji": "🎉",
        "greeting": "That's wonderful! Let me suggest meals to celebrate with you!",
        "meal_filters": ["celebration", "indulgent", "special"],
        "response_style": "enthusiastic",
        "temperature": "any",
    },
    "stress": {
        "emoji": "😰",
        "greeting": "Take a breath. Here are some calming foods to ease your mind.",
        "meal_filters": ["calm-peaceful", "grounding", "soothing"],
        "response_style": "soothing",
        "temperature": "warm",
    },
    "anger": {
        "emoji": "😤",
        "greeting": "That sounds frustrating. Let me suggest foods to help you unwind.",
        "meal_filters": ["comfort", "satisfying", "grounding"],
        "response_style": "validating",
        "temperature": "warm",
    },
    "illness": {
        "emoji": "🤒",
        "greeting": "I hope you feel better soon. Here are some nourishing meals for recovery.",
        "meal_filters": ["nourishing", "gentle", "nutritious"],
        "response_style": "caring",
        "temperature": "warm",
    },
    "boredom": {
        "emoji": "😒",
        "greeting": "You need something exciting to spark your day! Let me suggest some energizing meals.",
        "meal_filters": ["exciting", "flavorful", "adventurous"],
        "response_style": "uplifting",
        "temperature": "any",
    },
    "loneliness": {
        "emoji": "🤝",
        "greeting": "I'm here for you. How about a comforting meal to brighten your day?",
        "meal_filters": ["comfort", "social", "sharing"],
        "response_style": "warm",
        "temperature": "warm",
    },
    "calm": {
        "emoji": "🧘",
        "greeting": "Beautiful. Here are some peaceful meals to maintain your serenity.",
        "meal_filters": ["light", "mindful", "nourishing"],
        "response_style": "gentle",
        "temperature": "warm",
    },
    "energy": {
        "emoji": "⚡",
        "greeting": "Amazing! Let me suggest some power meals to fuel your momentum!",
        "meal_filters": ["power", "energizing", "protein-rich"],
        "response_style": "energetic",
        "temperature": "any",
    },
    "romance": {
        "emoji": "❤️",
        "greeting": "How sweet! Let me suggest some romantic meals for this special moment.",
        "meal_filters": ["romantic", "elegant", "intimate"],
        "response_style": "romantic",
        "temperature": "any",
    },
    "adventure": {
        "emoji": "🚀",
        "greeting": "Exciting! Let me suggest some exotic and adventurous meals!",
        "meal_filters": ["exotic", "adventurous", "international"],
        "response_style": "exciting",
        "temperature": "any",
    },
    "nostalgia": {
        "emoji": "🏡",
        "greeting": "I understand. Let me suggest some nostalgic comfort meals to make you feel at home.",
        "meal_filters": ["comfort", "traditional", "homestyle"],
        "response_style": "nostalgic",
        "temperature": "warm",
    },
    "confidence": {
        "emoji": "💪",
        "greeting": "That's the spirit! Let me suggest meals worthy of your achievement.",
        "meal_filters": ["celebration", "empowering", "premium"],
        "response_style": "celebratory",
        "temperature": "any",
    },
}

# SITUATION KEYWORDS: "i'm at..." or "i have..." triggers
SITUATION_KEYWORDS = {
    "at-office": {
        "keywords": ["at office", "at work", "workplace", "desk", "cubicle", "meeting"],
        "meal_filters": ["quick", "desk-friendly", "no-mess", "portable"],
        "context": "Professional setting with limited time",
    },
    "on-date": {
        "keywords": ["on date", "date night", "romantic dinner", "with date"],
        "meal_filters": ["romantic", "elegant", "shareable", "impressive"],
        "context": "Romantic outing",
    },
    "family-meal": {
        "keywords": ["family dinner", "cooking family", "with kids", "family meal"],
        "meal_filters": ["family-friendly", "kid-approved", "filling", "nutritious"],
        "context": "Family gathering",
    },
    "quick-bite": {
        "keywords": ["quick", "fast", "in hurry", "5 minutes", "15 minutes", "hungry now"],
        "meal_filters": ["quick", "<15min", "instant", "no-prep"],
        "context": "Need food immediately",
    },
    "budget": {
        "keywords": ["budget", "cheap", "affordable", "poor", "tight budget", "broke"],
        "meal_filters": ["budget-friendly", "inexpensive", "filling"],
        "context": "Limited financial resources",
    },
    "premium": {
        "keywords": ["treat myself", "splurge", "expensive", "fancy", "premium", "luxury"],
        "meal_filters": ["premium", "gourmet", "upscale", "indulgent"],
        "context": "Special treat or celebration",
    },
    "fitness": {
        "keywords": ["just exercised", "post-workout", "gym", "running", "training"],
        "meal_filters": ["protein-rich", "recovery", "energy-restore"],
        "context": "Post-exercise nutrition needed",
    },
    "cooking": {
        "keywords": ["cooking", "can cook", "making dinner", "prepare", "cook myself"],
        "meal_filters": ["recipe", "ingredients", "instructions"],
        "context": "User wants to cook",
    },
    "ordering": {
        "keywords": ["order", "delivery", "takeout", "restaurant"],
        "meal_filters": ["available-delivery", "restaurant-suggestion"],
        "context": "User wants to order/delivery",
    },
    "diet-conscious": {
        "keywords": ["diet", "calories", "weight", "nutrition", "healthy"],
        "meal_filters": ["low-cal", "nutritious", "balanced", "diet-friendly"],
        "context": "Health-focused choice",
    },
    "vegan": {
        "keywords": ["vegan", "vegetarian", "plant-based", "no meat"],
        "meal_filters": ["vegan", "plant-based"],
        "context": "Dietary restriction",
    },
    "gluten-free": {
        "keywords": ["gluten-free", "celiac", "gf"],
        "meal_filters": ["gluten-free"],
        "context": "Dietary restriction",
    },
}

# VIETNAMESE EMOTION SUPPORT
VIETNAMESE_EMOTIONS = {
    # Sadness variants
    "tôi buồn": "sadness",
    "buồn lắm": "sadness",
    "tâm trạng không tốt": "sadness",
    "không tốt": "sadness",
    "tâm trạng xấu": "sadness",
    "cảm thấy buồn": "sadness",
    "mình buồn": "sadness",
    
    # Exhaustion/Tiredness
    "tôi mệt": "exhaustion",
    "mệt lắm": "exhaustion",
    "mệt mỏi": "exhaustion",
    "quá mệt": "exhaustion",
    "cảm thấy mệt": "exhaustion",
    
    # Joy/Happiness
    "tôi vui": "joy",
    "vui lắm": "joy",
    "rất vui": "joy",
    "cảm thấy vui": "joy",
    "mình vui": "joy",
    
    # Stress/Anxiety
    "tôi lo": "stress",
    "lo lắng": "stress",
    "cảm thấy lo lắng": "stress",
    "rất lo": "stress",
    "stress": "stress",
    "căng thẳng": "stress",
    
    # Anger
    "tôi giận": "anger",
    "giận lắm": "anger",
    "rất giận": "anger",
    "cảm thấy giận": "anger",
    
    # Illness/Sickness
    "tôi bị bệnh": "illness",
    "bị bệnh": "illness",
    "cảm": "illness",
    "sốt": "illness",
    "không khỏe": "illness",
    
    # Boredom
    "tôi chán": "boredom",
    "chán lắm": "boredom",
    "cảm thấy chán": "boredom",
    "rất chán": "boredom",
    
    # Loneliness
    "tôi cô đơn": "loneliness",
    "cô đơn lắm": "loneliness",
    "cảm thấy cô đơn": "loneliness",
    "một mình": "loneliness",
    
    # Calm
    "tôi yên tĩnh": "calm",
    "yên tĩnh": "calm",
    "bình tĩnh": "calm",
    "thư giãn": "calm",
    
    # Energy
    "tôi có năng lượng": "energy",
    "năng lượng": "energy",
    "tràn năng lượng": "energy",
    "đầy năng lượng": "energy",
    
    # Romance/Love
    "tôi lãng mạn": "romance",
    "lãng mạn": "romance",
    "yêu": "romance",
    "trong tình yêu": "romance",
    
    # Adventure/Exploration
    "tôi khám phá": "adventure",
    "khám phá": "adventure",
    "phiêu lưu": "adventure",
    "mạo hiểm": "adventure",
    
    # Nostalgia
    "tôi nhớ nhà": "nostalgia",
    "nhớ nhà": "nostalgia",
    "nhớ": "nostalgia",
    "hoài niệm": "nostalgia",
    
    # Confidence
    "tôi tự tin": "confidence",
    "tự tin": "confidence",
    "rất tự tin": "confidence",
    "đầy tự tin": "confidence",
}

def detect_language(text: str) -> str:
    """Auto-detect language from text (en or vi)"""
    # Vietnamese characters
    vietnamese_chars = "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
    text_lower = text.lower()
    
    # Count Vietnamese characters
    viet_char_count = sum(1 for c in text_lower if c in vietnamese_chars)
    viet_words = sum(1 for word in text_lower.split() if any(c in vietnamese_chars for c in word))
    
    # If significant Vietnamese content, return 'vi'
    if viet_char_count > 0 or viet_words > len(text_lower.split()) * 0.3:
        return "vi"
    return "en"

def detect_emotion(text: str) -> str:
    """
    Detect emotion from user text (English only for now).
    Returns emotion category or None if no emotion detected.
    
    Args:
        text: User input text

    Returns:
        Emotion category (e.g., 'sadness', 'joy') or None
    """
    text_lower = text.lower().strip()
    
    # Check English emotions - sort by keyword length (longest first)
    # This prevents "sick" from matching "homesick", etc.
    sorted_keywords = sorted(EMOTION_KEYWORDS.items(), key=lambda x: len(x[0]), reverse=True)
    for keyword, emotion in sorted_keywords:
        if keyword in text_lower:
            return emotion
    
    return None

def detect_situation(text: str) -> str:
    """
    Detect situation from user text.
    Returns situation category or None if no situation detected.
    """
    text_lower = text.lower().strip()
    
    for situation, config in SITUATION_KEYWORDS.items():
        for keyword in config["keywords"]:
            if keyword in text_lower:
                return situation
    
    return None

def get_emotion_response(emotion: str) -> dict:
    """Get emotion metadata for building responses."""
    return EMOTION_METADATA.get(emotion, {
        "emoji": "💚",
        "greeting": "I'm here to help. Let me suggest something delicious.",
        "meal_filters": ["comfort", "nourishing"],
        "response_style": "supportive",
    })

def get_situation_context(situation: str) -> dict:
    """Get situation metadata for filtering meals."""
    return SITUATION_KEYWORDS.get(situation, {})
