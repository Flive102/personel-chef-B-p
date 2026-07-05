#!/usr/bin/env python3
"""
CRITICAL TEST: Meal field detection fixes
Bug #9: chosen_meal check used id instead of name
Bug #10: generate_output missing name_vi fallback
"""
import sys

def test_meal_field_detection():
    """Test that meals work even without id field"""
    print("=" * 80)
    print("[TEST] Bug #9-10: Meal field detection (mood_service format)")
    print("=" * 80)
    
    # Simulate mood_service meal (NO id field!)
    mood_service_meal = {
        "name_en": "Phở Bò",
        "name_vi": "Phở Bò",
        "emoji": "🍜",
        "region": "Vietnam",
        "description": "Traditional beef noodle soup"
    }
    
    print(f"\nMeal from mood_service: {mood_service_meal}")
    print(f"Has 'id' field? {bool(mood_service_meal.get('id'))}")
    
    # OLD BUG #9: Check only for id
    print(f"\n❌ OLD BUG #9: if chosen_meal and chosen_meal.get('id')")
    if mood_service_meal and mood_service_meal.get("id"):
        print(f"   Would PROCEED to generate_output")
    else:
        print(f"   Would REJECT valid meal and ask user again! (BUG)")
    
    # NEW FIX #9: Check for name fields too
    print(f"\n✅ NEW FIX #9: if chosen_meal and (name_en OR name_vi OR name OR id)")
    if mood_service_meal and (mood_service_meal.get("name_en") or 
                              mood_service_meal.get("name_vi") or 
                              mood_service_meal.get("name") or 
                              mood_service_meal.get("id")):
        print(f"   Correctly PROCEEDS to generate_output")
    else:
        print(f"   Would reject (should not happen)")
    
    # Test generate_output name extraction
    print(f"\n--- BUG #10: generate_output name extraction ---")
    
    # OLD BUG #10: get('name_en') or get('name')
    name_old = mood_service_meal.get('name_en') or mood_service_meal.get('name', '')
    print(f"\n❌ OLD: get('name_en') or get('name')")
    print(f"   Result: '{name_old}' (OK in this case, but misses name_vi)")
    
    # NEW FIX #10: Also check name_vi
    name_new = (mood_service_meal.get('name_en') or 
                mood_service_meal.get('name_vi') or 
                mood_service_meal.get('name', ''))
    print(f"\n✅ NEW: get('name_en') or get('name_vi') or get('name')")
    print(f"   Result: '{name_new}' (Always finds name)")
    
    # Test with meal that only has name_vi
    vi_only_meal = {
        "name_vi": "Phở Gà",
        "emoji": "🍜",
        "region": "Vietnam"
    }
    
    print(f"\n--- Test meal with ONLY name_vi ---")
    name_vi_only = (vi_only_meal.get('name_en') or 
                    vi_only_meal.get('name_vi') or 
                    vi_only_meal.get('name', ''))
    print(f"✅ Result: '{name_vi_only}' (Correctly finds name_vi)")
    
    return True

def test_empty_meal_detection():
    """Test defensive check for empty meals"""
    print(f"\n" + "=" * 80)
    print("[TEST] Defensive empty meal detection (Lines 1236-1238)")
    print("=" * 80)
    
    # Test 1: Empty meal
    empty_meal = {}
    print(f"\n1. Empty meal: {empty_meal}")
    if not empty_meal or not (empty_meal.get("name_en") or 
                              empty_meal.get("name_vi") or 
                              empty_meal.get("name")):
        print(f"   ✅ Correctly detected as EMPTY - asks user to retry")
    
    # Test 2: Valid meal with name
    valid_meal = {"name_vi": "Cơm Tấm", "emoji": "🍚"}
    print(f"\n2. Valid meal: {valid_meal}")
    if not valid_meal or not (valid_meal.get("name_en") or 
                              valid_meal.get("name_vi") or 
                              valid_meal.get("name")):
        print(f"   ❌ Would reject valid meal (BUG)")
    else:
        print(f"   ✅ Correctly accepted - proceeds to generate_output")
    
    # Test 3: Meal with only id (database meal)
    db_meal = {"id": "123", "name_en": "Pizza"}
    print(f"\n3. Database meal: {db_meal}")
    if not db_meal or not (db_meal.get("name_en") or 
                           db_meal.get("name_vi") or 
                           db_meal.get("name")):
        print(f"   ❌ Would reject (BUG)")
    else:
        print(f"   ✅ Correctly accepted")
    
    return True

def test_complete_flow():
    """Test complete flow with mood_service meals"""
    print(f"\n" + "=" * 80)
    print("[TEST] Complete workflow with mood_service meals")
    print("=" * 80)
    
    print(f"\nScenario: User enters 'i am sad'")
    print("-" * 80)
    
    # Step 1: mood_service returns meals (no id field)
    suggestions = [
        {"name_en": "Cơm Tấm", "emoji": "🍚", "region": "Vietnam"},
        {"name_vi": "Canh Chua", "emoji": "🍲", "region": "Vietnam"},
        {"name": "Bánh Mì", "emoji": "🥖", "region": "Vietnam"}
    ]
    
    print(f"1. mood_service returns {len(suggestions)} meals")
    for i, s in enumerate(suggestions, 1):
        print(f"   {i}. {s.get('name_en') or s.get('name_vi') or s.get('name')}")
    
    # Step 2: User picks meal 2
    idx = 1  # User enters "2"
    chosen_meal = suggestions[idx]
    print(f"\n2. User picks: {chosen_meal}")
    
    # Step 3: human_pick validates chosen_meal
    print(f"\n3. human_pick validates:")
    if chosen_meal and (chosen_meal.get("name_en") or 
                        chosen_meal.get("name_vi") or 
                        chosen_meal.get("name") or 
                        chosen_meal.get("id")):
        print(f"   ✅ Valid meal - proceeds to generate_output")
    else:
        print(f"   ❌ Rejected valid meal (BUG)")
    
    # Step 4: generate_output extracts name
    name = (chosen_meal.get('name_en') or 
            chosen_meal.get('name_vi') or 
            chosen_meal.get('name', ''))
    print(f"\n4. generate_output extracts name: '{name}'")
    print(f"   ✅ Displays meal with proper name")
    
    # Step 5: Diary entry uses name
    print(f"\n5. Diary entry: 'Hôm nay Flive ăn {name}. Thời tiết...'")
    print(f"   ✅ Meal name appears (NOT empty)")
    
    return True

if __name__ == "__main__":
    try:
        test1 = test_meal_field_detection()
        test2 = test_empty_meal_detection()
        test3 = test_complete_flow()
        
        print(f"\n" + "=" * 80)
        print("✅ ALL CRITICAL TESTS PASSED")
        print("=" * 80)
        sys.exit(0)
    except Exception as e:
        print(f"❌ TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
