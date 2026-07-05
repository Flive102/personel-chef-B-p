from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_user
from services.recommendation_service import recommendation_service

router = APIRouter()

@router.get("/mood/{mood}")
async def get_recommendations_by_mood(mood: str, user_id: str = Depends(get_current_user)):
    """Get recommendations for a specific mood"""
    try:
        recommendations = recommendation_service.get_recommendations(mood, limit=10)
        return {
            "mood": mood,
            "recommendations": recommendations,
            "user_id": user_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
