from sqlalchemy import Column, String, DateTime, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), index=True)
    mood = Column(String, index=True)
    dishes = Column(JSON)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
