#!/usr/bin/env python3
"""Direct agent test - Import and run workflow"""

import sys
import os
import asyncio

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_workflow():
    """Test the actual workflow directly"""
    
    print("\n" + "█"*80)
    print("DIRECT WORKFLOW TEST - Import & Run")
    print("█"*80)
    
    try:
        # Import the workflow
        print("\n[STEP 1] Import workflow...")
        from mood_to_meal_butler.agent import root_agent
        print(f"  ✓ Imported: {root_agent}")
        
        # Create input
        print("\n[STEP 2] Create input state...")
        input_state = {}
        print(f"  ✓ Input state ready")
        
        # Run workflow
        print("\n[STEP 3] Run workflow with 'I am sad'...")
        
        # Collect outputs
        outputs = []
        async for output in root_agent.run(input_state):
            outputs.append(output)
            print(f"  Got output: {type(output).__name__}")
            
            # Check for meal suggestions
            output_str = str(output)
            if any(kw in output_str for kw in ["Pizza", "Cake", "meal", "recommendation"]):
                print(f"    ✓ Contains meals/suggestions")
        
        print(f"\n  Total outputs: {len(outputs)}")
        
        if outputs:
            print(f"\n✅ Workflow ran successfully")
            return True
        else:
            print(f"\n❌ No outputs from workflow")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_workflow())
    print("\n" + "█"*80 + "\n")
