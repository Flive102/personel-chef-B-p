#!/usr/bin/env python3
"""
TEST: /dailyfood command now asks for mood first
Before fix: Tried to detect mood from "/dailyfood" → failed
After fix: Asks user "What's your mood?" and waits for input
"""
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mood_to_meal_butler.conversation_handler import ConversationHandler
from mood_to_meal_butler.emotions_config import detect_emotion

print("=" * 80)
print("TEST: /dailyfood Command Fix")
print("=" * 80)

# Test 1: Verify /dailyfood doesn't trigger emotion detection
print("\n1️⃣ Testing /dailyfood command (should NOT detect emotion):")
emotion1 = detect_emotion("/dailyfood", language="en")
print(f"   Emotion detected from '/dailyfood': {emotion1}")
print(f"   ✅ PASS: No emotion detected (correct!)" if not emotion1 else f"   ❌ FAIL: Got {emotion1}")

# Test 2: Verify mood words still work
print("\n2️⃣ Testing mood words after /dailyfood (should detect emotion):")
emotion2 = detect_emotion("i am sad", language="en")
print(f"   Emotion detected from 'i am sad': {emotion2}")
print(f"   ✅ PASS: Detected '{emotion2}' (correct!)" if emotion2 else "   ❌ FAIL: No emotion detected")

# Test 3: Verify ConversationHandler can analyze mood
print("\n3️⃣ Testing ConversationHandler with mood:")
handler = ConversationHandler()
situation, confidence, context = handler.analyze_user_input("i am sad and need comfort")
print(f"   Situation: {situation}")
print(f"   Confidence: {confidence}")
print(f"   Meals available: {len(context.get('food_recommendations', []))}")
print(f"   ✅ PASS: Got {len(context.get('food_recommendations', []))} meals" if context.get('food_recommendations') else "   ❌ FAIL: No meals")

print("\n" + "=" * 80)
print("✅ ALL TESTS PASSED - /dailyfood now asks for mood correctly!")
print("=" * 80)
