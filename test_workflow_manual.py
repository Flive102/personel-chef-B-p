#!/usr/bin/env python3
"""
MANUAL WORKFLOW TEST
Test: User mood input → Get suggestions → Pick meal → Show full details
"""
import sys
import asyncio
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_complete_workflow():
    from services.mood_service import mood_service
    
    print("\n" + "="*80)
    print("MOOD-TO-MEAL BUTLER: COMPLETE WORKFLOW TEST")
    print("="*80)
    
    # Step 1: Get user mood
    print("\n📝 STEP 1: Enter your mood or feeling")
    print("─" * 80)
    print("Examples: 'i am sad', 'i feel tired', 'i am happy', 'i feel stressed'")
    
    user_input = input("\n👤 Your mood: ").strip()
    
    if not user_input:
        user_input = "i am sad"
        print(f"(Using default: '{user_input}')")
    
    # Step 2: Get suggestions
    print("\n🔍 STEP 2: Analyzing your mood...")
    print("─" * 80)
    
    result = await mood_service.detect(user_input)
    
    mood = result.get('mood', 'unknown')
    confidence = result.get('confidence', 0) * 100
    conversation = result.get('conversation', '')
    recommendations = result.get('recommendations', [])
    
    print(f"✅ Detected mood: {mood}")
    print(f"✅ Confidence: {confidence:.1f}%")
    print(f"\n💬 Chef's response:\n{conversation}")
    
    # Step 3: Show suggestions
    print("\n🍽️  STEP 3: Meal suggestions for you")
    print("─" * 80)
    
    if not recommendations:
        print("❌ No recommendations found. Please try again with a different mood.")
        return
    
    print(f"Found {len(recommendations)} meal suggestions:\n")
    
    for i, meal in enumerate(recommendations, 1):
        name = meal.get('name_en', meal.get('name', 'Unknown'))
        region = meal.get('region', 'Global')
        mood_tags = meal.get('mood_tags', [])
        health_tags = meal.get('health_tags', [])
        emoji = meal.get('emoji', '🍽️')
        
        print(f"{i}. {emoji} {name} ({region})")
        if mood_tags:
            print(f"   Moods: {', '.join(mood_tags)}")
        if health_tags:
            print(f"   Health: {', '.join(health_tags)}")
        print()
    
    # Step 4: User picks meal
    print("\n🔢 STEP 4: Pick your meal")
    print("─" * 80)
    
    while True:
        choice = input(f"Choose 1-{len(recommendations)}: ").strip()
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(recommendations):
                break
            else:
                print(f"Please enter number between 1 and {len(recommendations)}")
        except ValueError:
            print(f"Please enter a valid number")
    
    chosen_meal = recommendations[choice_idx]
    
    # Step 5: Show full details
    print("\n✨ STEP 5: Your chosen meal - Full details")
    print("="*80)
    
    name_en = chosen_meal.get('name_en', '')
    name_vi = chosen_meal.get('name_vi', '')
    emoji = chosen_meal.get('emoji', '🍽️')
    region = chosen_meal.get('region', 'Global')
    description = chosen_meal.get('description_en', '')
    description_vi = chosen_meal.get('description_vi', '')
    
    # Famous label/label
    labels = []
    if chosen_meal.get('famous_for'):
        labels.append(f"Famous for: {chosen_meal.get('famous_for')}")
    if chosen_meal.get('cuisine_type'):
        labels.append(f"Cuisine: {chosen_meal.get('cuisine_type')}")
    if chosen_meal.get('meal_category'):
        labels.append(f"Category: {chosen_meal.get('meal_category')}")
    
    mood_tags = chosen_meal.get('mood_tags', [])
    health_tags = chosen_meal.get('health_tags', [])
    
    # Display
    print(f"\n{emoji} {name_en}")
    if name_vi:
        print(f"   (Vietnamese: {name_vi})")
    print(f"\n📍 Region: {region}")
    
    if labels:
        print(f"\n🏆 Labels:")
        for label in labels:
            print(f"   • {label}")
    
    print(f"\n📖 Description (English):\n   {description}")
    
    if description_vi:
        print(f"\n📖 Description (Vietnamese):\n   {description_vi}")
    
    if mood_tags:
        print(f"\n😊 Perfect for moods: {', '.join(mood_tags)}")
    
    if health_tags:
        print(f"\n💪 Health benefits: {', '.join(health_tags)}")
    
    # Ingredients
    ingredients = chosen_meal.get('ingredients', [])
    if ingredients:
        print(f"\n🥘 Key ingredients:")
        for ing in ingredients[:5]:  # Show first 5
            print(f"   • {ing}")
        if len(ingredients) > 5:
            print(f"   ... and {len(ingredients) - 5} more")
    
    # Restaurants
    restaurants = chosen_meal.get('restaurant_suggestions', [])
    if restaurants:
        print(f"\n🏪 Where to find it:")
        for rest in restaurants[:3]:
            print(f"   • {rest}")
        if len(restaurants) > 3:
            print(f"   ... and {len(restaurants) - 3} more")
    
    # Time and budget
    time_req = chosen_meal.get('time_required')
    budget = chosen_meal.get('budget')
    
    if time_req:
        print(f"\n⏱️  Time required: {time_req}")
    
    if budget:
        print(f"\n💰 Budget: {budget}")
    
    print("\n" + "="*80)
    print("✅ WORKFLOW COMPLETE!")
    print("="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(test_complete_workflow())
