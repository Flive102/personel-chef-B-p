# tests/unit/test_mcp_score.py
# Test _score_meal() function from mcp_server.meals_server

from mcp_server.meals_server import _score_meal

def test_perfect_match():
    # Case 1: perfect match tất cả 7 chiều → score = 13
    # Weights: mood(3) + craving(3) + weather(2) + budget(2) + group(1) + time(1) + diet(1) = 13
    meal = {
        "mood_tags": ["mệt mỏi"],
        "craving_tags": ["cay"],
        "weather_tags": ["mưa"],
        "budget": "cheap",
        "group_size": ["một mình"],
        "time_required": "fast",
        "diet_ok": ["chay"]
    }
    score = _score_meal(
        meal=meal,
        mood="mệt mỏi",
        craving="cay",
        weather="mưa",
        budget="cheap",
        group="một mình",
        time_available="fast",
        diet="chay"
    )
    assert score == 13

def test_no_match():
    # Case 2: không match gì cả → score = 0
    meal = {
        "mood_tags": ["vui vẻ"],
        "craving_tags": ["ngọt"],
        "weather_tags": ["nắng"],
        "budget": "flexible",
        "group_size": ["nhóm bạn"],
        "time_required": "slow",
        "diet_ok": ["không thịt đỏ"]
    }
    score = _score_meal(
        meal=meal,
        mood="mệt mỏi",
        craving="cay",
        weather="mưa",
        budget="cheap",
        group="một mình",
        time_available="fast",
        diet="chay"
    )
    assert score == 0

def test_partial_match():
    # Case 3: match 3/7 chiều → score đúng với trọng số
    # Match: mood(3) + budget(2) + time(1) = 6
    meal = {
        "mood_tags": ["mệt mỏi"],
        "craving_tags": ["ngọt"],
        "weather_tags": ["nắng"],
        "budget": "cheap",
        "group_size": ["nhóm bạn"],
        "time_required": "fast",
        "diet_ok": ["không thịt đỏ"]
    }
    score = _score_meal(
        meal=meal,
        mood="mệt mỏi",
        craving="cay",
        weather="mưa",
        budget="cheap",
        group="một mình",
        time_available="fast",
        diet="chay"
    )
    assert score == 6
