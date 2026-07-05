# response_builder.py
# Build and format responses for users

"""
Response building utilities: format meals, emotions, situations
"""

def build_emotion_response(emotion: str, meals: list, situations: list = None) -> str:
    """
    Build complete emotion response with meals
    
    Args:
        emotion: Detected emotion
        meals: List of recommended meals
        situations: List of detected situations
        
    Returns:
        Formatted response string
    """
    from mood_to_meal_butler.emotions_config import EMOTION_METADATA
    from mood_to_meal_butler.meal_utilities import format_meal_for_display
    
    if not emotion or not meals:
        return "I'm here to help. Tell me what you're feeling!"
    
    # Get emotion metadata
    emotion_data = EMOTION_METADATA.get(emotion, {})
    emoji = emotion_data.get("emoji", "💚")
    greeting = emotion_data.get("greeting", "I hear you...")
    
    # Build response
    response = f"{emoji} {greeting}\n\n"
    response += "Here are my recommendations:\n\n"
    
    # Add meals (max 4)
    for idx, meal in enumerate(meals[:4], 1):
        response += format_meal_for_display(meal, idx)
        response += "\n"
    
    # Add situation context
    if situations:
        situation_str = ", ".join(situations)
        response += f"(Context detected: {situation_str})\n\n"
    
    response += "Which one sounds good to you?"
    
    return response

def build_situation_response(situations: list, meals: list) -> str:
    """
    Build response based on detected situations
    
    Args:
        situations: List of detected situations
        meals: List of recommended meals
        
    Returns:
        Formatted response string
    """
    from mood_to_meal_butler.situations_config import SITUATIONS
    from mood_to_meal_butler.meal_utilities import format_meal_for_display
    
    if not situations or not meals:
        return "Tell me more about what you'd like!"
    
    # Get first situation's emoji and greeting
    situation_key = situations[0]
    situation_data = SITUATIONS.get(situation_key, {})
    emoji = situation_data.get("emoji", "🍽️")
    greeting = situation_data.get("greeting", "Great choice!")
    
    # Build response
    response = f"{emoji} {greeting}\n\n"
    response += "Here are my suggestions:\n\n"
    
    # Add meals
    for idx, meal in enumerate(meals[:4], 1):
        response += format_meal_for_display(meal, idx)
        response += "\n"
    
    response += "(Type number 1-4 to select, or tell me more)"
    
    return response

def build_error_fallback() -> str:
    """
    Build generic fallback response when system fails
    
    Returns:
        Fallback message
    """
    return (
        "🤔 Let me think about that...\n\n"
        "I'm here to help you find the perfect meal.\n\n"
        "Try telling me:\n"
        "• How you're feeling (sad, happy, stressed)\n"
        "• Where you are (office, home)\n"
        "• Your preference (quick, budget, vegan)\n\n"
        "Example: 'I'm sad at office, need something quick'"
    )

def validate_response(response: str) -> bool:
    """
    Validate response meets quality standards
    
    Args:
        response: Response string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not response:
        return False
    
    if len(response) < 10:
        return False
    
    if len(response) > 2000:
        return False
    
    # Must have some emoji or formatting
    if emoji_count(response) < 1:
        return False
    
    return True

def emoji_count(text: str) -> int:
    """Count emoji in text"""
    # Simple emoji detection (emoji are Unicode 2+ bytes)
    count = 0
    for char in text:
        if ord(char) > 127:
            count += 1
    return count

def truncate_response(response: str, max_length: int = 1500) -> str:
    """
    Truncate response if too long
    
    Args:
        response: Response string
        max_length: Maximum length
        
    Returns:
        Truncated response
    """
    if len(response) <= max_length:
        return response
    
    # Truncate at word boundary
    truncated = response[:max_length]
    last_space = truncated.rfind(' ')
    if last_space > max_length - 100:
        truncated = truncated[:last_space]
    
    truncated += "\n\n...\n\n(Response truncated)"
    return truncated
