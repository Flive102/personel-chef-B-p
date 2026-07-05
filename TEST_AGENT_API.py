#!/usr/bin/env python3
"""Test agent API - Send 'I am sad' and check for meal suggestions"""

import asyncio
import httpx
import json

async def test_agent_api():
    """Call agent endpoint with user message"""
    
    print("\n" + "█"*80)
    print("TEST: Send 'I am sad' to mood_to_meal_butler agent")
    print("█"*80)
    
    async with httpx.AsyncClient(timeout=120) as client:
        try:
            # Step 1: Get agents (returns list)
            print("\n[STEP 1] Get available agents...")
            response = await client.get("http://127.0.0.1:8090/list-apps?relative_path=./")
            apps = response.json()
            
            if not isinstance(apps, list):
                print(f"❌ Unexpected response format: {type(apps)}")
                return False
            
            if "mood_to_meal_butler" not in apps:
                print(f"❌ mood_to_meal_butler not found in {apps}")
                return False
            
            print(f"  ✓ Found agent: mood_to_meal_butler")
            
            # Step 2: Start session with agent
            print(f"\n[STEP 2] Send message: 'I am sad'")
            response = await client.post(
                "http://127.0.0.1:8090/agents/mood_to_meal_butler/run",
                json={"text": "I am sad"},
                timeout=120
            )
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"  ❌ Error: {response.text[:200]}")
                return False
            
            result = response.json()
            response_text = json.dumps(result)
            
            print(f"  Response length: {len(response_text)} chars")
            
            # Check for meal suggestions
            meal_keywords = ["Pizza", "Cake", "Salmon", "Ramen", "Tacos", "meal", "recommendation"]
            has_meals = any(kw in response_text for kw in meal_keywords)
            
            if has_meals:
                print(f"\n✅ MEALS FOUND IN RESPONSE!")
                # Show sample
                print(f"  Sample: {response_text[:300]}...")
                return True
            else:
                print(f"\n❌ NO MEALS in response")
                print(f"  Response: {response_text[:300]}...")
                return False
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    result = asyncio.run(test_agent_api())
    print("\n" + "█"*80)
    print("END TEST")
    print("█"*80 + "\n")
