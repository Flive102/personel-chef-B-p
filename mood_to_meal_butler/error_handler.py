# error_handler.py
# Comprehensive error handling utilities

"""
Error handling and validation for mood-to-meal-butler system
"""

from typing import Dict, List, Optional, Any


class EmotionDetectionError(Exception):
    """Emotion detection failed"""
    pass


class SituationDetectionError(Exception):
    """Situation detection failed"""
    pass


class MealRecommendationError(Exception):
    """Meal recommendation failed"""
    pass


class ValidationError(Exception):
    """Input validation failed"""
    pass


def validate_user_input(text: str, max_length: int = 500) -> str:
    """
    Validate and sanitize user input
    
    Args:
        text: User input text
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
        
    Raises:
        ValidationError: If input invalid
    """
    if not text:
        raise ValidationError("Empty input")
    
    if not isinstance(text, str):
        raise ValidationError("Input must be string")
    
    text = text.strip()
    
    if len(text) > max_length:
        raise ValidationError(f"Input too long (max {max_length} chars)")
    
    # Check for malicious patterns
    dangerous_patterns = ["<script", "exec(", "eval(", "import os"]
    if any(pattern in text.lower() for pattern in dangerous_patterns):
        raise ValidationError("Invalid characters detected")
    
    return text

def validate_emotion(emotion: str) -> bool:
    """Validate emotion is recognized"""
    from mood_to_meal_butler.emotions_config import EMOTION_METADATA
    return emotion in EMOTION_METADATA

def validate_situations(situations: list) -> bool:
    """Validate situations are recognized"""
    from mood_to_meal_butler.situations_config import SITUATIONS
    return all(s in SITUATIONS for s in situations)

def validate_meal(meal: dict) -> bool:
    """Validate meal has required fields"""
    required_fields = ["id", "name_en", "emoji", "mood_tags"]
    return all(field in meal for field in required_fields)

def safe_get_meal_field(meal: dict, field: str, default=None):
    """Safely get meal field with fallback"""
    try:
        value = meal.get(field, default)
        if value is None:
            return default
        return value
    except (AttributeError, TypeError):
        return default

def log_error(error_type: str, message: str, context: dict = None):
    """
    Log error safely
    
    Args:
        error_type: Type of error
        message: Error message
        context: Additional context (emotion, situation, etc.)
    """
    import datetime
    timestamp = datetime.datetime.now().isoformat()
    
    log_entry = f"[{timestamp}] {error_type}: {message}"
    if context:
        log_entry += f" | Context: {context}"
    
    # In production, this would write to logging system
    # For now, just store in memory (max 100 entries)
    if not hasattr(log_error, 'logs'):
        log_error.logs = []
    
    log_error.logs.append(log_entry)
    if len(log_error.logs) > 100:
        log_error.logs.pop(0)
    
    print(f"[LOG] {log_entry}")

def handle_missing_meals(emotion: str, situations: list) -> list:
    """
    Handle case when no meals match emotion/situation
    
    Returns fallback meals
    """
    # Return generic comfort foods if no specific match
    fallback_meals = [
        {
            "id": "fallback_1",
            "name_en": "Rice & Broth",
            "emoji": "🍚",
            "description_en": "Simple, comforting rice with broth",
            "mood_tags": ["sadness", "stress"],
            "health_tags": ["gentle", "warm"]
        },
        {
            "id": "fallback_2",
            "name_en": "Tea & Biscuits",
            "emoji": "🍵",
            "description_en": "Warm tea with light snacks",
            "mood_tags": ["stress", "tiredness"],
            "health_tags": ["warm", "light"]
        },
        {
            "id": "fallback_3",
            "name_en": "Fresh Fruit",
            "emoji": "🍎",
            "description_en": "Refreshing and energizing",
            "mood_tags": ["sadness", "tiredness"],
            "health_tags": ["healthy", "energizing"]
        },
        {
            "id": "fallback_4",
            "name_en": "Soup",
            "emoji": "🍲",
            "description_en": "Warm, nourishing soup",
            "mood_tags": ["sadness", "sick"],
            "health_tags": ["warm", "healing"]
        }
    ]
    
    log_error("FALLBACK", "Using fallback meals", {
        "emotion": emotion,
        "situations": situations
    })
    
    return fallback_meals
