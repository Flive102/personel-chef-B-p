# developer_api.py
# PHASE 3: Developer API Framework
# Allows easy extension by any developer

"""
MOOD-TO-MEAL-BUTLER: DEVELOPER API

This module provides clean interfaces for developers to extend the system
without modifying core code. Follow these patterns to add features.

EXTENSION POINTS:
  1. Custom Emotion Detector
  2. Custom Recommendation Logic
  3. Custom Meal Sourcing
  4. Custom Integrations
"""

from typing import List, Dict, Optional, Callable
from abc import ABC, abstractmethod


# ============================================================================
# EMOTION SYSTEM EXTENSION
# ============================================================================

class EmotionDetector(ABC):
    """
    Base class for emotion detection.
    Developers can subclass this to add custom emotion detection.
    
    Example:
        class MLEmotionDetector(EmotionDetector):
            def detect(self, text: str) -> Optional[str]:
                # Use ML model to detect emotion
                return emotion
    """
    
    @abstractmethod
    def detect(self, text: str, language: str = "en") -> Optional[str]:
        """
        Detect emotion from user input.
        
        Args:
            text: User message
            language: Language code (en, vi, etc.)
        
        Returns:
            Emotion category (e.g., "sadness") or None
        """
        pass


class KeywordEmotionDetector(EmotionDetector):
    """Default keyword-based emotion detector."""
    
    def __init__(self, keywords: Dict[str, str]):
        self.keywords = keywords
    
    def detect(self, text: str, language: str = "en") -> Optional[str]:
        text_lower = text.lower()
        sorted_kw = sorted(self.keywords.items(), key=lambda x: len(x[0]), reverse=True)
        for keyword, emotion in sorted_kw:
            if keyword in text_lower:
                return emotion
        return None


# ============================================================================
# RECOMMENDATION SYSTEM EXTENSION
# ============================================================================

class MealRecommender(ABC):
    """
    Base class for meal recommendation.
    Developers can subclass to implement custom recommendation logic.
    
    Example:
        class MLRecommender(MealRecommender):
            def recommend(self, context: RecommendationContext) -> List[Dict]:
                # Use ML to recommend meals
                return meals
    """
    
    @abstractmethod
    def recommend(self, context: 'RecommendationContext') -> List[Dict]:
        """
        Recommend meals based on context.
        
        Args:
            context: User context with emotion, situation, preferences
        
        Returns:
            List of recommended meals (sorted by relevance)
        """
        pass


class RecommendationContext:
    """Context for making recommendations."""
    
    def __init__(self):
        self.emotion: Optional[str] = None
        self.situation: Optional[str] = None
        self.time_available_min: Optional[int] = None
        self.budget: Optional[str] = None
        self.dietary: Optional[str] = None
        self.group_size: int = 1
        self.weather: Optional[str] = None
        self.user_history: List[str] = []  # IDs of previously selected meals
        self.preferences: Dict[str, any] = {}
    
    def to_dict(self) -> Dict:
        """Convert context to dictionary for logging/debugging."""
        return {
            "emotion": self.emotion,
            "situation": self.situation,
            "time_available_min": self.time_available_min,
            "budget": self.budget,
            "dietary": self.dietary,
            "group_size": self.group_size,
            "weather": self.weather,
            "user_history_count": len(self.user_history),
        }


class SimpleRecommender(MealRecommender):
    """Simple tag-based recommender."""
    
    def __init__(self, meals: List[Dict], emotion_metadata: Dict):
        self.meals = meals
        self.emotion_metadata = emotion_metadata
    
    def recommend(self, context: RecommendationContext) -> List[Dict]:
        if not context.emotion:
            return self.meals[:4]
        
        # Get meal filters for this emotion
        metadata = self.emotion_metadata.get(context.emotion, {})
        filters = metadata.get("meal_filters", [])
        
        # Filter meals by mood tags
        matches = []
        for meal in self.meals:
            if meal["id"] in context.user_history:
                continue  # Don't repeat
            
            mood_tags = meal.get("mood_tags", [])
            if any(f in str(mood_tags) for f in filters):
                matches.append(meal)
        
        # Return top 4, or fallback to all meals
        return matches[:4] if matches else self.meals[:4]


# ============================================================================
# MEAL SOURCING EXTENSION
# ============================================================================

class MealSource(ABC):
    """
    Base class for meal sourcing.
    Developers can extend to add restaurant/delivery integrations.
    
    Example:
        class UberEatsSource(MealSource):
            def get_restaurants(self, meal_id: str) -> List[Restaurant]:
                # Query UberEats API
                return restaurants
    """
    
    @abstractmethod
    def get_restaurants(self, meal_id: str, location: str) -> List[Dict]:
        """
        Get restaurants offering this meal.
        
        Returns:
            List of restaurants with price, rating, delivery_time
        """
        pass
    
    @abstractmethod
    def get_price(self, meal_id: str, restaurant_id: str) -> float:
        """Get price for meal at specific restaurant."""
        pass


# ============================================================================
# INTEGRATION SYSTEM
# ============================================================================

class Integration(ABC):
    """
    Base class for third-party integrations.
    
    Example:
        class FitbitIntegration(Integration):
            def sync(self, user_id: str) -> None:
                # Pull exercise data from Fitbit
                # Recommend recovery meals
                pass
    """
    
    @abstractmethod
    def name(self) -> str:
        """Human-readable integration name."""
        pass
    
    @abstractmethod
    def sync(self, user_id: str, **kwargs) -> Dict:
        """
        Sync with external service.
        
        Returns:
            Data or recommendations from integration
        """
        pass


# ============================================================================
# PLUGIN MANAGER
# ============================================================================

class PluginManager:
    """
    Manages plugins and extensions.
    Developers register custom implementations here.
    """
    
    def __init__(self):
        self.emotion_detectors: Dict[str, EmotionDetector] = {}
        self.recommenders: Dict[str, MealRecommender] = {}
        self.meal_sources: Dict[str, MealSource] = {}
        self.integrations: Dict[str, Integration] = {}
    
    def register_emotion_detector(self, name: str, detector: EmotionDetector):
        """Register a custom emotion detector."""
        self.emotion_detectors[name] = detector
    
    def register_recommender(self, name: str, recommender: MealRecommender):
        """Register a custom recommender."""
        self.recommenders[name] = recommender
    
    def register_meal_source(self, name: str, source: MealSource):
        """Register a custom meal source."""
        self.meal_sources[name] = source
    
    def register_integration(self, integration: Integration):
        """Register a third-party integration."""
        self.integrations[integration.name()] = integration
    
    def get_emotion_detector(self, name: str = "default") -> EmotionDetector:
        """Get emotion detector by name."""
        return self.emotion_detectors.get(name)
    
    def get_recommender(self, name: str = "default") -> MealRecommender:
        """Get recommender by name."""
        return self.recommenders.get(name)


# ============================================================================
# EXAMPLE: HOW TO EXTEND
# ============================================================================

class ExampleCustomRecommender(MealRecommender):
    """Example: Custom recommender that prefers budget meals at office."""
    
    def recommend(self, context: RecommendationContext) -> List[Dict]:
        # Your custom logic here
        recommendations = []
        
        # Pseudocode
        if context.situation == "at-office":
            # Prefer quick, budget-friendly
            pass
        elif context.situation == "date-night":
            # Prefer romantic, premium
            pass
        
        return recommendations[:4]


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

"""
How developers use this:

# 1. Create custom emotion detector
class MyEmotionDetector(EmotionDetector):
    def detect(self, text, language="en"):
        # Custom logic using ML or rules
        return emotion

# 2. Register with system
manager = PluginManager()
manager.register_emotion_detector("my_detector", MyEmotionDetector())

# 3. Use in agent
detector = manager.get_emotion_detector("my_detector")
emotion = detector.detect(user_input)

# 4. Create custom recommender
class MyRecommender(MealRecommender):
    def recommend(self, context):
        # Custom logic
        return meals

manager.register_recommender("my_recommender", MyRecommender())

# 5. Use in agent
recommender = manager.get_recommender("my_recommender")
meals = recommender.recommend(context)
"""
