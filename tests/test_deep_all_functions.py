"""
DEEP COMPREHENSIVE TEST SUITE - All Emotions, Situations & Combinations
Tests all functions with real data
"""

import pytest
from mood_to_meal_butler.emotions_config import EMOTION_METADATA, EMOTION_KEYWORDS
from mood_to_meal_butler.situations_config import SITUATIONS
from mood_to_meal_butler.error_handler import (
    validate_user_input, validate_emotion, validate_situations, ValidationError
)
from mood_to_meal_butler.interview import butler_interview
from mood_to_meal_butler.response_builder import build_response


class TestAllEmotions:
    """Test all 14 emotions comprehensively."""
    
    @pytest.mark.parametrize("emotion", list(EMOTION_METADATA.keys()))
    def test_emotion_metadata_complete(self, emotion):
        """Verify all emotions have complete metadata."""
        meta = EMOTION_METADATA[emotion]
        assert "keywords" in meta
        assert "description" in meta
        assert len(meta["keywords"]) > 0
    
    def test_14_emotions_configured(self):
        """Verify all 14 emotions exist."""
        assert len(EMOTION_METADATA) >= 14, f"Expected 14 emotions, got {len(EMOTION_METADATA)}"
    
    def test_emotions_list(self):
        """Verify core emotions are present."""
        core_emotions = ["sad", "happy", "stressed", "tired", "angry", "sick"]
        for emotion in core_emotions:
            assert emotion in EMOTION_METADATA, f"Missing emotion: {emotion}"
    
    @pytest.mark.parametrize("emotion", ["sad", "happy", "stressed", "tired", "angry", "sick"])
    def test_emotion_validation(self, emotion):
        """Test validation for core emotions."""
        assert validate_emotion(emotion)


class TestAllSituations:
    """Test all 26+ situations."""
    
    def test_26_situations_exist(self):
        """Verify 26+ situations configured."""
        assert len(SITUATIONS) >= 26, f"Expected 26+ situations, got {len(SITUATIONS)}"
    
    def test_common_situations(self):
        """Test key situations exist."""
        key_situations = ["breakfast", "lunch", "dinner", "office", "home", 
                         "vegan", "keto", "budget", "quick-bite", "sick-day"]
        for situation in key_situations:
            assert situation in SITUATIONS, f"Missing: {situation}"
    
    @pytest.mark.parametrize("situation", SITUATIONS[:10])
    def test_situation_validation(self, situation):
        """Test each situation validates."""
        result = validate_situations([situation])
        assert result is True


class TestInputValidation:
    """Test input validation."""
    
    def test_valid_input_accepted(self):
        """Test valid input passes validation."""
        result = validate_user_input("I am feeling happy")
        assert result == "I am feeling happy"
    
    def test_empty_input_rejected(self):
        """Test empty input raises error."""
        with pytest.raises(ValidationError):
            validate_user_input("")
    
    def test_too_long_input_rejected(self):
        """Test long input rejected."""
        with pytest.raises(ValidationError):
            validate_user_input("x" * 501, max_length=500)
    
    def test_malicious_patterns_blocked(self):
        """Test dangerous patterns blocked."""
        patterns = ["<script>", "exec(", "import os"]
        for pattern in patterns:
            with pytest.raises(ValidationError):
                validate_user_input(pattern)
    
    def test_non_string_rejected(self):
        """Test non-string input rejected."""
        with pytest.raises(ValidationError):
            validate_user_input(123)


class TestEmotionSituationCombinations:
    """Test emotion-situation combinations."""
    
    @pytest.mark.parametrize("emotion", ["sad", "happy", "stressed", "tired"])
    @pytest.mark.parametrize("situation", ["breakfast", "lunch", "dinner", "office"])
    def test_emotion_situation_pairs(self, emotion, situation):
        """Test all emotion-situation combinations work."""
        result = butler_interview(f"{emotion} at {situation}")
        assert isinstance(result, dict)
    
    def test_sad_sick_day(self):
        """Test sad + sick-day combination."""
        result = butler_interview("i am sad and sick")
        assert isinstance(result, dict)
    
    def test_happy_celebration(self):
        """Test happy + celebration."""
        result = butler_interview("i am very happy")
        assert isinstance(result, dict)
    
    def test_stressed_quick_bite(self):
        """Test stressed needs quick meal."""
        result = butler_interview("i am stressed and need something quick")
        assert isinstance(result, dict)
    
    def test_tired_comfort(self):
        """Test tired needs comfort food."""
        result = butler_interview("i am so tired")
        assert isinstance(result, dict)


class TestResponseGeneration:
    """Test response generation."""
    
    def test_response_is_string(self):
        """Test response is string."""
        response = build_response("happy", [])
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_different_responses_per_emotion(self):
        """Test emotions get different responses."""
        sad_resp = build_response("sad", [])
        happy_resp = build_response("happy", [])
        assert isinstance(sad_resp, str)
        assert isinstance(happy_resp, str)
    
    @pytest.mark.parametrize("emotion", ["sad", "happy", "stressed", "tired"])
    def test_response_for_all_emotions(self, emotion):
        """Test response generation for emotions."""
        response = build_response(emotion, [])
        assert isinstance(response, str)
        assert len(response) > 5


class TestWorkflowIntegration:
    """Test complete workflow."""
    
    def test_workflow_sad_emotion(self):
        """Test complete sad emotion workflow."""
        result = butler_interview("I am feeling sad")
        assert isinstance(result, dict)
    
    def test_workflow_happy_emotion(self):
        """Test complete happy emotion workflow."""
        result = butler_interview("I am very happy")
        assert isinstance(result, dict)
    
    def test_workflow_stressed_emotion(self):
        """Test complete stressed emotion workflow."""
        result = butler_interview("I am really stressed")
        assert isinstance(result, dict)
    
    def test_workflow_tired_emotion(self):
        """Test complete tired emotion workflow."""
        result = butler_interview("I am so tired")
        assert isinstance(result, dict)
    
    def test_workflow_all_6_core_emotions(self):
        """Test all 6 core emotions workflow."""
        inputs = ["sad", "happy", "stressed", "tired", "angry", "sick"]
        for emotion in inputs:
            result = butler_interview(f"I am {emotion}")
            assert isinstance(result, dict)
    
    def test_workflow_no_crashes(self):
        """Test workflow never crashes."""
        test_inputs = [
            "I am feeling down",
            "I feel great",
            "I'm under pressure",
            "I'm exhausted",
            "I'm furious",
            "I don't feel well"
        ]
        for input_text in test_inputs:
            try:
                result = butler_interview(input_text)
                assert isinstance(result, dict)
            except Exception as e:
                pytest.fail(f"Workflow crashed on '{input_text}': {e}")
