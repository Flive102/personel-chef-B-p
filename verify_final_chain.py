#!/usr/bin/env python3
"""
FINAL VERIFICATION: Complete meal chain
From mood_service.detect() → what gets returned?
Check if meals are from 200+ database or generic
"""
import sys
import asyncio
import json
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def verify_complete_chain():
    from services.mood_service import mood_service
    
    print("\n" + "="*80)
    print("FINAL VERIFICATION: mood_service.detect() Complete Output")
    print("="*80)
    
    test_moods = [
        "i am sad",
        "i'm tired", 
        "i feel happy",
    ]
    
    for user_input in test_moods:
        print(f"\n{'─'*80}")
        print(f"INPUT: '{user_input}'")
        print(f"{'─'*80}")
        
        result = await mood_service.detect(user_input)
        
        mood = result.get('mood', 'unknown')
        recs = result.get('recommendations', [])
        
        print(f"\n✅ Detected mood: {mood}")
        print(f"✅ Total recommendations: {len(recs)}")
        
        # Check each recommendation
        print(f"\n📋 Recommendations Details:")
        for i, meal in enumerate(recs, 1):
            name = meal.get('name', 'Unknown')
            desc = meal.get('description', '')[:60]
            region = meal.get('region', 'Global')
            mood_tags = meal.get('mood_tags', [])
            
            # Check if it's a real meal or generic
            is_generic = "comforting and delicious meal" in (meal.get('description', '').lower())
            
            status = "⚠️ GENERIC" if is_generic else "✅ REAL"
            
            print(f"\n   {i}. {status} {name}")
            print(f"      Region: {region}")
            print(f"      Desc: {desc}")
            print(f"      Moods: {', '.join(mood_tags)}")
        
        # Summary
        real_count = sum(1 for m in recs if "comforting and delicious meal" not in (m.get('description', '').lower()))
        generic_count = len(recs) - real_count
        
        print(f"\n   Summary: {real_count} REAL meals, {generic_count} GENERIC meals")

if __name__ == "__main__":
    asyncio.run(verify_complete_chain())
