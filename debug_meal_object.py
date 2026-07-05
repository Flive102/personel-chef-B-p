#!/usr/bin/env python3
"""
DEBUG: Check meal object structure
See what fields are actually in the meal objects
"""
import sys
import asyncio
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def debug_meal_objects():
    from services.mood_service import mood_service
    
    print("\n" + "="*80)
    print("DEBUG: Meal Object Structure")
    print("="*80)
    
    user_input = "i am sad"
    result = await mood_service.detect(user_input)
    recommendations = result.get('recommendations', [])
    
    if not recommendations:
        print("❌ No recommendations found!")
        return
    
    meal = recommendations[0]
    
    print(f"\n📋 Meal Object Keys:")
    for key in sorted(meal.keys()):
        print(f"   • {key}")
    
    print(f"\n📊 Full Meal Object:")
    import json
    print(json.dumps(meal, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(debug_meal_objects())
