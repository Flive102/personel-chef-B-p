#!/usr/bin/env python3
"""
AUTOMATIC WORKFLOW TEST
Simulates: User mood → Get suggestions → Pick meal → Show full details
No interactive prompts - runs automatically
"""
import sys
import asyncio
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_workflow_auto():
    from services.mood_service import mood_service
    
    print("\n" + "="*80)
    print("MOOD-TO-MEAL BUTLER: AUTOMATIC WORKFLOW TEST")
    print("="*80)
    
    # Test multiple moods
    test_moods = [
        "i am sad and need comfort",
        "i'm exhausted after work",
        "i feel happy today",
    ]
    
    for user_input in test_moods:
        print("\n" + "─"*80)
        print(f"🧪 TEST: User Input = '{user_input}'")
        print("─"*80)
        
        # STEP 1: Get suggestions
        print("\n1️⃣  ANALYZING MOOD...")
        result = await mood_service.detect(user_input)
        
        mood = result.get('mood', 'unknown')
        confidence = result.get('confidence', 0) * 100
        recommendations = result.get('recommendations', [])
        
        print(f"   ✅ Detected mood: {mood}")
        print(f"   ✅ Confidence: {confidence:.1f}%")
        print(f"   ✅ Suggestions found: {len(recommendations)}")
        
        if not recommendations:
            print(f"   ❌ No recommendations! Skipping...")
            continue
        
        # STEP 2: Show suggestions list
        print(f"\n2️⃣  SUGGESTIONS ({len(recommendations)} meals):")
        for i, meal in enumerate(recommendations[:3], 1):  # Show first 3
            name = meal.get('name_en', meal.get('name', 'Unknown'))
            region = meal.get('region', 'Global')
            emoji = meal.get('emoji', '🍽️')
            print(f"   {i}. {emoji} {name} ({region})")
        
        # STEP 3: Automatically pick first meal
        chosen_meal = recommendations[0]
        choice_num = 1
        
        print(f"\n3️⃣  USER PICKS: Option #{choice_num}")
        
        # STEP 4: Show full details
        print(f"\n4️⃣  FULL MEAL DETAILS:")
        print("   " + "─"*76)
        
        # Use correct field names from meal object
        name = chosen_meal.get('name', '')
        emoji = chosen_meal.get('emoji', '🍽️')
        region = chosen_meal.get('region', 'Global')
        description = chosen_meal.get('description', '')
        
        print(f"\n   {emoji} {name}")
        
        print(f"\n   📍 Region: {region}")
        
        # Famous label/Category
        famous = chosen_meal.get('famous_for', '')
        cuisine = chosen_meal.get('cuisine_type', '')
        category = chosen_meal.get('meal_category', '')
        
        if famous or cuisine or category:
            print(f"\n   🏆 Labels:")
            if famous:
                print(f"      • Famous for: {famous}")
            if cuisine:
                print(f"      • Cuisine: {cuisine}")
            if category:
                print(f"      • Category: {category}")
        
        print(f"\n   📖 Description:")
        print(f"      {description}")
        
        # Moods and Health tags
        mood_tags = chosen_meal.get('mood_tags', [])
        health_tags = chosen_meal.get('health_tags', [])
        
        if mood_tags:
            print(f"\n   😊 Perfect for: {', '.join(mood_tags)}")
        
        if health_tags:
            print(f"   💪 Health tags: {', '.join(health_tags)}")
        
        # Ingredients (first 5)
        ingredients = chosen_meal.get('ingredients', [])
        if ingredients:
            print(f"\n   🥘 Key ingredients:")
            for ing in ingredients[:5]:
                print(f"      • {ing}")
            if len(ingredients) > 5:
                print(f"      ... and {len(ingredients) - 5} more")
        
        # Restaurants
        restaurants = chosen_meal.get('restaurant_suggestions', [])
        if restaurants:
            print(f"\n   🏪 Where to find it:")
            for rest in restaurants[:3]:
                print(f"      • {rest}")
            if len(restaurants) > 3:
                print(f"      ... and {len(restaurants) - 3} more")
        
        # Budget and time
        time_req = chosen_meal.get('time_required')
        budget = chosen_meal.get('budget')
        
        if time_req or budget:
            print(f"\n   ⏱️ Details:")
            if time_req:
                print(f"      • Time: {time_req}")
            if budget:
                print(f"      • Budget: {budget}")
        
        print("\n   " + "─"*76)
        print(f"\n✅ Workflow complete for: {mood}")

if __name__ == "__main__":
    asyncio.run(test_workflow_auto())
