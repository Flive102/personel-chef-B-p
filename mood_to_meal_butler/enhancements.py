# mood_to_meal_butler/enhancements.py
# Optional enhanced features for Empathetic Culinary Butler
# Add energy level + health goal tracking

OPTIONAL_QUESTIONS_EN = [
    {
        "key": "energy",
        "question": "Butler: How's your energy level today?",
        "hint": "(low / medium / high)",
        "keywords": {
            "low":    ["low", "tired", "exhausted", "drained", "no energy"],
            "medium": ["medium", "okay", "normal", "average"],
            "high":   ["high", "energized", "energetic", "pumped", "great"],
        },
        "default": "medium"
    },
    {
        "key": "health_goal",
        "question": "Butler: Any health goals today?",
        "hint": "(protein / fiber / low-cal / balanced)",
        "keywords": {
            "protein":  ["protein", "muscle", "strength", "gains"],
            "fiber":    ["fiber", "digestion", "health", "fiber"],
            "low_cal":  ["low calorie", "light", "diet", "weight"],
            "balanced": ["balanced", "nutrition", "healthy", "normal"],
            "none":     ["none", "no", "doesn't matter"],
        },
        "default": "balanced"
    }
]

def get_energy_based_meals(energy_level: str) -> list[str]:
    """Return meal mood tags based on energy level"""
    energy_tags = {
        "low":    ["tired", "comfort", "light"],
        "medium": ["energized", "balanced", "normal"],
        "high":   ["celebration", "adventurous", "energized"]
    }
    return energy_tags.get(energy_level, ["energized"])

def get_health_based_meals(health_goal: str) -> list[str]:
    """Return meal health tags based on goal"""
    health_tags = {
        "protein":  ["high-protein", "muscle-building"],
        "fiber":    ["vegetable-rich", "low-calorie"],
        "low_cal":  ["low-calorie", "fresh-vegetables"],
        "balanced": ["balanced-meal", "moderate-calorie"],
        "none":     ["any"]
    }
    return health_tags.get(health_goal, ["any"])

def suggest_meal_variety(recent_meals: list[str], regions: list[str]) -> str:
    """Suggest meal from different region if user eating too much from one area"""
    from collections import Counter
    
    if not recent_meals:
        return "Pick from any region!"
    
    # Count meals by region
    region_counts = Counter(regions)
    most_common_region = region_counts.most_common(1)[0][0]
    
    if region_counts[most_common_region] >= 3:
        return f"You've been eating a lot from {most_common_region} lately. Let me suggest something from a different region!"
    
    return "Let me find something delicious for you!"

def get_nutrition_estimate(meal_name: str) -> dict:
    """Simple nutrition estimate (placeholder for enhancement)"""
    return {
        "estimated_calories": "400-800",
        "protein": "varies",
        "fiber": "varies",
        "note": "For detailed nutrition, check restaurant info"
    }
