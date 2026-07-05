# Interview Smart Recommendation Engine
# Suggests personalized meals based on interview answers + user history

from typing import List, Dict, Tuple
from mood_to_meal_butler.interview_analytics import InterviewAnalytics, InterviewEnhancer

class SmartRecommendationEngine:
    """Generate intelligent meal recommendations based on interview + history"""
    
    def __init__(self, meals_list: List[Dict] = None):
        self.meals = meals_list or []
        self.analytics = InterviewAnalytics()
        self.enhancer = InterviewEnhancer(self.analytics)
    
    def load_meals(self, meals: List[Dict]):
        """Set available meals"""
        self.meals = meals
    
    def rank_meals(self, interview_answers: Dict) -> List[Tuple[Dict, float]]:
        """
        Rank meals by match score (0-100) based on interview answers
        Returns: [(meal, score), ...] sorted by score descending
        """
        ranked = []
        
        for meal in self.meals:
            score = self._calculate_meal_score(meal, interview_answers)
            ranked.append((meal, score))
        
        # Sort by score descending
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked
    
    def _calculate_meal_score(self, meal: Dict, answers: Dict) -> float:
        """Calculate how well a meal matches the interview answers"""
        score = 50.0  # Base score
        
        # Mood matching (25 points max)
        mood_tags = meal.get("mood_tags", [])
        user_mood = answers.get("mood", "").lower()
        for tag in mood_tags:
            if tag.lower() in ["tired", "stressed", "sad", "happy", "neutral", "energetic"]:
                if tag.lower() == user_mood:
                    score += 15
                elif self._are_moods_compatible(tag.lower(), user_mood):
                    score += 8
        
        # Craving matching (20 points max)
        craving_tags = meal.get("craving_tags", [])
        user_craving = answers.get("craving", "").lower()
        for tag in craving_tags:
            if tag.lower() == user_craving:
                score += 12
            elif self._are_flavors_compatible(tag.lower(), user_craving):
                score += 6
        
        # Diet matching (15 points max)
        user_diet = answers.get("diet", "").lower()
        if user_diet and user_diet != "none":
            dietary_tags = meal.get("dietary_tags", [])
            for tag in dietary_tags:
                if tag.lower() == user_diet:
                    score += 15
                    break
        
        # Budget matching (15 points max)
        user_budget = answers.get("budget", "").lower()
        meal_price = meal.get("price_tier", "moderate").lower()
        budget_match = {
            "budget": ["budget", "inexpensive", "cheap"],
            "moderate": ["moderate", "fair", "normal"],
            "splurge": ["splurge", "expensive", "premium", "luxury"]
        }
        for budget_level, price_options in budget_match.items():
            if budget_level == user_budget:
                if meal_price in price_options:
                    score += 12
                else:
                    score -= 5
        
        # Time matching (10 points max)
        user_time = answers.get("time", "").lower()
        prep_time = meal.get("prep_time_minutes", 30)
        if user_time == "quick" and prep_time < 15:
            score += 10
        elif user_time == "normal" and 15 <= prep_time <= 45:
            score += 10
        elif user_time == "unhurried" and prep_time > 45:
            score += 10
        
        return min(100.0, max(0.0, score))
    
    def _are_moods_compatible(self, meal_mood: str, user_mood: str) -> bool:
        """Check if moods are compatible"""
        compatibility = {
            "energetic": ["happy", "neutral"],
            "comforting": ["tired", "sad", "stressed"],
            "light": ["tired", "neutral"],
            "rich": ["happy", "neutral"],
        }
        return user_mood in compatibility.get(meal_mood, [])
    
    def _are_flavors_compatible(self, meal_flavor: str, user_craving: str) -> bool:
        """Check if flavors are compatible"""
        compatibility = {
            "spicy": ["spicy", "rich"],
            "sweet": ["sweet", "light", "rich"],
            "light": ["light", "fresh"],
            "rich": ["rich", "comfort", "sweet"],
            "savory": ["rich", "comfort"],
        }
        return user_craving in compatibility.get(meal_flavor, [])
    
    def get_top_recommendations(self, interview_answers: Dict, count: int = 5) -> List[Dict]:
        """
        Get top N meal recommendations with confidence scores
        """
        ranked = self.rank_meals(interview_answers)
        
        recommendations = []
        for meal, score in ranked[:count]:
            rec = {
                "meal": meal,
                "confidence_score": round(score, 1),
                "match_reasons": self._get_match_reasons(meal, interview_answers, score)
            }
            recommendations.append(rec)
        
        return recommendations
    
    def _get_match_reasons(self, meal: Dict, answers: Dict, score: float) -> List[str]:
        """Generate human-readable reasons why this meal was recommended"""
        reasons = []
        
        # Check mood match
        meal_moods = meal.get("mood_tags", [])
        user_mood = answers.get("mood", "")
        for mood in meal_moods:
            if mood.lower() == user_mood.lower():
                reasons.append(f"Perfect for your {user_mood} mood")
                break
        
        # Check craving match
        meal_flavors = meal.get("craving_tags", [])
        user_craving = answers.get("craving", "")
        for flavor in meal_flavors:
            if flavor.lower() == user_craving.lower():
                reasons.append(f"Matches your craving for {user_craving}")
                break
        
        # Check diet
        user_diet = answers.get("diet", "")
        if user_diet != "none":
            dietary = meal.get("dietary_tags", [])
            for diet_tag in dietary:
                if diet_tag.lower() == user_diet.lower():
                    reasons.append(f"Aligns with your {user_diet} preference")
                    break
        
        # Check group size
        user_group = answers.get("group", "")
        meal_portions = meal.get("portion_size", [])
        if user_group in str(meal_portions).lower():
            reasons.append(f"Great for {user_group} dining")
        
        if not reasons:
            reasons.append(f"High match score ({score}% confidence)")
        
        return reasons
    
    def get_alternative_recommendations(self, 
                                       primary_meal: Dict,
                                       interview_answers: Dict,
                                       count: int = 3) -> List[Dict]:
        """
        Get alternative recommendations similar to primary meal
        Useful when user wants variety but same mood/theme
        """
        alternatives = []
        
        for meal in self.meals:
            if meal.get("id") == primary_meal.get("id"):
                continue  # Skip the meal itself
            
            # Check if similar mood tags
            overlap = set(meal.get("mood_tags", [])) & set(primary_meal.get("mood_tags", []))
            if not overlap:
                continue  # Skip if no mood tag overlap
            
            score = self._calculate_meal_score(meal, interview_answers)
            alternatives.append({
                "meal": meal,
                "similarity": round(len(overlap) / max(1, len(primary_meal.get("mood_tags", []))), 2),
                "confidence_score": round(score, 1)
            })
        
        alternatives.sort(key=lambda x: x["confidence_score"], reverse=True)
        return alternatives[:count]
