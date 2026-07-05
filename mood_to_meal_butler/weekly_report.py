# mood_agent/weekly_report.py
# CLI độc lập: đọc SQLite → sinh báo cáo tuần

import os
import sys
import sqlite3
import datetime
import textwrap
from collections import Counter
from google import genai

from mood_to_meal_butler.config import DB_PATH, GEMINI_API_KEY, MODEL_NAME, MEALS_PATH
from mood_to_meal_butler.interview import parse_answer
import json

# Đảm bảo in tiếng Việt chuẩn trên Windows terminal
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def build_weekly_prompt(summary_lines: str, fav_meal: str,
                         fav_mood: str, user_name: str) -> str:
    return f"""Dựa trên dữ liệu ăn uống 7 ngày của {user_name}:

{summary_lines}

Hãy viết Weekly Insight (5-7 câu, tiếng Việt, thân mật như người bạn):
1. Nhận xét tổng thể về pattern tâm trạng và lựa chọn món
2. 1 insight thú vị về mối liên hệ tâm trạng ↔ món ăn
3. Gợi ý 3 món chưa xuất hiện tuần này nhưng phù hợp với pattern

KHÔNG phán xét, KHÔNG sáo rỗng. Viết tự nhiên, ấm áp.
Chỉ output đoạn văn, không có tiêu đề hay bullet point."""

def load_meals_map():
    if not os.path.exists(MEALS_PATH):
        return {}
    try:
        with open(MEALS_PATH, "r", encoding="utf-8") as f:
            meals = json.load(f)
            return {m["name"]: m for m in meals}
    except Exception:
        return {}

def main():
    if not os.path.exists(DB_PATH):
        print("Chưa có dữ liệu")
        return
        
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 1. Đọc tên user
        cursor.execute("SELECT user_name FROM user_profile LIMIT 1")
        user_row = cursor.fetchone()
        user_name = user_row["user_name"] if user_row else "bạn"
        
        # 2. Đọc 7 rows mới nhất từ bảng diary
        cursor.execute("SELECT date, mood, weather, temp_c, meal_name, entry FROM diary ORDER BY date DESC LIMIT 7")
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
    except Exception as e:
        print(f"Lỗi truy vấn cơ sở dữ liệu: {e}")
        return
        
    if len(rows) < 1:
        print("Chưa đủ dữ liệu")
        return
        
    # Đảo ngược để theo thứ tự thời gian tăng dần khi phân tích
    rows.reverse()
    
    # 3. Tính toán thống kê
    meals_map = load_meals_map()
    
    meal_names = [r["meal_name"] for r in rows if r["meal_name"]]
    moods = [r["mood"] for r in rows if r["mood"]]
    
    fav_meal = Counter(meal_names).most_common(1)[0][0] if meal_names else "Không rõ"
    fav_mood = Counter(moods).most_common(1)[0][0] if moods else "Không rõ"
    
    # Xây dựng các dòng tóm tắt 7 ngày
    summary_lines = ""
    for r in rows:
        summary_lines += f"- Ngày {r['date']}: Ăn {r['meal_name']} khi cảm thấy {r['mood']}. Thời tiết {r['weather']}.\n"
        
    # 4. Gọi Gemini sinh insight
    prompt = build_weekly_prompt(
        summary_lines=summary_lines,
        fav_meal=fav_meal,
        fav_mood=fav_mood,
        user_name=user_name
    )
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        insight_text = response.text.strip()
    except Exception as e:
        insight_text = f"Bếp nhận thấy bạn {user_name} có xu hướng chọn những món ấm nóng khi thời tiết chuyển mát. Hãy giữ sức khỏe và cân đối dinh dưỡng nhé!"
        
    # 5. Format hiển thị report ra terminal
    week_start = rows[0]["date"]
    week_end = rows[-1]["date"]
    n_meals = len(rows)
    
    # In báo cáo theo khung viền chuẩn rộng 52 ký tự (khoảng cách bên trong là 46 ký tự)
    title = f"📊 TUẦN NÀY CỦA {user_name.upper()}"
    date_range = f"{week_start} -> {week_end}"
    
    # Helper to pad text with borders
    def print_border_line(content: str, align="left"):
        # Width inside border is 46 chars
        if align == "center":
            padded = content.center(46)
        else:
            padded = content.ljust(46)
        print(f"║  {padded}  ║")
        
    print("╔" + "═" * 50 + "╗")
    print_border_line(title, "center")
    print_border_line(date_range, "center")
    print("╠" + "═" * 50 + "╣")
    print_border_line(f"🍽️  Món ăn nhiều nhất:  {fav_meal}")
    print_border_line(f"💭  Tâm trạng thường:   {fav_mood}")
    print_border_line(f"📝  Số bữa đã ghi:      {n_meals} bữa")
    print("╠" + "═" * 50 + "╣")
    print_border_line("💡 NHẬN XÉT CỦA BẾP", "left")
    print("╠" + "═" * 50 + "╣")
    
    # Word wrap insight text to 46 characters
    wrapped_lines = textwrap.wrap(insight_text, width=46)
    for line in wrapped_lines:
        print_border_line(line)
        
    print("╚" + "═" * 50 + "╝")

if __name__ == "__main__":
    main()
