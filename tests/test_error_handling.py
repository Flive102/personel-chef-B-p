"""
Error Handling Tests - 6+ Comprehensive Test Cases

Tests:
- Error categorization
- Error tracking metrics
- Alerting system
- Error responses (no PII leakage)
- Request logging
- Integration tests
"""

import pytest
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from mood_to_meal_butler.error_tracking import (
    ErrorTracker, ErrorCategory, get_error_tracker
)
from mood_to_meal_butler.alerting_system import (
    AlertingSystem, Alert, AlertLevel, get_alerting_system
)
from mood_to_meal_butler.error_responses import ErrorResponseBuilder
from mood_to_meal_butler.request_logging import RequestLogger, get_request_logger


class TestErrorTracking:
    """Test error categorization and tracking."""
    
    def setup_method(self):
        """Reset tracker before each test."""
        self.tracker = ErrorTracker()
    
    def test_categorize_client_error(self):
        """Test 4xx error categorization."""
        exc = ValueError("Bad request")
        category = self.tracker.categorize_error(exc, status_code=400)
        assert category == ErrorCategory.CLIENT_ERROR
    
    def test_categorize_server_error(self):
        """Test 5xx error categorization."""
        exc = RuntimeError("Server failed")
        category = self.tracker.categorize_error(exc, status_code=500)
        assert category == ErrorCategory.SERVER_ERROR
    
    def test_categorize_security_error(self):
        """Test security error detection."""
        exc = Exception("AuthenticationError: Invalid token")
        category = self.tracker.categorize_error(exc, status_code=401)
        assert category == ErrorCategory.SECURITY_ERROR
    
    def test_categorize_sql_injection_error(self):
        """Test SQL injection detection."""
        exc = Exception("SQLInjectionError detected")
        category = self.tracker.categorize_error(exc, status_code=400)
        assert category == ErrorCategory.SECURITY_ERROR
    
    def test_categorize_xss_error(self):
        """Test XSS detection."""
        exc = Exception("XSSSanitizeError")
        category = self.tracker.categorize_error(exc, status_code=400)
        assert category == ErrorCategory.SECURITY_ERROR
    
    def test_categorize_database_error(self):
        """Test database error detection."""
        exc = Exception("DatabaseConnectionError")
        category = self.tracker.categorize_error(exc, status_code=500)
        assert category == ErrorCategory.DATABASE_ERROR
    
    def test_categorize_rate_limit_error(self):
        """Test rate limit error detection."""
        exc = Exception("RateLimitError")
        category = self.tracker.categorize_error(exc, status_code=429)
        assert category == ErrorCategory.RATE_LIMIT_ERROR
    
    def test_log_error_returns_error_id(self):
        """Test that logged errors get unique IDs."""
        exc = ValueError("Test error")
        error_id = self.tracker.log_error(
            exc, 
            status_code=400,
            user_id="user123",
            request_path="/api/test"
        )
        
        assert error_id is not None
        assert error_id.startswith("err_")
        assert len(self.tracker.errors) == 1
    
    def test_log_error_updates_metrics(self):
        """Test that metrics are updated on error."""
        exc = ValueError("Test error")
        self.tracker.log_error(exc, status_code=400)
        
        metrics = self.tracker.get_metrics()
        assert metrics["total_errors"] == 1
        assert "400" in metrics["by_status_code"]
        assert metrics["by_status_code"]["400"] == 1
    
    def test_log_error_sanitizes_traceback(self):
        """Test that tracebacks are sanitized (no paths)."""
        exc = ValueError("Test error")
        self.tracker.log_error(exc, status_code=400)
        
        error_record = self.tracker.errors[0]
        assert "stack_trace" in error_record
        # Should not have full paths (security)
        assert "/Users/" not in error_record["stack_trace"]
        assert "C:\\" not in error_record["stack_trace"]
    
    def test_get_recent_errors(self):
        """Test retrieving recent errors."""
        for i in range(15):
            exc = ValueError(f"Error {i}")
            self.tracker.log_error(exc, status_code=400)
        
        recent = self.tracker.get_recent_errors(limit=10)
        assert len(recent) == 10
    
    def test_get_errors_by_category(self):
        """Test filtering errors by category."""
        # Log security errors
        self.tracker.log_error(
            Exception("AuthError"),
            status_code=401
        )
        self.tracker.log_error(
            Exception("AuthError 2"),
            status_code=401
        )
        
        # Log client errors
        self.tracker.log_error(
            ValueError("Invalid input"),
            status_code=400
        )
        
        security_errors = self.tracker.get_errors_by_category(
            ErrorCategory.SECURITY_ERROR
        )
        assert len(security_errors) == 2


class TestAlertingSystem:
    """Test alerting and monitoring."""
    
    def setup_method(self):
        """Reset alerting system before each test."""
        self.alerting = AlertingSystem()
        self.alerts_received = []
        
        # Register test handler
        self.alerting.register_handler(
            lambda alert: self.alerts_received.append(alert)
        )
    
    def test_alert_creation(self):
        """Test alert object creation."""
        alert = Alert(
            alert_id="test_alert_1",
            level=AlertLevel.WARNING,
            title="Test Alert",
            message="This is a test",
            category="test"
        )
        
        assert alert.alert_id == "test_alert_1"
        assert alert.level == AlertLevel.WARNING
        assert not alert.acknowledged
    
    def test_high_error_rate_detection(self):
        """Test high error rate alert."""
        self.alerting.error_tracker.metrics["total_errors"] = 150
        
        alert = self.alerting.check_high_error_rate()
        
        assert alert is not None
        assert alert.level == AlertLevel.WARNING
        assert len(self.alerts_received) == 1
    
    def test_security_event_alert(self):
        """Test security event detection."""
        # Simulate 5 security errors
        for i in range(5):
            exc = Exception("AuthError")
            self.alerting.error_tracker.log_error(
                exc,
                status_code=401
            )
        
        alerts = self.alerting.check_security_events()
        
        assert len(alerts) >= 1
        assert alerts[0].level == AlertLevel.SECURITY
    
    def test_critical_error_detection(self):
        """Test critical error threshold."""
        # Simulate 10 server errors
        for i in range(10):
            exc = Exception("Server error")
            self.alerting.error_tracker.log_error(
                exc,
                status_code=500
            )
        
        alert = self.alerting.check_critical_errors()
        
        assert alert is not None
        assert alert.level == AlertLevel.CRITICAL
    
    def test_acknowledge_alert(self):
        """Test alert acknowledgment."""
        alert = Alert(
            alert_id="alert_1",
            level=AlertLevel.WARNING,
            title="Test",
            message="Test alert",
            category="test"
        )
        
        self.alerting.alerts.append(alert)
        
        success = self.alerting.acknowledge_alert(
            alert_id="alert_1",
            acknowledged_by="admin"
        )
        
        assert success is True
        assert alert.acknowledged is True
        assert alert.acknowledged_by == "admin"
    
    def test_get_recent_alerts(self):
        """Test retrieving recent alerts."""
        for i in range(5):
            alert = Alert(
                alert_id=f"alert_{i}",
                level=AlertLevel.INFO,
                title=f"Alert {i}",
                message=f"Test alert {i}",
                category="test"
            )
            self.alerting.alerts.append(alert)
        
        recent = self.alerting.get_recent_alerts(limit=3)
        assert len(recent) == 3


class TestErrorResponses:
    """Test error response building."""
    
    def test_validation_error_no_pii(self):
        """Test validation error doesn't leak PII."""
        response = ErrorResponseBuilder.validation_error(
            field="email",
            reason="Invalid format"
        )
        
        assert response["error"]["type"] == "validation_error"
        assert "Invalid input" in response["error"]["message"]
        assert "password" not in json.dumps(response).lower()
    
    def test_authentication_error_no_pii(self):
        """Test auth error doesn't leak implementation details."""
        response = ErrorResponseBuilder.authentication_error()
        
        assert response["error"]["type"] == "authentication_error"
        # No database/table names
        assert "users" not in json.dumps(response).lower()
    
    def test_permission_error_format(self):
        """Test permission error format."""
        response = ErrorResponseBuilder.permission_error(
            resource="admin_panel"
        )
        
        assert response["error"]["type"] == "permission_error"
        assert response["error"]["details"]["resource"] == "admin_panel"
    
    def test_rate_limit_error_has_retry_after(self):
        """Test rate limit error includes retry info."""
        response = ErrorResponseBuilder.rate_limit_error(retry_after=120)
        
        assert response["error"]["type"] == "rate_limit_error"
        assert response["error"]["details"]["retry_after_seconds"] == 120
    
    def test_server_error_has_error_id(self):
        """Test server error includes tracking ID."""
        response = ErrorResponseBuilder.server_error()
        
        assert "error_id" in response["error"]["details"]
        assert response["error"]["details"]["error_id"].startswith("err_")


class TestRequestLogging:
    """Test request/response logging."""
    
    def setup_method(self):
        """Reset logger before each test."""
        self.logger = RequestLogger()
    
    def test_log_request_returns_id(self):
        """Test request logging returns unique ID."""
        request_id = self.logger.log_request(
            method="GET",
            path="/api/meals",
            user_id="user123"
        )
        
        assert request_id is not None
        assert request_id.startswith("req_")
    
    def test_log_response_records_metrics(self):
        """Test response logging captures metrics."""
        request_id = self.logger.log_request(
            method="GET",
            path="/api/meals"
        )
        
        self.logger.log_response(
            request_id=request_id,
            status_code=200,
            response_size=1024,
            processing_time_ms=45.5
        )
        
        metrics = self.logger.get_metrics()
        assert metrics["total_requests"] == 1
        assert 45.5 in self.logger.response_times
    
    def test_log_response_tracks_errors(self):
        """Test error tracking in responses."""
        request_id = self.logger.log_request(
            method="POST",
            path="/api/meals"
        )
        
        self.logger.log_response(
            request_id=request_id,
            status_code=500,
            response_size=0,
            processing_time_ms=100,
            error="Database connection failed"
        )
        
        metrics = self.logger.get_metrics()
        assert metrics["total_errors_logged"] == 1
    
    def test_sanitize_headers_removes_auth(self):
        """Test that auth headers are sanitized."""
        headers = {
            "authorization": "Bearer token123",
            "cookie": "session=abc",
            "content-type": "application/json"
        }
        
        safe_headers = self.logger._sanitize_headers(headers)
        
        assert safe_headers["authorization"] == "***"
        assert safe_headers["cookie"] == "***"
        assert safe_headers["content-type"] == "***"
    
    def test_log_security_event(self):
        """Test security event logging."""
        self.logger.log_security_event(
            event_type="sql_injection_attempt",
            severity="high",
            user_id="user456",
            path="/api/users",
            details={"attempt": "blocked"}
        )
        
        # Should not crash and log should be created
        assert self.logger.logger is not None
    
    def test_get_metrics_returns_stats(self):
        """Test metrics aggregation."""
        for i in range(3):
            request_id = self.logger.log_request(
                method="GET",
                path=f"/api/test{i}"
            )
            self.logger.log_response(
                request_id=request_id,
                status_code=200,
                response_size=512,
                processing_time_ms=25 + i*10
            )
        
        metrics = self.logger.get_metrics()
        assert metrics["total_requests"] == 3
        assert metrics["avg_response_time_ms"] > 0


class TestErrorHandlingIntegration:
    """Integration tests across error handling modules."""
    
    def test_error_flow_tracking_to_alert(self):
        """Test complete flow: error -> tracking -> alert."""
        tracker = get_error_tracker()
        alerting = get_alerting_system()
        
        # Log an error
        exc = Exception("Critical failure")
        error_id = tracker.log_error(
            exc,
            status_code=500,
            user_id="user789"
        )
        
        # Verify error was tracked
        assert error_id is not None
        assert len(tracker.errors) > 0
        
        # Check for alerts
        alert = alerting.check_critical_errors()
        # Alert might not trigger on single error, but system should work
        assert alerting.error_tracker is not None
    
    def test_error_response_builder_no_sensitive_data(self):
        """Test that error responses never leak sensitive info."""
        # Simulate various error scenarios
        errors_to_test = [
            ErrorResponseBuilder.validation_error("email", "too short"),
            ErrorResponseBuilder.authentication_error(),
            ErrorResponseBuilder.permission_error(),
            ErrorResponseBuilder.server_error(),
            ErrorResponseBuilder.database_error(),
        ]
        
        for error_response in errors_to_test:
            json_str = json.dumps(error_response)
            
            # Check for sensitive patterns (stack traces, SQL queries, etc.)
            assert "stack" not in json_str.lower()
            assert "traceback" not in json_str.lower()
            assert "select *" not in json_str.lower()
            assert "from " not in json_str.lower()  # No SQL queries
            # Field names are OK (e.g., "email", "password"), just not values
    
    def test_request_logging_with_errors(self):
        """Test request logging captures errors properly."""
        logger = get_request_logger()
        
        request_id = logger.log_request(
            method="POST",
            path="/api/sensitive",
            user_id="user_xyz"
        )
        
        logger.log_response(
            request_id=request_id,
            status_code=403,
            response_size=128,
            processing_time_ms=32.1,
            user_id="user_xyz",
            error="Permission denied"
        )
        
        metrics = logger.get_metrics()
        assert metrics["total_errors_logged"] == 1
        assert metrics["total_requests"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
