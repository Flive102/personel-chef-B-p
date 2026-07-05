#!/usr/bin/env python3
"""
DEBUG: Verify meal lookup works
Check if ConversationHandler suggestions match database meals
"""
import sys
import json
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mood_to_meal_butler.conversation_handler import ConversationHandler

handler = ConversationHandler()

print("\n" + "="*80)
print("DEBUG: Meal Lookup Verification")
print("="*80)

# ConversationHandler suggestions
suggestions_by_mood = {
    "sad": ["Ice Cream", "Chocolate Brownie", "Tiramisu", "Cheesecake", "Pizza"],
    "tired": ["Salmon", "Butter Chicken", "Ramen", "Dark chocolate", "Eggs"],
    "happy": ["Argentinian Steak", "Paella", "Korean BBQ", "Sushi", "Cheesecake"]
}

print("\n📋 Testing meal lookups:\n")

for mood, meal_names in suggestions_by_mood.items():
    print(f"Mood: {mood.upper()}")
    print("─" * 76)
    
    for short_name in meal_names:
        result = handler._get_meal_with_description(short_name)
        
        if result:
            full_name = result.get("name", "")
            description = result.get("description", "")[:50] + "..."
            
            status = "✅" if result.get("description") else "⚠️"
            print(f"{status} '{short_name}' → '{full_name}'")
            if not result.get("description"):
                print(f"   WARNING: No description found!")
        else:
            print(f"❌ '{short_name}' → NOT FOUND")
    
    print()

print("="*80)
