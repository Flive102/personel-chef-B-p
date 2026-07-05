#!/usr/bin/env python3
# mood_to_meal_butler/interview_enhancements.py
# Optional enhanced interview questions for energy and health goal tracking
# Can be integrated into main interview flow in Phase 2

OPTIONAL_QUESTIONS_EN = [
    {
        "key": "energy",
        "question": "Butler: How's your energy level today?",
        "hint": "(low / medium / high)",
        "keywords": {
            "low":    ["low", "tired", "exhausted", "drained", "no energy", "worn out"],
            "medium": ["medium", "okay", "normal", "average", "fair"],
            "high":   ["high", "energized", "energetic", "pumped", "great", "excellent"],
        },
        "default": "medium"
    },
    {
        "key": "health_goal",
        "question": "Butler: Any health goals for today?",
        "hint": "(protein / fiber / low-cal / balanced / none)",
        "keywords": {
            "protein":  ["protein", "muscle", "strength", "gains", "lean"],
            "fiber":    ["fiber", "digestion", "health", "vegetables"],
            "low_cal":  ["low calorie", "light", "diet", "weight", "slim"],
            "balanced": ["balanced", "nutrition", "healthy", "normal"],
            "none":     ["none", "no", "doesn't matter", "any"],
        },
        "default": "balanced"
    },
]

OPTIONAL_QUESTIONS_VI = [
    {
        "key": "energy",
        "question": "Bep: Muc nang luong cua ban hom nay the nao?",
        "hint": "(thap / trung binh / cao)",
        "keywords": {
            "thap":    ["thap", "met", "kiet suc", "khong suc"],
            "trung binh": ["trung binh", "binh thuong", "on", "binh"],
            "cao":     ["cao", "tran nang luong", "phan chan", "tuyet"],
        },
        "default": "trung binh"
    },
    {
        "key": "health_goal",
        "question": "Bep: Co muc tieu suc khoe nao hom nay khong?",
        "hint": "(dam / chat xo / it calo / can bang / khong)",
        "keywords": {
            "dam":    ["dam", "co bap", "suc manh"],
            "chat xo":   ["chat xo", "tieu hoa"],
            "it calo":  ["it calo", "nhe", "giam can"],
            "can bang": ["can bang", "dinh duong"],
            "khong":     ["khong", "tuy"],
        },
        "default": "can bang"
    },
]

def get_energy_based_meal_tags(energy_level: str) -> list:
    """Return meal mood tags that match user's energy level"""
    tags_map = {
        "low":    ["tired", "comfort", "light"],
        "medium": ["energized", "balanced", "normal"],
        "high":   ["celebration", "adventurous", "energized"]
    }
    return tags_map.get(energy_level, ["energized"])

def get_health_goal_meal_tags(health_goal: str) -> list:
    """Return meal health tags based on health goal"""
    tags_map = {
        "protein":  ["high-protein"],
        "fiber":    ["vegetable-rich"],
        "low_cal":  ["low-calorie"],
        "balanced": ["balanced-meal"],
        "none":     ["any"]
    }
    return tags_map.get(health_goal, ["any"])
