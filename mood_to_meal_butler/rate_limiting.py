"""Rate limiting decorator for production API endpoints."""

import time
from functools import wraps
from typing import Callable, Dict, Tuple
from datetime import datetime, timedelta


class RateLimiter:
    """Simple in-memory rate limiter for MVP deployment."""
    
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Max requests allowed in time window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}  # user_id -> [timestamp, ...]
    
    def is_allowed(self, user_id: str) -> Tuple[bool, int]:
        """
        Check if user is allowed to make request.
        
        Args:
            user_id: Unique user identifier
        
        Returns:
            Tuple of (allowed: bool, remaining_requests: int)
        """
        now = time.time()
        window_start = now - self.window_seconds
        
        # Initialize user if not seen before
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        # Remove old timestamps outside window
        self.requests[user_id] = [
            ts for ts in self.requests[user_id] 
            if ts > window_start
        ]
        
        # Check if under limit
        current_count = len(self.requests[user_id])
        remaining = self.max_requests - current_count
        
        if current_count < self.max_requests:
            self.requests[user_id].append(now)
            return True, remaining
        
        return False, 0
    
    def cleanup(self):
        """Remove stale user entries (call periodically)."""
        now = time.time()
        window_start = now - (self.window_seconds * 2)  # Keep extra buffer
        
        for user_id in list(self.requests.keys()):
            self.requests[user_id] = [
                ts for ts in self.requests[user_id]
                if ts > window_start
            ]
            if not self.requests[user_id]:
                del self.requests[user_id]


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=60, window_seconds=60)


def rate_limit(get_user_id: Callable = None):
    """
    Decorator for rate limiting async functions.
    
    Args:
        get_user_id: Function to extract user_id from function args
    
    Example:
        @rate_limit(lambda ctx, *args: ctx.user_id)
        async def my_endpoint(ctx: Context):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract user_id
            if get_user_id:
                user_id = get_user_id(*args, **kwargs)
            else:
                user_id = kwargs.get("user_id", "anonymous")
            
            # Check rate limit
            allowed, remaining = rate_limiter.is_allowed(user_id)
            
            if not allowed:
                raise Exception(
                    f"Rate limit exceeded. "
                    f"Max 60 requests per minute. Try again later."
                )
            
            # Call original function
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator
