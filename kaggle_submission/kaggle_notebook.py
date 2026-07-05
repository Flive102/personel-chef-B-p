# Mood-to-Meal Butler: AI Emotional Intelligence Meal Recommender
# Kaggle Notebook Demo
# This notebook demonstrates emotion detection and meal recommendation

import pandas as pd
import numpy as np
import json
from collections import Counter

# ========================
# CELL 1: LOAD DATASETS
# ========================
print("="*60)
print("MOOD-TO-MEAL BUTLER: AI Emotion Detection & Recommendation")
print("="*60)

# Load emotions config
emotions_df = pd.read_csv('/kaggle/input/datasets/drololol/personel-chef-bp/emotions_config.csv')
print(f"\n✅ Loaded {len(emotions_df)} emotion categories")
print(emotions_df[['emotion_category', 'emoji']].head(10))

# Load meals database
meals_df = pd.read_csv('/kaggle/input/datasets/drololol/personel-chef-bp/meals_database.csv')
print(f"\n✅ Loaded {len(meals_df)} curated meals")
print(meals_df[['name_en', 'emoji', 'cuisine', 'mood_tags']].head(10))

# Load interview questions
with open('/kaggle/input/datasets/drololol/personel-chef-bp/interview_questions.json') as f:
    questions = json.load(f)
print(f"\n✅ Loaded {len(questions['interview_questions'])} interview questions")

# ========================
# CELL 2: EMOTION DETECTION LOGIC
# ========================
print("\n" + "="*60)
print("EMOTION DETECTION ENGINE")
print("="*60)

def detect_emotion(text):
    """Auto-detect emotion from natural language"""
    emotions_dict = {}
    
    # Build emotion keywords from CSV
    for idx, row in emotions_df.iterrows():
        keywords = [k.strip() for k in row['keywords'].split(',')]
        emotions_dict[row['emotion_category']] = keywords
    
    text_lower = text.lower()
    
    # Check for emotion keywords (longest first to avoid false matches)
    for emotion, keywords in emotions_dict.items():
        for keyword in sorted(keywords, key=len, reverse=True):
            if keyword in text_lower:
                return emotion
    
    return None

# Test emotion detection
test_inputs = [
    "i am tired",
    "i'm feeling stressed",
    "i am happy",
    "feeling sad today",
    "i'm celebrating!",
    "just woke up, exhausted"
]

print("\n🎯 EMOTION DETECTION DEMO:")
for text in test_inputs:
    emotion = detect_emotion(text)
    print(f"  '{text}' → {emotion}")

# ========================
# CELL 3: MEAL RECOMMENDATION ENGINE
# ========================
print("\n" + "="*60)
print("MEAL RECOMMENDATION ENGINE")
print("="*60)

def get_meals_for_emotion(emotion, limit=9):
    """Get meals recommended for specific emotion"""
    matching_meals = meals_df[
        meals_df['mood_tags'].str.contains(emotion, case=False, na=False)
    ]
    return matching_meals.head(limit)

print("\n🍽️ SAMPLE RECOMMENDATIONS:")

emotions_to_demo = ['exhaustion', 'joy', 'stress', 'sadness']
for emotion in emotions_to_demo:
    meals = get_meals_for_emotion(emotion, limit=3)
    print(f"\n{emotion.upper()} - Recommended meals:")
    for idx, meal in meals.iterrows():
        print(f"  {meal['emoji']} {meal['name_en']} ({meal['cuisine']})")
        print(f"     Tags: {meal['health_tags']}")

# ========================
# CELL 4: COMPLETE CONVERSATION FLOW DEMO
# ========================
print("\n" + "="*60)
print("COMPLETE CONVERSATION FLOW DEMO")
print("="*60)

def recommend_meals(user_input, interview_answers=None):
    """Complete recommendation pipeline"""
    
    # Step 1: Detect emotion from user input
    detected_emotion = detect_emotion(user_input)
    
    if detected_emotion:
        print(f"\n✅ Emotion detected: {detected_emotion}")
        
        # Step 2: Get meal recommendations
        meals = get_meals_for_emotion(detected_emotion, limit=9)
        
        if len(meals) > 0:
            print(f"🍽️ Recommended {len(meals)} meals for {detected_emotion}:")
            for i, (idx, meal) in enumerate(meals.iterrows(), 1):
                print(f"\n{i}. {meal['emoji']} {meal['name_en']}")
                print(f"   Cuisine: {meal['cuisine']}")
                print(f"   Energy: {meal['energy_level']}")
                print(f"   Time: {meal['time_required']}")
                print(f"   Budget: {meal['budget']}")
                print(f"   Description: {meal['description']}")
            
            return meals
        else:
            return None
    else:
        print(f"\n❌ Could not detect emotion. Try: 'i am tired', 'i'm happy', etc.")
        return None

# Demo conversations
demo_inputs = [
    "i am tired after work",
    "i'm feeling happy today",
    "i'm so stressed right now"
]

for user_input in demo_inputs:
    print(f"\n{'='*60}")
    print(f"USER: {user_input}")
    recommend_meals(user_input)

# ========================
# CELL 5: STATISTICS & ANALYSIS
# ========================
print("\n" + "="*60)
print("DATASET STATISTICS")
print("="*60)

print(f"\n📊 Emotions: {len(emotions_df)}")
print(f"📊 Meals: {len(meals_df)}")
print(f"📊 Interview Questions: {len(questions['interview_questions'])}")

print(f"\n📊 Meals by Cuisine:")
cuisine_counts = meals_df['cuisine'].value_counts()
for cuisine, count in cuisine_counts.head(10).items():
    print(f"   {cuisine}: {count}")

print(f"\n📊 Meals by Budget:")
budget_counts = meals_df['budget'].value_counts()
for budget, count in budget_counts.items():
    print(f"   {budget}: {count}")

print(f"\n📊 Meals by Time Required:")
time_counts = meals_df['time_required'].value_counts()
for time_req, count in time_counts.items():
    print(f"   {time_req}: {count}")

print("\n" + "="*60)
print("✅ MOOD-TO-MEAL BUTLER DEMO COMPLETE")
print("="*60)
