#!/usr/bin/env python3
"""
CORRECT TRAINING DATA - Using ONLY 35 REAL MEALS from meals_global.json
Distributed across 10 moods for maximum diversity
"""

DEEP_CONTEXT_ANALYSIS_EXPANDED = {
    "illness_cold": {
        "keywords": ["cold", "flu", "cough", "sore throat", "sneezing", "sick"],
        "empathetic_phrases": ["That sounds uncomfortable", "Being sick is miserable"],
        "food_recommendations": ["Vietnamese Pho", "Russian Borscht", "Greek Moussaka", "Thai Pad Thai"],
        "nutritional_rules": {
            "immune_support": "Warm foods boost immune",
            "food": {"options": ["Vietnamese Pho", "Russian Borscht", "Greek Moussaka", "Thai Pad Thai",
                               "Brazilian Feijoada", "Polish Pierogi", "Moroccan Tagine"]},
            "drinks": {"options": ["Thai Mango Sticky Rice", "Tea", "Warm Water"]}
        },
    },
    
    "stress_exam": {
        "keywords": ["exam", "test", "study", "deadline", "stressed", "tired", "exhausted"],
        "empathetic_phrases": ["Exams are stressful", "You care about doing well"],
        "food_recommendations": ["Grilled Salmon with Lemon Butter", "Indian Butter Chicken", "Japanese Ramen Bowl",
                                 "Korean Bibimbap", "Thai Pad Thai"],
        "nutritional_rules": {
            "brain_fuel": "Protein enhances focus",
            "food": {"options": ["Grilled Salmon with Lemon Butter", "Indian Butter Chicken", "Japanese Ramen Bowl",
                               "Korean Bibimbap", "Thai Pad Thai", "Chinese Kung Pao Chicken", "Quinoa Buddha Bowl"]},
            "drinks": {"options": ["Tea", "Coffee", "Water"]}
        },
    },
    
    "heartbreak_breakup": {
        "keywords": ["breakup", "broke up", "heartbreak", "relationship", "miss you"],
        "empathetic_phrases": ["I'm so sorry", "Your pain is valid"],
        "food_recommendations": ["Creamy Chocolate Cake", "Thai Mango Sticky Rice", "Italian Margherita Pizza",
                                 "Classic Cheeseburger", "American BBQ Ribs"],
        "nutritional_rules": {
            "comfort": "Comfort foods soothe pain",
            "food": {"options": ["Creamy Chocolate Cake", "Thai Mango Sticky Rice", "Italian Margherita Pizza",
                               "Classic Cheeseburger", "American BBQ Ribs", "Caprese Sandwich", "French Croissant"]},
            "drinks": {"options": ["Hot Chocolate", "Coffee", "Tea"]}
        },
    },
    
    "burnout_exhaustion": {
        "keywords": ["burned out", "exhausted", "no energy", "drained", "overworked"],
        "empathetic_phrases": ["Burnout is real", "You've worked hard"],
        "food_recommendations": ["Brazilian Feijoada", "Spanish Paella", "Thai Pad Thai", "Mexican Tacos Al Pastor",
                                 "Polish Pierogi"],
        "nutritional_rules": {
            "energy_restore": "Rich foods restore energy",
            "food": {"options": ["Brazilian Feijoada", "Spanish Paella", "Thai Pad Thai", "Mexican Tacos Al Pastor",
                               "Polish Pierogi", "Swedish Meatballs", "Lebanese Mezze Platter"]},
            "drinks": {"options": ["Coffee", "Tea", "Water"]}
        },
    },
    
    "celebration_success": {
        "keywords": ["promoted", "won", "achieved", "celebration", "excited", "success", "happy"],
        "empathetic_phrases": ["That's amazing!", "You deserve celebration"],
        "food_recommendations": ["Argentinian Steak", "Spanish Paella", "Peruvian Ceviche", "Lebanese Kibbeh",
                                 "Creamy Chocolate Cake"],
        "nutritional_rules": {
            "celebration": "Premium foods mark achievements",
            "food": {"options": ["Argentinian Steak", "Spanish Paella", "Peruvian Ceviche", "Lebanese Kibbeh",
                               "Creamy Chocolate Cake", "Thai Mango Sticky Rice", "Portuguese Bacalhau à Brás"]},
            "drinks": {"options": ["Tea", "Coffee", "Water"]}
        },
    },
    
    "anxiety_nervous": {
        "keywords": ["nervous", "anxious", "panic", "worried", "scared", "afraid"],
        "empathetic_phrases": ["Anxiety is real", "You can do this"],
        "food_recommendations": ["Quinoa Buddha Bowl", "Greek Mediterranean Salad", "Vietnamese Pho",
                                 "Middle Eastern Falafel Wrap"],
        "nutritional_rules": {
            "calm": "Light foods ease anxiety",
            "food": {"options": ["Quinoa Buddha Bowl", "Greek Mediterranean Salad", "Vietnamese Pho",
                               "Middle Eastern Falafel Wrap", "Greek Moussaka", "Japanese Tonkatsu", "Caprese Sandwich"]},
            "drinks": {"options": ["Tea", "Water", "Coffee"]}
        },
    },
    
    "loneliness_isolation": {
        "keywords": ["lonely", "alone", "isolated", "nobody", "no friends"],
        "empathetic_phrases": ["Loneliness hurts", "You matter"],
        "food_recommendations": ["Vietnamese Pho", "Japanese Ramen Bowl", "Thai Pad Thai", "Brazilian Feijoada",
                                 "Polish Pierogi"],
        "nutritional_rules": {
            "comfort": "Warm foods ease loneliness",
            "food": {"options": ["Vietnamese Pho", "Japanese Ramen Bowl", "Thai Pad Thai", "Brazilian Feijoada",
                               "Polish Pierogi", "Spanish Paella", "Russian Borscht"]},
            "drinks": {"options": ["Tea", "Coffee", "Hot Chocolate"]}
        },
    },
    
    "anger_frustration": {
        "keywords": ["angry", "frustrated", "mad", "irritated", "furious"],
        "empathetic_phrases": ["Your anger is valid", "That's infuriating"],
        "food_recommendations": ["Mexican Tacos Al Pastor", "Indian Butter Chicken", "Turkish Doner Kebab",
                                 "Lebanese Shawarma", "Chinese Kung Pao Chicken"],
        "nutritional_rules": {
            "release": "Spicy foods channel anger",
            "food": {"options": ["Mexican Tacos Al Pastor", "Indian Butter Chicken", "Turkish Doner Kebab",
                               "Lebanese Shawarma", "Chinese Kung Pao Chicken", "Korean Bibimbap", "Thai Pad Thai"]},
            "drinks": {"options": ["Tea", "Water", "Coffee"]}
        },
    },
    
    "hangover_recovery": {
        "keywords": ["hangover", "drunk", "wasted", "headache", "nauseous"],
        "empathetic_phrases": ["Hangovers are rough", "Let's get you better"],
        "food_recommendations": ["Classic Cheeseburger", "American BBQ Ribs", "Japanese Ramen Bowl",
                                 "Vietnamese Pho", "Peruvian Ceviche"],
        "nutritional_rules": {
            "recovery": "Greasy foods restore energy",
            "food": {"options": ["Classic Cheeseburger", "American BBQ Ribs", "Japanese Ramen Bowl",
                               "Vietnamese Pho", "Peruvian Ceviche", "French Croissant", "Polish Pierogi"]},
            "drinks": {"options": ["Water", "Coconut Water", "Tea"]}
        },
    },
    
    "sad_unlucky": {
        "keywords": ["sad", "blue", "down", "unlucky", "bad day"],
        "empathetic_phrases": ["I'm sorry you're sad", "Bad days happen"],
        "food_recommendations": ["Creamy Chocolate Cake", "Italian Margherita Pizza", "Thai Mango Sticky Rice",
                                 "Classic Cheeseburger", "French Croissant"],
        "nutritional_rules": {
            "mood": "Sweet treats boost mood",
            "food": {"options": ["Creamy Chocolate Cake", "Italian Margherita Pizza", "Thai Mango Sticky Rice",
                               "Classic Cheeseburger", "French Croissant", "Caprese Sandwich", "American BBQ Ribs"]},
            "drinks": {"options": ["Tea", "Coffee", "Hot Chocolate"]}
        },
    },
    
    "general_unknown": {
        "keywords": [],
        "empathetic_phrases": ["Tell me more", "I'm listening"],
        "food_recommendations": ["Italian Margherita Pizza", "Japanese Ramen Bowl", "Vietnamese Pho"],
        "nutritional_rules": {
            "basic": "Good food always helps",
            "food": {"options": ["Italian Margherita Pizza", "Japanese Ramen Bowl", "Vietnamese Pho",
                               "Greek Mediterranean Salad", "Thai Pad Thai", "Korean Bibimbap"]},
            "drinks": {"options": ["Tea", "Water", "Coffee"]}
        },
    }
}

def get_deep_context_expanded(user_input: str):
    """Match user input to situation"""
    user_lower = user_input.lower()
    best_match = None
    highest_score = 0
    
    for situation_key, situation_data in DEEP_CONTEXT_ANALYSIS_EXPANDED.items():
        keywords = situation_data.get("keywords", [])
        score = sum(1 for kw in keywords if kw.lower() in user_lower)
        
        if score > highest_score:
            highest_score = score
            best_match = situation_key
    
    if best_match and highest_score > 0:
        context = DEEP_CONTEXT_ANALYSIS_EXPANDED.get(best_match, {})
        confidence = highest_score * 1000
        return best_match, confidence, context
    
    return "general_unknown", 0, DEEP_CONTEXT_ANALYSIS_EXPANDED.get("general_unknown", {})
