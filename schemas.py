from pydantic import BaseModel, constr, validator
from typing import Optional, List
from datetime import datetime

class MoodRequest(BaseModel):
    text: constr(min_length=1, max_length=500)
    
    @validator('text')
    def validate_text(cls, v):
        if not isinstance(v, str):
            raise ValueError('Text must be string')
        if len(v.strip()) == 0:
            raise ValueError('Text cannot be empty')
        return v.strip()

class MoodResponse(BaseModel):
    mood: str
    confidence: float
    recommendations: List[dict]

class RecommendationResponse(BaseModel):
    id: str
    mood: str
    dishes: List[dict]
    confidence: float
    created_at: datetime

class UserRegister(BaseModel):
    email: constr(min_length=5, max_length=100)
    password: constr(min_length=8, max_length=100)

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
