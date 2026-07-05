# scratch/simulate_run.py
import asyncio
import os
import sys
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.genai import types

# Make sure we can import mood_to_meal_butler
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mood_to_meal_butler.agent import root_agent

async def main():
    session_service = InMemorySessionService()
    session = await session_service.create_session(user_id="flive_user", app_name="test")
    runner = Runner(agent=root_agent, session_service=session_service, app_name="test")

    # We will step through the workflow by resuming it with answers.
    steps = [
        {"new_message": types.Content(role="user", parts=[types.Part.from_text(text="hello")])},
        {"resume_inputs": {"ask_user_name": "Flive"}},
        {"resume_inputs": {"mood": "vui vẻ"}},
        {"resume_inputs": {"craving": "cay"}},
        {"resume_inputs": {"group": "một mình"}},
        {"resume_inputs": {"budget": "cheap"}},
        {"resume_inputs": {"time": "fast"}},
        {"resume_inputs": {"diet": "chay"}},
        {"resume_inputs": {"chosen_idx_0": "1"}},
    ]

    for i, step_args in enumerate(steps, 1):
        print(f"\n=== STEP {i}: {step_args} ===")
        try:
            async for event in runner.run_async(
                user_id="flive_user",
                session_id=session.id,
                run_config=RunConfig(streaming_mode=StreamingMode.SSE),
                **step_args
            ):
                # Print event type and text if any
                print(f"Event: {type(event).__name__}")
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(f"  Text: {part.text.strip()}")
                        if part.function_call:
                            print(f"  ReqInput/FuncCall: {part.function_call.name} (id={part.function_call.id})")
                            print(f"    args={part.function_call.args}")
                if event.output:
                    print(f"  Output: {event.output}")
        except Exception as e:
            print("ERROR IN STEP:", e)
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
