#!/usr/bin/env python3
"""
Test Vietnamese language detection and emotion recognition
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mood_to_meal_butler.emotions_config import detect_emotion, detect_language
from services.mood_service import mood_service

async def test_vietnamese():
    """Test Vietnamese emotion detection"""
    
    print("=" * 80)
    print("TESTING VIETNAMESE LANGUAGE & EMOTION DETECTION")
    print("=" * 80)
    
    test_cases = [
        ("Tôi buồn", "Vietnamese sad"),
        ("Tôi vui lắm", "Vietnamese happy"),
        ("I am sad", "English sad"),
        ("Tôi đang cảm thấy lo lắng", "Vietnamese anxiety"),
        ("Hôm nay tâm trạng không tốt", "Vietnamese bad mood"),
        ("I'm so excited", "English excited"),
    ]
    
    print("\n[TEST 1] Language Detection")
    print("-" * 80)
    for text, description in test_cases:
        lang = detect_language(text)
        print(f"  '{text}' → {lang} ({description})")
    
    print("\n[TEST 2] Emotion Detection (Auto-language)")
    print("-" * 80)
    for text, description in test_cases:
        emotion = detect_emotion(text)
        lang = detect_language(text)
        print(f"  '{text}'")
        print(f"    Language: {lang}, Emotion: {emotion} ({description})")
    
    print("\n[TEST 3] Full Mood Service with Vietnamese")
    print("-" * 80)
    viet_text = "Tôi buồn lắm, không biết ăn gì"  # "I'm so sad, don't know what to eat"
    result = await mood_service.detect(viet_text)
    
    print(f"Input: '{viet_text}'")
    print(f"Mood detected: {result.get('mood')}")
    print(f"Confidence: {result.get('confidence')}")
    print(f"Recommendations: {len(result.get('recommendations', []))} meals")
    print(f"Conversation: {result.get('conversation')[:100]}...")
    
    if result.get('recommendations'):
        print("\nFirst 3 meals:")
        for i, meal in enumerate(result.get('recommendations', [])[:3], 1):
            name = meal.get('name_en') or meal.get('name', 'Unknown')
            print(f"  {i}. {name}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_vietnamese())
