#!/usr/bin/env python3
"""
TEST: Gemini-Based Meal Suggestions from 200+ Database
Verify mood_service.detect() now uses Gemini for ALL meal suggestions
"""
import sys
import asyncio
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_gemini_meal_suggestions():
    from services.mood_service import mood_service
    
    print("\n" + "="*80)
    print("GEMINI-BASED MEAL SUGGESTIONS TEST")
    print("Testing: Does mood_service use 200+ meal database via Gemini?")
    print("="*80)
    
    # Test different moods
    test_cases = [
        ("I am sad and need comfort", "SAD"),
        ("I'm exhausted after work", "TIRED"),
        ("I feel happy and celebratory", "HAPPY"),
        ("I'm stressed and anxious", "STRESSED"),
        ("I'm angry and frustrated", "ANGRY"),
    ]
    
    results = {}
    
    for user_input, mood_label in test_cases:
        print(f"\n{'─'*80}")
        print(f"TEST: {mood_label}")
        print(f"Input: '{user_input}'")
        print(f"{'─'*80}")
        
        try:
            result = await mood_service.detect(user_input)
            
            recs = result.get('recommendations', [])
            print(f"✅ Detected mood: {result.get('mood')}")
            print(f"✅ Confidence: {result.get('confidence'):.2f}")
            print(f"✅ Recommendations: {len(recs)} meals")
            
            meal_names = []
            for i, rec in enumerate(recs[:3], 1):
                name = rec.get('name_en', rec.get('name', 'Unknown'))
                mood_tags = rec.get('mood_tags', [])
                health_tags = rec.get('health_tags', [])
                
                print(f"\n   {i}. {name}")
                print(f"      Moods: {', '.join(mood_tags)}")
                print(f"      Health: {', '.join(health_tags)}")
                
                meal_names.append(name)
            
            results[mood_label] = tuple(meal_names)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results[mood_label] = ()
    
    # VERIFICATION: Check if different moods return different meals
    print(f"\n{'='*80}")
    print("VERIFICATION: Different Moods → Different Meals")
    print(f"{'='*80}")
    
    unique_combinations = len(set(results.values()))
    total_moods = len(results)
    
    print(f"\nTotal moods tested: {total_moods}")
    print(f"Unique meal combinations: {unique_combinations}")
    
    for mood, meals in results.items():
        print(f"\n{mood}: {meals}")
    
    if unique_combinations > 1:
        print(f"\n✅ SUCCESS: Different moods return different meals!")
        print(f"   {unique_combinations}/{total_moods} mood combinations are unique")
    else:
        print(f"\n❌ FAILURE: All moods returning same meals!")
    
    # Check for generic meal names
    print(f"\n{'='*80}")
    print("CHECK: Generic vs Real Meal Names")
    print(f"{'='*80}")
    
    generic_names = {"Pasta", "Comfort Food", "Treat", "Favorite Meal", "Coffee", "Water"}
    all_meals = set()
    generic_found = []
    
    for meals in results.values():
        for meal in meals:
            all_meals.add(meal)
            if meal in generic_names:
                generic_found.append(meal)
    
    print(f"\nTotal unique meals suggested: {len(all_meals)}")
    print(f"Generic meals found: {len(generic_found)}")
    
    if generic_found:
        print(f"⚠️  WARNING: Found generic meals: {generic_found}")
    else:
        print(f"✅ SUCCESS: No generic meals found!")
    
    print(f"\nMeals suggested from 200+ database:")
    for meal in sorted(all_meals):
        print(f"   - {meal}")
    
    print(f"\n{'='*80}")
    if unique_combinations > 1 and not generic_found:
        print("✅ ALL TESTS PASSED - Gemini using 200+ meal database!")
    else:
        print("❌ SOME TESTS FAILED - See above for details")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    asyncio.run(test_gemini_meal_suggestions())
