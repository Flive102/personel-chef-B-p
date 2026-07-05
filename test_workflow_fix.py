#!/usr/bin/env python3
"""
WORKFLOW TEST: Verify butler_interview captures input and routes to llm_suggest correctly
Tests: /goal <mood> → mood_service path and /dailyfood → interview path
"""

import asyncio
from unittest.mock import Mock, AsyncMock, MagicMock
from google.adk.agents.context import Context
from google.adk.events.request_input import RequestInput
from google.adk.events.event import Event

# Import the fixed butler_interview
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mood_to_meal_butler.agent import butler_interview
from mood_to_meal_butler.interview import get_interview_questions, parse_answer, DEFAULT_LANGUAGE


async def test_direct_mood_input():
    """Test /goal command captures mood and passes to mood_service"""
    print("\n" + "="*70)
    print("TEST 1: Direct Mood Input (/goal happy)")
    print("="*70 + "\n")
    
    # Create mock context
    ctx = Mock(spec=Context)
    ctx.state = {
        "user_name": "GenericUser",
        "weather_desc": "sunny",
        "temp_c": 28.0,
        "history": {}
    }
    ctx.resume_inputs = None
    
    # First call - show greeting
    print("Step 1: First call (no input yet - show greeting)")
    events = []
    async for event in butler_interview(ctx, {}):
        events.append(event)
        if isinstance(event, RequestInput):
            print(f"  → RequestInput waiting for: {event.interrupt_id}")
            break
    
    # Second call - user types /goal happy
    print("\nStep 2: User enters '/goal happy'")
    ctx.resume_inputs = {"user_message": "/goal happy"}
    
    events = []
    async for event in butler_interview(ctx, {}):
        events.append(event)
        if isinstance(event, Event) and event.output:
            output = event.output
            print(f"  → Output received:")
            print(f"    - mood: {output.get('mood')}")
            print(f"    - use_mood_service: {output.get('use_mood_service')}")
            print(f"    - raw_user_input: {output.get('raw_user_input')}")
            
            # VERIFY the critical fix
            assert output.get("use_mood_service") == True, "❌ use_mood_service not set to True!"
            assert output.get("mood") == "happy", f"❌ mood should be 'happy', got {output.get('mood')}"
            assert output.get("raw_user_input") == "/goal happy", "❌ raw_user_input not captured!"
            print("  ✅ PASS: Direct mood input captured and routed to mood_service")
            return True
    
    print("  ❌ FAIL: No output event received")
    return False


async def test_dailyfood_interview():
    """Test /dailyfood command starts interview questions"""
    print("\n" + "="*70)
    print("TEST 2: /dailyfood Interview Flow")
    print("="*70 + "\n")
    
    # Create mock context
    ctx = Mock(spec=Context)
    ctx.state = {
        "user_name": "GenericUser",
        "weather_desc": "rainy",
        "temp_c": 25.0,
        "history": {}
    }
    ctx.resume_inputs = None
    
    # First call - show greeting
    print("Step 1: First call (show greeting)")
    events = []
    async for event in butler_interview(ctx, {}):
        events.append(event)
        if isinstance(event, RequestInput):
            print(f"  → Waiting for user_message")
            break
    
    # Second call - user types /dailyfood
    print("\nStep 2: User enters '/dailyfood' to start interview")
    ctx.resume_inputs = {"user_message": "/dailyfood"}
    
    events = []
    interview_questions = get_interview_questions(DEFAULT_LANGUAGE)
    
    # Simulate answering each question
    for step, q in enumerate(interview_questions):
        key = q["key"]
        print(f"\nStep {step + 3}: Question '{key}' → answering...")
        
        # Simulate user answer
        if key == "mood":
            ctx.resume_inputs[key] = "sad"
        elif key == "craving":
            ctx.resume_inputs[key] = "comfort"
        elif key == "group":
            ctx.resume_inputs[key] = "solo"
        elif key == "budget":
            ctx.resume_inputs[key] = "moderate"
        elif key == "time":
            ctx.resume_inputs[key] = "normal"
        elif key == "diet":
            ctx.resume_inputs[key] = "none"
        
        events = []
        async for event in butler_interview(ctx, {}):
            events.append(event)
            if isinstance(event, RequestInput):
                print(f"    → Next question requested")
                break
            elif isinstance(event, Event) and event.output and "mood" in event.output:
                # All questions answered - interview complete
                output = event.output
                print(f"    → Interview complete!")
                print(f"      - mood: {output.get('mood')}")
                print(f"      - use_mood_service: {output.get('use_mood_service')}")
                
                # VERIFY the critical fix
                assert output.get("mood") == "sad", "❌ mood not captured from interview!"
                assert output.get("craving") == "comfort", "❌ craving not captured!"
                assert output.get("use_mood_service") == False, "❌ use_mood_service should be False for /dailyfood"
                assert output.get("raw_user_input") == "/dailyfood", "❌ raw_user_input not set!"
                print("  ✅ PASS: Interview captured all answers and returned to llm_suggest")
                return True
    
    print("  ❌ FAIL: Interview did not complete")
    return False


async def test_chat_flow():
    """Test normal chat (not /dailyfood or /goal) loops back for more input"""
    print("\n" + "="*70)
    print("TEST 3: Normal Chat Flow (no command)")
    print("="*70 + "\n")
    
    # Create mock context
    ctx = Mock(spec=Context)
    ctx.state = {
        "user_name": "GenericUser",
        "weather_desc": "sunny",
        "temp_c": 28.0,
        "history": {}
    }
    ctx.resume_inputs = None
    
    # First call - show greeting
    print("Step 1: Show greeting")
    async for event in butler_interview(ctx, {}):
        if isinstance(event, RequestInput):
            break
    
    # Second call - user just chats
    print("\nStep 2: User enters regular chat message")
    ctx.resume_inputs = {"user_message": "I'm feeling a bit tired today"}
    
    events = []
    async for event in butler_interview(ctx, {}):
        events.append(event)
        if isinstance(event, RequestInput):
            print(f"  → Still waiting for /dailyfood or /goal command")
            print("  ✅ PASS: Chat message acknowledged, looped back for more input")
            return True
    
    print("  ❌ FAIL: Did not loop back for more input")
    return False


async def main():
    print("\n" + "█" * 70)
    print("WORKFLOW TEST: butler_interview Input Capture Fix")
    print("█" * 70)
    
    results = []
    
    try:
        result1 = await test_direct_mood_input()
        results.append(("Direct /goal mood input", result1))
    except Exception as e:
        print(f"\n❌ TEST 1 ERROR: {e}")
        results.append(("Direct /goal mood input", False))
    
    try:
        result2 = await test_dailyfood_interview()
        results.append(("Interview /dailyfood flow", result2))
    except Exception as e:
        print(f"\n❌ TEST 2 ERROR: {e}")
        results.append(("Interview /dailyfood flow", False))
    
    try:
        result3 = await test_chat_flow()
        results.append(("Normal chat flow", result3))
    except Exception as e:
        print(f"\n❌ TEST 3 ERROR: {e}")
        results.append(("Normal chat flow", False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    print("\n" + ("🎉 ALL TESTS PASSED!" if all_passed else "⚠️  SOME TESTS FAILED"))
    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
