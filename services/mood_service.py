import sys
import os
import json
import asyncio
from typing import Optional, Dict, List
from google import genai

# Add project to path to avoid import issues
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try to import ConversationHandler
    from mood_to_meal_butler.conversation_handler import ConversationHandler
    HAS_CONVERSATION_HANDLER = True
except (ImportError, ModuleNotFoundError):
    # Fallback if imports fail
    HAS_CONVERSATION_HANDLER = False


class MoodService:
    def __init__(self):
        """Initialize mood detection service with ConversationHandler"""
        if HAS_CONVERSATION_HANDLER:
            self.conversation_handler = ConversationHandler()
        else:
            self.conversation_handler = None
        self.build_keyword_index()
        # Load meals for validation
        self.meals = self._load_meals()

    def build_keyword_index(self):
        """Fallback: Build O(1) keyword index at startup"""
        self.keyword_index = {}
        try:
            from mood_to_meal_butler.deep_context_training_25_expanded_FIXED import DEEP_CONTEXT_ANALYSIS_EXPANDED
            for situation_name, situation_data in DEEP_CONTEXT_ANALYSIS_EXPANDED.items():
                for keyword in situation_data.get("keywords", []):
                    if keyword not in self.keyword_index:
                        self.keyword_index[keyword] = situation_name
        except:
            pass

    def _load_meals(self):
        """Load meals from JSON with descriptions and labels"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            meals_path = os.path.join(current_dir, "..", "mood_to_meal_butler", "data", "meals_global.json")
            
            if os.path.exists(meals_path):
                with open(meals_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("meals", [])
        except Exception as e:
            print(f"Could not load meals: {e}")
        return []
    
    def _is_valid_meal(self, meal_dict):
        """Check if meal has real description (not generic fallback)"""
        if not meal_dict:
            return False
        
        # BUG FIX #6: Check both description and description_en variants
        description = meal_dict.get('description') or meal_dict.get('description_en', '')
        # Generic fallback description to avoid
        generic_desc = "A comforting and delicious meal that's perfect for this moment."
        
        # Valid if:
        # 1. Has a description different from generic
        # 2. Has mood_tags (indicates real meal data)
        has_real_desc = description and description != generic_desc
        has_mood_tags = bool(meal_dict.get('mood_tags', []))
        # Check all possible name keys (ConversationHandler returns 'name', database returns 'name_en')
        has_name = bool(meal_dict.get('name') or meal_dict.get('name_en') or meal_dict.get('name_vi'))
        
        return has_real_desc or (has_mood_tags and has_name)

    def _build_meals_prompt(self) -> str:
        """Build a compact prompt with TOP 30 meals only for FREE TIER token limits
        
        FREE TIER limits: Only ~15k tokens per day. Sending 200 meals exhausts quota.
        Solution: Send only names + emoji + mood tags (minimal tokens), skip descriptions
        """
        meals_list = []
        # Send only TOP 30 meals to fit in free tier token limits
        for m in self.meals[:30]:
            name_en = m.get('name_en', '')
            mood_tags = ', '.join(m.get('mood_tags', []))
            health_tags = ', '.join(m.get('health_tags', []))
            emoji = m.get('emoji', '🍽️')
            
            if name_en:
                # MINIMAL: Name + emoji + tags only (no descriptions to save tokens)
                meals_list.append(
                    f"{emoji} {name_en} - Moods: {mood_tags}"
                )
        
        return "\\n".join(meals_list)  # Only 30 meals, no descriptions

    async def _detect_mood_with_gemini(self, user_input: str) -> Optional[Dict]:
        """Use Gemini ONLY for mood detection (minimal prompt, no meal data)
        
        This is ultra-lightweight - just detects emotion, no meal suggestions.
        Keeps token usage minimal to avoid quota issues.
        
        Returns: {mood, confidence, conversation} or None on error
        """
        try:
            from mood_to_meal_butler.config import GEMINI_API_KEY, MODEL_NAME
            
            system_prompt = """You are an emotion detection AI. Analyze the user's message and:
1. Detect their mood/emotion (sad, happy, stressed, tired, etc)
2. Respond with empathy
3. Do NOT suggest meals

Format: 
MOOD: [emotion]
CONFIDENCE: [0.0-1.0]
RESPONSE: [empathetic message]"""
            
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = await client.aio.models.generate_content(
                model=MODEL_NAME,
                contents=[{"role": "user", "parts": [{"text": user_input}]}],
                config={"system_instruction": system_prompt}
            )
            
            response_text = response.text.strip()
            
            # Parse response
            mood = "general_unknown"
            confidence = 0.5
            conversation = response_text
            
            for line in response_text.split('\n'):
                if line.startswith('MOOD:'):
                    mood = line.split(':')[1].strip().lower()
                elif line.startswith('CONFIDENCE:'):
                    try:
                        confidence = float(line.split(':')[1].strip())
                    except:
                        pass
            
            return {
                "mood": mood,
                "confidence": confidence,
                "conversation": conversation,
                "recommendations": []  # NO MEALS from Gemini
            }
            
        except Exception as e:
            error_str = str(e)
            print(f"🔴 [GEMINI MOOD DETECTION] Error: {error_str[:100]}")
            if "429" in error_str or "quota" in error_str.lower():
                print(f"⚠️  Gemini quota exhausted")
                return None
            return None

    def _get_fallback_meals(self, count: int = 8, mood: str = None) -> List[Dict]:
        """Return mood-specific meals from 200+ local database
        
        Args:
            count: Number of meals to return
            mood: Mood/emotion to filter by (sad, tired, stressed, etc)
            
        Returns:
            List of mood-matched meal dicts from database
        """
        if not self.meals:
            return []
        
        # If mood provided, filter meals by mood_tags (26 situations support)
        if mood:
            mood_lower = mood.lower().replace("_", "").replace("-", "")
            mood_filtered = []
            
            for meal in self.meals:
                mood_tags = [tag.lower().replace("_", "").replace("-", "") 
                            for tag in meal.get("mood_tags", [])]
                # Match if mood appears in tags
                if any(mood_lower in tag for tag in mood_tags):
                    mood_filtered.append(meal)
            
            if mood_filtered:
                return mood_filtered[:count]
        
        # No mood or no mood-specific meals found
        # Prioritize meals with valid descriptions and mood tags
        valid_meals = [m for m in self.meals if self._is_valid_meal(m)]
        
        if valid_meals:
            # Return diverse mix (up to count meals)
            return valid_meals[:count]
        else:
            # Fallback to any meals if validation fails
            return self.meals[:count]

    def _extract_recommendations(self, structured_response: Dict) -> List[Dict]:
        """Extract meal recommendations from structured response with details
        CRITICAL: Filter out invalid meals with generic descriptions

        Args:
            structured_response: Structured response from ConversationHandler

        Returns:
            List of meal recommendation dicts with name, description, region, emoji, health_tags, mood_tags
        """
        recommendations = []
        if not self.conversation_handler:
            return recommendations

        try:
            step_4 = structured_response.get("step_4_recommendation", {})
            if isinstance(step_4, dict):
                suggestions = step_4.get("suggestions", {})
                if isinstance(suggestions, dict):
                    # suggestions is {'drinks': [...], 'food': [...]}
                    for category in ['food', 'drinks']:
                        items = suggestions.get(category, [])
                        if isinstance(items, list):
                            for item in items:
                                if isinstance(item, str) and item.strip():
                                    meal_details = self.conversation_handler._get_meal_with_description(item.strip())
                                    if meal_details and self._is_valid_meal(meal_details):
                                        recommendations.append(meal_details)
        except Exception as e:
            print(f"Error extracting recommendations: {e}")
        return recommendations[:10]  # Return max 10 recommendations

    async def detect(self, text: str) -> Dict:
        """Detect mood from user input and return LOCAL MEALS (200+)
        
        ARCHITECTURE:
        - Gemini: SKIPPED (quota exhausted, returns 429 errors)
        - Local meals: 200+ suggestions (ConversationHandler only)
        - Fallback: ConversationHandler → Keyword → Local meals
        
        Args:
            text: User input text

        Returns:
            Dict with mood detection, confidence, conversation, and 200+ meals available
        """
        if not text or not isinstance(text, str):
            return {
                "mood": "general_unknown",
                "confidence": 0.0,
                "conversation": "Tell me more about what you're feeling",
                "recommendations": self._get_fallback_meals(8)
            }

        # Try Gemini first for mood (simple, minimal tokens)
        # If 429 quota error → fallback catches it
        gemini_mood = None
        try:
            gemini_result = await self._detect_mood_with_gemini(text)
            if gemini_result:
                gemini_mood = gemini_result.get("mood")
                print(f"✅ Gemini mood detected: {gemini_mood}")
        except Exception as e:
            print(f"Gemini unavailable (will use local fallback): {str(e)[:50]}")

        # FALLBACK 1: Try ConversationHandler (local)
        if self.conversation_handler:
            try:
                result = self.conversation_handler.generate_conversation_flow(text)
                if result and isinstance(result, dict) and result.get("success"):
                    structured = result.get("structured_response", {})
                    recommendations = self._extract_recommendations(structured)
                    if not isinstance(recommendations, list):
                        recommendations = []
                    
                    mood_for_filter = result.get("situation_detected") or gemini_mood or "general"
                    
                    if not recommendations:
                        # Use mood-aware fallback
                        recommendations = self._get_fallback_meals(8, mood=mood_for_filter)
                    return {
                        "mood": mood_for_filter,
                        "confidence": result.get("confidence", 0.7),
                        "conversation": result.get("conversation", ""),
                        "recommendations": recommendations,
                        "structured_response": structured
                    }
            except Exception as e:
                print(f"ConversationHandler error: {e}")

        # FALLBACK 2: Use keyword index
        words = text.lower().split()
        for word in words:
            if word in self.keyword_index:
                mood_name = self.keyword_index[word]
                return {
                    "mood": mood_name,
                    "confidence": 0.85,
                    "conversation": f"I detected: {mood_name}",
                    "recommendations": self._get_fallback_meals(8, mood=mood_name)
                }

        # FINAL FALLBACK: Return local meals
        final_mood = gemini_mood or "general_unknown"
        return {
            "mood": final_mood,
            "confidence": 0.5,
            "conversation": "Here are some meals for you",
            "recommendations": self._get_fallback_meals(8, mood=final_mood)
        }


mood_service = MoodService()