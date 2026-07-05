#!/usr/bin/env python3
# mood_to_meal_butler/emotional_responses.py
# Human-like emotional responses based on mood for natural conversation

EMOTIONAL_RESPONSES_EN = {
    "tired": {
        "empathy": "I hear you—exhaustion can be draining. Let me find something nourishing that'll help you feel restored.",
        "food_note": "Something light but energizing will help lift your spirits.",
        "follow_up": "Take care of yourself. A good meal can work wonders."
    },
    "happy": {
        "empathy": "That's wonderful! Let's celebrate with something delicious!",
        "food_note": "Time to treat yourself to something special that matches your mood.",
        "follow_up": "Enjoy every bite—you deserve it!"
    },
    "stressed": {
        "empathy": "I know stress is tough. Sometimes a comforting meal is exactly what you need to decompress.",
        "food_note": "Let me suggest something soothing and satisfying to help you relax.",
        "follow_up": "Remember, taking a break to enjoy good food is self-care too."
    },
    "sad": {
        "empathy": "I'm sorry you're feeling down. A little comfort food and care might help brighten your day.",
        "food_note": "Let me find something warm and comforting to lift your mood.",
        "follow_up": "You're not alone. Sometimes good food and a moment for yourself can help."
    },
    "neutral": {
        "empathy": "Let's find something tasty for today!",
        "food_note": "I'll suggest some great options for any occasion.",
        "follow_up": "Hope you enjoy your meal!"
    }
}

EMOTIONAL_RESPONSES_VI = {
    "mệt mỏi": {
        "empathy": "Mình hiểu—mệt mỏi thực sự suy sụp. Để mình tìm một cái gì đó bổ dưỡng giúp bạn phục hồi.",
        "food_note": "Một cái gì đó nhẹ nhàng nhưng có năng lượng sẽ giúp bạn cảm thấy tốt hơn.",
        "follow_up": "Chăm sóc bản thân. Một bữa ăn tốt có thể thay đổi mọi thứ."
    },
    "vui vẻ": {
        "empathy": "Thật tuyệt vời! Hãy ăn mừng với một cái gì đó ngon lành!",
        "food_note": "Đó là lúc để tự thưởng cho mình cái gì đó đặc biệt.",
        "follow_up": "Hưởng thụ từng miếng—bạn xứng đáng được!"
    },
    "stress": {
        "empathy": "Mình biết stress khó khăn. Đôi khi một bữa ăn thoải mái chính xác là những gì bạn cần.",
        "food_note": "Hãy để mình gợi ý một cái gì đó dễ chịu và thỏa mãn.",
        "follow_up": "Nhớ rằng dành thời gian để thưởng thức đồ ăn ngon là tự chăm sóc bản thân."
    },
    "buồn": {
        "empathy": "Mình rất tiếc bạn cảm thấy buồn. Một chút ăn thoải mái có thể giúp bạn cảm thấy tốt hơn.",
        "food_note": "Hãy để mình tìm cái gì đó ấm áp và thoải mái để nâng cao tâm trạng của bạn.",
        "follow_up": "Bạn không đơn độc. Đôi khi đồ ăn ngon và một khoảnh khắc cho riêng mình có thể giúp."
    },
    "bình thường": {
        "empathy": "Tuyệt vời! Hãy tìm một cái gì đó ngon cho hôm nay!",
        "food_note": "Mình sẽ gợi ý một số tùy chọn tuyệt vời cho bất kỳ dịp nào.",
        "follow_up": "Mong bạn thích bữa ăn của mình!"
    }
}

def get_emotional_response(mood: str, language: str = "en") -> dict:
    """Get empathetic response based on mood and language."""
    responses = EMOTIONAL_RESPONSES_EN if language == "en" else EMOTIONAL_RESPONSES_VI
    return responses.get(mood, responses.get("neutral", {}))

def format_emotional_intro(mood: str, language: str = "en") -> str:
    """Format an empathetic introduction before meal suggestions."""
    response = get_emotional_response(mood, language)
    return response.get("empathy", "")

def format_emotional_closing(mood: str, language: str = "en") -> str:
    """Format a warm closing after meal selection."""
    response = get_emotional_response(mood, language)
    return response.get("follow_up", "")
