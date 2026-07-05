"""
CORS Security Headers for mood-to-meal-butler
Prevents cross-origin attacks and enforces security policies
"""

from typing import Optional, List


class SecurityHeaders:
    """Configure security headers for Flask applications."""
    
    @staticmethod
    def get_cors_headers(allowed_origins: Optional[List[str]] = None) -> dict:
        """
        Get CORS headers for responses.
        
        Args:
            allowed_origins: List of allowed origin domains
        
        Returns:
            Dict of CORS headers
        """
        if allowed_origins is None:
            allowed_origins = ["https://localhost:3000", "https://example.com"]
        
        return {
            "Access-Control-Allow-Origin": ", ".join(allowed_origins),
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "3600",
            "Access-Control-Allow-Credentials": "true"
        }
    
    @staticmethod
    def get_security_headers() -> dict:
        """
        Get essential security headers.
        
        Returns:
            Dict of security headers
        """
        return {
            # Prevent clickjacking
            "X-Frame-Options": "DENY",
            
            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",
            
            # Enable XSS protection (legacy)
            "X-XSS-Protection": "1; mode=block",
            
            # Referrer policy
            "Referrer-Policy": "strict-origin-when-cross-origin",
            
            # Content Security Policy
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' https:; "
                "font-src 'self'; "
                "connect-src 'self' https:; "
                "frame-ancestors 'none'"
            ),
            
            # Feature Policy / Permissions Policy
            "Permissions-Policy": (
                "geolocation=(), "
                "microphone=(), "
                "camera=(), "
                "payment=(), "
                "usb=(), "
                "magnetometer=(), "
                "gyroscope=(), "
                "accelerometer=()"
            )
        }
    
    @staticmethod
    def get_all_headers(allowed_origins: Optional[List[str]] = None) -> dict:
        """
        Get combined CORS and security headers.
        
        Args:
            allowed_origins: List of allowed origins
        
        Returns:
            Dict of all security headers
        """
        headers = {}
        headers.update(SecurityHeaders.get_cors_headers(allowed_origins))
        headers.update(SecurityHeaders.get_security_headers())
        return headers


def attach_security_headers_to_app(app, allowed_origins: Optional[List[str]] = None):
    """
    Attach security headers to all Flask responses.
    
    Usage:
        from flask import Flask
        from mood_to_meal_butler.cors_headers import attach_security_headers_to_app
        
        app = Flask(__name__)
        attach_security_headers_to_app(app, allowed_origins=["https://example.com"])
    
    Args:
        app: Flask application instance
        allowed_origins: List of allowed origin domains
    """
    
    @app.after_request
    def set_security_headers(response):
        """Add security headers to every response."""
        headers = SecurityHeaders.get_all_headers(allowed_origins)
        
        for header, value in headers.items():
            response.headers[header] = value
        
        return response
    
    @app.before_request
    def handle_preflight():
        """Handle CORS preflight requests."""
        from flask import request
        
        if request.method == "OPTIONS":
            headers = SecurityHeaders.get_cors_headers(allowed_origins)
            response = app.make_default_options_response()
            
            for header, value in headers.items():
                response.headers[header] = value
            
            return response
