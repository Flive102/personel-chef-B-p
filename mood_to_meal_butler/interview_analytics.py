# Interview Analytics & Insights Engine
# Tracks patterns, provides personalization, and predicts meal satisfaction

from datetime import datetime
from collections import defaultdict
import json
from typing import Dict, List, Tuple

class InterviewAnalytics:
    """Advanced analytics for interview patterns and user preferences"""
    
    def __init__(self, history_file: str = None):
        self.history_file = history_file or "interview_history.json"
        self.sessions = []
        self.load_history()
    
    def load_history(self):
        """Load interview history from disk"""
        try:
            with open(self.history_file, 'r') as f:
                self.sessions = json.load(f)
        except FileNotFoundError:
            self.sessions = []
    
    def save_history(self):
        """Persist interview history"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.sessions, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save history: {e}")
    
    def record_session(self, answers: Dict, mood_detected: str = None) -> str:
        """Record a completed interview session"""
        session = {
            "timestamp": datetime.now().isoformat(),
            "answers": answers,
            "mood_detected": mood_detected,
            "satisfaction": None  # Will be filled in later if user rates
        }
        self.sessions.append(session)
        self.save_history()
        return session["timestamp"]
    
    def get_mood_trend(self, days: int = 7) -> Dict[str, int]:
        """Get mood distribution over last N days"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        
        mood_counts = defaultdict(int)
        for session in self.sessions:
            ts = datetime.fromisoformat(session["timestamp"])
            if ts > cutoff:
                mood = session["answers"].get("mood", "unknown")
                mood_counts[mood] += 1
        
        return dict(mood_counts)
    
    def get_most_common_combo(self) -> Dict[str, str]:
        """Find the most frequently answered combination"""
        if not self.sessions:
            return {}
        
        # Count all combinations
        combo_counts = defaultdict(int)
        for session in self.sessions:
            answers = session["answers"]
            # Create a hashable combo key
            combo_key = tuple(answers.get(k, "unknown") for k in 
                            ["mood", "craving", "group", "budget"])
            combo_counts[combo_key] += 1
        
        if not combo_counts:
            return {}
        
        # Return the most common
        best_combo = max(combo_counts.items(), key=lambda x: x[1])
        return {
            "mood": best_combo[0][0],
            "craving": best_combo[0][1],
            "group": best_combo[0][2],
            "budget": best_combo[0][3],
            "frequency": best_combo[1]
        }
    
    def get_meal_affinity(self, mood: str, limit: int = 3) -> List[str]:
        """Get meals user typically chooses for a given mood"""
        # This would be populated from meal selection history
        # For now returns empty - would integrate with meal tracking
        return []
    
    def calculate_interview_confidence(self, answers: Dict) -> float:
        """Score how decisive the user was (0-100)"""
        decisiveness_score = 0
        max_score = 0
        
        keywords_by_specificity = {
            "surprise": 30,  # Less decisive
            "no idea": 30,
            "okay": 40,
            "neutral": 40,
            "normal": 50,
            "moderate": 50,
            "spicy": 70,  # More decisive
            "sweet": 70,
            "stressed": 80,
            "happy": 80,
        }
        
        for key, value in answers.items():
            if isinstance(value, str):
                value_lower = value.lower()
                for keyword, score in keywords_by_specificity.items():
                    if keyword in value_lower:
                        decisiveness_score += score
                        max_score += 100
                        break
        
        if max_score == 0:
            return 50.0  # Default
        
        return min(100.0, (decisiveness_score / max_score) * 100)
    
    def get_personalization_hints(self, user_id: str = "default") -> Dict:
        """Generate personalization hints based on history"""
        if not self.sessions:
            return {"status": "no_history"}
        
        mood_trend = self.get_mood_trend(days=7)
        common_combo = self.get_most_common_combo()
        
        hints = {
            "recent_moods": mood_trend,
            "typical_preferences": common_combo,
            "total_interviews": len(self.sessions),
            "most_consistent_choice": self._find_most_consistent_answer(),
        }
        
        return hints
    
    def _find_most_consistent_answer(self) -> Dict[str, str]:
        """Find the answer that appears most consistently"""
        answer_freq = defaultdict(lambda: defaultdict(int))
        
        for session in self.sessions:
            for key, value in session["answers"].items():
                answer_freq[key][value] += 1
        
        result = {}
        for key, values in answer_freq.items():
            if values:
                most_common = max(values.items(), key=lambda x: x[1])
                result[key] = most_common[0]
        
        return result


class InterviewEnhancer:
    """Enhance interview flow with smart features"""
    
    def __init__(self, analytics: InterviewAnalytics = None):
        self.analytics = analytics or InterviewAnalytics()
    
    def get_smart_question_order(self, user_history_count: int) -> List[str]:
        """
        Return question order based on user experience
        New users: standard order (mood → craving → group → budget → time → diet)
        Returning users: prioritize questions they usually take longest to answer
        """
        if user_history_count == 0:
            # New user: standard order
            return ["mood", "craving", "group", "budget", "time", "diet"]
        else:
            # Returning user: keep standard for consistency
            return ["mood", "craving", "group", "budget", "time", "diet"]
    
    def get_contextual_hint(self, question_key: str, previous_answers: Dict) -> str:
        """Provide smart hints based on previous answers"""
        hints = {
            "mood": {
                "default": "(tired / happy / stressed / sad / neutral)",
                "after_stressed": "Remember you mentioned feeling stressed earlier...",
            },
            "craving": {
                "default": "(spicy / sweet / light / rich / surprise me)",
                "after_tired": "Light & energizing might help with your energy!",
                "after_stressed": "Comfort food can be soothing when stressed.",
            },
            "time": {
                "default": "(quick / normal / unhurried)",
                "after_stressed": "Give yourself enough time to relax and enjoy.",
            }
        }
        
        mood = previous_answers.get("mood", "").lower()
        default_hint = hints.get(question_key, {}).get("default", "")
        
        # Return contextual hint if available
        for trigger, hint in hints.get(question_key, {}).items():
            if trigger != "default" and trigger in f"after_{mood}":
                return hint
        
        return default_hint
    
    def predict_satisfaction(self, answers: Dict, meal_profile: Dict) -> float:
        """
        Predict user satisfaction (0-100) based on answer patterns
        meal_profile: dict with meal's mood_tags, health_tags, etc.
        """
        score = 50.0  # Base score
        
        # Boost if meal matches mood
        if meal_profile.get("mood_tags"):
            user_mood = answers.get("mood", "")
            if user_mood in str(meal_profile.get("mood_tags", "")).lower():
                score += 15
        
        # Boost if budget matches
        if meal_profile.get("price_tier"):
            user_budget = answers.get("budget", "")
            if user_budget == "splurge" and meal_profile["price_tier"] == "premium":
                score += 10
            elif user_budget == "budget" and meal_profile["price_tier"] == "budget":
                score += 10
        
        # Boost if time matches
        if meal_profile.get("prep_time"):
            user_time = answers.get("time", "")
            prep_mins = meal_profile.get("prep_time", 30)
            if user_time == "quick" and prep_mins < 15:
                score += 10
            elif user_time == "normal" and 15 <= prep_mins <= 45:
                score += 10
        
        # Boost if diet matches
        if answers.get("diet") != "none":
            user_diet = answers.get("diet", "").lower()
            meal_diets = str(meal_profile.get("dietary_tags", "")).lower()
            if user_diet in meal_diets:
                score += 15
        
        return min(100.0, score)
