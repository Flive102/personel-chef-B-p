import pytest
from services.mood_service import MoodService

@pytest.fixture
def mood_service_instance():
    return MoodService()

def test_detect_happy_mood(mood_service_instance):
    result = mood_service_instance.detect("I'm so happy today!")
    assert result["confidence"] >= 0
    assert isinstance(result["mood"], str)

def test_detect_sad_mood(mood_service_instance):
    result = mood_service_instance.detect("I'm sad and unlucky")
    assert result["confidence"] >= 0

def test_detect_unknown_mood(mood_service_instance):
    result = mood_service_instance.detect("xyzabc qwerty")
    assert result["mood"] == "general_unknown"

def test_empty_input(mood_service_instance):
    result = mood_service_instance.detect("")
    assert result["mood"] == "general_unknown"

def test_none_input(mood_service_instance):
    result = mood_service_instance.detect(None)
    assert result["mood"] == "general_unknown"

def test_case_insensitivity(mood_service_instance):
    result1 = mood_service_instance.detect("HAPPY")
    result2 = mood_service_instance.detect("happy")
    assert result1["mood"] == result2["mood"]
