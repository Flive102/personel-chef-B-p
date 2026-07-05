# ── Node 4: butler_interview (HITL) ──────────────────────────────
@node(rerun_on_resume=True)
async def butler_interview(ctx: Context, node_input: dict):
    """Chat freely OR start /interview for food recommendations"""
    user_name = ctx.state.get("user_name", "bạn")
    weather_desc = ctx.state.get("weather_desc", "không rõ")
    temp_c = ctx.state.get("temp_c", 28.0)
    history = ctx.state.get("history", {})
    
    # Show greeting if first time
    has_user_message = ctx.resume_inputs and "user_message" in ctx.resume_inputs
    if not has_user_message:
        greeting = f"👨‍🍳 Welcome {user_name}! I'm your Empathetic Culinary Butler.\n"
        greeting += f"Today is {weather_desc}, {temp_c:.0f}°C.\n\n"
        greeting += "💬 Chat freely with me, share your thoughts, feelings, or cravings.\n"
        greeting += "📋 When you're ready for personalized food recommendations, type: **/interview**\n\n"
        greeting += "I'm here to listen and suggest meals that will truly take care of you! 🍽️"
        print(greeting)
        yield Event(content=types.Content(role="model", parts=[types.Part.from_text(text=greeting)]))
        
        # Wait for user input
        yield RequestInput(
            interrupt_id="user_message",
            message="Go ahead, I'm listening..."
        )
        return
    
    # Get user message
    user_message = ctx.resume_inputs.get("user_message", "").strip()
    
    # CHECK IF USER WANTS INTERVIEW
    if user_message.lower() == "/interview" or user_message.lower().startswith("/interview"):
        # Initialize interview state if first time
        if "_interview_answers" not in ctx.state:
            ctx.state["_interview_answers"] = {}
            ctx.state["_interview_step"] = 0
        
        interview_questions = get_interview_questions(DEFAULT_LANGUAGE)
        collected_answers = ctx.state.get("_interview_answers", {})
        current_step = ctx.state.get("_interview_step", 0)
        
        # Process all questions sequentially
        while current_step < len(interview_questions):
            q = interview_questions[current_step]
            key = q["key"]
            
            # Check if this answer was just provided
            if key in ctx.resume_inputs:
                raw_ans = ctx.resume_inputs[key]
                parsed_ans = parse_answer(raw_ans, q)
                collected_answers[key] = parsed_ans
                collected_answers[key + "_raw"] = raw_ans
                ctx.state["_interview_answers"] = collected_answers
                current_step += 1
                ctx.state["_interview_step"] = current_step
            else:
                # Ask for this question and return
                msg = f"{q['question']} {q['hint']}"
                yield RequestInput(interrupt_id=key, message=msg)
                return
        
        # All mandatory questions answered, check optional (energy)
        if "energy" not in collected_answers:
            energy_q = OPTIONAL_QUESTIONS_EN[0]  # Get first optional question
            msg = f"{energy_q['question']} {energy_q['hint']}"
            yield RequestInput(interrupt_id="energy", message=msg)
            return
        
        # Process energy answer if it just came in
        if "energy" in ctx.resume_inputs and "energy" not in collected_answers:
            energy_raw = ctx.resume_inputs.get("energy", "medium")
            energy_q = OPTIONAL_QUESTIONS_EN[0]
            energy_parsed = parse_answer(energy_raw, energy_q)
            collected_answers["energy"] = energy_parsed
            collected_answers["energy_raw"] = energy_raw
            ctx.state["_interview_answers"] = collected_answers
        
        # All questions answered - compile results
        raw_texts = [
            collected_answers.get(k + "_raw", "") 
            for k in ["mood", "craving", "group", "budget", "time", "diet"]
        ]
        raw_interview = " | ".join(raw_texts)
        
        # Show health note
        mood_value = collected_answers.get("mood", "neutral")
        health_note = get_health_suggestion(mood_value)
        if health_note:
            print(f"\n{health_note}\n")
        
        # Clean up interview state
        del ctx.state["_interview_answers"]
        del ctx.state["_interview_step"]
        
        # Return interview results
        interview_result = {
            "mood": collected_answers.get("mood", "neutral"),
            "craving": collected_answers.get("craving", "surprise"),
            "group": collected_answers.get("group", "solo"),
            "budget": collected_answers.get("budget", "moderate"),
            "time": collected_answers.get("time", "normal"),
            "diet": collected_answers.get("diet", "none"),
            "energy": collected_answers.get("energy", "medium"),
            "raw_interview": raw_interview,
            "raw_user_input": user_message
        }
        yield Event(output=interview_result, state=interview_result)
    else:
        # User just chatted - acknowledge and offer interview option
        response = f"🤔 Got it! You said: '{user_message}'\n\n"
        response += "When you're ready for personalized food recommendations, just type **/interview**"
        print(response)
        yield Event(content=types.Content(role="model", parts=[types.Part.from_text(text=response)]))
        
        # Ask again for next input
        yield RequestInput(
            interrupt_id="user_message",
            message="What else would you like to share? Or type /interview when ready..."
        )
