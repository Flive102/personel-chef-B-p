#!/usr/bin/env python3
"""
Context Understanding & Situation Analysis
Analyzes user situations to make intelligent food/drink recommendations
"""

SITUATION_CONTEXT = {
    "sick": {
        "keywords": ["cold", "flu", "fever", "cough", "caught", "ill", "sick", "headache", "sore throat", "nauseous"],
        "recommendations": {
            "drinks": ["Warm Honey Lemon Tea", "Chicken Broth", "Ginger Tea", "Herbal Soup"],
            "food": ["Congee", "Oatmeal", "Soft Boiled Eggs", "Vegetable Soup"],
            "reason": "Warm liquids soothe and chicken broth helps recovery"
        }
    },
    
    "stressed_exam": {
        "keywords": ["exam", "test", "presentation", "interview", "deadline", "project", "report"],
        "recommendations": {
            "drinks": ["Coffee", "Green Tea", "Protein Smoothie", "Energy Drink"],
            "food": ["Salmon", "Nuts & Seeds", "Whole Grain Toast", "Chicken Rice Bowl", "Dark Chocolate"],
            "reason": "Protein and omega-3s boost focus and energy"
        }
    },
    
    "heartbreak": {
        "keywords": ["breakup", "broke up", "relationship", "heartbreak", "dumped", "sad about", "miss", "lost someone"],
        "recommendations": {
            "drinks": ["Hot Chocolate", "Chamomile Tea", "Red Wine (if adult)", "Smoothie"],
            "food": ["Chocolate Cake", "Ice Cream", "Comfort Pasta", "Pizza", "Cookies"],
            "reason": "Comfort foods release endorphins and provide emotional support"
        }
    },
    
    "exhausted": {
        "keywords": ["exhausted", "tired", "sleepy", "no energy", "burnt out", "fatigue", "worn out", "drained"],
        "recommendations": {
            "drinks": ["Coffee", "Energy Drink", "Protein Shake", "Fresh Orange Juice"],
            "food": ["Salmon", "Steak", "Eggs", "Bananas", "Almonds", "Whole Grain Bread"],
            "reason": "Iron, B vitamins, and protein restore energy"
        }
    },
    
    "celebrating": {
        "keywords": ["won", "passed", "got", "celebrate", "achievement", "promoted", "success", "great news", "happy"],
        "recommendations": {
            "drinks": ["Champagne", "Wine", "Special Juice", "Cocktail"],
            "food": ["Sushi", "Steak", "Premium Dessert", "Fancy Pasta", "Lobster"],
            "reason": "Treat yourself with premium options to honor your achievement"
        }
    },
    
    "lonely": {
        "keywords": ["lonely", "alone", "isolated", "no one", "by myself", "friend left", "miss my friends"],
        "recommendations": {
            "drinks": ["Warm Tea", "Hot Chocolate", "Coffee"],
            "food": ["Pizza (call friends!)", "Comfort Pasta", "Cookies", "Cake"],
            "reason": "Comfort foods + suggestion to connect with others"
        }
    },
    
    "anxious": {
        "keywords": ["anxious", "nervous", "worried", "anxious about", "scared", "nervous about", "panic"],
        "recommendations": {
            "drinks": ["Chamomile Tea", "Peppermint Tea", "Warm Milk", "Calming Herbal Tea"],
            "food": ["Oatmeal", "Almonds", "Avocado", "Whole Grain", "Dark Chocolate"],
            "reason": "Magnesium-rich foods calm the nervous system"
        }
    },
    
    "bored": {
        "keywords": ["bored", "nothing to do", "boring", "dull", "no plans"],
        "recommendations": {
            "drinks": ["Interesting Cocktail", "Fruit Smoothie", "Bubble Tea", "Specialty Coffee"],
            "food": ["Spicy Food", "Exotic Cuisine", "Tapas", "Street Food", "Adventure Food"],
            "reason": "New and interesting flavors can spark excitement"
        }
    },
    
    "angry": {
        "keywords": ["angry", "mad", "furious", "hate", "pissed", "frustrated", "irritated", "upset about"],
        "recommendations": {
            "drinks": ["Ice Cold Water", "Iced Tea", "Smoothie", "Fresh Juice"],
            "food": ["Spicy Food", "Pizza", "Burger", "Grilled Food", "Pasta"],
            "reason": "Hot/spicy foods channel intensity, carbs help calm"
        }
    },
    
    "hangover": {
        "keywords": ["hangover", "drunk", "alcohol", "last night", "head hurts", "feeling sick"],
        "recommendations": {
            "drinks": ["Water", "Coconut Water", "Fresh Orange Juice", "Electrolyte Drink", "Coffee"],
            "food": ["Bacon & Eggs", "Toast", "Soup", "Fried Food", "Rice Porridge"],
            "reason": "Greasy food + hydration + carbs help recovery"
        }
    }
}

CONVERSATIONAL_RESPONSES = {
    "sick": {
        "empathy": "Oh no, that sounds rough. Being sick is never fun. Let me help you feel better.",
        "follow_up": "How are you feeling? Do you have a fever or just general symptoms?",
        "care": "Make sure to stay hydrated and rest lots. 💚"
    },
    "stressed_exam": {
        "empathy": "That sounds stressful! Tests and deadlines are tough.",
        "follow_up": "When is it? Do you want something to keep your energy up?",
        "care": "You've got this! Let's fuel you with brain food. 💪"
    },
    "heartbreak": {
        "empathy": "I'm truly sorry you're going through this. Heartbreak is one of the hardest things.",
        "follow_up": "How long ago did this happen? Do you need comfort or distraction?",
        "care": "It's okay to feel sad. Let's get you something comforting. 💚"
    },
    "exhausted": {
        "empathy": "Exhaustion is real. When you're burned out, everything feels harder.",
        "follow_up": "Is this from work, lack of sleep, or life catching up?",
        "care": "Let's get your energy back up. You deserve rest AND good fuel. 💚"
    },
    "celebrating": {
        "empathy": "That's amazing! I'm so happy for you!",
        "follow_up": "What did you achieve? I want to celebrate with you!",
        "care": "You deserve to celebrate big. Let's find something special. 🎉"
    },
    "lonely": {
        "empathy": "Feeling lonely is really hard. But you're not alone right now - I'm here.",
        "follow_up": "Do you want to reach out to someone, or do you need space?",
        "care": "Let's get you something comforting, and maybe you could text a friend? 💚"
    },
    "anxious": {
        "empathy": "Anxiety can be really overwhelming. I'm here to help.",
        "follow_up": "What's making you anxious? Sometimes talking helps.",
        "care": "Let's get you something calming. Deep breaths. You're going to be okay. 💚"
    },
    "bored": {
        "empathy": "Boredom can actually be an opportunity for adventure!",
        "follow_up": "What kind of adventure sounds fun to you right now?",
        "care": "Let's try something new and exciting! 🎉"
    },
    "angry": {
        "empathy": "It's okay to be angry. That's a valid feeling.",
        "follow_up": "What happened? Sometimes it helps to talk about it.",
        "care": "Let's find something satisfying for you. 💚"
    },
    "hangover": {
        "empathy": "Ouch, hangover mornings are rough. You're not alone!",
        "follow_up": "How bad is it? Water is going to be your best friend.",
        "care": "Let's get you hydrated and fed. You'll feel better soon. 💚"
    }
}


def analyze_user_situation(user_input):
    """
    Analyze user input to understand their situation
    Returns: (situation_type, confidence, context_details)
    """
    user_input_lower = user_input.lower()
    
    matches = []
    
    for situation, data in SITUATION_CONTEXT.items():
        for keyword in data["keywords"]:
            if keyword.lower() in user_input_lower:
                matches.append((situation, len(keyword)))
    
    if not matches:
        return None, 0, None
    
    # Sort by keyword length (longer = more specific)
    matches.sort(key=lambda x: x[1], reverse=True)
    best_match = matches[0]
    
    situation = best_match[0]
    confidence = min(100, (best_match[1] / len(user_input_lower)) * 100)
    
    return situation, confidence, SITUATION_CONTEXT[situation]


def get_empathetic_response(situation):
    """Get empathetic response for a situation"""
    if situation in CONVERSATIONAL_RESPONSES:
        return CONVERSATIONAL_RESPONSES[situation]
    return None


def get_recommendations(situation):
    """Get food/drink recommendations for a situation"""
    if situation in SITUATION_CONTEXT:
        return SITUATION_CONTEXT[situation]["recommendations"]
    return None


def build_conversational_suggestion(situation, user_context):
    """Build a full conversational suggestion"""
    response = get_empathetic_response(situation)
    recommendations = get_recommendations(situation)
    
    if not response or not recommendations:
        return None
    
    return {
        "empathy": response["empathy"],
        "follow_up": response["follow_up"],
        "drinks": recommendations["drinks"],
        "food": recommendations["food"],
        "reason": recommendations["reason"],
        "care": response["care"]
    }


# Example usage for testing
if __name__ == "__main__":
    test_inputs = [
        "I've caught a cold, my head hurts and I can't stop coughing",
        "I have an exam tomorrow and I'm so stressed",
        "My girlfriend broke up with me yesterday",
        "I'm so exhausted from work, I have no energy left",
        "I just got promoted! So happy!",
        "I feel so alone right now",
        "I'm really nervous about my presentation",
        "I'm so angry at what happened",
    ]
    
    for test_input in test_inputs:
        situation, confidence, context = analyze_user_situation(test_input)
        print(f"\nInput: {test_input}")
        print(f"Situation: {situation} ({confidence:.1f}% confidence)")
        if situation:
            suggestion = build_conversational_suggestion(situation, test_input)
            print(f"Empathy: {suggestion['empathy']}")
            print(f"Recommendations: {suggestion['drinks']} / {suggestion['food']}")
