#!/usr/bin/env python3
"""
FINAL INTEGRATION TEST: MCP Completely Disabled, mood_service as Primary
Test: No MCP errors, mood_service returns mood-specific meals
"""
import sys
import asyncio
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_app_initialization():
    """Test App initializes without MCP errors"""
    print("=" * 80)
    print("[TEST 1] App Initialization (No MCP)")
    print("=" * 80)
    
    try:
        from mood_to_meal_butler.agent import app
        print("\n✅ App imported successfully (NO MCP TaskGroup errors)")
        print(f"   App name: {app.root_agent.name}")
        print(f"   Toolsets configured: {getattr(app, 'toolsets', 'N/A')}")
        return True
    except Exception as e:
        print(f"\n❌ App initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mood_specific_suggestions():
    """Test mood_service returns DIFFERENT meals for DIFFERENT moods"""
    print("\n" + "=" * 80)
    print("[TEST 2] mood_service: Different Moods → Different Meals")
    print("=" * 80)
    
    from services.mood_service import mood_service
    
    moods = {
        "sad": "I am sad",
        "happy": "I am happy",
        "tired": "I am tired",
        "angry": "I am angry",
        "stressed": "I am stressed"
    }
    
    results = {}
    for mood_key, user_input in moods.items():
        result = mood_service.detect(user_input)
        recs = result.get('recommendations', [])
        
        # Extract meal names
        meal_names = []
        for r in recs[:3]:  # Top 3
            name = r.get('name_en') or r.get('name_vi') or r.get('name', 'Unknown')
            meal_names.append(name)
        
        results[mood_key] = meal_names
        print(f"\n{mood_key.upper()}:")
        for i, name in enumerate(meal_names, 1):
            print(f"  {i}. {name}")
    
    # Verify meals are DIFFERENT for different moods
    print("\n--- VERIFICATION ---")
    unique_meal_sets = {}
    all_same = True
    
    for mood, meals in results.items():
        meal_set = tuple(sorted(meals))
        if meal_set not in unique_meal_sets:
            unique_meal_sets[meal_set] = []
        unique_meal_sets[meal_set].append(mood)
    
    num_unique = len(unique_meal_sets)
    print(f"Number of unique meal combinations: {num_unique} (out of {len(moods)} moods)")
    
    if num_unique > 1:
        print("✅ DIFFERENT moods return DIFFERENT meals")
        for meal_set, mood_list in unique_meal_sets.items():
            print(f"   Meals {meal_set[:2]}... for moods: {mood_list}")
        return True
    else:
        print("❌ ALL moods return SAME meals (still broken)")
        print(f"   All moods get: {results[list(results.keys())[0]]}")
        return False

def test_meal_name_extraction():
    """Test meal names are properly extracted (not empty)"""
    print("\n" + "=" * 80)
    print("[TEST 3] Meal Name Extraction (No Empty Names)")
    print("=" * 80)
    
    from services.mood_service import mood_service
    
    result = mood_service.detect("I am sad")
    recs = result.get('recommendations', [])
    
    print(f"\nTesting {len(recs)} recommendations from mood_service:")
    
    all_have_names = True
    for i, rec in enumerate(recs[:5], 1):
        # Test extraction logic from generate_output
        name = rec.get('name_en') or rec.get('name_vi') or rec.get('name', '')
        
        if not name:
            print(f"❌ Rec {i}: EMPTY NAME")
            all_have_names = False
        else:
            print(f"✅ Rec {i}: {name}")
    
    if all_have_names:
        print("\n✅ All meals have proper names (no empty)")
        return True
    else:
        print("\n❌ Some meals have empty names")
        return False

def test_diary_format():
    """Test diary entry format with meal name"""
    print("\n" + "=" * 80)
    print("[TEST 4] Diary Entry Format")
    print("=" * 80)
    
    from services.mood_service import mood_service
    
    result = mood_service.detect("I am sad")
    recs = result.get('recommendations', [])
    
    if recs:
        meal = recs[0]
        meal_name = meal.get('name_en') or meal.get('name_vi') or meal.get('name', '')
        
        # Simulate diary entry
        diary_entry = f"Hôm nay Flive ăn {meal_name}. Thời tiết sunny, tâm trạng sad."
        
        print(f"\nDiary entry: {diary_entry}")
        
        if meal_name and meal_name not in ["", "."]:
            print("✅ Meal name present in diary (not empty)")
            return True
        else:
            print("❌ Meal name empty in diary")
            return False
    else:
        print("❌ No recommendations from mood_service")
        return False

def test_no_generic_meals():
    """Test that mood_service does NOT return generic meals like 'Coffee', 'Water'"""
    print("\n" + "=" * 80)
    print("[TEST 5] No Generic Fallback Meals")
    print("=" * 80)
    
    from services.mood_service import mood_service
    
    generic_meals = {"coffee", "water", "favorite beverage", "comfort food", "pasta", "treat"}
    
    result = mood_service.detect("I am sad")
    recs = result.get('recommendations', [])
    
    meal_names = [r.get('name_en') or r.get('name_vi') or r.get('name', '') for r in recs[:5]]
    
    print(f"\nFirst 5 recommendations for 'I am sad':")
    has_generic = False
    for i, name in enumerate(meal_names, 1):
        is_generic = name.lower() in generic_meals
        status = "⚠️ GENERIC" if is_generic else "✅"
        print(f"  {i}. {name} {status}")
        if is_generic:
            has_generic = True
    
    if not has_generic:
        print("\n✅ All recommendations are SPECIFIC (not generic)")
        return True
    else:
        print("\n⚠️ Some generic meals present (fallback is active)")
        return False

async def run_all_tests():
    """Run all tests"""
    print("\n\n")
    print("█" * 80)
    print("█ FINAL INTEGRATION TEST SUITE".ljust(80))
    print("█ Date: 2026-07-02 | Goal: Verify MCP disabled, mood_service working".ljust(80))
    print("█" * 80)
    
    test_results = {}
    
    # Test 1: App initialization
    test_results["App Init"] = await test_app_initialization()
    
    # Test 2: Mood-specific suggestions
    test_results["Mood-Specific"] = test_mood_specific_suggestions()
    
    # Test 3: Meal name extraction
    test_results["Name Extract"] = test_meal_name_extraction()
    
    # Test 4: Diary format
    test_results["Diary Format"] = test_diary_format()
    
    # Test 5: No generic meals
    test_results["No Generic"] = test_no_generic_meals()
    
    # Summary
    print("\n\n")
    print("█" * 80)
    print("█ TEST SUMMARY".ljust(80))
    print("█" * 80)
    
    passed = sum(1 for v in test_results.values() if v)
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"█ {test_name:.<40} {status}".ljust(79) + "█")
    
    print("█" * 80)
    print(f"█ RESULT: {passed}/{total} tests passed".ljust(80))
    
    if passed == total:
        print("█ STATUS: ✅ READY FOR agents-cli TESTING".ljust(80))
    else:
        print("█ STATUS: ❌ ISSUES REMAIN - FIX NEEDED".ljust(80))
    
    print("█" * 80)
    
    return passed == total

if __name__ == "__main__":
    try:
        success = asyncio.run(run_all_tests())
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n\n❌ TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
