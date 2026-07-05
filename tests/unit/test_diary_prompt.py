# tests/unit/test_diary_prompt.py
# Test build_diary_prompt() function from mood_agent.interview

from mood_to_meal_butler.interview import build_diary_prompt

def test_does_not_contain_cliche_chuc_ngon_mieng():
    # Case 1: prompt output KHÔNG chứa cụm "chúc ngon miệng"
    prompt = build_diary_prompt(
        user_name="Alex",
        today="2026-06-22",
        mood="mệt mỏi",
        weather_desc="mưa nhẹ",
        temp_c=24.0,
        meal_name="Bún Bò Huế",
        pattern_note="Lần đầu Alex thử Bún Bò Huế."
    )
    assert "chúc ngon miệng" not in prompt.lower()

def test_does_not_contain_cliche_bon_appetit():
    # Case 2: prompt output KHÔNG chứa cụm "bon appétit"
    prompt = build_diary_prompt(
        user_name="Alex",
        today="2026-06-22",
        mood="mệt mỏi",
        weather_desc="mưa nhẹ",
        temp_c=24.0,
        meal_name="Bún Bò Huế",
        pattern_note="Lần đầu Alex thử Bún Bò Huế."
    )
    assert "bon appétit" not in prompt.lower()
    assert "bon appetit" not in prompt.lower()

def test_contains_pattern_note():
    # Case 3: nếu pattern_note có nội dung → prompt phải chứa pattern_note
    note = "Đây là lần thứ 3 Alex chọn Bún Bò Huế gần đây."
    prompt = build_diary_prompt(
        user_name="Alex",
        today="2026-06-22",
        mood="mệt mỏi",
        weather_desc="mưa nhẹ",
        temp_c=24.0,
        meal_name="Bún Bò Huế",
        pattern_note=note
    )
    assert note in prompt

