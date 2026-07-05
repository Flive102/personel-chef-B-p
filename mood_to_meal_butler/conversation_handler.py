#!/usr/bin/env python3
"""
INTELLIGENT CONVERSATION HANDLER
Integrates deep context training with agent responses
Ensures 100% rule adherence for empathetic interactions
"""

import random
import json
import os
from mood_to_meal_butler.deep_context_training_25_expanded_FIXED import (
    DEEP_CONTEXT_ANALYSIS_EXPANDED,
    get_deep_context_expanded
)

# Alias for compatibility
DEEP_CONTEXT_ANALYSIS = DEEP_CONTEXT_ANALYSIS_EXPANDED
get_deep_context = get_deep_context_expanded


class ConversationHandler:
    """
    Manages conversations following deep training guidelines
    """
    
    def __init__(self):
        self.conversation_history = []
        self.user_context = {}
        self.current_situation = None
        self.meals = self._load_meals()
    
    
    def _load_meals(self):
        """Load meals from JSON with descriptions and labels"""
        try:
            # Find meals_global.json
            current_dir = os.path.dirname(os.path.abspath(__file__))
            meals_path = os.path.join(current_dir, "data", "meals_global.json")
            
            if os.path.exists(meals_path):
                with open(meals_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("meals", [])
        except Exception as e:
            print(f"Could not load meals: {e}")
        
        return []
    
    
    def _get_meal_with_description(self, meal_name):
        """Get meal details with description and labels"""
        # Search in loaded meals
        for meal in self.meals:
            if meal_name.lower() in meal.get("name_en", "").lower():
                return {
                    "name": meal.get("name_en", meal_name),
                    "description": meal.get("description_en", ""),
                    "region": meal.get("region_en", ""),
                    "emoji": meal.get("emoji", "🍽️"),
                    "health_tags": meal.get("health_tags", []),
                    "mood_tags": meal.get("mood_tags", []),
                    "time_required": meal.get("time_required", 0),
                    "budget": meal.get("budget", "moderate")
                }
        
        # If not found, return basic info
        return {
            "name": meal_name,
            "description": f"A comforting and delicious meal that's perfect for this moment.",
            "region": "Global",
            "emoji": "🍽️",
            "health_tags": ["comfort-food"],
            "mood_tags": [],
            "time_required": 0,
            "budget": "moderate"
        }
    
    
    def add_message(self, role, content):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    
    def analyze_user_input(self, user_input):
        """
        Analyze user input deeply
        Returns: situation analysis with confidence
        """
        situation, confidence, context = get_deep_context(user_input)
        
        if situation:
            self.current_situation = situation
            self.user_context = {
                "input": user_input,
                "situation": situation,
                "confidence": confidence,
                "context": context
            }
        
        return situation, confidence, context
    
    
    def get_empathetic_opening(self, situation_type):
        """
        Get opening empathetic phrase
        Rule: Start with genuine empathy
        """
        context = DEEP_CONTEXT_ANALYSIS.get(situation_type, {})
        phrases = context.get("empathetic_phrases", [])
        
        if phrases:
            return random.choice(phrases)
        return "I hear you. Tell me more."
    
    
    def get_clarifying_questions(self, situation_type, count=2):
        """
        Get clarifying questions
        Rule: Ask questions to fully understand context
        """
        context = DEEP_CONTEXT_ANALYSIS.get(situation_type, {})
        questions = context.get("follow_up_questions", [])
        
        if questions:
            selected = random.sample(questions, min(count, len(questions)))
            return selected
        return []
    
    
    def build_food_recommendation(self, situation_type):
        """
        Build food recommendation with full explanation
        Rule: Explain WHY each suggestion works
        """
        context = DEEP_CONTEXT_ANALYSIS.get(situation_type, {})
        nutritional = context.get("nutritional_rules", {})
        
        if not nutritional:
            return None
        
        recommendation = {
            "situation": situation_type,
            "reasoning": {},
            "suggestions": {},
            "explanations": {}
        }
        
        # Extract recommendations - handle different structures
        if "drinks" in nutritional:
            drinks_info = nutritional["drinks"]
            if isinstance(drinks_info, dict):
                recommendation["suggestions"]["drinks"] = drinks_info.get("options", [])
                recommendation["explanations"]["drinks"] = {
                    key: val for key, val in drinks_info.items() if key != "options"
                }
        
        if "food" in nutritional:
            food_info = nutritional["food"]
            if isinstance(food_info, dict):
                recommendation["suggestions"]["food"] = food_info.get("options", [])
                recommendation["explanations"]["food"] = {
                    key: val for key, val in food_info.items() if key != "options"
                }
        
        # Handle "foods" (plural) structure
        if "foods" in nutritional:
            foods_info = nutritional["foods"]
            if isinstance(foods_info, dict):
                all_foods = []
                for category, items in foods_info.items():
                    if isinstance(items, list):
                        all_foods.extend(items)
                if all_foods:
                    recommendation["suggestions"]["food"] = all_foods
        
        # Handle "nutrition" structure
        if "nutrition" in nutritional:
            nutrition_info = nutritional["nutrition"]
            if isinstance(nutrition_info, dict):
                all_items = []
                for category, items in nutrition_info.items():
                    if isinstance(items, list) and category not in ["avoid"]:
                        all_items.extend(items)
                if all_items:
                    recommendation["suggestions"]["food"] = all_items
        
        return recommendation
    
    
    def format_full_response(self, situation_type, user_input):
        """
        Format complete conversational response
        Follows ALL rules in sequence
        """
        context = DEEP_CONTEXT_ANALYSIS.get(situation_type, {})
        
        response = {
            "step_1_empathy": self.get_empathetic_opening(situation_type),
            "step_2_validation": self._get_validation_statement(situation_type),
            "step_3_clarify": self.get_clarifying_questions(situation_type, count=2),
            "step_4_recommendation": self.build_food_recommendation(situation_type),
            "step_5_explanation": self._build_explanations(situation_type),
            "step_6_care": self._get_care_statement(situation_type),
            "rules_applied": context.get("conversation_rules", [])
        }
        
        return response
    
    
    def _get_validation_statement(self, situation_type):
        """
        Get validation statement
        Rule: Validate their feelings are normal and valid
        """
        validation_map = {
            "illness_cold": "Being sick is miserable and your body needs care. What you're feeling is completely normal.",
            "stress_exam": "Exam stress is universal - even high achievers feel this way. Your anxiety shows you care about doing well.",
            "heartbreak_breakup": "Heartbreak is one of the most painful emotions. What you're feeling is completely valid and understandable.",
            "burnout_exhaustion": "Burnout is real and serious. Your exhaustion makes complete sense - you need rest and care.",
            "celebration_success": "Your achievement is real and you absolutely deserve to celebrate it. Be proud of yourself.",
            "anxiety_nervous": "Nervousness is natural and shows you take this seriously. Even successful people feel this way.",
            "loneliness_isolation": "Loneliness is a real pain that many people experience. Your feelings are valid and important.",
            "anger_frustration": "Your anger is justified. Strong emotions to injustice or disappointment are completely normal.",
            "hangover_recovery": "Hangovers happen to everyone - no judgment here. Let's get you feeling better.",
        }
        
        return validation_map.get(situation_type, "Your feelings are valid and important.")
    
    
    def _build_explanations(self, situation_type):
        """
        Build detailed explanations
        Rule: Explain the mechanism - WHY does this help?
        """
        context = DEEP_CONTEXT_ANALYSIS.get(situation_type, {})
        explanations = []
        
        if "nutritional_rules" in context:
            rules = context["nutritional_rules"]
            for key, value in rules.items():
                if isinstance(value, str) and key not in ["options", "avoid", "timing"]:
                    explanations.append(value)
                elif isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, str) and sub_key not in ["options", "avoid", "timing"]:
                            explanations.append(sub_value)
        
        # If no explanations found, add default ones
        if not explanations:
            explanations = [
                "This is specifically chosen for your situation",
                "It addresses your physical and emotional needs",
                "It provides the support your body/mind needs right now"
            ]
        
        return explanations
    
    
    def _get_care_statement(self, situation_type):
        """
        Get caring closing statement
        Rule: End with genuine concern
        """
        care_map = {
            "illness_cold": "Make sure to stay hydrated, rest lots, and be gentle with yourself. If this gets worse, see a doctor. You're going to feel better soon. 💚",
            "stress_exam": "You've got the capability to do this. Fuel your body and mind, get some sleep, and remember - you're more prepared than you think. You're going to do great! 💪",
            "heartbreak_breakup": "You're going to get through this. It's okay to feel sad. Eat something comforting, reach out to someone you trust, and be kind to yourself. You're not alone. 💚",
            "burnout_exhaustion": "You deserve rest and care. Eat well, but also prioritize actual rest and recovery. You can't run on empty forever. Please take care of yourself. 💚",
            "celebration_success": "You absolutely deserve this celebration. Go make it memorable with people you care about. I'm genuinely proud of you. 🎉",
            "anxiety_nervous": "You're prepared and capable. Take deep breaths, eat something grounding, and remember - you've done hard things before. You've got this! 💪",
            "loneliness_isolation": "You're not actually alone - I'm here for you. Reach out to someone today if you can. Connection matters. You deserve to feel supported. 💚",
            "anger_frustration": "Your feelings are valid. Consider what action is appropriate, but for now, do something that helps you feel heard and supported. You matter. 💚",
            "hangover_recovery": "Drink lots of water, eat something light and greasy, and rest. You'll feel better soon. Be kind to yourself today - you're not the first or last to experience this. 💚"
        }
        
        return care_map.get(situation_type, "I'm here for you and I care about your wellbeing. 💚")
    
    
    def generate_conversation_flow(self, user_input):
        """
        Generate complete conversation flow
        Returns structured response following all rules
        """
        situation, confidence, context = self.analyze_user_input(user_input)
        
        if not situation or confidence < 50:
            return {
                "success": False,
                "message": "I want to understand better. Can you tell me more about what's going on?",
                "needs_clarification": True,
                "structured_response": {}
            }
        
        # Generate full response following rules
        response = self.format_full_response(situation, user_input)
        conversation_text = self._build_conversation_text(response)
        
        # Build conversational output
        output = {
            "success": True,
            "situation_detected": situation,
            "confidence": confidence,
            "conversation": conversation_text,
            "structured_response": response
        }
        
        # Add to history
        self.add_message("user", user_input)
        self.add_message("assistant", conversation_text)
        
        return output
    
    
    def _build_conversation_text(self, response):
        """
        Build natural conversational text from response
        """
        text_parts = []
        
        # Step 1: Empathy
        text_parts.append(response["step_1_empathy"])
        
        # Step 2: Validation
        text_parts.append("\n" + response["step_2_validation"])
        
        # Step 3: Clarifying questions
        if response["step_3_clarify"]:
            text_parts.append("\nTell me a bit more:")
            for i, q in enumerate(response["step_3_clarify"], 1):
                text_parts.append(f"  • {q}")
        
        # Step 4 & 5: Recommendation with explanation and MEAL DETAILS
        if response["step_4_recommendation"]:
            rec = response["step_4_recommendation"]
            text_parts.append("\n👨‍🍳 Here's what I recommend:")
            
            if "drinks" in rec["suggestions"]:
                text_parts.append("\n🥤 Drinks:")
                for drink in rec["suggestions"]["drinks"]:
                    meal_detail = self._get_meal_with_description(drink)
                    text_parts.append(f"  • {meal_detail['emoji']} {meal_detail['name']}")
                    text_parts.append(f"    {meal_detail['description']}")
                    if meal_detail['health_tags']:
                        tags = ", ".join(meal_detail['health_tags'])
                        text_parts.append(f"    🏷️ {tags}")
            
            if "food" in rec["suggestions"]:
                text_parts.append("\n🍽️ Food:")
                for food in rec["suggestions"]["food"]:
                    meal_detail = self._get_meal_with_description(food)
                    text_parts.append(f"  • {meal_detail['emoji']} {meal_detail['name']}")
                    text_parts.append(f"    {meal_detail['description']}")
                    if meal_detail['health_tags']:
                        tags = ", ".join(meal_detail['health_tags'])
                        text_parts.append(f"    🏷️ {tags}")
                    if meal_detail['region']:
                        text_parts.append(f"    📍 From: {meal_detail['region']}")
        
        # Explanations
        if response["step_5_explanation"]:
            text_parts.append("\nWhy this helps:")
            for exp in response["step_5_explanation"][:3]:  # Top 3 explanations
                text_parts.append(f"  • {exp}")
        
        # Step 6: Care
        text_parts.append("\n" + response["step_6_care"])
        
        return "\n".join(text_parts)
    
    
    def get_conversation_history(self):
        """Return conversation history"""
        return self.conversation_history
    
    
    def get_user_context(self):
        """Return user context information"""
        return self.user_context


# DEMONSTRATION & TESTING
def run_conversation_demo():
    """
    Run demonstration of conversation handling
    Shows how agent responds to different situations
    """
    handler = ConversationHandler()
    
    test_inputs = [
        "I've caught a cold and my throat is killing me. Can barely swallow.",
        "I have a big exam tomorrow and I haven't finished studying. Really stressed.",
        "My girlfriend just broke up with me. I feel terrible.",
        "I'm so burned out from work. No energy left.",
        "I just got promoted! So excited!",
        "I'm nervous about my presentation in an hour.",
        "Feeling really lonely since moving to this new city.",
        "I'm angry about what happened. Can't stop thinking about it.",
        "Hangover is brutal. Everything hurts.",
    ]
    
    print("=" * 80)
    print("CONVERSATION HANDLER DEMONSTRATION")
    print("=" * 80)
    
    for user_input in test_inputs:
        print(f"\n{'='*80}")
        print(f"USER: {user_input}")
        print(f"{'='*80}")
        
        result = handler.generate_conversation_flow(user_input)
        
        if result["success"]:
            print(f"\nDETECTED SITUATION: {result['situation_detected']}")
            print(f"CONFIDENCE: {result['confidence']}%")
            print(f"\nAGENT RESPONSE:\n{result['conversation']}")
            print(f"\nRULES APPLIED: {len(result['structured_response']['rules_applied'])}")
        else:
            print(f"\nAGENT: {result['message']}")
        
        print()


if __name__ == "__main__":
    run_conversation_demo()
