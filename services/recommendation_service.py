import json
import redis
from config import get_settings
import os

settings = get_settings()

try:
    redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
except:
    redis_client = None

class RecommendationService:
    def __init__(self, meals_file: str = None):
        if meals_file is None:
            meals_file = os.path.join(
                os.path.dirname(__file__),
                "..",
                "mood_to_meal_butler",
                "data",
                "meals_200_global.json"
            )
        self.load_meals(meals_file)
    
    def load_meals(self, meals_file: str):
        """Load meals from JSON file"""
        try:
            with open(meals_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.meals = data.get("meals", [])
        except FileNotFoundError:
            self.meals = []
    
    def get_recommendations(self, mood: str, limit: int = 5) -> list:
        """Get dish recommendations for a mood"""
        if not redis_client:
            return self._compute_recommendations(mood, limit)
        
        cache_key = f"recommendations:{mood}"
        try:
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        except:
            pass
        
        recommendations = self._compute_recommendations(mood, limit)
        
        try:
            redis_client.setex(cache_key, 86400, json.dumps(recommendations))
        except:
            pass
        
        return recommendations
    
    def _compute_recommendations(self, mood: str, limit: int = 5) -> list:
        """Compute recommendations"""
        recommendations = []
        for dish in self.meals:
            if mood in dish.get("mood_tags", []):
                recommendations.append({
                    "name": dish.get("name_en"),
                    "region": dish.get("region_en"),
                    "emoji": dish.get("emoji"),
                    "description": dish.get("description_en"),
                    "budget_level": dish.get("budget_level"),
                    "time_required": dish.get("time_required")
                })
                
                if len(recommendations) >= limit:
                    break
        
        return recommendations

recommendation_service = RecommendationService()
