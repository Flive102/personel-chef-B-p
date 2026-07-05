"""
Structured Error Responses - Consistent Error Format for API

Ensures:
- Consistent error structure across API
- No sensitive data leakage
- User-friendly error messages
- Error tracking integration
"""

import json
from typing import Dict, Any, Optional
from mood_to_meal_butler.error_tracking import get_error_tracker


class ErrorResponse:
    """Structured error response."""
    
    def __init__(
        self,
        error_id: str,
        status_code: int,
        user_message: str,
        error_type: str,
        details: Optional[Dict] = None
    ):
        self.error_id = error_id
        self.status_code = status_code
        self.user_message = user_message
        self.error_type = error_type
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-safe dictionary."""
        return {
            "error": {
                "id": self.error_id,
                "type": self.error_type,
                "message": self.user_message,
                "details": self.details,
            }
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


class ErrorResponseBuilder:
    """Build structured error responses."""
    
    # User-friendly messages (no technical details)
    MESSAGES = {
        "validation_error": "Invalid input provided",
        "authentication_error": "Authentication required",
        "permission_error": "You don't have permission to access this",
        "not_found": "Resource not found",
        "conflict": "Request conflicts with existing resource",
        "rate_limit": "Too many requests. Please try again later",
        "server_error": "An error occurred. Please try again",
        "service_unavailable": "Service temporarily unavailable",
        "database_error": "Database error occurred",
    }
    
    @staticmethod
    def validation_error(
        field: str,
        reason: str,
        status_code: int = 400
    ) -> Dict[str, Any]:
        """Build validation error response."""
        tracker = get_error_tracker()
        error_id = f"err_validation_{tracker.metrics['total_errors']}"
        
        response = ErrorResponse(
            error_id=error_id,
            status_code=status_code,
            user_message=ErrorResponseBuilder.MESSAGES["validation_error"],
            error_type="validation_error",
            details={
                "field": field,
                "reason": reason,
            }
        )
        
        return response.to_dict()
    
    @staticmethod
    def authentication_error(
        reason: str = "Invalid credentials",
        status_code: int = 401
    ) -> Dict[str, Any]:
        """Build authentication error response."""
        tracker = get_error_tracker()
        error_id = f"err_auth_{tracker.metrics['total_errors']}"
        
        response = ErrorResponse(
            error_id=error_id,
            status_code=status_code,
            user_message=ErrorResponseBuilder.MESSAGES["authentication_error"],
            error_type="authentication_error",
            details={"hint": "Check your credentials"}
        )
        
        return response.to_dict()
    
    @staticmethod
    def permission_error(
        resource: str = "resource",
        status_code: int = 403
    ) -> Dict[str, Any]:
        """Build permission error response."""
        tracker = get_error_tracker()
        error_id = f"err_perm_{tracker.metrics['total_errors']}"
        
        response = ErrorResponse(
            error_id=error_id,
            status_code=status_code,
            user_message=ErrorResponseBuilder.MESSAGES["permission_error"],
            error_type="permission_error",
            details={"resource": resource}
        )
        
        return response.to_dict()
    
    @staticmethod
    def not_found_error(
        resource_type: str = "resource",
        status_code: int = 404
    ) -> Dict[str, Any]:
        """Build not found error response."""
        tracker = get_error_tracker()
        error_id = f"err_notfound_{tracker.metrics['total_errors']}"
        
        response = ErrorResponse(
            error_id=error_id,
            status_code=status_code,
            user_message=ErrorResponseBuilder.MESSAGES["not_found"],
            error_type="not_found",
            details={"resource_type": resource_type}
        )
        
        return response.to_dict()
    
    @staticmethod
    def rate_limit_error(
        retry_after: int = 60,
        status_code: int = 429
    ) -> Dict[str, Any]:
        """Build rate limit error response."""
        tracker = get_error_tracker()
        error_id = f"err_ratelimit_{tracker.metrics['total_errors']}"
        
        response = ErrorResponse(
            error_id=error_id,
            status_code=status_code,
            user_message=ErrorResponseBuilder.MESSAGES["rate_limit"],
            error_type="rate_limit_error",
            details={"retry_after_seconds": retry_after}
        )
        
        return response.to_dict()
    
    @staticmethod
    def server_error(
        status_code: int = 500
    ) -> Dict[str, Any]:
        """Build generic server error response."""
        tracker = get_error_tracker()
        error_id = f"err_server_{tracker.metrics['total_errors']}"
        
        response = ErrorResponse(
            error_id=error_id,
            status_code=status_code,
            user_message=ErrorResponseBuilder.MESSAGES["server_error"],
            error_type="server_error",
            details={"error_id": error_id, "hint": "Contact support if problem persists"}
        )
        
        return response.to_dict()
    
    @staticmethod
    def database_error(
        status_code: int = 500
    ) -> Dict[str, Any]:
        """Build database error response."""
        tracker = get_error_tracker()
        error_id = f"err_database_{tracker.metrics['total_errors']}"
        
        response = ErrorResponse(
            error_id=error_id,
            status_code=status_code,
            user_message=ErrorResponseBuilder.MESSAGES["database_error"],
            error_type="database_error",
            details={"error_id": error_id}
        )
        
        return response.to_dict()
