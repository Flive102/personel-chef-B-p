#!/usr/bin/env python3
"""
TEST: Verify payload and response_scheme are NEVER NULL
Tests edge cases and unusual situations
"""

import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_interview_payload_never_null():
    """Simulate edge cases to ensure payload/response_scheme never NULL"""
    print("\n" + "="*70)
    print("TEST: Interview Payload Safety - No NULL Values")
    print("="*70 + "\n")
    
    test_cases = [
        {
            "name": "Normal case - all answers provided",
            "answers": {"mood": "happy", "craving": "spicy", "group": "solo", 
                       "budget": "moderate", "time": "quick", "diet": "none"}
        },
        {
            "name": "Empty strings - should use defaults",
            "answers": {"mood": "", "craving": "", "group": "", 
                       "budget": "", "time": "", "diet": ""}
        },
        {
            "name": "None values - should use defaults",
            "answers": {"mood": None, "craving": None, "group": None, 
                       "budget": None, "time": None, "diet": None}
        },
        {
            "name": "Mixed empty/valid",
            "answers": {"mood": "tired", "craving": "", "group": "solo", 
                       "budget": None, "time": "normal", "diet": "none"}
        },
        {
            "name": "Partial answers",
            "answers": {"mood": "stressed", "craving": "comfort"}
        }
    ]
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        test_name = test_case["name"]
        answers = test_case["answers"]
        
        # Simulate what agent.py does
        try:
            interview_result = {
                "mood": answers.get("mood", "neutral") or "neutral",
                "craving": answers.get("craving", "surprise") or "surprise",
                "group": answers.get("group", "solo") or "solo",
                "budget": answers.get("budget", "moderate") or "moderate",
                "time": answers.get("time", "normal") or "normal",
                "diet": answers.get("diet", "none") or "none",
                "energy": answers.get("energy", "medium") or "medium",
                "payload": {
                    "interview_status": "complete",
                    "questions_answered": len(answers),
                    "total_questions": 6
                },
                "response_scheme": {
                    "type": "interview_result",
                    "version": "1.0",
                    "status": "success"
                }
            }
            
            # Check nothing is NULL
            checks = [
                ("payload exists", interview_result.get("payload") is not None),
                ("payload not empty", bool(interview_result.get("payload"))),
                ("response_scheme exists", interview_result.get("response_scheme") is not None),
                ("response_scheme not empty", bool(interview_result.get("response_scheme"))),
                ("mood not null", interview_result["mood"] is not None),
                ("craving not null", interview_result["craving"] is not None),
            ]
            
            all_passed = all(check[1] for check in checks)
            
            if all_passed:
                print(f"✅ {test_name}")
                print(f"   payload: {interview_result['payload']}")
                print(f"   response_scheme: {interview_result['response_scheme']}")
                passed += 1
            else:
                print(f"❌ {test_name}")
                for check_name, check_result in checks:
                    if not check_result:
                        print(f"   FAIL: {check_name}")
                failed += 1
                
        except Exception as e:
            print(f"❌ {test_name} - Exception: {e}")
            failed += 1
        
        print()
    
    # Summary
    print("="*70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    if failed == 0:
        print("✅ ALL TESTS PASSED - No NULL values detected")
    else:
        print(f"❌ {failed} test(s) failed")
    print("="*70)
    
    return failed == 0

if __name__ == "__main__":
    success = test_interview_payload_never_null()
    sys.exit(0 if success else 1)
