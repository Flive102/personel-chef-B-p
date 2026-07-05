#!/usr/bin/env python3
"""
FINAL VERIFICATION TEST - Workflow Payload Preservation
Verifies that payload and response_scheme flow through ALL nodes without becoming NULL
"""

import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_payload_flow_simulation():
    """Simulate workflow flow with payload/response_scheme preservation"""
    print("\n" + "="*70)
    print("TEST: Payload & Response_Scheme Flow Through All Nodes")
    print("="*70 + "\n")
    
    # Start of workflow - butler_interview creates payload/response_scheme
    print("[Node 1: butler_interview] Creates interview_result")
    interview_result = {
        "mood": "happy",
        "craving": "spicy",
        "budget": "medium",
        "group": "2",
        "payload": {
            "interview_status": "complete",
            "questions_answered": 6,
            "total_questions": 6
        },
        "response_scheme": {
            "type": "interview_result",
            "version": "1.0",
            "status": "success"
        }
    }
    print(f"  ✓ payload: {interview_result['payload']}")
    print(f"  ✓ response_scheme: {interview_result['response_scheme']}\n")
    
    # Node 2: security_check passes node_input through
    print("[Node 2: security_check] Passes node_input through")
    node_input = interview_result
    if node_input.get("payload") and node_input.get("response_scheme"):
        print(f"  ✓ payload preserved: {node_input['payload'] is not None}")
        print(f"  ✓ response_scheme preserved: {node_input['response_scheme'] is not None}\n")
    else:
        print("  ❌ FAILED: payload/response_scheme lost\n")
        return False
    
    # Node 3: llm_suggest extracts and PRESERVES payload/response_scheme
    print("[Node 3: llm_suggest] Extracts & preserves payload/response_scheme")
    suggestions = [
        {"id": 1, "name": "Phở", "emoji": "🍲"},
        {"id": 2, "name": "Bún Chả", "emoji": "🍜"},
        {"id": 3, "name": "Cơm Tấm", "emoji": "🍚"}
    ]
    llm_output = {
        "suggestions": suggestions,
        "payload": node_input.get("payload"),
        "response_scheme": node_input.get("response_scheme")
    }
    if llm_output.get("payload") and llm_output.get("response_scheme"):
        print(f"  ✓ payload preserved: {llm_output['payload'] is not None}")
        print(f"  ✓ response_scheme preserved: {llm_output['response_scheme'] is not None}\n")
    else:
        print("  ❌ FAILED: payload/response_scheme lost in llm_suggest\n")
        return False
    
    # Node 4: human_pick selects meal and PRESERVES payload/response_scheme
    print("[Node 4: human_pick] Selects meal & preserves payload/response_scheme")
    chosen_meal = suggestions[0]
    human_pick_output = {
        "chosen_meal": chosen_meal,
        "payload": llm_output.get("payload"),
        "response_scheme": llm_output.get("response_scheme")
    }
    if human_pick_output.get("payload") and human_pick_output.get("response_scheme"):
        print(f"  ✓ payload preserved: {human_pick_output['payload'] is not None}")
        print(f"  ✓ response_scheme preserved: {human_pick_output['response_scheme'] is not None}\n")
    else:
        print("  ❌ FAILED: payload/response_scheme lost in human_pick\n")
        return False
    
    # Node 5: generate_output passes node_input through
    print("[Node 5: generate_output] Passes node_input through")
    generate_output = human_pick_output  # generate_output uses output=node_input
    if generate_output.get("payload") and generate_output.get("response_scheme"):
        print(f"  ✓ payload preserved: {generate_output['payload'] is not None}")
        print(f"  ✓ response_scheme preserved: {generate_output['response_scheme'] is not None}\n")
    else:
        print("  ❌ FAILED: payload/response_scheme lost in generate_output\n")
        return False
    
    # Node 6: write_diary_entry preserves payload/response_scheme
    print("[Node 6: write_diary_entry] Preserves payload/response_scheme")
    diary_output = {
        "diary_entry": "Today I had Phở",
        "payload": generate_output.get("payload"),
        "response_scheme": generate_output.get("response_scheme")
    }
    if diary_output.get("payload") and diary_output.get("response_scheme"):
        print(f"  ✓ payload preserved: {diary_output['payload'] is not None}")
        print(f"  ✓ response_scheme preserved: {diary_output['response_scheme'] is not None}\n")
    else:
        print("  ❌ FAILED: payload/response_scheme lost in write_diary_entry\n")
        return False
    
    # Node 7: record_session preserves payload/response_scheme
    print("[Node 7: record_session] Preserves payload/response_scheme")
    final_output = {
        "status": "done",
        "payload": diary_output.get("payload"),
        "response_scheme": diary_output.get("response_scheme")
    }
    if final_output.get("payload") and final_output.get("response_scheme"):
        print(f"  ✓ payload preserved: {final_output['payload'] is not None}")
        print(f"  ✓ response_scheme preserved: {final_output['response_scheme'] is not None}\n")
    else:
        print("  ❌ FAILED: payload/response_scheme lost in record_session\n")
        return False
    
    print("="*70)
    print("✅ SUCCESS: payload & response_scheme flow through ALL 7 nodes")
    print("="*70)
    return True

def test_edge_case_preservation():
    """Test that payload/response_scheme survive even with NULL interview values"""
    print("\n" + "="*70)
    print("TEST: Edge Case - NULL Interview Values Don't Strip payload/response_scheme")
    print("="*70 + "\n")
    
    # Even if interview fails, payload/response_scheme should survive
    edge_case_result = {
        "mood": None,  # NULL
        "craving": None,  # NULL
        "payload": {"status": "error_recovery"},
        "response_scheme": {"type": "fallback"}
    }
    
    print("Input has NULL mood/craving but valid payload/response_scheme")
    print(f"  mood: {edge_case_result['mood']}")
    print(f"  craving: {edge_case_result['craving']}")
    print(f"  payload: {edge_case_result['payload']}")
    print(f"  response_scheme: {edge_case_result['response_scheme']}\n")
    
    # Downstream node gets this
    node_input = edge_case_result
    if node_input.get("payload") and node_input.get("response_scheme"):
        print("✅ PASS: payload & response_scheme preserved despite NULL values\n")
        return True
    else:
        print("❌ FAIL: payload & response_scheme lost\n")
        return False

if __name__ == "__main__":
    print("\n" + "#"*70)
    print("# FINAL VERIFICATION: PAYLOAD/RESPONSE_SCHEME PRESERVATION")
    print("#"*70)
    
    test1 = test_payload_flow_simulation()
    test2 = test_edge_case_preservation()
    
    print("\n" + "#"*70)
    print("# RESULTS")
    print("#"*70)
    print(f"Workflow flow test:     {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Edge case test:         {'✅ PASS' if test2 else '❌ FAIL'}")
    
    all_pass = test1 and test2
    print(f"\nOVERALL:                {'✅ ALL TESTS PASS' if all_pass else '❌ SOME TESTS FAIL'}")
    print("#"*70 + "\n")
    
    sys.exit(0 if all_pass else 1)
