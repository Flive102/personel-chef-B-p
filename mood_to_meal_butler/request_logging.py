"""
Request/Response Logging - Sanitized Logging with Performance Metrics

Tracks:
- Request metadata (path, method, user_id)
- Response status + size
- Processing time
- Error events
- Security events (no PII)
"""

import time
import json
from datetime import datetime
from typing import Dict, Any, Optional, Callable
import logging


class RequestLogger:
    """Centralized request/response logging."""
    
    def __init__(self):
        self.logger = logging.getLogger("request_logging")
        self.request_count = 0
        self.response_times = []
        self.errors_logged = 0
        
        # Setup file handler for request logs
        if not self.logger.handlers:
            handler = logging.FileHandler("request_log.json")
            formatter = logging.Formatter(
                '{"timestamp": "%(asctime)s", "message": "%(message)s"}'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def log_request(
        self,
        method: str,
        path: str,
        user_id: Optional[str] = None,
        query_params: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> str:
        """Log incoming request. Returns request_id."""
        request_id = f"req_{int(time.time() * 1000)}"
        self.request_count += 1
        
        # Sanitize headers (remove sensitive ones)
        safe_headers = self._sanitize_headers(headers or {})
        
        log_data = {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "method": method,
            "path": path,
            "user_id": user_id,
            "query_param_count": len(query_params or {}),
            "headers": safe_headers,
            "type": "request",
        }
        
        self.logger.info(json.dumps(log_data))
        return request_id
    
    def log_response(
        self,
        request_id: str,
        status_code: int,
        response_size: int,
        processing_time_ms: float,
        user_id: Optional[str] = None,
        error: Optional[str] = None
    ) -> None:
        """Log outgoing response."""
        self.response_times.append(processing_time_ms)
        
        if error:
            self.errors_logged += 1
        
        log_data = {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "status_code": status_code,
            "response_size_bytes": response_size,
            "processing_time_ms": processing_time_ms,
            "user_id": user_id,
            "error": error,
            "type": "response",
        }
        
        self.logger.info(json.dumps(log_data))
    
    def log_security_event(
        self,
        event_type: str,
        severity: str,
        user_id: Optional[str] = None,
        path: Optional[str] = None,
        details: Optional[Dict] = None
    ) -> None:
        """Log security-related event."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "severity": severity,
            "user_id": user_id,
            "path": path,
            "details": details or {},
            "type": "security_event",
        }
        
        self.logger.warning(json.dumps(log_data))
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get logging metrics."""
        avg_time = (
            sum(self.response_times) / len(self.response_times)
            if self.response_times else 0
        )
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_requests": self.request_count,
            "total_errors_logged": self.errors_logged,
            "avg_response_time_ms": round(avg_time, 2),
            "min_response_time_ms": round(min(self.response_times), 2) if self.response_times else 0,
            "max_response_time_ms": round(max(self.response_times), 2) if self.response_times else 0,
            "recent_requests": self.request_count,
        }
    
    def _sanitize_headers(self, headers: Dict) -> Dict:
        """Remove sensitive headers from logs."""
        sensitive_keys = {
            "authorization", "cookie", "x-api-key",
            "x-auth-token", "password", "token",
            "x-csrf-token"
        }
        
        safe_headers = {}
        for key, value in headers.items():
            if key.lower() in sensitive_keys:
                safe_headers[key] = "***"
            else:
                safe_headers[key] = "***" if value else None
        
        return safe_headers


def log_request_response(logger: RequestLogger) -> Callable:
    """Decorator for logging requests/responses."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            # Extract request context (Flask-specific)
            try:
                from flask import request
                method = request.method
                path = request.path
                user_id = getattr(request, 'user_id', None)
                headers = dict(request.headers)
            except:
                # Fallback if not in Flask context
                method = "UNKNOWN"
                path = "unknown"
                user_id = None
                headers = {}
            
            request_id = logger.log_request(
                method=method,
                path=path,
                user_id=user_id,
                headers=headers
            )
            
            start_time = time.time()
            error = None
            
            try:
                result = func(*args, **kwargs)
                status_code = 200
                response_size = len(json.dumps(result)) if isinstance(result, dict) else 0
                return result
            except Exception as e:
                status_code = 500
                response_size = 0
                error = str(e)[:100]
                raise
            finally:
                processing_time_ms = (time.time() - start_time) * 1000
                logger.log_response(
                    request_id=request_id,
                    status_code=status_code,
                    response_size=response_size,
                    processing_time_ms=processing_time_ms,
                    user_id=user_id,
                    error=error
                )
        
        return wrapper
    return decorator


# Global logger instance
_request_logger = None


def get_request_logger() -> RequestLogger:
    """Get or create global request logger."""
    global _request_logger
    if _request_logger is None:
        _request_logger = RequestLogger()
    return _request_logger
