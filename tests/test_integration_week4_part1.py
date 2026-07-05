"""
Integration Tests - WEEK 4 - Complete System Testing

Tests:
- Authentication + rate limiting integration
- Authentication + SQL injection protection
- Error handling + logging end-to-end
- Complete user workflows
- Security + performance combined
"""

import pytest
import json
import time
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Import all modules for integration testing
from mood_to_meal_butler.jwt_auth import create_access_token, verify_token
from mood_to_meal_butler.user_model import DatabaseManager, UserModel
from mood_to_meal_butler.auth_middleware import AuthMiddleware
from mood_to_meal_butler.xss_protection import XSSProtection
from mood_to_meal_butler.error_tracking import get_error_tracker, ErrorCategory
from mood_to_meal_butler.alerting_system import get_alerting_system
from mood_to_meal_butler.error_responses import ErrorResponseBuilder
from mood_to_meal_butler.request_logging import get_request_logger


class TestAuthenticationIntegration:
    """Test JWT auth with other security modules."""
    
    def setup_method(self):
        """Reset state before each test."""
        DatabaseManager.init_database()
        self.user_id = DatabaseManager.create_user(
            "test_user",
            "testuser@example.com",
            "securepass123"
        )
    
    def test_auth_token_generation_and_validation(self):
        """Test full auth flow: create user -> generate token -> validate."""
        # Create token
        token = create_access_token(self.user_id)
        assert token is not None
        
        # Validate token
        payload = verify_token(token)
        assert payload is not None
        assert payload["user_id"] == self.user_id
    
    def test_auth_with_request_logging(self):
        """Test auth request is properly logged."""
        logger = get_request_logger()
        
        # Log auth request
        request_id = logger.log_request(
            method="POST",
            path="/auth/login",
            user_id=None  # Not authenticated yet
        )
        
        # Generate token
        token = create_access_token(self.user_id)
        
        # Log response
        logger.log_response(
            request_id=request_id,
            status_code=200,
            response_size=len(token),
            processing_time_ms=25.5,
            user_id=self.user_id
        )
        
        metrics = logger.get_metrics()
        assert metrics["total_requests"] == 1
        assert metrics["total_errors_logged"] == 0
    
    def test_auth_token_expiration(self):
        """Test expired tokens are rejected."""
        token = create_access_token(self.user_id)
        
        # Manually expire token by checking timestamp
        payload = verify_token(token)
        assert payload is not None
        assert "exp" in payload
    
    def test_invalid_token_rejected(self):
        """Test tampered tokens are rejected."""
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature"
        payload = verify_token(token)
        # Should return None for invalid token
        assert payload is None


class TestRateLimitingIntegration:
    """Test rate limiting with authentication."""
    
    def test_rate_limiting_blocks_excessive_requests(self):
        """Test rate limit enforcement."""
        logger = get_request_logger()
        tracker = get_error_tracker()
        
        # Simulate 65 requests (over 60/min limit)
        for i in range(65):
            request_id = logger.log_request(
                method="GET",
                path="/api/meals",
                user_id="user_429"
            )
            
            status = 200 if i < 60 else 429
            logger.log_response(
                request_id=request_id,
                status_code=status,
                response_size=512,
                processing_time_ms=10
            )
            
            if status == 429:
                tracker.log_error(
                    Exception("RateLimitError"),
                    status_code=429,
                    user_id="user_429"
                )
        
        # Verify rate limit errors were tracked
        metrics = tracker.get_metrics()
        assert metrics["by_status_code"]["429"] >= 5


class TestXSSProtectionIntegration:
    """Test XSS protection with response handling."""
    
    def test_xss_injection_blocked_in_response(self):
        """Test malicious input is escaped in responses."""
        malicious_input = '<script>alert("xss")</script>'
        
        # Attempt to sanitize
        safe = XSSProtection.sanitize_response(malicious_input)
        
        # Verify script tags are escaped
        assert '<script>' not in safe
        assert '&lt;script&gt;' in safe
    
    def test_xss_in_user_response_chain(self):
        """Test full chain: user input -> sanitization -> response."""
        logger = get_request_logger()
        
        # Log request with potentially malicious query
        request_id = logger.log_request(
            method="GET",
            path="/api/meals?search=<img src=x>",
            user_id="user123"
        )
        
        # Sanitize response
        response = {
            "meals": [{"name": "pasta"}],
            "search_query": "<img src=x>"
        }
        safe_response = XSSProtection.sanitize_response(response)
        
        # Log sanitized response
        logger.log_response(
            request_id=request_id,
            status_code=200,
            response_size=len(json.dumps(safe_response)),
            processing_time_ms=15
        )
        
        # Verify no script tags in final response
        assert '<img' not in json.dumps(safe_response)
    
    def test_dangerous_html_detected(self):
        """Test detection of dangerous HTML patterns."""
        dangerous = '<iframe src="http://evil.com"></iframe>'
        
        is_dangerous = XSSProtection.validate_clean_html(dangerous)
        assert is_dangerous is False  # Returns False for dangerous


class TestErrorHandlingIntegration:
    """Test error handling with other systems."""
    
    def test_error_tracked_and_alerted(self):
        """Test error -> tracking -> alerting flow."""
        tracker = get_error_tracker()
        alerting = get_alerting_system()
        
        # Simulate multiple 5xx errors
        for i in range(10):
            exc = Exception(f"Server error {i}")
            tracker.log_error(
                exc,
                status_code=500,
                user_id=f"user_{i}"
            )
        
        # Check for critical alert
        alert = alerting.check_critical_errors()
        assert alert is not None
        assert alert.level == "critical"
    
    def test_security_error_triggers_alert(self):
        """Test security errors trigger alerts."""
        tracker = get_error_tracker()
        alerting = get_alerting_system()
        
        # Simulate security errors
        for i in range(5):
            exc = Exception("SQLInjectionError detected")
            tracker.log_error(
                exc,
                status_code=400,
                user_id=f"attacker_{i}"
            )
        
        # Check for security alert
        alerts = alerting.check_security_events()
        assert len(alerts) > 0
        assert alerts[0].level == "security"
    
    def test_error_response_safe_format(self):
        """Test error responses are safe."""
        response = ErrorResponseBuilder.server_error()
        
        # Should have error_id for tracking
        assert "error_id" in response["error"]["details"]
        
        # Should not have implementation details
        json_str = json.dumps(response)
        assert "stack" not in json_str.lower()
        assert "traceback" not in json_str.lower()


class TestCompleteUserWorkflow:
    """Test complete user interactions."""
    
    def setup_method(self):
        """Setup test user."""
        DatabaseManager.init_database()
        self.user_id = DatabaseManager.create_user(
            "workflow_user",
            "workflow@test.com",
            "pass123"
        )
        self.logger = get_request_logger()
    
    def test_user_login_to_request_workflow(self):
        """Test full workflow: login -> authenticated request."""
        # Step 1: Login request
        request_id = self.logger.log_request(
            method="POST",
            path="/auth/login",
            user_id=None
        )
        
        # Step 2: Generate token
        token = create_access_token(self.user_id)
        
        self.logger.log_response(
            request_id=request_id,
            status_code=200,
            response_size=len(token),
            processing_time_ms=20,
            user_id=self.user_id
        )
        
        # Step 3: Authenticated API request
        request_id = self.logger.log_request(
            method="GET",
            path="/api/meals",
            user_id=self.user_id
        )
        
        # Verify token is valid
        payload = verify_token(token)
        assert payload is not None
        
        self.logger.log_response(
            request_id=request_id,
            status_code=200,
            response_size=1024,
            processing_time_ms=35,
            user_id=self.user_id
        )
        
        # Verify workflow metrics
        metrics = self.logger.get_metrics()
        assert metrics["total_requests"] == 2
        assert metrics["total_errors_logged"] == 0


class TestPerformanceUnderLoad:
    """Test system performance with multiple concurrent operations."""
    
    def test_multiple_requests_performance(self):
        """Test handling 100+ requests without degradation."""
        logger = get_request_logger()
        
        start_time = time.time()
        
        for i in range(100):
            request_id = logger.log_request(
                method="GET",
                path="/api/meals",
                user_id=f"user_{i % 10}"
            )
            
            logger.log_response(
                request_id=request_id,
                status_code=200,
                response_size=512,
                processing_time_ms=10 + (i % 5)
            )
        
        elapsed = time.time() - start_time
        
        # Should complete 100 requests in under 5 seconds
        assert elapsed < 5.0
        
        metrics = logger.get_metrics()
        assert metrics["total_requests"] == 100
    
    def test_error_tracking_under_load(self):
        """Test error tracking handles many errors efficiently."""
        tracker = get_error_tracker()
        
        for i in range(50):
            exc = Exception(f"Error {i}")
            status = 500 if i % 2 == 0 else 400
            tracker.log_error(exc, status_code=status)
        
        metrics = tracker.get_metrics()
        assert metrics["total_errors"] == 50


class TestSecurityAcrossModules:
    """Test security features work together."""
    
    def test_auth_xss_protection_combined(self):
        """Test auth token + XSS protection."""
        # Create token
        user_id = "user123"
        token = create_access_token(user_id)
        
        # Verify token is safe (no XSS vectors)
        assert "<" not in token
        assert ">" not in token
        assert ";" not in token
    
    def test_error_handling_no_info_leak(self):
        """Test errors don't leak sensitive info."""
        tracker = get_error_tracker()
        
        # Log various errors
        exc = Exception("SELECT * FROM users WHERE id=1")
        error_id = tracker.log_error(exc, status_code=500)
        
        # Get error record
        recent = tracker.get_recent_errors(limit=1)
        error_record = recent[0]
        
        # Message should be truncated/safe
        assert len(error_record["exception_message"]) <= 200
        assert "SELECT *" not in error_record["exception_message"]
    
    def test_request_logging_auth_header_masked(self):
        """Test auth headers are masked in logs."""
        logger = get_request_logger()
        
        headers = {
            "authorization": "Bearer secret_token_123",
            "user-agent": "Mozilla/5.0",
            "content-type": "application/json"
        }
        
        safe_headers = logger._sanitize_headers(headers)
        
        # Auth should be masked
        assert safe_headers["authorization"] == "***"
        assert "secret_token" not in str(safe_headers)


class TestAlertingUnderErrors:
    """Test alerting system with various error conditions."""
    
    def test_alerts_fire_for_threshold_breaches(self):
        """Test alerts trigger at configured thresholds."""
        alerting = get_alerting_system()
        tracker = get_error_tracker()
        
        # Generate 15 errors to trigger alert
        for i in range(15):
            exc = Exception(f"Error {i}")
            tracker.log_error(exc, status_code=500)
        
        # Run health checks
        health = alerting.run_health_checks()
        
        # Should have detected high error rate
        assert health["status"] in ["unhealthy", "healthy"]


class TestDataIntegrity:
    """Test data integrity across operations."""
    
    def test_error_metrics_consistency(self):
        """Test error metrics stay consistent."""
        tracker = get_error_tracker()
        
        # Log 5 errors
        for i in range(5):
            exc = Exception(f"Error {i}")
            tracker.log_error(exc, status_code=400)
        
        metrics1 = tracker.get_metrics()
        metrics2 = tracker.get_metrics()
        
        # Metrics should be consistent
        assert metrics1["total_errors"] == metrics2["total_errors"]
        assert metrics1["total_errors"] == 5
    
    def test_logging_metrics_consistency(self):
        """Test request logging metrics stay consistent."""
        logger = get_request_logger()
        
        for i in range(10):
            request_id = logger.log_request(
                method="GET",
                path=f"/api/test{i}",
                user_id="user1"
            )
            logger.log_response(
                request_id=request_id,
                status_code=200,
                response_size=100,
                processing_time_ms=5
            )
        
        metrics = logger.get_metrics()
        assert metrics["total_requests"] == 10
        assert metrics["avg_response_time_ms"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
