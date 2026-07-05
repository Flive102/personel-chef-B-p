# mcp_server/meals_server.py
import json
import sqlite3
import os
import datetime
from collections import Counter
from fastmcp import FastMCP
from mood_to_meal_butler.config import DB_PATH, MEALS_PATH, DEFAULT_LANGUAGE

mcp = FastMCP("Empathetic Culinary Butler Meals Server")

def _score_meal(meal: dict, mood: str, craving: str, weather: str,
                budget: str, group: str, time_available: str, diet: str) -> int:
    """
    Calculate compatibility score for a meal based on user context.
    Pure function: no side effects, doesn't read files or connect to DB.
    Used for unit testing in tests/unit/test_mcp_score.py
    """
    score = 0
    if mood        in meal.get("mood_tags", []):    score += 3
    if craving     in meal.get("craving_tags", []): score += 3
    if weather     in meal.get("weather_tags", []): score += 2
    if meal.get("budget") == budget:                score += 2
    if group       in meal.get("group_size", []):   score += 1
    if meal.get("time_required") == time_available: score += 1
    if diet        in meal.get("diet_ok", []):      score += 1
    return score

def _load_meals() -> list[dict]:
    """Load meals from global database."""
    if not os.path.exists(MEALS_PATH):
        return []
    with open(MEALS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("meals", [])

def _format_meal_response(meal: dict, language: str = "en") -> dict:
    """
    Format meal data for response, including localized fields and restaurant suggestions.
    """
    name_key = "name_en" if language == "en" else "name_vi"
    desc_key = "description_en" if language == "en" else "description_vi"
    
    return {
        "id": meal.get("id"),
        "name": meal.get(name_key, meal.get("name_en", "")),
        "description": meal.get(desc_key, meal.get("description_en", "")),
        "restaurant_suggestions": meal.get("restaurant_suggestions", []),
        "ingredients": meal.get("ingredients", []),
        "time_required": meal.get("time_required"),
        "budget": meal.get("budget"),
        "mood_tags": meal.get("mood_tags", []),
        "health_tags": meal.get("health_tags", []),
    }

@mcp.tool()
def search_meals(mood: str, craving: str, weather: str, budget: str,
                 group: str, time_available: str, diet: str,
                 exclude_ids: list[str], language: str = "en") -> list[dict]:
    """
    Search and score meals based on mood, flavor preference, weather, budget, time, and diet.
    Returns top 3 meals with restaurant suggestions in the specified language.
    """
    meals = _load_meals()
    scored_meals = []
    
    for meal in meals:
        if meal.get("id") in exclude_ids:
            continue
        
        score = _score_meal(
            meal=meal,
            mood=mood,
            craving=craving,
            weather=weather,
            budget=budget,
            group=group,
            time_available=time_available,
            diet=diet
        )
        
        # Only include meals with positive score
        if score > 0:
            meal_response = _format_meal_response(meal, language)
            meal_response["score"] = score
            scored_meals.append(meal_response)
    
    # Sort by score descending
    scored_meals.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top 3
    return scored_meals[:3]

@mcp.tool()
def get_meal_detail(meal_id: str, language: str = "en") -> dict:
    """
    Get detailed information for a specific meal by ID.
    Returns localized name, description, and restaurant suggestions.
    """
    meals = _load_meals()
    for meal in meals:
        if meal.get("id") == meal_id:
            return _format_meal_response(meal, language)
    return {"error": "Meal not found"}

@mcp.tool()
def get_history_summary(days: int = 7) -> dict:
    """
    Get summary of user's meal history for the specified number of days.
    Returns recent meals, last meal, favorite mood, and total sessions.
    """
    default_summary = {
        "user_name": "friend",
        "recent_meal_ids": [],
        "recent_meal_names": [],
        "last_meal_name": None,
        "last_meal_date": None,
        "favorite_mood": None,
        "total_sessions": 0
    }
    
    if not os.path.exists(DB_PATH):
        return default_summary
        
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get user name
        cursor.execute("SELECT user_name FROM user_profile LIMIT 1")
        user_row = cursor.fetchone()
        user_name = user_row["user_name"] if user_row else "friend"
        
        # Get total sessions count
        cursor.execute("SELECT COUNT(*) as count FROM session_history")
        total_sessions = cursor.fetchone()["count"]
        
        # Get recent meal history and find last meal
        cursor.execute("SELECT meal_id, meal_name, date, mood FROM session_history ORDER BY id DESC")
        all_sessions = [dict(row) for row in cursor.fetchall()]
        
        last_meal_name = None
        last_meal_date = None
        if all_sessions:
            last_meal_name = all_sessions[0]["meal_name"]
            last_meal_date = all_sessions[0]["date"]
            
        # Filter by number of recent days
        cutoff_date = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
        recent_sessions = [s for s in all_sessions if s["date"] >= cutoff_date]
        
        recent_meal_ids = [s["meal_id"] for s in recent_sessions if s["meal_id"]]
        recent_meal_names = [s["meal_name"] for s in recent_sessions if s["meal_name"]]
        
        # Find favorite mood from all history
        moods = [s["mood"] for s in all_sessions if s["mood"]]
        favorite_mood = None
        if moods:
            favorite_mood = Counter(moods).most_common(1)[0][0]
            
        conn.close()
        
        return {
            "user_name": user_name,
            "recent_meal_ids": recent_meal_ids,
            "recent_meal_names": recent_meal_names,
            "last_meal_name": last_meal_name,
            "last_meal_date": last_meal_date,
            "favorite_mood": favorite_mood,
            "total_sessions": total_sessions
        }
    except Exception:
        return default_summary

if __name__ == "__main__":
    mcp.run()

