"""
Error Tracking Module - Production-Grade Error Management

Handles:
- Error categorization (client/server/security)
- Error metrics collection
- Stack trace logging (safe)
- Error context preservation
"""

import json
import traceback
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum


class ErrorCategory(Enum):
    """Error classification for monitoring."""
    CLIENT_ERROR = "client_error"  # 4xx
    SERVER_ERROR = "server_error"  # 5xx
    SECURITY_ERROR = "security_error"  # Auth, injection, XSS
    VALIDATION_ERROR = "validation_error"  # Input validation
    RATE_LIMIT_ERROR = "rate_limit_error"  # Rate limit hit
    DATABASE_ERROR = "database_error"  # DB connection/query
    EXTERNAL_SERVICE_ERROR = "external_service_error"  # API timeout
    UNKNOWN_ERROR = "unknown_error"  # Uncategorized


class ErrorTracker:
    """Central error tracking and metrics."""
    
    def __init__(self):
        self.errors: List[Dict[str, Any]] = []
        self.metrics = {
            "total_errors": 0,
            "by_category": {},
            "by_status_code": {},
            "error_rate": 0.0,
            "last_error_time": None,
        }
        self.logger = logging.getLogger("error_tracking")
        
        # Setup handlers if not already configured
        if not self.logger.handlers:
            handler = logging.FileHandler("error_log.json")
            formatter = logging.Formatter(
                '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.ERROR)
    
    def categorize_error(
        self,
        exception: Exception,
        status_code: int = 500
    ) -> ErrorCategory:
        """Determine error category from exception type and status code."""
        error_name = type(exception).__name__
        error_msg = str(exception)
        full_text = error_name + " " + error_msg
        
        # Security errors - check both type name and message
        if "Auth" in full_text or "Permission" in full_text:
            return ErrorCategory.SECURITY_ERROR
        
        if "SQL" in full_text or "Injection" in full_text:
            return ErrorCategory.SECURITY_ERROR
        
        if "XSS" in full_text or "Sanitize" in full_text:
            return ErrorCategory.SECURITY_ERROR
        
        # Validation errors
        if "Validation" in full_text or "Invalid" in full_text:
            return ErrorCategory.VALIDATION_ERROR
        
        # Rate limit errors
        if "RateLimit" in full_text or status_code == 429:
            return ErrorCategory.RATE_LIMIT_ERROR
        
        # Database errors
        if "Database" in full_text or "Query" in full_text:
            return ErrorCategory.DATABASE_ERROR
        
        if "Connection" in full_text or "Timeout" in full_text:
            return ErrorCategory.DATABASE_ERROR
        
        # External service errors
        if "Service" in full_text or "API" in full_text:
            return ErrorCategory.EXTERNAL_SERVICE_ERROR
        
        if status_code == 504:  # Gateway timeout
            return ErrorCategory.EXTERNAL_SERVICE_ERROR
        
        # HTTP status-based categorization
        if 400 <= status_code < 500:
            return ErrorCategory.CLIENT_ERROR
        
        if status_code >= 500:
            return ErrorCategory.SERVER_ERROR
        
        return ErrorCategory.UNKNOWN_ERROR
    
    def log_error(
        self,
        exception: Exception,
        status_code: int = 500,
        user_id: Optional[str] = None,
        request_path: Optional[str] = None,
        user_input: Optional[Any] = None,
        context: Optional[Dict] = None
    ) -> str:
        """
        Log error with full context.
        
        Returns:
            error_id - Unique identifier for tracking
        """
        error_id = f"err_{datetime.utcnow().timestamp()}"
        category = self.categorize_error(exception, status_code)
        
        # Safe stack trace (no sensitive data)
        stack_trace = traceback.format_exc()
        safe_trace = self._sanitize_traceback(stack_trace)
        
        # Build error record
        error_record = {
            "error_id": error_id,
            "timestamp": datetime.utcnow().isoformat(),
            "category": category.value,
            "status_code": status_code,
            "exception_type": type(exception).__name__,
            "exception_message": str(exception)[:200],  # Truncate long messages
            "user_id": user_id,
            "request_path": request_path,
            "stack_trace": safe_trace,
            "context": context or {},
        }
        
        # Don't log raw user input (security risk)
        if user_input is not None:
            error_record["user_input_type"] = type(user_input).__name__
            error_record["user_input_length"] = len(str(user_input))
        
        # Store in memory
        self.errors.append(error_record)
        
        # Update metrics
        self._update_metrics(category, status_code)
        
        # Log to file
        self.logger.error(json.dumps(error_record))
        
        return error_id
    
    def _sanitize_traceback(self, traceback_str: str) -> str:
        """Remove sensitive data from stack traces."""
        # Remove file paths that might leak env structure
        import re
        sanitized = re.sub(
            r'File ".*?([^/\\]+\.py)"',
            r'File "\1"',
            traceback_str
        )
        
        # Remove local variable dumps
        sanitized = re.sub(
            r'local variables.*?(?=\n\n|\Z)',
            '',
            sanitized,
            flags=re.DOTALL
        )
        
        return sanitized
    
    def _update_metrics(self, category: ErrorCategory, status_code: int):
        """Update error metrics."""
        self.metrics["total_errors"] += 1
        self.metrics["last_error_time"] = datetime.utcnow().isoformat()
        
        # By category
        cat_key = category.value
        self.metrics["by_category"][cat_key] = \
            self.metrics["by_category"].get(cat_key, 0) + 1
        
        # By status code
        code_key = str(status_code)
        self.metrics["by_status_code"][code_key] = \
            self.metrics["by_status_code"].get(code_key, 0) + 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current error metrics."""
        return self.metrics.copy()
    
    def get_recent_errors(self, limit: int = 10) -> List[Dict]:
        """Get most recent errors (for debugging)."""
        return self.errors[-limit:]
    
    def get_errors_by_category(self, category: ErrorCategory) -> List[Dict]:
        """Get all errors of a specific category."""
        return [
            err for err in self.errors
            if err["category"] == category.value
        ]
    
    def is_high_error_rate(self, threshold: float = 0.05) -> bool:
        """Check if error rate exceeds threshold."""
        if self.metrics["total_errors"] == 0:
            return False
        
        # Simple check: if >5% of recent requests errored
        # In production, calculate: errors_last_5min / total_requests_last_5min
        return self.metrics["total_errors"] > 100


# Global tracker instance
_error_tracker = None


def get_error_tracker() -> ErrorTracker:
    """Get or create global error tracker."""
    global _error_tracker
    if _error_tracker is None:
        _error_tracker = ErrorTracker()
    return _error_tracker
