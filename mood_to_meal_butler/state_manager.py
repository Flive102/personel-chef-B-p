# state_manager.py
# Manage conversation state and user context

"""
State management: track emotion, situation, meals, choices across conversation
"""

class ConversationState:
    """Track conversation state across turns"""
    
    def __init__(self):
        self.emotion = None
        self.situations = []
        self.last_meals = []
        self.selected_meal = None
        self.turn_count = 0
        self.interaction_log = []
    
    def set_emotion(self, emotion: str):
        """Record detected emotion"""
        self.emotion = emotion
        self.log_interaction("emotion_detected", emotion)
    
    def set_situations(self, situations: list):
        """Record detected situations"""
        self.situations = situations
        self.log_interaction("situations_detected", situations)
    
    def set_meals(self, meals: list):
        """Record meal recommendations shown"""
        self.last_meals = meals
        meal_ids = [m.get("id") for m in meals]
        self.log_interaction("meals_suggested", meal_ids)
    
    def set_selected_meal(self, meal_id: str):
        """Record meal user selected"""
        self.selected_meal = meal_id
        self.log_interaction("meal_selected", meal_id)
    
    def log_interaction(self, event_type: str, data):
        """Log interaction for debugging"""
        import datetime
        timestamp = datetime.datetime.now().isoformat()
        
        self.interaction_log.append({
            "timestamp": timestamp,
            "event": event_type,
            "data": data
        })
        
        # Keep only last 50 interactions
        if len(self.interaction_log) > 50:
            self.interaction_log.pop(0)
    
    def get_context(self) -> dict:
        """Get current state as dict"""
        return {
            "emotion": self.emotion,
            "situations": self.situations,
            "last_meals": [m.get("id") for m in self.last_meals],
            "selected_meal": self.selected_meal,
            "turn_count": self.turn_count,
            "interactions": len(self.interaction_log)
        }
    
    def reset(self):
        """Reset state for new conversation"""
        self.emotion = None
        self.situations = []
        self.last_meals = []
        self.selected_meal = None
        self.turn_count = 0

def initialize_state(ctx_state: dict) -> ConversationState:
    """
    Initialize or load conversation state
    
    Args:
        ctx_state: Context state dict from agent
        
    Returns:
        ConversationState object
    """
    state = ConversationState()
    
    # Load from existing context if available
    if "mood_emotion" in ctx_state:
        state.emotion = ctx_state["mood_emotion"]
    
    if "mood_situations" in ctx_state:
        state.situations = ctx_state["mood_situations"]
    
    if "mood_selected_meal" in ctx_state:
        state.selected_meal = ctx_state["mood_selected_meal"]
    
    return state

def save_state(state: ConversationState, ctx_state: dict):
    """
    Save state back to context
    
    Args:
        state: ConversationState object
        ctx_state: Context state dict (modified in place)
    """
    ctx_state["mood_emotion"] = state.emotion
    ctx_state["mood_situations"] = state.situations
    ctx_state["mood_selected_meal"] = state.selected_meal

def should_ask_for_meal_selection(state: ConversationState) -> bool:
    """
    Determine if system should ask user to select meal
    
    Returns:
        True if user should pick a meal
    """
    return (
        state.emotion is not None and
        len(state.last_meals) > 0 and
        state.selected_meal is None
    )

def should_ask_for_more_info(state: ConversationState) -> bool:
    """
    Determine if system should ask for more information
    
    Returns:
        True if system needs more context
    """
    return (
        state.emotion is None and
        len(state.situations) == 0
    )
