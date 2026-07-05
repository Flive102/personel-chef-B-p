# meal_utilities.py
# Utility functions for meal handling and filtering

"""
Meal utility functions: filtering, matching, formatting, validation
"""

def filter_meals_by_emotion(meals: list, emotion: str) -> list:
    """
    Filter meals by emotion type
    
    Args:
        meals: List of meal dictionaries
        emotion: Emotion to filter by
        
    Returns:
        Filtered list of meals
    """
    if not meals or not emotion:
        return []
    
    emotion_base = emotion.split("_")[0].lower()
    filtered = []
    
    for meal in meals:
        mood_tags = meal.get("mood_tags", [])
        if any(emotion_base in str(tag).lower() for tag in mood_tags):
            filtered.append(meal)
    
    return filtered

def filter_meals_by_situation(meals: list, situations: list) -> list:
    """
    Filter meals by situation tags
    
    Args:
        meals: List of meal dictionaries
        situations: List of situation keys
        
    Returns:
        Filtered list of meals
    """
    if not meals or not situations:
        return meals
    
    from mood_to_meal_butler.situations_config import get_situation_filters
    
    filters = get_situation_filters(situations)
    include_tags = set(filters.get("include_tags", []))
    
    if not include_tags:
        return meals
    
    filtered = []
    for meal in meals:
        meal_tags = set(meal.get("health_tags", []))
        if meal_tags & include_tags:  # Intersection check
            filtered.append(meal)
    
    return filtered

def rank_meals(meals: list, emotion: str, situations: list) -> list:
    """
    Rank meals by relevance (emotion + situation match score)
    
    Args:
        meals: List of meal dictionaries
        emotion: Detected emotion
        situations: List of situations
        
    Returns:
        Ranked list (best first)
    """
    if not meals:
        return []
    
    scored_meals = []
    emotion_base = emotion.split("_")[0].lower() if emotion else ""
    
    for meal in meals:
        score = 0
        
        # Emotion match: +3 points
        mood_tags = meal.get("mood_tags", [])
        if emotion_base and any(emotion_base in str(tag).lower() for tag in mood_tags):
            score += 3
        
        # Situation match: +1 point per situation tag
        health_tags = set(meal.get("health_tags", []))
        for situation in situations:
            if situation in health_tags:
                score += 1
        
        scored_meals.append((score, meal))
    
    # Sort by score (highest first)
    scored_meals.sort(key=lambda x: x[0], reverse=True)
    return [meal for score, meal in scored_meals]

def format_meal_for_display(meal: dict, index: int = 1) -> str:
    """
    Format meal for user display
    
    Args:
        meal: Meal dictionary
        index: Display number
        
    Returns:
        Formatted meal string
    """
    emoji = meal.get("emoji", "🍽️")
    name = meal.get("name_en", "Unknown Meal")
    desc = meal.get("description_en", "A delicious dish")
    mood_tags = meal.get("mood_tags", [])
    health_tags = meal.get("health_tags", [])
    
    output = f"{index}. {emoji} **{name}**\n"
    output += f"   {desc}\n"
    
    if mood_tags:
        output += f"   #mood: {', '.join(mood_tags)}\n"
    
    if health_tags:
        output += f"   #health: {', '.join(health_tags)}\n"
    
    return output

def get_meal_by_id(meals: list, meal_id: str) -> dict:
    """
    Find meal by ID
    
    Args:
        meals: List of meal dictionaries
        meal_id: Meal ID to find
        
    Returns:
        Meal dictionary or None
    """
    for meal in meals:
        if meal.get("id") == meal_id:
            return meal
    return None

def get_meals_by_tags(meals: list, tags: list, match_all: bool = False) -> list:
    """
    Get meals by tags
    
    Args:
        meals: List of meal dictionaries
        tags: Tags to match
        match_all: If True, meal must have ALL tags. If False, ANY tag match.
        
    Returns:
        Filtered list of meals
    """
    if not meals or not tags:
        return meals
    
    filtered = []
    
    for meal in meals:
        meal_tags = set(meal.get("health_tags", []) + meal.get("mood_tags", []))
        search_tags = set(tags)
        
        if match_all:
            # Meal must have ALL search tags
            if search_tags.issubset(meal_tags):
                filtered.append(meal)
        else:
            # Meal must have ANY search tag
            if meal_tags & search_tags:
                filtered.append(meal)
    
    return filtered

def get_unique_tags(meals: list, tag_type: str = "all") -> set:
    """
    Get all unique tags from meals
    
    Args:
        meals: List of meal dictionaries
        tag_type: "mood", "health", or "all"
        
    Returns:
        Set of unique tags
    """
    tags = set()
    
    for meal in meals:
        if tag_type in ["mood", "all"]:
            tags.update(meal.get("mood_tags", []))
        if tag_type in ["health", "all"]:
            tags.update(meal.get("health_tags", []))
    
    return tags
