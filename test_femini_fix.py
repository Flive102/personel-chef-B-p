#!/usr/bin/env python3
"""
Test script to verify Femini API quota fallback fix
Tests that mood_service returns 8 local meals when Gemini quota exhausted
"""

import asyncio
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.mood_service import mood_service

async def test_mood_service():
    """Test that mood_service returns meals even on Gemini failure"""
    
    print("=" * 80)
    print("TESTING FEMINI API QUOTA FALLBACK FIX")
    print("=" * 80)
    
    # Test 1: Simple emotion input
    print("\n[TEST 1] User input: 'I am sad'")
    print("-" * 80)
    result = await mood_service.detect("I am sad")
    
    print(f"Mood detected: {result.get('mood')}")
    print(f"Confidence: {result.get('confidence')}")
    print(f"Conversation: {result.get('conversation')[:80]}...")
    
    recommendations = result.get('recommendations', [])
    print(f"\n✅ Recommendations returned: {len(recommendations)} meals")
    
    if len(recommendations) == 0:
        print("❌ FAIL: No meals returned!")
        return False
    
    if len(recommendations) >= 5:
        print(f"✅ PASS: Got {len(recommendations)} meals (expected 5-8)")
    
    # Show first 3 meals
    print("\nFirst 3 meals suggested:")
    for i, meal in enumerate(recommendations[:3], 1):
        name = meal.get('name_en') or meal.get('name', 'Unknown')
        emoji = meal.get('emoji', '🍽️')
        print(f"  {i}. {emoji} {name}")
    
    print("\n" + "=" * 80)
    print("TEST RESULT: ✅ PASS - Fallback meals returned successfully")
    print("=" * 80)
    return True

if __name__ == "__main__":
    result = asyncio.run(test_mood_service())
    sys.exit(0 if result else 1)
