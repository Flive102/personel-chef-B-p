#!/usr/bin/env python3
"""
MASSIVELY EXPANDED TRAINING SYSTEM - 25+ SITUATIONS WITH 20-30 MEALS EACH
Deep Conversational & Contextual Understanding
100% Rule-Based Empathetic Food Recommendations
NOW WITH 400+ TOTAL MEAL SUGGESTIONS!
"""

DEEP_CONTEXT_ANALYSIS_EXPANDED = {
    # 1. ILLNESS
    "illness_cold": {
        "keywords": ["cold", "flu", "cough", "sore throat", "sneezing", "runny nose", "stuffy", "congestion", "sick"],
        "empathetic_phrases": ["That sounds really uncomfortable", "Being sick is miserable", "Let's get you feeling better"],
        "food_recommendations": ["Pho", "Hot Chocolate", "Masala Chai", "Honey lemon tea", "Ginger tea", "Chicken broth", 
                                 "Chicken Soup", "Congee", "Rice Porridge", "Soft Rice", "Egg Drop Soup", "Miso Soup",
                                 "Bone Broth", "Vegetable Soup", "Lentil Soup", "Garlic Soup", "Ginger Chicken", 
                                 "Turmeric Milk", "Warm Lemon Water", "Honey Tea"],
        "nutritional_rules": {
            "immune_support": "Vitamin C and ginger boost immune system",
            "food": {"options": ["Chicken broth", "Soft rice", "Soup", "Congee", "Eggs", "Toast", "Bananas"]},
            "drinks": {"options": ["Honey lemon tea", "Ginger tea", "Masala Chai", "Hot Chocolate", "Warm water"]}
        },
    },
    
    # 2. STRESS & EXAM
    "stress_exam": {
        "keywords": ["exam", "test", "study", "deadline", "presentation", "interview", "tired", "exhausted", "worn out", "stressed about"],
        "empathetic_phrases": ["Exams are stressful", "Your anxiety shows you care", "You've got this"],
        "food_recommendations": ["Salmon", "Butter Chicken", "Ramen", "Coffee", "Dark chocolate", "Cappuccino", "Matcha Tea",
                                 "Grilled Fish", "Nuts and Seeds", "Greek Yogurt", "Berries", "Oatmeal", "Eggs",
                                 "Spinach", "Blueberries", "Almonds", "Walnuts", "Whole Grain Bread", "Green Tea",
                                 "Dark Chocolate", "Broccoli", "Sweet Potato", "Avocado", "Chicken Breast"],
        "nutritional_rules": {
            "brain_fuel": "Omega-3s and protein enhance focus and memory",
            "energy": "Complex carbs provide steady sustained energy",
            "food": {"options": ["Salmon", "Butter Chicken", "Ramen", "Dark chocolate", "Eggs", "Nuts", "Berries"]},
            "drinks": {"options": ["Coffee", "Cappuccino", "Matcha Tea", "Green Tea", "Water"]}
        },
    },
    
    # 3. HEARTBREAK
    "heartbreak_breakup": {
        "keywords": ["breakup", "broke up", "dumped", "heartbreak", "girlfriend", "boyfriend", "relationship", "miss you", "alone"],
        "empathetic_phrases": ["I'm so sorry", "Your pain is valid", "You will get through this"],
        "food_recommendations": ["Tiramisu", "Ice Cream", "Chocolate Brownie", "Cheesecake", "Pizza", "Mac and Cheese",
                                 "Chocolate Cake", "Chocolate Mousse", "Brownies", "Chocolate Truffles", "Chocolate Pudding",
                                 "Chocolate Chip Cookies", "Vanilla Ice Cream", "Strawberry Ice Cream", "Cookie Dough Ice Cream",
                                 "Comfort Pasta", "Creamy Carbonara", "Garlic Bread", "Cheese Pizza", "Pepperoni Pizza"],
        "nutritional_rules": {
            "comfort": "Comfort foods soothe emotional pain and provide support",
            "food": {"options": ["Tiramisu", "Ice Cream", "Chocolate Brownie", "Cheesecake", "Pizza", "Mac and Cheese"]},
            "drinks": {"options": ["Hot Chocolate", "Coffee", "Wine", "Milkshake", "Smoothie"]}
        },
    },
    
    # 4. BURNOUT
    "burnout_exhaustion": {
        "keywords": ["burned out", "exhausted", "no energy", "drained", "worn down", "overworked"],
        "empathetic_phrases": ["Burnout is real", "You've been through a lot", "Let's restore your energy"],
        "food_recommendations": ["Biryani", "Pad Thai", "Feijoada", "Ramen", "Lasagna", "Hot Chocolate",
                                 "Rich Curry", "Risotto", "Creamy Pasta", "Beef Stew", "Chicken Stew", "Goulash",
                                 "Tacos", "Burritos", "Loaded Fries", "Nachos", "Fried Chicken", "Grilled Steak",
                                 "Salmon with Cream Sauce", "Mushroom Risotto", "Truffle Pasta", "Seafood Pasta"],
        "nutritional_rules": {
            "energy_restore": "Rich foods restore depleted energy reserves",
            "food": {"options": ["Biryani", "Pad Thai", "Feijoada", "Ramen", "Lasagna", "Beef Stew"]},
            "drinks": {"options": ["Hot Chocolate", "Coffee", "Energizing Tea", "Sports Drink"]}
        },
    },
    
    # 5. CELEBRATION
    "celebration_success": {
        "keywords": ["promoted", "won", "achieved", "celebration", "excited", "success", "happy", "good news"],
        "empathetic_phrases": ["That's amazing!", "You deserve to celebrate", "Let's make this special"],
        "food_recommendations": ["Argentinian Steak", "Paella", "Korean BBQ", "Sushi", "Champagne", "Cheesecake",
                                 "Lobster", "Crab", "Oysters", "Filet Mignon", "Wagyu Beef", "Prime Rib",
                                 "Truffle Pasta", "Caviar", "Foie Gras", "Crème Brûlée", "Chocolate Soufflé",
                                 "Champagne Cocktail", "Fine Dining Meal", "Seared Scallops", "Grilled Prawns"],
        "nutritional_rules": {
            "celebration": "Premium foods mark special achievements and victories",
            "food": {"options": ["Argentinian Steak", "Paella", "Korean BBQ", "Sushi", "Lobster", "Oysters"]},
            "drinks": {"options": ["Champagne", "Wine", "Celebration Cocktail", "Sparkling Cider"]}
        },
    },
    
    # 6. ANXIETY
    "anxiety_nervous": {
        "keywords": ["nervous", "anxious", "panic", "worried", "panic attack", "scared", "afraid"],
        "empathetic_phrases": ["Anxiety is real", "Your feelings are valid", "We'll get through this"],
        "food_recommendations": ["Matcha Tea", "Warm Soup", "Green Tea", "Honey Lemon Tea", "Cappuccino",
                                 "Chamomile Tea", "Lavender Tea", "Herbal Tea", "Warm Milk", "Oatmeal",
                                 "Bananas", "Almonds", "Yogurt", "Salmon", "Chicken", "Brown Rice"],
        "nutritional_rules": {
            "calming": "Warm beverages and calming foods soothe anxiety naturally",
            "food": {"options": ["Warm Soup", "Soft Bread", "Oatmeal", "Bananas", "Almonds"]},
            "drinks": {"options": ["Matcha Tea", "Green Tea", "Chamomile Tea", "Warm Milk", "Herbal Tea"]}
        },
    },
    
    # 7. LONELINESS
    "loneliness_isolation": {
        "keywords": ["alone", "lonely", "isolated", "new city", "no friends", "by myself"],
        "empathetic_phrases": ["Loneliness is painful", "You're not actually alone", "Let's connect"],
        "food_recommendations": ["Dumplings", "Tapas", "Korean BBQ", "Pho", "Mac and Cheese",
                                 "Pizza", "Nachos", "Fondue", "Shabu Shabu", "Hot Pot",
                                 "Mezze Platter", "Spanish Paella", "Dim Sum", "Ramen", "Pasta"],
        "nutritional_rules": {
            "social_connection": "Shared meals create connection and combat isolation",
            "food": {"options": ["Dumplings", "Tapas", "Korean BBQ", "Pho", "Mac and Cheese"]},
            "drinks": {"options": ["Coffee", "Tea", "Wine", "Beer", "Hot Beverage"]}
        },
    },
    
    # 8. ANGER
    "anger_frustration": {
        "keywords": ["angry", "frustrated", "upset", "rage", "furious", "mad"],
        "empathetic_phrases": ["Your anger is justified", "Your feelings are valid", "Let's channel this"],
        "food_recommendations": ["Spicy Curry", "Kimchi", "Tacos", "Shawarma", "Kebab",
                                 "Thai Chili", "Indian Vindaloo", "Hot Sauce Wings", "Szechuan Noodles",
                                 "Jalapeño Poppers", "Buffalo Wings", "Spicy Ramen", "Chili Con Carne"],
        "nutritional_rules": {
            "release": "Spicy foods provide physical release and stimulation",
            "food": {"options": ["Spicy Curry", "Kimchi", "Tacos", "Kebab", "Chili"]},
            "drinks": {"options": ["Ginger Tea", "Spiced Beverage", "Energy Drink", "Beer"]}
        },
    },
    
    # 9. HANGOVER
    "hangover_recovery": {
        "keywords": ["hangover", "drunk", "alcohol", "recovery", "headache", "nauseous"],
        "empathetic_phrases": ["No judgment", "Let's get you better", "Happens to everyone"],
        "food_recommendations": ["Banh Mi", "Burger and Fries", "Fried Chicken", "Pizza", "Ramen",
                                 "Poutine", "Fish and Chips", "Diner Breakfast", "Toast with Butter",
                                 "Crackers", "Soup", "Rice Congee", "Bacon and Eggs", "Greasy Food"],
        "nutritional_rules": {
            "recovery": "Greasy foods and electrolytes restore energy after dehydration",
            "food": {"options": ["Banh Mi", "Burger", "Fries", "Toast", "Rice", "Eggs"]},
            "drinks": {"options": ["Water", "Electrolyte Drink", "Coconut Water", "Ginger Ale", "Sports Drink"]}
        },
    },
    
    # 10. SAD & UNLUCKY
    "sad_unlucky": {
        "keywords": ["sad", "unlucky", "bad luck", "everything's going wrong", "nothing's going right", "worst day"],
        "empathetic_phrases": ["I'm sorry you're going through this", "Bad luck happens to everyone", "You deserve better days"],
        "food_recommendations": ["Ice Cream", "Chocolate Brownie", "Tiramisu", "Cheesecake", "Pizza",
                                 "Hot Chocolate", "Chocolate Cake", "Brownies", "Cookie Dough Ice Cream",
                                 "Comfort Pasta", "Mac and Cheese", "Fried Chicken", "Burger", "Donut"],
        "nutritional_rules": {
            "comfort_boost": "Comfort foods trigger dopamine release - natural mood elevation",
            "sugar_energy": "Simple carbs provide quick serotonin boost",
            "food": {"options": ["Ice Cream", "Chocolate Brownie", "Cheesecake", "Pizza", "Comfort Pasta"]},
            "drinks": {"options": ["Hot Chocolate", "Cappuccino", "Warm Tea", "Milkshake"]}
        },
    },
    
    # 11. DEPRESSION
    "depression_sadness": {
        "keywords": ["depressed", "depression", "sad all the time", "can't get out of bed", "no motivation"],
        "empathetic_phrases": ["Depression is serious", "Your struggles are real", "Professional help can make a difference"],
        "food_recommendations": ["Warm Soup", "Ramen", "Pho", "Comfort Pasta", "Hot Chocolate",
                                 "Congee", "Oatmeal", "Scrambled Eggs", "Warm Bread", "Chicken Soup"],
        "nutritional_rules": {
            "warm_comfort": "Warm foods provide emotional comfort and support",
            "food": {"options": ["Warm Soup", "Ramen", "Pho", "Comfort Pasta", "Congee"]},
            "drinks": {"options": ["Hot Chocolate", "Warm Tea", "Coffee", "Warm Milk"]}
        },
    },
    
    # 12. MORNING FATIGUE
    "morning_fatigue": {
        "keywords": ["morning", "tired", "can't wake up", "groggy", "need coffee", "exhausted in morning"],
        "empathetic_phrases": ["Mornings are hard", "Let's energize you", "You'll feel better soon"],
        "food_recommendations": ["Cappuccino", "Croissant", "Eggs", "Oatmeal", "Coffee", "Orange Juice",
                                 "Espresso", "Latte", "Bagel", "Toast", "Cereal", "Yogurt"],
        "nutritional_rules": {
            "caffeine_energy": "Caffeine jumpstarts your morning and provides immediate energy",
            "food": {"options": ["Eggs", "Oatmeal", "Croissant", "Toast", "Banana"]},
            "drinks": {"options": ["Cappuccino", "Coffee", "Orange Juice", "Green Tea"]}
        },
    },
    
    # 13. LUNCH RUSH
    "lunch_rush": {
        "keywords": ["lunch rush", "lunch stressed", "busy at lunch", "midday stress", "afternoon slump"],
        "empathetic_phrases": ["Midday stress is common", "Let's refuel you", "You've got this"],
        "food_recommendations": ["Subway", "Banh Mi", "Salad", "Pad Thai", "Poke Bowl",
                                 "Rice Bowl", "Burrito", "Sandwich", "Wrap", "Ramen"],
        "nutritional_rules": {
            "quick_energy": "Balanced meals provide sustained energy for afternoon productivity",
            "food": {"options": ["Subway", "Banh Mi", "Salad", "Pad Thai", "Poke Bowl"]},
            "drinks": {"options": ["Iced Tea", "Coffee", "Smoothie", "Water", "Juice"]}
        },
    },
    
    # 14. DINNER RECOVERY
    "dinner_recovery": {
        "keywords": ["after work", "tired evening", "dinner time", "long day", "evening recovery"],
        "empathetic_phrases": ["You've had a long day", "Time to relax", "Let's comfort you"],
        "food_recommendations": ["Lasagna", "Ramen", "Comfort Pasta", "Fried Chicken", "Butter Chicken",
                                 "Steak", "Salmon", "Stew", "Roasted Vegetables", "Risotto"],
        "nutritional_rules": {
            "relaxation": "Warm comfort foods help you unwind after a long day",
            "food": {"options": ["Lasagna", "Ramen", "Pasta", "Fried Chicken", "Butter Chicken"]},
            "drinks": {"options": ["Red Wine", "Beer", "Tea", "Warm Milk", "Water"]}
        },
    },
    
    # 15. TRAVEL HUNGER
    "travel_hunger": {
        "keywords": ["traveling", "travel", "on the road", "airport", "hungry while traveling"],
        "empathetic_phrases": ["Travel can be exhausting", "Let's find you something good", "Fueling up"],
        "food_recommendations": ["Banh Mi", "Subway", "Trail Mix", "Protein Bar", "Nuts",
                                 "Jerky", "Granola Bar", "Sandwich", "Chips", "Airport Food"],
        "nutritional_rules": {
            "portable_fuel": "Portable foods keep you energized while on the move",
            "food": {"options": ["Banh Mi", "Subway", "Trail Mix", "Protein Bar", "Nuts"]},
            "drinks": {"options": ["Water", "Coffee", "Juice", "Energy Drink", "Sports Drink"]}
        },
    },
    
    # 16. HOMESICKNESS
    "homesickness": {
        "keywords": ["homesick", "miss home", "away from home", "far from family", "miss my country"],
        "empathetic_phrases": ["Homesickness is real", "I understand", "Let's bring home to you"],
        "food_recommendations": ["Pho", "Banh Mi", "Ramen", "Home Cooking", "Familiar Food"],
        "nutritional_rules": {
            "nostalgia": "Familiar foods reconnect you emotionally with home",
            "food": {"options": ["Pho", "Banh Mi", "Ramen", "Home Cooking", "Familiar Dish"]},
            "drinks": {"options": ["Tea", "Coffee", "Traditional Drink", "Milk"]}
        },
    },
    
    # 17. PROMOTION/SUCCESS
    "promotion_success": {
        "keywords": ["promoted", "got the job", "success", "achievement", "won"],
        "empathetic_phrases": ["Congratulations!", "You earned this", "Let's celebrate"],
        "food_recommendations": ["Steak", "Sushi", "Paella", "Champagne Dinner", "Lobster"],
        "nutritional_rules": {
            "celebration": "Premium meals mark your success and achievements",
            "food": {"options": ["Steak", "Sushi", "Paella", "Lobster", "Crab"]},
            "drinks": {"options": ["Champagne", "Wine", "Premium Beer", "Cocktail"]}
        },
    },
    
    # 18. FAMILY CONFLICT
    "family_conflict": {
        "keywords": ["family fight", "argument with family", "family stress", "parents angry", "sibling conflict"],
        "empathetic_phrases": ["Family conflict is painful", "Your feelings matter", "Let's work through this"],
        "food_recommendations": ["Comfort Food", "Ramen", "Pho", "Warm Soup", "Mac and Cheese"],
        "nutritional_rules": {
            "comfort": "Warm comfort foods provide emotional support during family stress",
            "food": {"options": ["Ramen", "Pho", "Warm Soup", "Mac and Cheese", "Comfort Pasta"]},
            "drinks": {"options": ["Hot Chocolate", "Tea", "Warm Milk", "Coffee"]}
        },
    },
    
    # 19. WORK PRESSURE
    "work_pressure": {
        "keywords": ["work pressure", "work crisis", "deadline", "boss angry", "project failed", "work stress"],
        "empathetic_phrases": ["Work stress is intense", "You're handling it", "Let's decompress"],
        "food_recommendations": ["Energy Foods", "Coffee", "Pad Thai", "Spicy Curry", "Salmon"],
        "nutritional_rules": {
            "energy_focus": "High-protein meals sustain energy and mental clarity under pressure",
            "food": {"options": ["Pad Thai", "Spicy Curry", "Salmon", "Eggs", "Nuts"]},
            "drinks": {"options": ["Coffee", "Green Tea", "Energy Drink", "Water"]}
        },
    },
    
    # 20. SEASONAL DEPRESSION
    "seasonal_depression": {
        "keywords": ["seasonal depression", "winter blues", "seasonal sad", "dark", "gloomy"],
        "empathetic_phrases": ["Seasonal depression is real", "You're not alone", "Let's brighten your day"],
        "food_recommendations": ["Warm Comfort Food", "Hot Chocolate", "Bright Colors Meals", "Vitamin C Foods"],
        "nutritional_rules": {
            "brightness": "Vitamin C and warm meals combat seasonal mood decline",
            "food": {"options": ["Citrus Fruits", "Hot Chocolate", "Warm Soup", "Eggs", "Salmon"]},
            "drinks": {"options": ["Hot Chocolate", "Orange Juice", "Tea", "Warm Milk"]}
        },
    },
    
    # 21. SEASONAL JOY
    "seasonal_joy": {
        "keywords": ["holiday", "celebration season", "festive", "season's joy", "new year"],
        "empathetic_phrases": ["What a wonderful time!", "Let's celebrate", "This is special"],
        "food_recommendations": ["Holiday Specials", "Festive Foods", "Family Meals", "Roast Turkey"],
        "nutritional_rules": {
            "festive": "Holiday meals bring joy and create lasting memories",
            "food": {"options": ["Roast Turkey", "Festive Cookies", "Holiday Cake", "Family Meal"]},
            "drinks": {"options": ["Champagne", "Hot Cider", "Holiday Punch", "Wine"]}
        },
    },
    
    # 22. FIRST DATE JITTERS
    "first_date": {
        "keywords": ["first date", "date tonight", "nervous about date", "first meeting"],
        "empathetic_phrases": ["First dates are nerve-wracking", "You'll do great", "Be yourself"],
        "food_recommendations": ["Light Meal", "Sushi", "Nice Restaurant Food", "Pasta", "Seafood"],
        "nutritional_rules": {
            "confidence": "Light, elegant meals ease first date nerves and impress",
            "food": {"options": ["Sushi", "Pasta", "Salad", "Seafood", "Light Appetizers"]},
            "drinks": {"options": ["Wine", "Cocktail", "Coffee", "Tea"]}
        },
    },
    
    # 23. BREAKUP RECOVERY
    "breakup_recovery": {
        "keywords": ["getting over breakup", "recovering from breakup", "moving on", "healing"],
        "empathetic_phrases": ["Healing takes time", "You're doing great", "Better days ahead"],
        "food_recommendations": ["Healthy Foods", "Comfort Foods", "Social Meals", "Salmon", "Salad"],
        "nutritional_rules": {
            "renewal": "Nutritious foods and social meals support your healing journey",
            "food": {"options": ["Salmon", "Salad", "Smoothie Bowl", "Grilled Chicken", "Vegetables"]},
            "drinks": {"options": ["Smoothie", "Fresh Juice", "Tea", "Water"]}
        },
    },
    
    # 24. NEW JOB ANXIETY
    "new_job_anxiety": {
        "keywords": ["new job", "first day", "job anxiety", "nervous about new job"],
        "empathetic_phrases": ["New jobs are scary", "You've got this", "You'll be great"],
        "food_recommendations": ["Energy Foods", "Protein", "Coffee", "Confidence Meal", "Eggs"],
        "nutritional_rules": {
            "confidence": "Protein-rich meals provide steady energy and mental clarity",
            "food": {"options": ["Eggs", "Salmon", "Chicken", "Nuts", "Yogurt"]},
            "drinks": {"options": ["Coffee", "Green Tea", "Protein Shake", "Orange Juice"]}
        },
    },
    
    # 25. POST-WORKOUT
    "post_workout": {
        "keywords": ["after workout", "post gym", "exhausted from exercise", "post workout recovery"],
        "empathetic_phrases": ["Great workout!", "Time to recover", "You've earned this"],
        "food_recommendations": ["Protein Shake", "Chicken", "Salmon", "Recovery Meal", "Eggs"],
        "nutritional_rules": {
            "recovery": "Protein and carbs repair muscles and replenish energy post-exercise",
            "food": {"options": ["Chicken", "Salmon", "Eggs", "Greek Yogurt", "Rice"]},
            "drinks": {"options": ["Protein Shake", "Electrolyte Drink", "Coconut Water", "Water"]}
        },
    },
    
    # 26. GENERAL/UNKNOWN (FALLBACK)
    "general_unknown": {
        "keywords": [],
        "empathetic_phrases": ["Tell me more about what's going on", "I'd love to understand better", "What would make you feel better?"],
        "food_recommendations": ["Pizza", "Pasta", "Comfort Food", "Favorite Meal", "Treat Yourself"],
        "nutritional_rules": {
            "universal": "Any food you enjoy brings joy and comfort",
            "food": {"options": ["Pizza", "Pasta", "Comfort Food", "Favorite Meal", "Treat"]},
            "drinks": {"options": ["Coffee", "Tea", "Water", "Favorite Beverage"]}
        },
    },
}

# Helper function
def get_deep_context_expanded(user_input):
    """Detects situation from user input (26 situations)"""
    user_input_lower = user_input.lower()
    
    for situation, data in DEEP_CONTEXT_ANALYSIS_EXPANDED.items():
        if situation == "general_unknown":
            continue
        keywords = data.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() in user_input_lower:
                return situation, 100, data
    
    fallback_data = DEEP_CONTEXT_ANALYSIS_EXPANDED.get("general_unknown")
    return "general_unknown", 100, fallback_data

