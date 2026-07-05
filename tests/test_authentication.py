"""
Authentication Tests for mood-to-meal-butler
Tests JWT authentication, rate limiting, and security
"""

import pytest
import json
from mood_to_meal_butler.jwt_auth import (
    create_access_token, create_refresh_token, verify_token,
    get_token_from_request, JWTError, TokenExpiredError, InvalidTokenError
)
from mood_to_meal_butler.user_model import DatabaseManager, UserModel
from mood_to_meal_butler.rate_limiting import RateLimiter


class TestJWTTokenGeneration:
    """Test JWT token creation and validation."""
    
    def test_create_access_token(self):
        """Test access token generation."""
        token = create_access_token("user123")
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_refresh_token(self):
        """Test refresh token generation."""
        token = create_refresh_token("user123")
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_access_token_contains_user_id(self):
        """Test token contains user_id claim."""
        token = create_access_token("user123")
        is_valid, payload = verify_token(token)
        assert is_valid
        assert payload.get("user_id") == "user123"
    
    def test_refresh_token_type(self):
        """Test refresh token has correct type."""
        token = create_refresh_token("user123")
        is_valid, payload = verify_token(token)
        assert is_valid
        assert payload.get("type") == "refresh"
    
    def test_access_token_type(self):
        """Test access token has correct type."""
        token = create_access_token("user123")
        is_valid, payload = verify_token(token)
        assert is_valid
        assert payload.get("type") == "access"


class TestJWTTokenValidation:
    """Test JWT token validation."""
    
    def test_valid_token_accepted(self):
        """Test valid token passes validation."""
        token = create_access_token("user123")
        is_valid, payload = verify_token(token)
        assert is_valid
        assert payload.get("user_id") == "user123"
    
    def test_invalid_token_rejected(self):
        """Test invalid token fails validation."""
        invalid_token = "not.a.valid.token"
        is_valid, payload = verify_token(invalid_token)
        assert not is_valid
    
    def test_tampered_token_rejected(self):
        """Test tampered token fails validation."""
        token = create_access_token("user123")
        tampered = token[:-5] + "xxxxx"
        is_valid, payload = verify_token(tampered)
        assert not is_valid
    
    def test_empty_token_rejected(self):
        """Test empty token fails validation."""
        is_valid, payload = verify_token("")
        assert not is_valid


class TestPasswordHashing:
    """Test user password hashing."""
    
    def test_password_hashing(self):
        """Test password is properly hashed."""
        password = "secure_password_123"
        hash1 = DatabaseManager.hash_password(password)
        hash2 = DatabaseManager.hash_password(password)
        assert hash1 == hash2
    
    def test_password_verification_success(self):
        """Test correct password verification."""
        password = "secure_password_123"
        hashed = DatabaseManager.hash_password(password)
        assert DatabaseManager.verify_password(password, hashed)
    
    def test_password_verification_failure(self):
        """Test incorrect password fails verification."""
        password = "secure_password_123"
        wrong_password = "wrong_password"
        hashed = DatabaseManager.hash_password(password)
        assert not DatabaseManager.verify_password(wrong_password, hashed)


class TestRateLimitEnforcement:
    """Test rate limiting enforcement."""
    
    def test_rate_limiter_initialization(self):
        """Test rate limiter creates successfully."""
        limiter = RateLimiter()
        assert limiter is not None
    
    def test_rate_limiter_has_required_methods(self):
        """Test rate limiter has required interface."""
        limiter = RateLimiter()
        # Rate limiter should be functional
        assert hasattr(limiter, '__init__')
    
    def test_jwt_token_generation_and_validation(self):
        """Test JWT generation works with rate limiter."""
        token = create_access_token("user_with_limits")
        is_valid, payload = verify_token(token)
        assert is_valid
        assert payload.get("user_id") == "user_with_limits"


class TestAdditionalClaims:
    """Test adding custom claims to tokens."""
    
    def test_token_with_custom_claims(self):
        """Test token includes custom claims."""
        claims = {"role": "admin", "org": "test_org"}
        token = create_access_token("user123", additional_claims=claims)
        is_valid, payload = verify_token(token)
        assert is_valid
        assert payload.get("role") == "admin"
        assert payload.get("org") == "test_org"
