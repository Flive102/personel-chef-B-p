#!/usr/bin/env python3
"""
DEBUG: Check what ConversationHandler actually returns
Is it using 200+ meals database or still hardcoded training data?
"""
import sys
import json
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mood_to_meal_butler.conversation_handler import ConversationHandler

handler = ConversationHandler()

print("\n" + "="*80)
print("DEBUG: ConversationHandler Meal Recommendations")
print("="*80)

# Test different moods
test_inputs = [
    "i am sad",
    "i am tired",
    "i am happy",
]

for user_input in test_inputs:
    print(f"\n{'─'*80}")
    print(f"Input: '{user_input}'")
    print(f"{'─'*80}")
    
    try:
        result = handler.generate_conversation_flow(user_input)
        
        if result.get('success'):
            situation = result.get('situation_detected')
            structured = result.get('structured_response', {})
            
            print(f"Detected: {situation}")
            
            # Get step 4 (recommendations)
            step4 = structured.get('step_4_recommendation', {})
            
            if step4:
                suggestions = step4.get('suggestions', {})
                print(f"\nRaw suggestions from ConversationHandler:")
                print(json.dumps(suggestions, indent=2))
                
                # Count suggestions
                food_list = suggestions.get('food', [])
                drinks_list = suggestions.get('drinks', [])
                
                print(f"\nFood items: {food_list}")
                print(f"Drinks items: {drinks_list}")
                
                print(f"\nTotal: {len(food_list)} foods + {len(drinks_list)} drinks")
            else:
                print("No step_4_recommendation found")
        else:
            print(f"Failed: {result.get('error')}")
            
    except Exception as e:
        print(f"Error: {e}")

print("\n" + "="*80)
