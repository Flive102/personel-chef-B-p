from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from services.mood_service import mood_service
from auth import get_current_user
from middleware import log_api_call, limiter

router = APIRouter()


class MoodRequest(BaseModel):
    text: str


class MoodResponse(BaseModel):
    mood: str
    confidence: float
    conversation: str
    recommendations: Optional[list] = []
    structured_response: Optional[Dict[str, Any]] = {}


@router.post("/detect", response_model=MoodResponse)
@limiter.limit("10/minute")
async def detect_mood(request: MoodRequest, user_id: str = Depends(get_current_user)):
    """Detect mood from user input with full conversation and recommendations"""
    try:
        # Get full mood detection with conversation
        mood_result = mood_service.detect(request.text)
        
        mood = mood_result.get("mood", "general_unknown")
        confidence = mood_result.get("confidence", 0.0)
        conversation = mood_result.get("conversation", "")
        structured_response = mood_result.get("structured_response", {})
        
        # Extract recommendations from structured response if available
        recommendations = []
        if structured_response and structured_response.get("step_4_recommendation"):
            rec_data = structured_response.get("step_4_recommendation", {})
            suggestions = rec_data.get("suggestions", {})
            if "food" in suggestions:
                recommendations.extend(suggestions.get("food", []))
            if "drinks" in suggestions:
                recommendations.extend(suggestions.get("drinks", []))
        
        log_api_call(user_id, "/api/mood/detect", mood, "success")
        
        return MoodResponse(
            mood=mood,
            confidence=confidence,
            conversation=conversation,
            recommendations=recommendations,
            structured_response=structured_response
        )
    
    except Exception as e:
        log_api_call(user_id, "/api/mood/detect", None, "error")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mood/{mood}")
async def get_recommendations_by_mood(mood: str, user_id: str = Depends(get_current_user)):
    """Get recommendations for a specific mood"""
    try:
        from services.recommendation_service import recommendation_service
        
        recommendations = recommendation_service.get_recommendations(mood)
        
        log_api_call(user_id, f"/api/mood/{mood}", mood, "success")
        
        return {
            "mood": mood,
            "recommendations": recommendations,
            "user_id": user_id
        }
    except Exception as e:
        log_api_call(user_id, f"/api/mood/{mood}", None, "error")
        raise HTTPException(status_code=500, detail=str(e))
