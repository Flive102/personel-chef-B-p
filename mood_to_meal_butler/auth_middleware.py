"""
Authentication Middleware for mood-to-meal-butler
Handles request authentication and user context setup
"""

from functools import wraps
from typing import Callable, Optional, Dict
from flask import request, jsonify
from mood_to_meal_butler.jwt_auth import get_token_from_request, verify_token
from mood_to_meal_butler.rate_limiting import RateLimiter


class AuthMiddleware:
    """Handle authentication across API endpoints."""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
    
    def require_auth(self, f: Callable) -> Callable:
        """
        Decorator to enforce JWT authentication on endpoints.
        
        Usage:
            @app.route('/protected')
            @auth_middleware.require_auth
            def protected_endpoint():
                return {"user": request.user_id}
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Extract token from Authorization header
            token = get_token_from_request()
            
            if not token:
                return jsonify({"error": "Missing authentication token"}), 401
            
            # Verify token validity
            is_valid, payload = verify_token(token)
            
            if not is_valid:
                return jsonify({
                    "error": payload.get("error", "Invalid token")
                }), 401
            
            # Check token type (must be access token)
            if payload.get("type") != "access":
                return jsonify({"error": "Invalid token type"}), 401
            
            # Extract user_id from payload
            user_id = payload.get("user_id")
            if not user_id:
                return jsonify({"error": "Invalid token payload"}), 401
            
            # Check rate limit for user
            is_allowed, remaining = self.rate_limiter.check_limit(user_id)
            if not is_allowed:
                return jsonify({
                    "error": "Rate limit exceeded",
                    "retry_after": 60
                }), 429
            
            # Attach user context to request
            request.user_id = user_id
            request.token_payload = payload
            request.rate_limit_remaining = remaining
            
            # Add rate limit headers to response
            response = f(*args, **kwargs)
            
            if isinstance(response, tuple):
                data, status_code = response[0], response[1] if len(response) > 1 else 200
                response = (data, status_code)
            else:
                response = (response, 200)
            
            return response
        
        return decorated_function
    
    def optional_auth(self, f: Callable) -> Callable:
        """
        Decorator for optional authentication.
        Sets request.user_id if token provided, but doesn't require it.
        
        Usage:
            @app.route('/public')
            @auth_middleware.optional_auth
            def public_endpoint():
                if request.user_id:
                    return {"authenticated": True}
                return {"authenticated": False}
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = get_token_from_request()
            
            if token:
                is_valid, payload = verify_token(token)
                if is_valid and payload.get("type") == "access":
                    request.user_id = payload.get("user_id")
                    request.token_payload = payload
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    def check_rate_limit(self, f: Callable) -> Callable:
        """
        Decorator to enforce rate limiting (with or without auth).
        
        Usage:
            @app.route('/endpoint')
            @auth_middleware.check_rate_limit
            def endpoint():
                return {"data": "value"}
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get user_id from auth or IP address
            user_id = getattr(request, "user_id", request.remote_addr)
            
            # Check rate limit
            is_allowed, remaining = self.rate_limiter.check_limit(user_id)
            
            if not is_allowed:
                return jsonify({
                    "error": "Rate limit exceeded",
                    "retry_after": 60
                }), 429
            
            request.rate_limit_remaining = remaining
            return f(*args, **kwargs)
        
        return decorated_function


# Global middleware instance
auth_middleware = AuthMiddleware()


def attach_auth_to_app(app):
    """
    Attach authentication middleware to Flask app.
    
    Usage:
        from flask import Flask
        from mood_to_meal_butler.auth_middleware import attach_auth_to_app
        
        app = Flask(__name__)
        attach_auth_to_app(app)
    """
    
    @app.before_request
    def before_request():
        """Log authentication attempts and add rate limit headers."""
        pass
    
    @app.after_request
    def after_request(response):
        """Add rate limit headers to all responses."""
        if hasattr(request, "rate_limit_remaining"):
            response.headers["X-RateLimit-Remaining"] = str(request.rate_limit_remaining)
            response.headers["X-RateLimit-Limit"] = "60"
            response.headers["X-RateLimit-Reset"] = "3600"
        
        return response
