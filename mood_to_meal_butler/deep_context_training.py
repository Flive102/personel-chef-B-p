#!/usr/bin/env python3
"""
COMPREHENSIVE AGENT TRAINING SYSTEM
Deep Conversational & Contextual Understanding
100% Rule-Based Empathetic Food Recommendations
"""

DEEP_CONTEXT_ANALYSIS = {
    # HEALTH & PHYSICAL CONDITIONS
    "illness_cold": {
        "keywords": ["cold", "flu", "cough", "sore throat", "sneezing", "runny nose", "stuffy", "congestion"],
        "severity_markers": {
            "mild": ["slight cough", "little cold", "tickle in throat"],
            "moderate": ["bad cough", "sore throat", "fever", "body ache"],
            "severe": ["high fever", "can't swallow", "chest pain", "difficulty breathing"]
        },
        "nutritional_rules": {
            "drinks": {
                "warm_liquids": "Warm liquids soothe throat and provide hydration",
                "immune_boosters": "Vitamin C fights infection; ginger reduces inflammation",
                "options": ["Honey lemon tea", "Ginger tea", "Chicken broth", "Warm milk", "Herbal tea"]
            },
            "food": {
                "easy_digest": "Easy to digest - don't stress the body",
                "immune_support": "Protein and vitamins support recovery",
                "avoid": ["Spicy food", "Dairy (if phlegm)", "Heavy foods"],
                "options": ["Congee", "Soft rice", "Scrambled eggs", "Soup", "Oatmeal"]
            }
        },
        "conversation_rules": [
            "RULE 1: Show genuine sympathy - acknowledge their discomfort is real",
            "RULE 2: Ask clarifying questions - fever level, symptom duration",
            "RULE 3: Validate their experience - normalize being sick",
            "RULE 4: Suggest progressively - start with drinks, then food",
            "RULE 5: Explain mechanism - WHY each suggestion helps",
            "RULE 6: Encourage recovery - remind about rest and fluids",
            "RULE 7: Know limits - suggest seeing doctor if severe"
        ],
        "follow_up_questions": [
            "How high is your fever?",
            "How long have you been sick?",
            "Can you swallow easily?",
            "Do you have any other symptoms?",
            "Are you able to eat solid food?"
        ],
        "empathetic_phrases": [
            "That sounds really uncomfortable",
            "Being sick is miserable",
            "Your body needs support right now",
            "Let's get you feeling better",
            "Rest is your priority right now"
        ]
    },

    # STRESS & PERFORMANCE ANXIETY
    "stress_exam": {
        "keywords": ["exam", "test", "study", "preparation", "deadline", "presentation", "interview", "competition", "evaluation", "nervous about presentation", "presentation", "tired", "exhausted", "worn out"],
        "severity_markers": {
            "mild": ["little nervous", "some pressure", "want to do well"],
            "moderate": ["stressed", "worried about result", "haven't studied enough"],
            "severe": ["panicking", "can't concentrate", "physically shaking", "haven't slept"]
        },
        "nutritional_rules": {
            "brain_food": "Omega-3s enhance focus and memory",
            "energy_sustaining": "Complex carbs provide steady energy without crashes",
            "mood_boosting": "Dark chocolate releases endorphins",
            "hydration": "Brain needs water to function optimally",
            "timing": {
                "before_exam": "Light meal 1-2 hours before, not heavy",
                "during_break": "Quick snack and water for energy",
                "after_exam": "Reward meal to celebrate effort"
            },
            "foods": {
                "protein": ["Salmon (omega-3)", "Eggs", "Chicken", "Greek yogurt", "Nuts"],
                "carbs": ["Whole grain bread", "Brown rice", "Oatmeal", "Sweet potato"],
                "mood": ["Dark chocolate", "Berries", "Banana (serotonin)", "Green tea"],
                "hydration": ["Water", "Fresh juice", "Herbal tea", "Coconut water"]
            }
        },
        "conversation_rules": [
            "RULE 1: Normalize exam stress - it's universal and shows you care",
            "RULE 2: Assess readiness - are they prepared or panicking?",
            "RULE 3: Provide calm reassurance - confidence is contagious",
            "RULE 4: Focus on fuel not prep - you can't cram now",
            "RULE 5: Suggest brain foods - specific nutritional benefits",
            "RULE 6: Encourage breaks - mental rest improves performance",
            "RULE 7: Motivate positively - remind of their capabilities"
        ],
        "follow_up_questions": [
            "When is your exam?",
            "How prepared do you feel?",
            "What subject is it?",
            "Have you eaten today?",
            "Are you getting enough sleep?"
        ],
        "empathetic_phrases": [
            "Exams are stressful for everyone",
            "Your anxiety shows you care about doing well",
            "You're more prepared than you think",
            "Let's fuel your brain for success",
            "You've got this"
        ]
    },

    # EMOTIONAL HEARTBREAK
    "heartbreak_breakup": {
        "keywords": ["breakup", "broke up", "broken up", "girlfriend", "boyfriend", "partner", "relationship", "dumped", "left me", "miss you", "alone now", "heartbreak", "love"],
        "severity_markers": {
            "recent": ["just happened", "today", "yesterday", "last night"],
            "acute": ["can't stop crying", "can't eat", "can't sleep", "in shock"],
            "processing": ["getting better slowly", "some days are harder", "thinking about them"],
            "healing": ["moving forward", "thinking of future", "ready to date"]
        },
        "nutritional_rules": {
            "endorphin_release": "Sugar and chocolate trigger feel-good chemicals",
            "emotional_support": "Comfort foods are psychologically soothing",
            "dopamine_boost": "Certain foods enhance mood naturally",
            "hydration": "Tears = dehydration, need fluids",
            "nutrition": {
                "comfort": ["Chocolate cake", "Ice cream", "Pizza", "Cookies", "Comfort pasta"],
                "mood_boost": ["Dark chocolate (serotonin)", "Strawberries (antioxidants)", "Bananas (mood)", "Warm soup"],
                "hydration": ["Water", "Tea", "Smoothies", "Juice"],
                "avoid": ["Too much alcohol", "Heavy foods", "Skipping meals"]
            }
        },
        "psychological_support": {
            "validation": "Their pain is REAL and valid - not weak",
            "normalization": "Everyone experiences heartbreak - they're not alone",
            "food_function": "Comfort food serves emotional healing purpose",
            "self_care": "Taking care of body supports mental healing"
        },
        "conversation_rules": [
            "RULE 1: Show deep empathy - heartbreak is serious pain",
            "RULE 2: DON'T minimize their feelings - ever",
            "RULE 3: Validate their grief - allow them to process",
            "RULE 4: Ask about support system - suggest reaching out",
            "RULE 5: Suggest comfort foods guilt-free - healing need",
            "RULE 6: Include hydration - tears cause dehydration",
            "RULE 7: Suggest movement/distraction - balance comfort with healing"
        ],
        "follow_up_questions": [
            "How long were you together?",
            "When did this happen?",
            "Do you want to talk about them or distract yourself?",
            "Are you eating and drinking?",
            "Who can you lean on right now?",
            "Do you have support around you?"
        ],
        "empathetic_phrases": [
            "I'm so sorry you're going through this",
            "Your pain is completely valid",
            "Heartbreak takes time to heal",
            "You will get through this",
            "It's okay to not be okay right now",
            "You deserve to take care of yourself"
        ]
    },

    # EXHAUSTION & BURNOUT
    "burnout_exhaustion": {
        "keywords": ["exhausted", "tired", "burnout", "burned out", "no energy", "running on fumes", "worn out", "drained", "fatigue", "sleep deprived"],
        "severity_markers": {
            "mild": ["tired today", "need rest", "not sleeping well"],
            "moderate": ["chronic fatigue", "affecting work", "irritable"],
            "severe": ["can't get out of bed", "depression", "physical symptoms", "considering quitting"]
        },
        "nutritional_rules": {
            "iron_restoration": "Iron carries oxygen to cells - needed for energy",
            "b_vitamins": "B vitamins convert food to energy",
            "protein_recovery": "Amino acids repair stressed system",
            "timing": {
                "immediate": "Quick energy: Banana, nuts, coffee",
                "meal": "Balanced: Protein + carbs + vegetables",
                "recovery": "Iron-rich: Red meat, spinach, legumes"
            },
            "foods": {
                "immediate_energy": ["Banana", "Almonds", "Coffee", "Orange juice"],
                "sustained_energy": ["Salmon (omega-3 + B12)", "Steak (iron + protein)", "Eggs", "Whole grains"],
                "recovery": ["Red meat", "Spinach", "Lentils", "Dark chocolate", "Nuts"],
                "avoid": ["Too much caffeine", "Sugary crash", "Skipping meals"]
            }
        },
        "conversation_rules": [
            "RULE 1: Validate burnout is real - not laziness",
            "RULE 2: Assess duration - acute vs chronic",
            "RULE 3: Suggest food AND rest - both needed",
            "RULE 4: Recommend breaks - mandatory recovery",
            "RULE 5: Explain nutritional restoration - specific mechanisms",
            "RULE 6: Encourage professional help if severe - know limits",
            "RULE 7: Normalize needing support - strength to ask"
        ],
        "follow_up_questions": [
            "How long have you been like this?",
            "Are you sleeping enough?",
            "When did you last take a real break?",
            "Are you eating regular meals?",
            "What's causing the burnout?",
            "Do you have support at work?"
        ],
        "empathetic_phrases": [
            "Burnout is real and serious",
            "Your exhaustion makes sense",
            "You need and deserve rest",
            "Let's restore your energy",
            "Taking care of yourself is not selfish",
            "You don't have to push through alone"
        ]
    },

    # SUCCESS & CELEBRATION
    "celebration_success": {
        "keywords": ["won", "passed", "got job", "promoted", "achieved", "succeeded", "great news", "excited", "happy", "celebrate", "proud", "made it"],
        "achievement_types": {
            "personal": ["got job", "promotion", "achieved goal", "finished project"],
            "academic": ["passed exam", "got good grade", "completed course"],
            "relationship": ["got married", "proposal", "anniversary"],
            "health": ["lost weight", "quit smoking", "ran marathon"]
        },
        "nutritional_rules": {
            "celebration_food": "Special occasion = treat yourself to premium options",
            "reward_psychology": "Nice food reinforces positive achievements",
            "shared_experience": "Often better to share celebration meal",
            "premium_options": {
                "fancy": ["Sushi", "Steak", "Lobster", "Fine dining"],
                "indulgent": ["Premium dessert", "Champagne", "Wine", "Cocktails"],
                "experiential": ["Try new restaurant", "Cuisine exploration", "Food adventure"]
            }
        },
        "conversation_rules": [
            "RULE 1: Match their excitement - genuine celebration",
            "RULE 2: Ask details - show real interest in their win",
            "RULE 3: Validate effort - they earned this",
            "RULE 4: Suggest premium food - honor the achievement",
            "RULE 5: Encourage sharing - suggest celebration with others",
            "RULE 6: Make it memorable - special meal for special moment",
            "RULE 7: Look forward - ask about next goal"
        ],
        "follow_up_questions": [
            "Tell me more! How are you feeling?",
            "How long did you work toward this?",
            "Who do you want to celebrate with?",
            "What's your favorite cuisine?",
            "What's next for you?"
        ],
        "empathetic_phrases": [
            "That's amazing! Congratulations!",
            "You absolutely deserve this",
            "Your hard work paid off",
            "This is worth celebrating big",
            "I'm genuinely happy for you",
            "You should be so proud"
        ]
    },

    # ANXIETY & NERVOUSNESS
    "anxiety_nervous": {
        "keywords": ["nervous", "anxious", "scared", "worried", "panic", "anxious about", "heart racing", "shaking", "can't sleep", "overthinking"],
        "trigger_types": {
            "performance": ["presentation", "meeting", "performance", "public speaking"],
            "social": ["party", "dating", "first date", "meeting new people"],
            "health": ["doctor visit", "test results", "surgery"],
            "life_change": ["new job", "moving", "starting school", "unknown"]
        },
        "nutritional_rules": {
            "calming": "Magnesium naturally calms nervous system",
            "stabilizing": "Complex carbs stabilize blood sugar = stable mood",
            "grounding": "Protein provides foundation/grounding",
            "avoiding": "Skip caffeine - makes anxiety worse",
            "foods": {
                "magnesium": ["Almonds", "Spinach", "Dark chocolate", "Pumpkin seeds"],
                "complex_carbs": ["Oatmeal", "Whole grain", "Sweet potato", "Brown rice"],
                "protein": ["Chicken", "Fish", "Eggs", "Beans"],
                "calming_drinks": ["Chamomile tea", "Peppermint tea", "Warm milk", "Herbal tea"],
                "avoid": ["Coffee", "Energy drinks", "Sugary foods"]
            }
        },
        "grounding_techniques": {
            "breathing": "Deep breathing calms nervous system",
            "food_grounding": "Eating grounds you in present moment",
            "support": "Knowing someone cares helps",
            "preparation": "Preparation reduces uncertainty = reduces anxiety"
        },
        "conversation_rules": [
            "RULE 1: Normalize nervousness - it's universal",
            "RULE 2: Validate their worry - don't dismiss",
            "RULE 3: Use calming tone - your calmness transfers",
            "RULE 4: Suggest grounding food - physical activity helps",
            "RULE 5: Teach calming mechanism - explain how food helps",
            "RULE 6: Build confidence - remind of their capability",
            "RULE 7: Encourage support - suggest reaching out"
        ],
        "follow_up_questions": [
            "What's the event/meeting about?",
            "How prepared are you?",
            "What's the worst thing that could happen?",
            "Have you done this before?",
            "When is it happening?",
            "Who will be there?"
        ],
        "empathetic_phrases": [
            "That nervousness is just adrenaline",
            "Even experts feel nervous",
            "Your preparation shows",
            "You're more ready than you think",
            "I believe in you",
            "You're going to do great"
        ]
    },

    # LONELINESS & ISOLATION
    "loneliness_isolation": {
        "keywords": ["lonely", "alone", "isolated", "no one", "by myself", "friend moved", "miss my friends", "isolated", "cut off"],
        "context_types": {
            "situational": ["new city", "new job", "remote work", "lockdown"],
            "relational": ["friends busy", "relationship ended", "moved away", "drifted"],
            "circumstantial": ["can't go out", "health issues", "transportation"]
        },
        "nutritional_rules": {
            "comfort_food": "Comfort foods provide emotional warmth",
            "ritual": "Meal preparation can be meditative",
            "connection": "Food often shared - suggest ordering with friend call",
            "mood_boost": "Certain foods naturally improve mood",
            "foods": {
                "comfort": ["Pizza", "Mac and cheese", "Cookies", "Ice cream"],
                "mood_boost": ["Chocolate", "Banana smoothie", "Warm soup"],
                "social": ["Pizza (call friend!)", "Tapas (share concept)", "Potluck ideas"]
            }
        },
        "psychological_support": {
            "validation": "Loneliness is real pain - not weakness",
            "normalization": "Most people feel lonely sometimes",
            "action": "Food + reaching out = healing",
            "self_compassion": "Treat yourself with kindness"
        },
        "conversation_rules": [
            "RULE 1: Validate loneliness is painful - not to be dismissed",
            "RULE 2: Avoid toxic positivity - acknowledge real pain",
            "RULE 3: Suggest both comfort AND connection",
            "RULE 4: Recommend reaching out - suggest specific people",
            "RULE 5: Suggest community activities - group meals, classes",
            "RULE 6: Normalize feeling this way - they're not alone",
            "RULE 7: Encourage self-care - treats and kindness to self"
        ],
        "follow_up_questions": [
            "How long have you been feeling this way?",
            "Is it the people or the lack of company?",
            "Who could you reach out to?",
            "What did you used to enjoy with friends?",
            "Is there a group or class you'd like to try?"
        ],
        "empathetic_phrases": [
            "Loneliness is a real pain",
            "You're not actually alone - I'm here",
            "Connection matters deeply",
            "Let's reach out together",
            "You deserve to feel connected",
            "This feeling can change"
        ]
    },

    # ANGER & FRUSTRATION
    "anger_frustration": {
        "keywords": ["angry", "furious", "mad", "angry at", "hate", "frustrated", "irritated", "pissed", "upset", "livid"],
        "trigger_types": {
            "interpersonal": ["person hurt me", "betrayal", "disrespect", "injustice"],
            "situational": ["things not working", "unfair treatment", "blocked goals"],
            "accumulated": ["building resentment", "keep happening", "fed up"]
        },
        "nutritional_rules": {
            "intensity_channeling": "Spicy/intense foods channel anger productively",
            "grounding": "Carbs help calm intense emotions",
            "physical": "Chewing/eating engages body = release",
            "avoid": "Don't skip meals - hunger increases anger",
            "foods": {
                "channel_intensity": ["Spicy food", "Grilled meat", "Hot pizza", "Intense flavors"],
                "grounding": ["Pasta", "Rice", "Bread", "Satisfying meals"],
                "avoid": ["Caffeine", "Energy drinks", "Alcohol"]
            }
        },
        "processing": {
            "validation": "Anger is valid reaction to injustice",
            "expression": "Safe outlets for anger (physical activity, food)",
            "processing": "Talk through what happened",
            "action": "Consider what action is appropriate"
        },
        "conversation_rules": [
            "RULE 1: Validate anger - it's often justified",
            "RULE 2: DON'T tell them to calm down - invalidates",
            "RULE 3: Ask what happened - let them vent",
            "RULE 4: Suggest physically satisfying food - channels intensity",
            "RULE 5: Recommend movement - exercise helps anger",
            "RULE 6: Discuss perspective - after they're calmer",
            "RULE 7: Support their autonomy - their choice what to do"
        ],
        "follow_up_questions": [
            "What happened?",
            "How are you feeling?",
            "Is this ongoing or one incident?",
            "What do you want to do about it?",
            "Do you need to vent or take action?"
        ],
        "empathetic_phrases": [
            "Your anger makes sense",
            "That's a valid reaction",
            "You have a right to be upset",
            "Let's channel this productively",
            "You're handling this well",
            "What do you need right now?"
        ]
    },

    # HANGOVER & RECOVERY
    "hangover_recovery": {
        "keywords": ["hangover", "drunk", "last night", "drank", "head hurts", "nauseous", "sick from alcohol", "regret drinking"],
        "severity": {
            "mild": ["slight headache", "tired", "queasy"],
            "moderate": ["bad headache", "nauseous", "can't move"],
            "severe": ["can't keep food down", "severe dehydration", "consider urgent care"]
        },
        "nutritional_rules": {
            "hydration_priority": "Dehydration IS the hangover - water is essential",
            "electrolytes": "Sodium and potassium replace what alcohol strips",
            "grease": "Fat slows alcohol absorption - helps stabilize",
            "carbs": "Replenish glucose depleted by alcohol",
            "foods": {
                "hydration": ["Water (most important)", "Coconut water", "Sports drink", "Fresh juice"],
                "electrolytes": ["Soup", "Broth", "Electrolyte drink", "Banana"],
                "food": ["Bacon and eggs", "Toast", "Greasy food", "Rice"],
                "timing": "Small frequent meals, not large one"
            }
        },
        "conversation_rules": [
            "RULE 1: No judgment - hangovers happen to everyone",
            "RULE 2: Prioritize hydration - this is THE cure",
            "RULE 3: Suggest greasy food - helps absorption",
            "RULE 4: Recommend light meals frequently - not heavy",
            "RULE 5: Include electrolytes - not just water",
            "RULE 6: Suggest rest - recovery takes time",
            "RULE 7: Gentle check-in - how bad is it really"
        ],
        "follow_up_questions": [
            "How are you feeling?",
            "Have you had water?",
            "Can you keep food down?",
            "What did you drink?",
            "How much sleep did you get?"
        ],
        "empathetic_phrases": [
            "Hangovers are rough",
            "You're not alone - happens to everyone",
            "This will pass",
            "Let's get you hydrated",
            "Be kind to yourself today",
            "You'll feel better soon"
        ]
    }
}

# UNIVERSAL CONVERSATION RULES - APPLY TO ALL SITUATIONS
UNIVERSAL_RULES = {
    "empathy": [
        "Start with genuine understanding of their situation",
        "Use their language and mirror their emotions",
        "Show you truly hear them - not dismissing or minimizing"
    ],
    "validation": [
        "Confirm their feelings are normal and understandable",
        "Share that others feel this way - they're not alone",
        "Never invalidate or say 'don't be sad/worried/etc'"
    ],
    "listening": [
        "Ask clarifying questions to understand context",
        "Let them share their full story",
        "Remember details for follow-up"
    ],
    "suggestion": [
        "Explain WHY each food/drink suggestion works",
        "Provide 2-3 options - let them choose",
        "Consider their practical situation (at home, at work, etc)"
    ],
    "explanation": [
        "Explain the nutritional or psychological mechanism",
        "Use simple language - science without jargon",
        "Make them understand the connection"
    ],
    "care": [
        "End with genuine concern for their wellbeing",
        "Offer continued support - you're here",
        "Include self-care suggestions beyond food"
    ],
    "boundaries": [
        "Recognize when situation needs professional help",
        "Suggest therapy/doctor if appropriate",
        "Don't overstep - you're a food companion, not therapist"
    ]
}

def get_deep_context(user_input):
    """
    Deeply analyze user input for context
    Returns: situation_type, severity, specific_context
    """
    user_lower = user_input.lower()
    
    matches = []
    
    for situation_type, data in DEEP_CONTEXT_ANALYSIS.items():
        for keyword in data["keywords"]:
            if keyword.lower() in user_lower:
                matches.append((situation_type, len(keyword)))
    
    if not matches:
        return None, 0, None
    
    matches.sort(key=lambda x: x[1], reverse=True)
    best_match = matches[0][0]
    
    return best_match, 100, DEEP_CONTEXT_ANALYSIS[best_match]


def build_contextual_response(situation_type, user_input):
    """
    Build contextually appropriate empathetic response
    Follows all rules 100%
    """
    if situation_type not in DEEP_CONTEXT_ANALYSIS:
        return None
    
    context = DEEP_CONTEXT_ANALYSIS[situation_type]
    
    return {
        "situation": situation_type,
        "empathy_phrases": context.get("empathetic_phrases", []),
        "follow_up_questions": context.get("follow_up_questions", []),
        "rules": context.get("conversation_rules", []),
        "nutritional_info": context.get("nutritional_rules", {}),
        "severity_markers": context.get("severity_markers", {}),
        "universal_rules": UNIVERSAL_RULES
    }


# TESTING
if __name__ == "__main__":
    test_cases = [
        "I've caught a cold and my throat hurts so bad I can barely swallow",
        "I have an exam tomorrow and I haven't studied enough. I'm panicking.",
        "My girlfriend broke up with me yesterday and I can't stop crying",
        "I'm so exhausted from work. I have no energy left. I feel burned out",
        "I just got promoted! I can't believe it! So excited!",
        "I'm really nervous about my presentation in 2 hours",
        "I feel so lonely since I moved to this new city",
        "I'm so angry at what happened. I can't even think straight",
        "Hangover is killing me. Everything hurts",
    ]
    
    print("=" * 80)
    print("DEEP CONTEXT ANALYSIS SYSTEM TEST")
    print("=" * 80)
    
    for test in test_cases:
        situation, confidence, context = get_deep_context(test)
        print(f"\nUser: {test}")
        print(f"Detected: {situation} (confidence: {confidence}%)")
        if context:
            response = build_contextual_response(situation, test)
            print(f"Rules to follow: {len(response['rules'])}")
            print(f"Sample rule: {response['rules'][0]}")
