"""Interactive runner for Empathetic Culinary Butler with proper HITL handling"""
import asyncio
import sys
from google.adk.runners import InMemoryRunner
from google.adk.events.request_input import RequestInput
from google import genai
from mood_to_meal_butler.agent import app

async def interactive_runner():
    """Run agent with proper interactive HITL flow"""
    runner = InMemoryRunner(app=app)
    session = await runner.session_service.create_session(
        app_name="mood_to_meal_butler", 
        user_id="console_user"
    )
    
    print("🍳 Starting Empathetic Culinary Butler...\n")
    
    resume_inputs = {}
    first_run = True
    
    while True:
        try:
            # Prepare input message
            if first_run:
                new_message = genai.types.Content(
                    role="user", 
                    parts=[genai.types.Part.from_text(text="hello")]
                )
                first_run = False
            else:
                new_message = None
            
            # Run workflow - pass resume_inputs through context
            async for event in runner.run_async(
                user_id="console_user",
                session_id=session.id,
                new_message=new_message,
            ):
                # Check for RequestInput (HITL interrupt)
                if isinstance(event, RequestInput):
                    interrupt_id = event.interrupt_id
                    message = event.message
                    
                    # Print prompt and get user input
                    print(f"\n{message}")
                    user_input = input("👤 You: ").strip()
                    
                    # Store response in resume_inputs for next iteration
                    resume_inputs[interrupt_id] = user_input or "no"
                    
                    # Resume workflow with this input by restarting loop
                    # The session maintains state, so next run will use these inputs
                    break
                else:
                    # Regular event - just consume it
                    if hasattr(event, 'content') and event.content:
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                pass  # Output already printed by agent
            else:
                # Workflow completed successfully
                print("\n✨ Your meal has been saved. Looking forward to our next conversation! 👨‍🍳")
                break
                
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            break

def main():
    """Entry point for interactive agent"""
    try:
        asyncio.run(interactive_runner())
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)

if __name__ == "__main__":
    main()
