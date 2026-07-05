# mood_agent/interview.py
# Empathetic Culinary Butler: Questions, greeting, wellness suggestions

# Default language: English. Vietnamese available as extension.
DEFAULT_LANGUAGE = "en"

INTERVIEW_QUESTIONS_EN = [
    {
        "key": "mood",
        "question": "Butler: How are you feeling today?",
        "hint": "(tired / happy / stressed / sad / neutral)",
        "keywords": {
            "tired":   ["tired", "exhausted", "worn out", "beat", "fatigued"],
            "happy":   ["happy", "great", "wonderful", "excellent", "amazing", "good"],
            "stressed": ["stressed", "anxious", "tense", "overwhelmed", "pressured"],
            "sad":     ["sad", "down", "blue", "upset", "depressed"],
            "neutral": ["okay", "fine", "alright", "neutral", "normal"],
        },
        "default": "neutral"
    },
    {
        "key": "craving",
        "question": "Butler: What kind of flavor are you craving?",
        "hint": "(spicy / sweet / light / rich / surprise me)",
        "keywords": {
            "spicy":   ["spicy", "hot", "kick", "fiery"],
            "sweet":   ["sweet", "dessert", "treat", "sugary"],
            "light":   ["light", "fresh", "healthy", "clean", "salad"],
            "rich":    ["rich", "comfort", "indulgent", "hearty", "creamy"],
            "surprise": ["surprise", "whatever", "you choose", "no idea"],
        },
        "default": "surprise"
    },
    {
        "key": "group",
        "question": "Butler: Dining alone or with others?",
        "hint": "(solo / couple / group / family)",
        "keywords": {
            "solo":    ["alone", "solo", "by myself", "one", "myself"],
            "couple":  ["two", "couple", "partner", "date", "with someone"],
            "group":   ["group", "friends", "team", "multiple people"],
            "family":  ["family", "kids", "parents", "relatives"],
        },
        "default": "solo"
    },
    {
        "key": "budget",
        "question": "Butler: What's your budget today?",
        "hint": "(budget / moderate / splurge)",
        "keywords": {
            "budget":   ["cheap", "budget", "inexpensive", "afford", "limited"],
            "moderate": ["moderate", "fair", "reasonable", "normal"],
            "splurge":  ["splurge", "expensive", "special", "treat", "indulge"],
        },
        "default": "moderate"
    },
    {
        "key": "time",
        "question": "Butler: How much time do you have?",
        "hint": "(quick / normal / unhurried)",
        "keywords": {
            "quick":   ["quick", "fast", "rush", "hurry", "5 minutes"],
            "normal":  ["normal", "medium", "average"],
            "slow":    ["slow", "time", "relax", "savor", "hours"],
        },
        "default": "normal"
    },
    {
        "key": "diet",
        "question": "Butler: Any dietary preferences or restrictions?",
        "hint": "(none / vegetarian / no seafood / no red meat)",
        "keywords": {
            "vegetarian": ["vegetarian", "vegan", "no meat"],
            "no_seafood": ["no seafood", "no fish", "shellfish allergy"],
            "no_red_meat": ["no red meat", "no beef", "no pork"],
            "none": ["none", "everything", "no restrictions"],
        },
        "default": "none"
    },
    # Optional questions for deeper personalization (used in /dailyfood mode)
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
            "low_cal":  ["low calorie", "light", "diet", "diet", "weight", "slim"],
            "balanced": ["balanced", "nutrition", "healthy", "balanced", "nutritious", "wholesome"],
            "none":     ["none", "no", "doesn't matter", "any"],
        },
        "default": "balanced"
    },
]

INTERVIEW_QUESTIONS_VI = [
    {
        "key": "mood",
        "question": "Bếp: Hôm nay bạn thấy thế nào?",
        "hint": "(mệt / vui / stress / buồn / bình thường)",
        "keywords": {
            "mệt mỏi":   ["mệt", "kiệt sức", "đuối", "mệt mỏi"],
            "vui vẻ":    ["vui", "tốt", "tuyệt", "ổn", "phấn"],
            "stress":    ["stress", "áp lực", "lo", "căng"],
            "buồn":      ["buồn", "chán", "uể oải", "không vui"],
            "bình thường": ["bình thường", "cũng được", "bình"],
        },
        "default": "bình thường"
    },
    {
        "key": "craving",
        "question": "Bếp: Đang thèm vị gì không?",
        "hint": "(cay / ngọt / thanh nhẹ / đậm đà / không biết)",
        "keywords": {
            "cay":       ["cay", "ớt", "nóng bỏng"],
            "ngọt":      ["ngọt", "chè", "tráng miệng"],
            "thanh nhẹ": ["nhẹ", "thanh", "mát", "salad", "gỏi"],
            "đậm đà":    ["đậm", "đậm đà", "béo", "ngậy", "mặn"],
            "không biết": ["không biết", "tùy", "gì cũng được", "không"],
        },
        "default": "không biết"
    },
    {
        "key": "group",
        "question": "Bếp: Ăn một mình hay có bạn bè / gia đình?",
        "hint": "(một mình / 2 người / nhóm bạn / gia đình)",
        "keywords": {
            "một mình":  ["một mình", "mình ơi", "solo", "1 mình"],
            "2 người":   ["2 người", "hai người", "với bạn", "với người yêu", "đôi"],
            "nhóm bạn":  ["nhóm", "bạn bè", "team", "hội", "mấy đứa"],
            "gia đình":  ["gia đình", "ba mẹ", "gia đình", "cả nhà", "con cái"],
        },
        "default": "một mình"
    },
    {
        "key": "budget",
        "question": "Bếp: Ngân sách hôm nay tầm bao nhiêu?",
        "hint": "(rẻ / vừa / thoải mái)",
        "keywords": {
            "rẻ":    ["rẻ", "ít tiền", "tiết kiệm", "bình dân"],
            "vừa":   ["vừa", "tạm", "tầm tầm"],
            "thoải mái": ["thoải mái", "không quan trọng", "tùy", "nhiều"],
        },
        "default": "vừa"
    },
    {
        "key": "time",
        "question": "Bếp: Bạn có nhiều thời gian không, hay cần nhanh?",
        "hint": "(nhanh / bình thường / thư thả)",
        "keywords": {
            "nhanh":   ["nhanh", "vội", "gấp", "15 phút", "ít thời gian"],
            "bình thường": ["bình thường", "tầm tầm", "vừa"],
            "thư thả":   ["thư thả", "từ từ", "không vội", "thoải mái", "nhiều giờ"],
        },
        "default": "bình thường"
    },
    {
        "key": "diet",
        "question": "Bếp: Có kiêng gì không? (chay, dị ứng...)",
        "hint": "(không kiêng / chay / không hải sản / không thịt đỏ)",
        "keywords": {
            "chay":            ["chay", "vegetarian", "vegan", "không thịt"],
            "không hải sản":   ["không hải sản", "dị ứng hải sản", "không cá", "không tôm"],
            "không thịt đỏ":   ["không thịt đỏ", "không bò", "không heo"],
            "không kiêng":     ["không", "bình thường", "ăn được hết", "không kiêng"],
        },
        "default": "không kiêng"
    },
    # Optional questions for deeper personalization (used in /dailyfood mode)
    {
        "key": "energy",
        "question": "Bếp: Mức năng lượng của bạn hôm nay thế nào?",
        "hint": "(thấp / trung bình / cao)",
        "keywords": {
            "thấp":    ["thấp", "mệt", "kiệt sức", "không sức"],
            "trung bình": ["trung bình", "bình thường", "ổn", "bình"],
            "cao":     ["cao", "tràn đầy năng lượng", "phấn chấn", "tuyệt"],
        },
        "default": "trung bình"
    },
    {
        "key": "health_goal",
        "question": "Bếp: Bạn có mục tiêu sức khỏe nào cho hôm nay không?",
        "hint": "(protein / chất xò / ít calo / cân bằng / không)",
        "keywords": {
            "protein":    ["protein", "cơ bắp", "sức mạnh", "thịt nạc"],
            "chất xò":    ["chất xò", "tiêu hoá", "rau củ", "trái cây"],
            "ít calo":    ["ít calo", "nhẹ", "giảm cân", "dinh dưỡng"],
            "cân bằng":   ["cân bằng", "dinh dưỡng", "phổ biến", "thông thường"],
            "không":      ["không", "không có", "gì cũng được", "bất kỳ"],
        },
        "default": "cân bằng"
    },
]

def get_interview_questions(language: str = "en"):
    """Get interview questions for specified language."""
    if language == "vi":
        return INTERVIEW_QUESTIONS_VI
    return INTERVIEW_QUESTIONS_EN

def parse_answer(raw_text: str, question_config: dict) -> str:
    """
    Map free-text user input to valid category value.
    Checks each keyword in the group.
    Returns the key of the first matching group.
    If no match: returns question_config["default"]
    """
    text = raw_text.lower().strip()
    for value, keywords in question_config["keywords"].items():
        if any(kw in text for kw in keywords):
            return value
    return question_config["default"]

def get_health_suggestion(mood: str, language: str = "en") -> str:
    """
    Empathetic Culinary Butler provides immediate wellness suggestion based on mood.
    Makes agent warm, caring, and responsive to user's emotional state.
    """
    suggestions_en = {
        "tired": "💧 I can tell you're tired. Let me suggest something light and energizing to help you recover. Good food + rest = you'll feel better!",
        "stressed": "🧘 You seem stressed today. Let me find something soothing and comforting to ease your mind. Sometimes the right meal is the best medicine.",
        "sad": "💚 When you're feeling down, good food can bring a little joy. Let me suggest something that might lift your spirits.",
        "happy": "🎉 Wonderful! I love your energy today. Let me find something special to celebrate this great mood!",
        "neutral": "👍 You're doing well. Let me find something delicious that matches your day perfectly.",
    }
    
    suggestions_vi = {
        "mệt mỏi": "💧 Gợi ý: Uống nước nhiều, ăn cái gì nhẹ để khỏe lại nhé. Nếu được thì nghỉ ngơi một chút!",
        "stress": "🧘 Nhận xét: Hôm nay bạn có vẻ căng thẳng. Hãy thử ăn cái gì thanh nhẹ, uống nước chanh tươi.",
        "buồn": "💚 Lời khuyên: Khi buồn, hãy ăn thứ gì đó yêu thích. Ăn chậm, tận hưởng từng miếng nhé.",
        "vui vẻ": "🎉 Tuyệt vời! Hôm nay bạn vui vẻ, thích thì tìm cái gì đó ngon hơn bình thường!",
        "bình thường": "👍 Okela, ta chọn cái gì phù hợp thôi!",
    }
    
    suggestions = suggestions_vi if language == "vi" else suggestions_en
    return suggestions.get(mood, "")

def build_diary_prompt(user_name: str, today: str, mood: str,
                        weather_desc: str, temp_c: float,
                        meal_name: str, pattern_note: str,
                        language: str = "en") -> str:
    """
    Build prompt for Gemini diary generation.
    Supports both English and Vietnamese with empathetic tone.
    """
    if language == "vi":
        return f"""Bạn là Bếp — người bạn thấu cảm của {user_name}.
Viết một đoạn nhật ký ngắn (3-4 câu, tiếng Việt, thân mật) ghi lại khoảnh khắc này:

- Ngày: {today}
- Tên: {user_name}
- Tâm trạng: {mood}
- Thời tiết: {weather_desc}, {temp_c:.0f}°C
- Món ăn: {meal_name}
- Ghi chú đặc biệt: {pattern_note}

QUAN TRỌNG — Bắt buộc tuân thủ:
1. Viết ở ngôi thứ 2 (dùng "{user_name}" hoặc "bạn")
2. Nếu ghi chú đặc biệt có nội dung, đề cập tự nhiên trong văn
3. KHÔNG dùng các cụm: "chúc_ngon_miệng", "hãy_tận_hưởng", "bon_appétit"
4. KHÔNG thêm tiêu đề, không giải thích, không bullet point
5. Viết như nhật ký thật — cảm xúc, không sáo rỗng
6. Chỉ output đoạn văn, không có gì khác"""
    
    return f"""You are the Empathetic Culinary Butler for {user_name}.
Write a brief diary entry (3-4 sentences in English, warm and personal) capturing this moment:

- Date: {today}
- Name: {user_name}
- Mood: {mood}
- Weather: {weather_desc}, {temp_c:.0f}°C
- Meal: {meal_name}
- Special note: {pattern_note}

IMPORTANT — Must follow these rules:
1. Write in second person (use "{user_name}" or "you")
2. If there's a special note, weave it naturally into the narrative
3. NO generic phrases like "bon_appétit", "enjoy your meal", "hope you love it"
4. NO title, explanation, or bullet points
5. Write like a real diary entry — genuine emotion, not flowery language
6. Output ONLY the diary paragraph, nothing else"""
