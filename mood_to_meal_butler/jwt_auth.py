"""
JWT Authentication Module for mood-to-meal-butler
Handles token generation, validation, and refresh
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import jwt
import os
from functools import wraps
from flask import request, jsonify


# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


class JWTError(Exception):
    """Base exception for JWT errors."""
    pass


class TokenExpiredError(JWTError):
    """Token has expired."""
    pass


class InvalidTokenError(JWTError):
    """Token is invalid."""
    pass


def create_access_token(user_id: str, additional_claims: Dict = None) -> str:
    """
    Generate JWT access token.
    
    Args:
        user_id: Unique user identifier
        additional_claims: Extra claims to include in token
    
    Returns:
        Signed JWT token string
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.utcnow(),
        "type": "access"
    }
    
    if additional_claims:
        payload.update(additional_claims)
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def create_refresh_token(user_id: str) -> str:
    """
    Generate JWT refresh token.
    
    Args:
        user_id: Unique user identifier
    
    Returns:
        Signed JWT refresh token string
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "iat": datetime.utcnow(),
        "type": "refresh"
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str) -> Tuple[bool, Dict]:
    """
    Verify JWT token validity.
    
    Args:
        token: JWT token string to verify
    
    Returns:
        Tuple of (is_valid, payload_dict)
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return False, {"error": "Invalid token"}


def get_token_from_request() -> Optional[str]:
    """
    Extract JWT token from request header.
    
    Expected format: Authorization: Bearer <token>
    
    Returns:
        Token string or None
    """
    auth_header = request.headers.get("Authorization", "")
    
    if not auth_header.startswith("Bearer "):
        return None
    
    return auth_header[7:]  # Remove "Bearer " prefix


def require_auth(f):
    """
    Decorator to require valid JWT authentication.
    
    Usage:
        @app.route('/protected')
        @require_auth
        def protected_endpoint():
            return {"data": "protected"}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_request()
        
        if not token:
            return jsonify({"error": "Missing authentication token"}), 401
        
        is_valid, payload = verify_token(token)
        
        if not is_valid:
            return jsonify({"error": payload.get("error", "Invalid token")}), 401
        
        # Add user_id to request context
        request.user_id = payload.get("user_id")
        request.token_payload = payload
        
        return f(*args, **kwargs)
    
    return decorated_function


def decode_token(token: str) -> Optional[Dict]:
    """
    Safely decode token without raising exceptions.
    
    Args:
        token: JWT token to decode
    
    Returns:
        Decoded payload dict or None
    """
    is_valid, payload = verify_token(token)
    return payload if is_valid else None
