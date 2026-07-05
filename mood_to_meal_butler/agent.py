# mood_agent/agent.py
# Định nghĩa 10 graph nodes sử dụng Google ADK 2.0 Workflow API

import os
import sys
import re
import sqlite3
import datetime
import httpx
import asyncio
from typing import Any
from google.adk.workflow import Workflow, node, START, FunctionNode
from google.adk.agents.context import Context
from google.adk.events.event import Event
from google.adk.events.request_input import RequestInput
from google.adk.apps import App, ResumabilityConfig
# from google.adk.tools import MCPToolset  # DISABLED: MCP causing TaskGroup errors
try:
    from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
    from mcp import StdioServerParameters
except ImportError:
    # Fallback if MCP imports not available
    StdioConnectionParams = None
    StdioServerParameters = None
from google.genai import types
from google import genai

from mood_to_meal_butler.config import (
    DB_PATH,
    GEMINI_API_KEY,
    MODEL_NAME,
    DEFAULT_LAT,
    DEFAULT_LON,
    DEFAULT_USER_NAME
)
from mood_to_meal_butler.emotions_config import (
    detect_emotion,
    EMOTION_KEYWORDS,
    EMOTION_METADATA,
    VIETNAMESE_EMOTIONS,
)
from mood_to_meal_butler.situations_config import (
    detect_situation,
    get_situation_filters,
    SITUATIONS,
)
from mood_to_meal_butler.error_handler import (
    validate_user_input,
    validate_emotion,
    validate_situations,
    handle_missing_meals,
    log_error,
    ValidationError,
)
from mood_to_meal_butler.interview import (
    parse_answer,
    build_diary_prompt,
    get_health_suggestion,
    get_interview_questions,
    DEFAULT_LANGUAGE
)
from mood_to_meal_butler.interview_enhancements import (
    OPTIONAL_QUESTIONS_EN,
    get_energy_based_meal_tags,
    get_health_goal_meal_tags
)
from mood_to_meal_butler.emotional_responses import (
    format_emotional_intro,
    format_emotional_closing
)
from mood_to_meal_butler.conversation_handler import ConversationHandler
from services.mood_service import mood_service

# Đảm bảo in tiếng Việt chuẩn trên Windows terminal
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Lazy initialization: Only create MCP toolset when actually used (not at import time)
_mcp_toolset = None

def get_mcp_toolset():
    """Lazy initialize MCP toolset to avoid hanging on startup"""
    global _mcp_toolset
    # MCP DISABLED: Return None to prevent TaskGroup errors
    print("ℹ️  MCP is disabled. Using mood_service instead.")
    return None

mcp_toolset = None  # Placeholder - use get_mcp_toolset() instead

def text_event(text: str) -> Event:
    return Event(content=types.Content(role="model", parts=[types.Part.from_text(text=text)]))

# ── Node 1: init_db (HITL) ───────────────────────────────────────
@node(rerun_on_resume=True)
async def init_db(ctx: Context, node_input: Any = None):
    """Khởi tạo SQLite DB và hỏi tên user nếu chưa có."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profile (
        id          INTEGER PRIMARY KEY DEFAULT 1,
        user_name   TEXT    NOT NULL DEFAULT 'bạn',
        created_at  TEXT    NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS session_history (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        date        TEXT NOT NULL,
        mood        TEXT,
        weather     TEXT,
        temp_c      REAL,
        meal_id     TEXT,
        meal_name   TEXT,
        budget      TEXT,
        group_size  TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diary (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        date        TEXT NOT NULL,
        mood        TEXT,
        weather     TEXT,
        temp_c      REAL,
        meal_name   TEXT,
        entry       TEXT NOT NULL
    );
    """)
    conn.commit()
    
    cursor.execute("SELECT user_name FROM user_profile LIMIT 1")
    row = cursor.fetchone()
    
    if not row:
        if not ctx.resume_inputs or "ask_user_name" not in ctx.resume_inputs:
            conn.close()
            msg = "Butler: Welcome! What's your name?"
            # Include payload/response_scheme if they exist, or empty defaults
            yield Event(
                content=types.Content(role="model", parts=[types.Part.from_text(text=msg)]),
                output={
                    "payload": ctx.state.get("payload", {}),
                    "response_scheme": ctx.state.get("response_scheme", {})
                }
            )
            yield RequestInput(interrupt_id="ask_user_name", message=msg)
            return
        
        user_name = ctx.resume_inputs.get("ask_user_name", "").strip()
        if not user_name:
            user_name = DEFAULT_USER_NAME
            
        cursor.execute("INSERT OR REPLACE INTO user_profile (id, user_name, created_at) VALUES (1, ?, ?)", 
                       (user_name, datetime.date.today().isoformat()))
        conn.commit()
    else:
        user_name = row[0]
        
    conn.close()
    yield Event(output={"user_name": user_name}, state={"user_name": user_name})

# ── Node 2: load_history_via_mcp ────────────────────────────────
@node
async def load_history_via_mcp(ctx: Context, node_input: dict):
    """Gọi MCP tool get_history_summary để lấy lịch sử ăn uống gần đây."""
    try:
        mcp = get_mcp_toolset()
        if mcp:
            tools = await mcp.get_tools()
            tool_map = {t.name: t for t in tools}
            summary_tool = tool_map.get("get_history_summary")
            if summary_tool:
                history = await summary_tool.run_async(args={"days": 7}, tool_context=None)
            else:
                history = {}
        else:
            history = {}
    except Exception:
        history = {}
        
    yield Event(output={"history": history}, state={"history": history})

# ── Node 3: fetch_weather ───────────────────────────────────────
WEATHER_MAP = {
    0:  ("sunny", "sunny"),
    1:  ("clear", "sunny"),
    2:  ("partly cloudy", "cloudy"),
    3:  ("mostly cloudy", "cloudy"),
    45: ("foggy", "cloudy"),
    48: ("foggy", "cloudy"),
    51: ("light drizzle", "rainy"),
    53: ("drizzle", "rainy"),
    55: ("heavy drizzle", "rainy"),
    61: ("light rain", "rainy"),
    63: ("moderate rain", "rainy"),
    65: ("heavy rain", "rainy"),
    80: ("rain showers", "rainy"),
    81: ("moderate rain showers", "rainy"),
    82: ("heavy rain showers", "rainy"),
    95: ("thunderstorm", "rainy"),
    99: ("thunderstorm with hail", "rainy"),
}

@node
async def fetch_weather(ctx: Context, node_input: dict):
    """Lấy thời tiết thật theo toạ độ thông qua Open-Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": DEFAULT_LAT,
        "longitude": DEFAULT_LON,
        "current": "temperature_2m,weather_code"
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, timeout=5.0)
            data = resp.json()
            current = data.get("current", {})
            temp_c = current.get("temperature_2m", 28.0)
            code = current.get("weather_code", current.get("weathercode", 2))
    except Exception:
        temp_c = 28.0
        code = 2
        
    desc, tag = WEATHER_MAP.get(code, ("không rõ", "mát"))
    weather_output = {"weather_desc": desc, "temp_c": temp_c, "weather_tag": tag}
    yield Event(output=weather_output, state=weather_output)

# ── Node 4: butler_interview (HITL) ──────────────────────────────
@node(rerun_on_resume=True)
async def butler_interview(ctx: Context, node_input: dict):
    """Chat freely OR start /dailyfood for food recommendations"""
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
        greeting += "📋 When you're ready for personalized food recommendations, type: **/dailyfood**\n\n"
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
    
    # CHECK IF USER WANTS INTERVIEW (via /dailyfood command)
    if user_message.lower() == "/dailyfood" or user_message.lower().startswith("/dailyfood"):
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
        
        # Clean up interview state is not necessary - keys will be overwritten on next /dailyfood
        # Note: State object doesn't support del or pop, so we just leave them (they persist harmlessly)
        
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
            "raw_user_input": user_message,
            "use_mood_service": False
        }
        yield Event(output=interview_result, state=interview_result)
    elif user_message.lower().startswith("/goal "):
        # DIRECT MOOD INPUT: /goal happy, /goal sad, "I am tired", etc.
        # Extract mood after /goal command
        mood_input = user_message[6:].strip()  # Remove "/goal " prefix
        
        # Pass directly to llm_suggest with use_mood_service flag
        direct_result = {
            "mood": mood_input,
            "craving": "any",
            "group": "solo",
            "budget": "moderate",
            "time": "normal",
            "diet": "none",
            "raw_interview": mood_input,
            "raw_user_input": mood_input,
            "use_mood_service": True  # CRITICAL: Flag to use mood_service
        }
        print(f"🎯 Direct mood detected: {mood_input}")
        yield Event(output=direct_result, state=direct_result)
    else:
        # AUTO-DETECT EMOTION from natural language (e.g., "i am tired")
        detected_emotion = detect_emotion(user_message)
        
        if detected_emotion:
            # EMOTION DETECTED: Use mood_service directly
            print(f"🎯 Emotion detected: {detected_emotion}")
            
            direct_result = {
                "mood": detected_emotion,
                "craving": "any",
                "group": "solo",
                "budget": "moderate",
                "time": "normal",
                "diet": "none",
                "raw_interview": user_message,
                "raw_user_input": user_message,
                "use_mood_service": True  # CRITICAL: Flag to use mood_service
            }
            yield Event(output=direct_result, state=direct_result)
        else:
            # NO EMOTION DETECTED: Acknowledge and offer options
            response = f"🤔 Got it! You said: '{user_message}'\n\n"
            response += "💡 Tips:\n"
            response += "  • Just tell me how you're feeling (e.g., 'I'm tired', 'I'm happy')\n"
            response += "  • Type **/dailyfood** for a full interview with questions\n"
            response += "  • Type **/goal <mood>** for instant suggestions\n"
            print(response)
            yield Event(content=types.Content(role="model", parts=[types.Part.from_text(text=response)]))
            
            # Ask again for next input
            yield RequestInput(
                interrupt_id="user_message",
                message="How are you feeling? Or type /dailyfood or /goal <mood>..."
            )

# ── Node 5: security_check ───────────────────────────────────────
def check_injection(text):
    """Check for prompt injection patterns"""
    if not text:
        return False
    patterns = [
        r"ignore.*previous.*instruction",
        r"forget.*your.*role",
        r"system.*prompt",
    ]
    import re
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

@node
def security_check(ctx: Context, node_input: dict):
    """Kiểm tra xem dữ liệu phỏng vấn có chứa prompt injection không."""
    raw_interview = node_input.get("raw_interview", "")
    if check_injection(raw_interview):
        return Event(output=node_input, route="flagged")
    return Event(output=node_input, route="clean")

# ── Node: flag_and_stop ──────────────────────────────────────────
@node
def flag_and_stop(ctx: Context, node_input: dict):
    """Xử lý khi phát hiện prompt injection, in thông báo và dừng."""
    # CRITICAL: Extract payload/response_scheme from ctx.state (survives RequestInput)
    payload_from_state = ctx.state.get("payload", {})
    response_scheme_from_state = ctx.state.get("response_scheme", {})
    
    msg = """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Butler: I'm sorry, I didn't quite catch that.
    Tell me how you're feeling and what
    you're craving — I'm here to help!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    print(msg)
    # PRESERVE payload and response_scheme from ctx.state even when flagged
    return Event(
        content=types.Content(role="model", parts=[types.Part.from_text(text=msg)]),
        output={
            "status": "flagged",
            "payload": payload_from_state,
            "response_scheme": response_scheme_from_state
        }
    )

# ── Node 6: llm_suggest ──────────────────────────────────────────
@node
async def llm_suggest(ctx: Context, node_input: dict):
    """Smart meal suggestion: MCP or mood_service (for direct emotion input)"""
    # CRITICAL: Extract payload/response_scheme from ctx.state (survives RequestInput)
    payload_from_state = ctx.state.get("payload", {})
    response_scheme_from_state = ctx.state.get("response_scheme", {})
    
    if ctx.state.get("chosen_meal"):
        yield Event(
            output={
                "suggestions": [ctx.state.get("chosen_meal")],
                "payload": payload_from_state,
                "response_scheme": response_scheme_from_state
            }, 
            state={"suggestions": [ctx.state.get("chosen_meal")]}
        )
        return
    mood = node_input.get("mood")
    craving = node_input.get("craving")
    weather_tag = ctx.state.get("weather_tag", "mát")
    budget = node_input.get("budget")
    group = node_input.get("group")
    time_available = node_input.get("time")
    diet = node_input.get("diet")
    use_mood_service = node_input.get("use_mood_service", False)  # NEW: Direct emotion flag
    raw_user_input = node_input.get("raw_user_input", "")
    
    # CHECK FOR /dailyfood COMMAND - bypass Gemini, use mood_service directly
    chat_history = ctx.state.get("chat_history", [])
    last_message = ""
    if chat_history:
        last_message = chat_history[-1].get("content", "").lower()
    
    is_dailyfood_command = "/dailyfood" in last_message or "/dailyfood" in raw_user_input.lower()
    
    history = ctx.state.get("history", {})
    exclude_ids = history.get("recent_meal_ids", [])
    
    suggestions = []
    
    # SHORTCUT: If user gave direct emotion input (e.g., "I am sad"), use mood_service immediately
    if use_mood_service and raw_user_input:
        try:
            mood_result = await mood_service.detect(raw_user_input)
            output_text = mood_result.get('conversation', '')
            
            recs = mood_result.get('recommendations', [])
            if recs:
                output_text += "\n\n👨‍🍳 Here are 9 meals I recommend for you:\n\n"
                for i, rec in enumerate(recs[:9], 1):
                    emoji = rec.get('emoji', '🍽️')
                    name = rec.get('name', '')
                    description = rec.get('description', '')
                    region = rec.get('region', 'Global')
                    health_tags = rec.get('health_tags', [])
                    mood_tags = rec.get('mood_tags', [])
                    tags_str = ''
                    if health_tags:
                        tags_str += ' '.join([f'#{tag}' for tag in health_tags[:2]])
                    if mood_tags:
                        if tags_str: tags_str += ' '
                        tags_str += ' '.join([f'@{tag}' for tag in mood_tags[:2]])
                    output_text += f"{i}. {emoji} {name} — {region}\n"
                    if description:
                        output_text += f"   {description}\n"
                    if tags_str:
                        output_text += f"   {tags_str}\n"
                    output_text += "\n"
            else:
                output_text += "\n\n💡 Tell me more!"
            
            output_text += "\n\n(Type 1-9 to pick, or tell me more)"
            print(output_text)
            # CRITICAL: Store recommendations in suggestions so human_pick can access them
            suggestions = recs  # ← FIX: Store recs in suggestions
            ctx.state["suggestions"] = suggestions  # ← FIX: Also store in ctx.state
            
            # PRESERVE payload and response_scheme from ctx.state
            yield Event(
                content=types.Content(role="model", parts=[types.Part.from_text(text=output_text)]),
                output={
                    "suggestions": suggestions,  # ← FIX: Pass recs, not empty
                    "use_mood_service": True,
                    "payload": payload_from_state,
                    "response_scheme": response_scheme_from_state
                },
                state={
                    "suggestions": suggestions,  # ← FIX: Pass recs, not empty
                    "use_mood_service": True
                }
            )
            return
        except Exception as e:
            print(f"Mood service error: {e}")
    
    # NORMAL PATH: Try MCP first
    # TEMPORARY WORKAROUND: Skip MCP due to TaskGroup errors, use mood_service directly
    mcp_enabled = False  # Set to False to bypass MCP temporarily
    
    if mcp_enabled:
        try:
            mcp = get_mcp_toolset()
            if mcp:
                tools = await mcp.get_tools()
                tool_map = {t.name: t for t in tools}
                search_tool = tool_map.get("search_meals")
                if search_tool:
                    suggestions = await search_tool.run_async(
                        args={
                            "mood": mood,
                            "craving": craving,
                            "weather": weather_tag,
                            "budget": budget,
                            "group": group,
                            "time_available": time_available,
                            "diet": diet,
                            "exclude_ids": exclude_ids
                        },
                        tool_context=None
                    )
        except Exception as e:
            print(f"⚠️  MCP connection failed: {e}")
            print(f"💡 Falling back to mood_service (MCP disabled: {mcp_enabled})")
    
    # FALLBACK 1: Skip MCP retry (disabled), go directly to mood_service
    
    # FALLBACK 2: Use mood_service as primary (MCP is disabled)
    if not suggestions:
        try:
            # Convert mood keyword to natural language for mood_service detection
            if mood and mood != "tell me more":
                user_input = f"I am {mood}"  # Convert "sad" → "I am sad"
            else:
                user_input = craving or mood or "tell me more"
            
            mood_result = await mood_service.detect(user_input)
            output_text = mood_result.get('conversation', '')
            
            # BUG FIX #3: Validate recommendations is a list (not None/string)
            recs = mood_result.get('recommendations', [])
            if recs is None:
                recs = []
            elif not isinstance(recs, list):
                print(f"WARNING: recommendations is {type(recs).__name__}, converting to []")
                recs = []
            
            suggestions = recs  # CRITICAL: Assign recommendations to suggestions variable
            if recs:
                output_text += "\n\n👨‍🍳 Here are some meals I recommend:\n\n"
                for i, rec in enumerate(recs[:5], 1):
                    # BUG FIX #1-2: Check for None meal and empty meal objects
                    if rec is None or not isinstance(rec, dict):
                        print(f"WARNING: Skipping invalid meal: {rec}")
                        continue
                    
                    if not rec:  # Empty dict
                        print(f"WARNING: Skipping empty meal dict")
                        continue
                    
                    # BUG FIX: Extract with fallbacks and prefer 'name' over 'name_en'
                    emoji = rec.get('emoji', '🍽️')
                    name = rec.get('name') or rec.get('name_en', '')
                    if not name:
                        print(f"WARNING: Meal has no name, skipping: {rec}")
                        continue
                    
                    description = rec.get('description') or rec.get('description_en', '')
                    region = rec.get('region') or rec.get('region_en', 'Global')
                    health_tags = rec.get('health_tags', [])
                    mood_tags = rec.get('mood_tags', [])
                    tags_str = ''
                    if health_tags:
                        tags_str += ' '.join([f'#{tag}' for tag in health_tags[:2]])
                    if mood_tags:
                        if tags_str: tags_str += ' '
                        tags_str += ' '.join([f'@{tag}' for tag in mood_tags[:2]])
                    output_text += f"{i}. {emoji} {name} — {region}\n"
                    if description:
                        output_text += f"   {description}\n"
                    if tags_str:
                        output_text += f"   {tags_str}\n"
                    output_text += "\n"
            else:
                output_text += "\n\n💡 Tell me more about what you're craving!"
            
            output_text += "\n\n(1/2/3 or tell me more)"
        except Exception as e:
            print(f"Fallback error: {e}")
            output_text = "I'm here to help. Tell me how you're feeling!\n\n(Vietnamese classics: Phở, Cơm Tấm, Bún Chả)"
    else:
        # Format output with emotional intro and rich descriptions (MCP path)
        emotional_intro = format_emotional_intro(mood, DEFAULT_LANGUAGE)
        output_text = f"{emotional_intro}\n\n👨‍🍳 Here are 3 delicious options I've chosen for you today:\n\n"
        
        for i, s in enumerate(suggestions, 1):
            emoji = s.get('emoji', '🍽️')
            name = s.get('name_en', s.get('name', ''))
            region = s.get('region_en', s.get('region', 'Global'))
            description = s.get('description_en', s.get('description', ''))
            b_name = "Budget" if s.get("budget") == "cheap" else ("Moderate" if s.get("budget") == "medium" else "Splurge")
            t_name = "Quick" if s.get("time_required") == "fast" else ("Normal" if s.get("time_required") == "normal" else "Leisurely")
            restaurants = s.get("restaurant_suggestions", [])
            rest_text = " • ".join([r.get("name", "") for r in restaurants[:2]]) if restaurants else "Check nearby"
            
            health_tags = s.get('health_tags', [])
            mood_tags = s.get('mood_tags', [])
            tags_str = ''
            if health_tags:
                tags_str += ' '.join([f'#{tag}' for tag in health_tags])
            if mood_tags:
                if tags_str: tags_str += ' '
                tags_str += ' '.join([f'@{tag}' for tag in mood_tags])
            
            output_text += f"{i}. {emoji} {name} — {region}\n"
            output_text += f"   {description}\n"
            if tags_str:
                output_text += f"   🏷️ {tags_str}\n"
            output_text += f"   [{b_name}] • [{t_name}] • {rest_text}\n\n"
        
        output_text += "💡 Which one appeals to you? (1/2/3)"
    print(output_text)
    # CRITICAL: Must set ctx.state DIRECTLY so human_pick can access it
    ctx.state["suggestions"] = suggestions
    # PRESERVE payload and response_scheme from ctx.state
    payload_from_state = ctx.state.get("payload", {})
    response_scheme_from_state = ctx.state.get("response_scheme", {})
    
    yield Event(
        content=types.Content(role="model", parts=[types.Part.from_text(text=output_text)]),
        output={
            "suggestions": suggestions,
            "payload": payload_from_state,
            "response_scheme": response_scheme_from_state
        },
        state={
            "suggestions": suggestions,
            "payload": payload_from_state,
            "response_scheme": response_scheme_from_state
        }
    )

# ── Node 7: human_pick (HITL) ────────────────────────────────────
@node(rerun_on_resume=True)
async def human_pick(ctx: Context, node_input: dict):
    """Cho phép người dùng chọn 1 trong 3 món ăn gợi ý."""
    # CRITICAL: Extract payload/response_scheme from ctx.state (survives RequestInput)
    payload_from_state = ctx.state.get("payload", {})
    response_scheme_from_state = ctx.state.get("response_scheme", {})
    
    chosen_meal = ctx.state.get("chosen_meal", {})
    if chosen_meal and (chosen_meal.get("name_en") or chosen_meal.get("name_vi") or chosen_meal.get("name") or chosen_meal.get("id")):  # Only skip if user already picked (has id)
        yield Event(
            output={
                "chosen_meal": chosen_meal,
                "payload": payload_from_state,
                "response_scheme": response_scheme_from_state
            }, 
            state={"chosen_meal": chosen_meal}
        )
        return
    suggestions = ctx.state.get("suggestions", [])
    if not suggestions:
        # No suggestions available - show error and ask user to continue conversation
        msg = "Bếp: I couldn't generate meal suggestions. Let's continue our conversation! Tell me more about what you're craving."
        yield Event(
            content=types.Content(role="model", parts=[types.Part.from_text(text=msg)]),
            output={
                "payload": payload_from_state,
                "response_scheme": response_scheme_from_state
            }
        )
        yield RequestInput(interrupt_id="user_message", message="Talk to your chef..."
)
        return
        
    retries = ctx.state.get("pick_retries", 0)
    int_id = f"chosen_idx_{retries}"
    
    if not ctx.resume_inputs or int_id not in ctx.resume_inputs:
        msg = "Bếp: Bạn chọn món nào? (1/2/3)" if retries == 0 else "Bếp: Lựa chọn không hợp lệ. Vui lòng chọn 1, 2, hoặc 3:"
        # CRITICAL: Include payload/response_scheme in output BEFORE RequestInput
        yield Event(
            content=types.Content(role="model", parts=[types.Part.from_text(text=msg)]),
            output={
                "payload": payload_from_state,
                "response_scheme": response_scheme_from_state
            }
        )
        yield RequestInput(interrupt_id=int_id, message=msg)
        return
        
    choice_val = ctx.resume_inputs.get(int_id)
    if choice_val is None or (isinstance(choice_val, str) and choice_val.strip() == ""):
        msg = "Bếp: Bạn chọn món nào? (1/2/3)" if retries == 0 else "Bếp: Lựa chọn không hợp lệ. Vui lòng chọn 1, 2, hoặc 3:"
        # CRITICAL: Include payload/response_scheme in output BEFORE RequestInput
        yield Event(
            content=types.Content(role="model", parts=[types.Part.from_text(text=msg)]),
            output={
                "payload": payload_from_state,
                "response_scheme": response_scheme_from_state
            }
        )
        yield RequestInput(interrupt_id=int_id, message=msg)
        return
    
    choice = str(choice_val).strip()  # Safe conversion
    if choice in ["1", "2", "3"]:
        idx = int(choice) - 1
    else:
        if retries < 2:
            next_id = f"chosen_idx_{retries + 1}"
            ctx.state["pick_retries"] = retries + 1
            msg = "Bếp: Lựa chọn không hợp lệ. Vui lòng chọn 1, 2, hoặc 3:"
            # CRITICAL: Include payload/response_scheme in output BEFORE RequestInput
            yield Event(
                content=types.Content(role="model", parts=[types.Part.from_text(text=msg)]),
                output={
                    "payload": payload_from_state,
                    "response_scheme": response_scheme_from_state
                }
            )
            yield RequestInput(interrupt_id=next_id, message=msg)
            return
        else:
            # Too many invalid attempts - ask user to try again
            msg = "Bếp: I need you to choose one. Please enter 1, 2, or 3:\n\n1. " + suggestions[0].get('name', 'Meal 1') + "\n2. " + suggestions[1].get('name', 'Meal 2') + "\n3. " + suggestions[2].get('name', 'Meal 3')
            yield Event(
                content=types.Content(role="model", parts=[types.Part.from_text(text=msg)]),
                output={
                    "payload": payload_from_state,
                    "response_scheme": response_scheme_from_state
                }
            )
            # Reset retries and ask again
            ctx.state["pick_retries"] = 0
            yield RequestInput(interrupt_id="chosen_idx_0", message=msg)
            return
    
    # Valid choice - proceed
    chosen_meal = suggestions[idx] if idx < len(suggestions) else suggestions[0]
    
    # DEFENSIVE: Ensure chosen_meal is a valid meal object (has name, not empty)
    if not chosen_meal or not (chosen_meal.get("name_en") or chosen_meal.get("name_vi") or chosen_meal.get("name")):
        # Fallback: show error and ask user to try again
        msg = "Bếp: I need you to choose a valid meal. Please try again: (1/2/3)"
        yield Event(
            content=types.Content(role="model", parts=[types.Part.from_text(text=msg)]),
            output={
                "payload": payload_from_state,
                "response_scheme": response_scheme_from_state
            }
        )
        ctx.state["pick_retries"] = 0
        yield RequestInput(interrupt_id="chosen_idx_0", message=msg)
        return
    # PRESERVE payload and response_scheme from ctx.state
    yield Event(
        output={
            "chosen_meal": chosen_meal,
            "payload": payload_from_state,
            "response_scheme": response_scheme_from_state
        }, 
        state={"chosen_meal": chosen_meal}
    )

# ── Node 8: generate_output ──────────────────────────────────────
@node
def generate_output(ctx: Context, node_input: dict):
    """Display meal details with description, ingredients, and restaurant suggestions."""
    # CRITICAL: Try node_input first, then fallback to ctx.state (like other nodes do)
    chosen_meal = node_input.get("chosen_meal") or ctx.state.get("chosen_meal", {})
    mood = ctx.state.get("mood", "neutral")
    
    emoji = chosen_meal.get('emoji', '🍽️')
    name = chosen_meal.get('name_en') or chosen_meal.get('name_vi') or chosen_meal.get('name', '')
    region = chosen_meal.get('region_en', chosen_meal.get('region', 'Global'))
    description = chosen_meal.get('description_en', chosen_meal.get('description', ''))
    
    ingredients_str = ""
    ingredients = chosen_meal.get("ingredients", [])
    if ingredients:
        for ing in ingredients:
            ingredients_str += f"   • {ing}\n"
    else:
        ingredients_str = "   • Check online recipe or ask a local chef!\n"
    
    restaurants_str = ""
    restaurants = chosen_meal.get("restaurant_suggestions", [])
    if restaurants:
        for r in restaurants[:3]:
            restaurants_str += f"   • {r.get('name')} ({r.get('type')})\n"
    else:
        restaurants_str = "   • Local restaurants • Food delivery apps • Try nearby!\n"
    
    # Add emotional closing
    emotional_closing = format_emotional_closing(mood, DEFAULT_LANGUAGE)
    
    msg = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{emoji} {name} — {region}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{description}

📝 Ingredients you'll need:
{ingredients_str}
🍴 You can find this at:
{restaurants_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{emotional_closing}
"""
    print(msg)
    # CRITICAL: Preserve payload/response_scheme + pass chosen_meal through
    payload_from_state = ctx.state.get("payload", {})
    response_scheme_from_state = ctx.state.get("response_scheme", {})
    
    return Event(
        content=types.Content(role="model", parts=[types.Part.from_text(text=msg)]),
        output={
            "chosen_meal": chosen_meal,
            "payload": payload_from_state,
            "response_scheme": response_scheme_from_state
        }
    )

# ── Node 9: write_diary_entry ────────────────────────────────────
@node
async def write_diary_entry(ctx: Context, node_input: dict):
    """Use Gemini to generate diary entry with emotional wellness and health insights."""
    # CRITICAL: Extract payload/response_scheme from ctx.state (survives RequestInput)
    payload_from_state = ctx.state.get("payload", {})
    response_scheme_from_state = ctx.state.get("response_scheme", {})
    # CRITICAL: Try node_input first, then fallback to ctx.state
    chosen_meal = node_input.get("chosen_meal") or ctx.state.get("chosen_meal", {})
    
    # BUG FIX #9: Handle missing meal name with multiple fallbacks
    meal_name = (
        chosen_meal.get("name_en") or 
        chosen_meal.get("name_vi") or 
        chosen_meal.get("name") or
        chosen_meal.get("emoji_name") or
        "một món ăn"  # Final fallback if all keys missing
    )
    # Strip if string, otherwise convert to string
    if isinstance(meal_name, str):
        meal_name = meal_name.strip()
    else:
        meal_name = "một món ăn"
    
    user_name = ctx.state.get("user_name", "bạn")
    mood = ctx.state.get("mood", "bình thường")
    weather_desc = ctx.state.get("weather_desc", "không rõ")
    temp_c = ctx.state.get("temp_c", 28.0)
    
    history = ctx.state.get("history", {})
    recent_meals = history.get("recent_meal_names", [])
    favorite_mood = history.get("favorite_mood", "")
    total_sessions = history.get("total_sessions", 0)
    
    # UPGRADED: Pattern analysis + health awareness
    if recent_meals.count(meal_name) >= 2:
        pattern_note = f"Đây là lần thứ {recent_meals.count(meal_name)} {user_name} chọn {meal_name} gần đây."
    elif recent_meals.count(meal_name) == 1:
        pattern_note = f"{user_name} đã chọn {meal_name} 1 lần gần đây — có vẻ đây là món comfort food."
    else:
        pattern_note = f"Lần đầu {user_name} thử {meal_name}."
    
    # Add health note if pattern detected
    health_note = ""
    if total_sessions > 5:
        crunchy_count = sum(1 for m in recent_meals if any(x in m.lower() for x in ['giòn', 'nướng', 'chiên']))
        if crunchy_count >= 3:
            health_note = "Gợi ý sức khỏe: Bạn ăn nhiều đồ giòn gần đây, hôm sau thử gỏi hay canh nhẹ thế nào?"
        
        cay_count = sum(1 for m in recent_meals if any(x in m.lower() for x in ['cay', 'ớt', 'sa tế']))
        if cay_count >= 4:
            health_note = "💡 Lưu ý: Bạn ăn khá nhiều đồ cay. Nên cân bằng với những món thanh nhẹ để bảo vệ dạ dày."
        
    today = datetime.date.today().isoformat()
    
    prompt = build_diary_prompt(
        user_name=user_name,
        today=today,
        mood=mood,
        weather_desc=weather_desc,
        temp_c=temp_c,
        meal_name=meal_name,
        pattern_note=pattern_note
    )
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    try:
        response = await client.aio.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        diary_text = response.text.strip()
    except Exception as e:
        diary_text = f"Hôm nay {user_name} ăn {meal_name}. Thời tiết {weather_desc}, tâm trạng {mood}."
    
    # Empathetic Butler diary format with wellness insights
    diary_msg = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 {today}  |  ⛅ {weather_desc} {temp_c:.0f}°C  |  💭 {mood}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{chosen_meal.get('emoji', '🍽️')}  {meal_name}

"{diary_text}"
"""
    
    if health_note:
        diary_msg += f"\n{health_note}"
    
    diary_msg += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print(diary_msg)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO diary (date, mood, weather, temp_c, meal_name, entry) VALUES (?, ?, ?, ?, ?, ?)",
            (today, mood, weather_desc, temp_c, meal_name, diary_text)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Lỗi lưu nhật ký vào SQLite: {e}")
    
    yield Event(
        content=types.Content(role="model", parts=[types.Part.from_text(text=diary_msg)]),
        output={
            "diary_entry": diary_text,
            "payload": payload_from_state,
            "response_scheme": response_scheme_from_state
        },
        state={"diary_entry": diary_text}
    )

# ── Node 10: record_session ──────────────────────────────────────
@node
def record_session(ctx: Context, node_input: dict):
    """Ghi lại lịch sử session hoàn tất vào SQLite."""
    # CRITICAL: Extract payload/response_scheme from ctx.state (survives RequestInput)
    payload_from_state = ctx.state.get("payload", {})
    response_scheme_from_state = ctx.state.get("response_scheme", {})
    
    chosen_meal = ctx.state.get("chosen_meal", {})
    meal_id = chosen_meal.get("id")
    meal_name = chosen_meal.get("name")
    
    mood = ctx.state.get("mood")
    weather_desc = ctx.state.get("weather_desc")
    temp_c = ctx.state.get("temp_c")
    budget = ctx.state.get("budget")
    group_size = ctx.state.get("group")
    
    today = datetime.date.today().isoformat()
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO session_history (date, mood, weather, temp_c, meal_id, meal_name, budget, group_size) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (today, mood, weather_desc, temp_c, meal_id, meal_name, budget, group_size)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Lỗi ghi nhận session vào SQLite: {e}")
        
    msg = "Butler: Your meal has been saved 📝 Looking forward to our next conversation!"
    print(msg)
    # PRESERVE payload and response_scheme through final output
    return Event(
        content=types.Content(role="model", parts=[types.Part.from_text(text=msg)]),
        output={
            "status": "done",
            "payload": payload_from_state,
            "response_scheme": response_scheme_from_state
        }
    )

# ── Khởi dựng đồ thị Workflow ────────────────────────────────────
edges = [
    ('START', init_db),
    (init_db, load_history_via_mcp),
    (load_history_via_mcp, fetch_weather),
    (fetch_weather, butler_interview),
    (butler_interview, security_check),
    (security_check, {"clean": llm_suggest, "flagged": flag_and_stop}),
    (llm_suggest, human_pick),
    (human_pick, generate_output),
    (generate_output, write_diary_entry),
    (write_diary_entry, record_session),
    (record_session, butler_interview)  # ← FIX: Loop back for next conversation
]

root_agent = Workflow(
    name="bep_workflow",
    edges=edges,
)

app = App(
    root_agent=root_agent,
    name="mood_to_meal_butler",
    resumability_config=ResumabilityConfig(is_resumable=True)
)

async def _main():
    from google.adk.runners import InMemoryRunner
    runner = InMemoryRunner(app=app)
    session = await runner.session_service.create_session(
        app_name="mood_to_meal_butler", user_id="console_user"
    )
    
    # Run the workflow interactively via stdin/stdout
    print("Starting Empathetic Culinary Butler...")
    async for event in runner.run_async(
        user_id="console_user",
        session_id=session.id,
        new_message=types.Content(role="user", parts=[types.Part.from_text(text="hello")]),
    ):
        pass

if __name__ == "__main__":
    # Nhận chạy standalone trực tiếp
    asyncio.run(_main())
