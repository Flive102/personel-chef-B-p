# meals_expansion.py
# PHASE 2: Add nutrition fields to meals database
# Developers can use this as template for expanding meals

MEAL_EXPANSION_TEMPLATE = {
    "id": "meal_pho_001",
    "name_en": "Pho Bo (Beef Noodle Soup)",
    "name_vi": "Phở Bò",
    "emoji": "🍲",
    
    # BASIC FIELDS (existing)
    "mood_tags": ["comfort", "warmth", "energy"],
    "health_tags": ["protein", "energy-boost", "traditional"],
    "description_en": "Vietnamese beef noodle soup with aromatic broth",
    "description_vi": "Súp mì bò Việt Nam với nước dùng thơm ngon",
    
    # NUTRITION DATA (NEW - PHASE 2)
    "calories": 350,
    "protein_g": 25,
    "carbs_g": 45,
    "fat_g": 8,
    "fiber_g": 3,
    "sodium_mg": 800,
    "iron_mg": 3.5,
    
    # COOKING INFO (NEW)
    "prep_time_min": 10,
    "cook_time_min": 20,
    "total_time_min": 30,
    "servings": 2,
    "difficulty": "medium",  # easy/medium/advanced
    "cuisine": "vietnamese",
    
    # DIETARY TAGS (NEW)
    "diet_ok": ["pescatarian", "dairy-free", "gluten-free"],
    "allergens": ["soy", "celery"],
    "can_substitute": {
        "beef": ["chicken", "tofu", "vegetable"],
        "noodles": ["rice noodles", "egg noodles"],
    },
    
    # RECIPE & INGREDIENTS (NEW)
    "ingredients": [
        {"item": "beef broth", "amount": "1", "unit": "liter"},
        {"item": "beef sirloin", "amount": "500", "unit": "g"},
        {"item": "rice noodles", "amount": "200", "unit": "g"},
        {"item": "onion", "amount": "1", "unit": "piece"},
        {"item": "ginger", "amount": "2", "unit": "tbsp"},
    ],
    "instructions": [
        "Boil water and add beef broth",
        "Add sliced beef and simmer for 5 minutes",
        "Add rice noodles to serving bowl",
        "Pour hot broth over noodles",
        "Top with fresh herbs (basil, cilantro, lime)",
    ],
    
    # SOURCING OPTIONS (NEW)
    "restaurant_suggestions": ["Pho King", "Authentic Pho House", "Saigon Express"],
    "recipe_source": "https://www.example.com/pho",
    "available_delivery": ["UberEats", "DoorDash", "Grubhub"],
    "grocery_items": ["Amazon Fresh", "Instacart"],
    
    # SITUATION & CONTEXT (NEW)
    "best_for_situation": ["office-lunch", "family-dinner", "date-night"],
    "weather_suitability": ["cold-comfort", "rainy-cozy", "year-round"],
    "time_of_day": ["lunch", "dinner"],
    "group_size": ["solo", "couple", "family"],
    "budget": "budget",  # budget/standard/premium
    
    # WELLNESS TAGS (NEW)
    "health_benefits": ["protein-rich", "warming", "energy-restore"],
    "intensity": "medium",  # light/medium/heavy (satiation)
    "spice_level": 1,  # 0-5 scale
    "sweetness": 0,
    "umami": 4,  # 0-5
}

# EXPANSION CATEGORIES: Add these meal types
NEW_MEAL_CATEGORIES = {
    "vietnamese_classics": 30,  # Pho, Banh Mi, Bun Bo, etc.
    "quick_meals": 40,  # <15 min to prepare/get
    "vegan_vegetarian": 50,
    "high_protein": 40,
    "low_calorie": 35,
    "fine_dining": 20,
    "comfort_food": 50,
    "international_cuisine": 100,
    "meal_prep_friendly": 30,
    "healthy_bowls": 35,
}

TOTAL_NEW_MEALS = sum(NEW_MEAL_CATEGORIES.values())

print(f"""
PHASE 2: MEAL DATABASE EXPANSION PLAN
=====================================

Current state:
  - Meals: ~274
  - Fields per meal: ~10 (basic)

Target state:
  - Meals: ~400-500
  - Fields per meal: ~20+ (full nutrition/context)

New meal categories to add:
""")

for category, count in NEW_MEAL_CATEGORIES.items():
    print(f"  + {category}: {count} meals")

print(f"""
Total new meals: {TOTAL_NEW_MEALS}
Expansion factor: 1.5-2x current database

Key additions:
  ✓ Nutrition data (calories, macros, micros)
  ✓ Cooking instructions with ingredients
  ✓ Dietary & allergen info
  ✓ Multiple sourcing options
  ✓ Context & situation tags
  ✓ Wellness indicators

How to extend:
  1. Use MEAL_EXPANSION_TEMPLATE as reference
  2. Add new meals to meals_global.json
  3. Run migration script to validate
  4. Test with emotion detection
""")
