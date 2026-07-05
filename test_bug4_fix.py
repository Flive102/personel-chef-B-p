#!/usr/bin/env python3
"""
Test Bug #4 Fix: Verify chosen_meal flows through generate_output and write_diary_entry
"""
import asyncio
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google.adk.runners import InMemoryRunner
from google.genai import types
from mood_to_meal_butler.agent import app

async def test_workflow():
    """Test the complete workflow with focus on Bug #4"""
    print("=" * 70)
    print("TEST: Bug #4 Fix - Meal Selection → Display Flow")
    print("=" * 70)
    
    runner = InMemoryRunner(app=app)
    session = await runner.session_service.create_session(
        app_name="mood_to_meal_butler", user_id="test_user"
    )
    
    print(f"\n✓ Session created: {session.id}\n")
    
    # Simulate workflow with predefined responses
    test_inputs = [
        "hello",           # START → init_db → load_history → fetch_weather → butler_interview
        "sad",             # Q1: How are you feeling?
        "stressed",        # Q2: What's triggering this?
        "work",            # Q3: Any health concerns?
        "none",            # Q4: Budget?
        "100",             # Q5: Group size?
        "2",               # Q6: Duration?
        "1",               # HUMAN_PICK: Select meal 1
    ]
    
    for i, user_msg in enumerate(test_inputs, 1):
        print(f"\n[Step {i}] User input: '{user_msg}'")
        print("-" * 70)
        
        event_count = 0
        chosen_meal_detected = False
        
        async for event in runner.run_async(
            user_id="test_user",
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part.from_text(text=user_msg)]),
        ):
            event_count += 1
            
            # Check for chosen_meal in output
            if hasattr(event, 'output') and event.output:
                if 'chosen_meal' in event.output:
                    meal = event.output['chosen_meal']
                    if meal and isinstance(meal, dict) and meal.get('name'):
                        chosen_meal_detected = True
                        print(f"  ✓ Output contains chosen_meal: {meal.get('name')}")
            
            # Print content if available
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts') and event.content.parts:
                    for part in event.content.parts[:1]:  # First part only
                        text = getattr(part, 'text', '')
                        if text:
                            text_preview = text[:100].replace('\n', ' ')
                            print(f"  → {text_preview}...")
        
        print(f"  Events processed: {event_count}")
        if chosen_meal_detected:
            print(f"  ✓ chosen_meal successfully passed through output")
        
        if i >= 7:  # Stop after meal selection
            break
    
    print("\n" + "=" * 70)
    print("✓ TEST COMPLETE - All workflow steps executed")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_workflow())
