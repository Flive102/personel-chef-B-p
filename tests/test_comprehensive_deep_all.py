"""
DEEP COMPREHENSIVE TEST SUITE
Tests all emotions, situations, and real functions
Chunk 1/2 - Configuration & Emotion Tests
"""

import pytest
from mood_to_meal_butler.emotions_config import EMOTION_METADATA, EMOTION_KEYWORDS
from mood_to_meal_butler.situations_config import SITUATIONS
from mood_to_meal_butler.error_handler import validate_user_input, validate_emotion, ValidationError
from mood_to_meal_butler.interview import (
    get_interview_questions, parse_answer, get_health_suggestion
)
from mood_to_meal_butler.response_builder import (
    build_emotion_response, build_situation_response, validate_response
)


class TestEmotionMetadata:
    """Test all 14 emotions are configured."""
    
    def test_14_emotions_exist(self):
        """Verify 14 emotions configured."""
        assert len(EMOTION_METADATA) >= 14
    
    @pytest.mark.parametrize("emotion", list(EMOTION_METADATA.keys()))
    def test_emotion_has_metadata(self, emotion):
        """Test each emotion has metadata fields."""
        meta = EMOTION_METADATA[emotion]
        # Check for at least one of these fields
        assert any(k in meta for k in ["emoji", "greeting", "response_style"]), \
            f"Emotion {emotion} missing metadata"
    
    def test_sadness_emotion_exists(self):
        """Test sadness emotion."""
        assert "sadness" in EMOTION_METADATA
    
    def test_joy_emotion_exists(self):
        """Test joy emotion."""
        assert "joy" in EMOTION_METADATA
    
    def test_stress_emotion_exists(self):
        """Test stress emotion."""
        assert "stress" in EMOTION_METADATA
    
    def test_exhaustion_emotion_exists(self):
        """Test exhaustion emotion."""
        assert "exhaustion" in EMOTION_METADATA


class TestSituationConfiguration:
    """Test all 26+ situations."""
    
    def test_26_plus_situations(self):
        """Verify 26+ situations."""
        assert len(SITUATIONS) >= 26
    
    def test_breakfast_situation(self):
        """Test breakfast situation."""
        assert "breakfast" in SITUATIONS
    
    def test_lunch_situation(self):
        """Test lunch situation."""
        assert "lunch" in SITUATIONS
    
    def test_dinner_situation(self):
        """Test dinner situation."""
        assert "dinner" in SITUATIONS
    
    def test_diet_vegan_situation(self):
        """Test vegan situation."""
        assert "diet-vegan" in SITUATIONS
    
    def test_diet_keto_situation(self):
        """Test keto situation."""
        assert "diet-keto" in SITUATIONS
    
    def test_budget_friendly_situation(self):
        """Test budget-friendly situation."""
        assert "budget-friendly" in SITUATIONS
    
    def test_sick_day_situation(self):
        """Test sick-day situation."""
        assert "sick-day" in SITUATIONS


class TestInputValidation:
    """Test input validation."""
    
    def test_valid_input(self):
        """Test valid input passes."""
        result = validate_user_input("I am happy")
        assert result == "I am happy"
    
    def test_empty_input_fails(self):
        """Test empty input fails."""
        with pytest.raises(ValidationError):
            validate_user_input("")
    
    def test_too_long_input_fails(self):
        """Test long input fails."""
        with pytest.raises(ValidationError):
            validate_user_input("x" * 501, max_length=500)
    
    def test_emotion_validation(self):
        """Test emotion validation."""
        assert validate_emotion("sadness")
        assert validate_emotion("joy")
        assert validate_emotion("stress")
        assert validate_emotion("exhaustion")


class TestInterviewQuestions:
    """Test interview questions."""
    
    def test_get_questions_english(self):
        """Test getting questions in English."""
        questions = get_interview_questions("en")
        assert isinstance(questions, list)
        assert len(questions) > 0
    
    def test_questions_have_keys(self):
        """Test questions have required keys."""
        questions = get_interview_questions("en")
        for q in questions:
            assert "key" in q
            assert "question" in q


class TestResponseBuilding:
    """Test response building."""
    
    def test_emotion_response_sad(self):
        """Test sad emotion response."""
        response = build_emotion_response("sadness", [])
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_emotion_response_joy(self):
        """Test joy emotion response."""
        response = build_emotion_response("joy", [])
        assert isinstance(response, str)
    
    def test_situation_response(self):
        """Test situation response."""
        response = build_situation_response(["breakfast"], [])
        assert isinstance(response, str)


class TestHealthSuggestions:
    """Test health suggestions."""
    
    def test_health_suggestion_sad(self):
        """Test health suggestion for sad."""
        suggestion = get_health_suggestion("sad", "en")
        assert isinstance(suggestion, str)
        assert len(suggestion) > 0
    
    def test_health_suggestion_stressed(self):
        """Test health suggestion for stressed."""
        suggestion = get_health_suggestion("stressed", "en")
        assert isinstance(suggestion, str)
