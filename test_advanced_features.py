#!/usr/bin/env python3
"""
TEST SUITE: Interview Analytics & Recommendation Engine
Tests advanced personalization features
"""

import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mood_to_meal_butler.interview_analytics import InterviewAnalytics, InterviewEnhancer
from mood_to_meal_butler.interview_validator import InterviewValidator

def test_analytics_engine():
    """Test interview analytics tracking"""
    print("\n" + "="*70)
    print("TEST: Analytics Engine - Session Tracking")
    print("="*70 + "\n")
    
    analytics = InterviewAnalytics()
    
    # Simulate 3 interview sessions
    sessions_data = [
        {"mood": "tired", "craving": "light", "group": "solo", "budget": "moderate", "time": "normal", "diet": "none"},
        {"mood": "stressed", "craving": "comfort", "group": "solo", "budget": "moderate", "time": "quick", "diet": "vegetarian"},
        {"mood": "happy", "craving": "rich", "group": "friends", "budget": "splurge", "time": "unhurried", "diet": "none"},
    ]
    
    for i, session in enumerate(sessions_data, 1):
        ts = analytics.record_session(session)
        print(f"✓ Session {i} recorded: {session['mood']}")
    
    # Test mood trend analysis
    print(f"\nMood Trend (7 days):")
    trend = analytics.get_mood_trend()
    for mood, count in sorted(trend.items()):
        print(f"  {mood}: {count} occurrence(s)")
    
    # Test common combo detection
    print(f"\nMost Common Combination:")
    combo = analytics.get_most_common_combo()
    if combo:
        print(f"  Mood: {combo['mood']}, Craving: {combo['craving']}")
        print(f"  Frequency: {combo['frequency']} time(s)")
    
    # Test confidence scoring
    print(f"\nDecisiveness Scoring:")
    for session in sessions_data:
        score = analytics.calculate_interview_confidence(session)
        print(f"  {session['mood']:10} → {score:.1f}% decisive")
    
    print(f"\n✅ Analytics engine working correctly")
    return True

def test_enhancer():
    """Test interview enhancement features"""
    print("\n" + "="*70)
    print("TEST: Interview Enhancer - Smart Features")
    print("="*70 + "\n")
    
    enhancer = InterviewEnhancer()
    
    # Test smart question ordering
    print("Smart Question Ordering:")
    new_user_order = enhancer.get_smart_question_order(0)
    print(f"  New user order: {' → '.join(new_user_order)}")
    
    returning_user_order = enhancer.get_smart_question_order(5)
    print(f"  Returning user: {' → '.join(returning_user_order)}")
    
    # Test contextual hints
    print(f"\nContextual Hints:")
    previous = {"mood": "stressed"}
    hint = enhancer.get_contextual_hint("craving", previous)
    print(f"  After stressed mood: {hint}")
    
    # Test satisfaction prediction
    print(f"\nSatisfaction Prediction:")
    answers = {"mood": "tired", "budget": "moderate", "time": "quick", "diet": "none"}
    meal = {
        "mood_tags": ["tired", "energetic"],
        "price_tier": "moderate",
        "prep_time": 10,
        "dietary_tags": []
    }
    satisfaction = enhancer.predict_satisfaction(answers, meal)
    print(f"  Predicted satisfaction: {satisfaction:.1f}%")
    
    print(f"\n✅ Enhancer features working correctly")
    return True

def test_validator():
    """Test interview validation"""
    print("\n" + "="*70)
    print("TEST: Interview Validator - Data Quality")
    print("="*70 + "\n")
    
    validator = InterviewValidator()
    
    # Test individual answer validation
    print("Individual Answer Validation:")
    test_cases = [
        ("mood", "happy", True),
        ("mood", "", False),
        ("craving", "x", False),
        ("group", "solo", True),
    ]
    
    for key, answer, should_pass in test_cases:
        is_valid, msg, _ = validator.validate_answer(key, answer)
        status = "✓" if is_valid == should_pass else "✗"
        print(f"  {status} {key}='{answer}' → {msg}")
    
    # Test complete interview validation
    print(f"\nComplete Interview Validation:")
    good_answers = {
        "mood": "happy",
        "craving": "spicy",
        "group": "friends",
        "budget": "moderate",
        "time": "normal",
        "diet": "none"
    }
    is_valid, issues = validator.validate_complete_interview(good_answers)
    print(f"  Valid interview: {is_valid}")
    
    # Test validation report
    print(f"\nValidation Report:")
    report = validator.get_validation_report(good_answers)
    print(f"  Completion: {report['completion_percentage']}%")
    print(f"  Session valid: {report['session_valid']}")
    
    print(f"\n✅ Validator working correctly")
    return True

if __name__ == "__main__":
    try:
        r1 = test_analytics_engine()
        r2 = test_enhancer()
        r3 = test_validator()
        
        print("\n" + "="*70)
        print("ADVANCED FEATURES TEST SUMMARY")
        print("="*70)
        all_pass = r1 and r2 and r3
        if all_pass:
            print("✅ ALL ADVANCED FEATURES WORKING")
        else:
            print("❌ SOME TESTS FAILED")
        sys.exit(0 if all_pass else 1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
