"""
WEEK 6: Caching Layer - Redis-style In-Memory Cache (Part 1/2)

Implements LRU cache with TTL:
- Cache meal recommendations (TTL: 5 min)
- Cache user preferences (TTL: 1 hour)
- Cache error metrics (TTL: 1 min)
- LRU eviction when max capacity reached
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class CacheEntry:
    """Single cache entry with TTL."""
    key: str
    value: Any
    created_at: datetime
    ttl_seconds: int
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    
    def is_expired(self) -> bool:
        """Check if entry has expired."""
        age = (datetime.now() - self.created_at).total_seconds()
        return age > self.ttl_seconds
    
    def access(self) -> Any:
        """Access entry and update stats."""
        self.access_count += 1
        self.last_accessed = datetime.now()
        return self.value


class LRUCache:
    """LRU (Least Recently Used) cache with TTL support."""
    
    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.cache: Dict[str, CacheEntry] = {}
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def put(self, key: str, value: Any, ttl_seconds: int = 300):
        """Add/update cache entry."""
        # Remove expired entries first
        self._remove_expired()
        
        # If key exists, update it
        if key in self.cache:
            self.cache[key] = CacheEntry(
                key=key,
                value=value,
                created_at=datetime.now(),
                ttl_seconds=ttl_seconds
            )
            return
        
        # Check if need to evict
        if len(self.cache) >= self.max_size:
            self._evict_lru()
        
        # Add new entry
        self.cache[key] = CacheEntry(
            key=key,
            value=value,
            created_at=datetime.now(),
            ttl_seconds=ttl_seconds
        )
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key not in self.cache:
            self.misses += 1
            return None
        
        entry = self.cache[key]
        
        # Check expiration
        if entry.is_expired():
            del self.cache[key]
            self.misses += 1
            return None
        
        # Return value and update stats
        self.hits += 1
        return entry.access()
    
    def delete(self, key: str):
        """Delete entry from cache."""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """Clear entire cache."""
        self.cache.clear()
    
    def _remove_expired(self):
        """Remove all expired entries."""
        expired_keys = [
            key for key, entry in self.cache.items()
            if entry.is_expired()
        ]
        for key in expired_keys:
            del self.cache[key]
    
    def _evict_lru(self):
        """Evict least recently used entry."""
        if not self.cache:
            return
        
        # Find entry with oldest last_accessed (or created_at if never accessed)
        def get_last_time(entry):
            if entry.last_accessed:
                return entry.last_accessed
            return entry.created_at
        
        lru_key = min(
            self.cache.keys(),
            key=lambda k: get_last_time(self.cache[k])
        )
        
        del self.cache[lru_key]
        self.evictions += 1
    
    def get_stats(self) -> Dict:
        """Get cache statistics."""
        total_accesses = self.hits + self.misses
        hit_rate = (self.hits / total_accesses * 100) if total_accesses > 0 else 0
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'evictions': self.evictions,
        }


class MealRecommendationCache:
    """Cache for meal recommendations (TTL: 5 min)."""
    
    def __init__(self, max_size: int = 5000):
        self.cache = LRUCache(max_size)
        self.ttl_seconds = 300  # 5 minutes
    
    def cache_recommendation(self, emotion: str, situation: str, meals: List[Dict]):
        """Cache meal recommendation."""
        key = f"meal_rec:{emotion}:{situation}"
        self.cache.put(key, meals, self.ttl_seconds)
    
    def get_recommendation(self, emotion: str, situation: str) -> Optional[List[Dict]]:
        """Get cached recommendation."""
        key = f"meal_rec:{emotion}:{situation}"
        return self.cache.get(key)
    
    def invalidate_recommendation(self, emotion: str, situation: str):
        """Invalidate specific recommendation."""
        key = f"meal_rec:{emotion}:{situation}"
        self.cache.delete(key)


class UserPreferenceCache:
    """Cache for user preferences (TTL: 1 hour)."""
    
    def __init__(self, max_size: int = 2000):
        self.cache = LRUCache(max_size)
        self.ttl_seconds = 3600  # 1 hour
    
    def cache_preferences(self, user_id: str, prefs: Dict):
        """Cache user preferences."""
        key = f"user_prefs:{user_id}"
        self.cache.put(key, prefs, self.ttl_seconds)
    
    def get_preferences(self, user_id: str) -> Optional[Dict]:
        """Get cached user preferences."""
        key = f"user_prefs:{user_id}"
        return self.cache.get(key)


class ErrorMetricsCache:
    """Cache for error metrics (TTL: 1 min)."""
    
    def __init__(self, max_size: int = 1000):
        self.cache = LRUCache(max_size)
        self.ttl_seconds = 60  # 1 minute
    
    def cache_metrics(self, metric_key: str, metrics: Dict):
        """Cache error metrics."""
        key = f"metrics:{metric_key}"
        self.cache.put(key, metrics, self.ttl_seconds)
    
    def get_metrics(self, metric_key: str) -> Optional[Dict]:
        """Get cached metrics."""
        key = f"metrics:{metric_key}"
        return self.cache.get(key)


class CachingLayer:
    """Central caching management."""
    
    def __init__(self):
        self.meals = MealRecommendationCache()
        self.users = UserPreferenceCache()
        self.metrics = ErrorMetricsCache()
    
    def get_cache_stats(self) -> Dict:
        """Get all cache statistics."""
        return {
            'meal_recommendations': self.meals.cache.get_stats(),
            'user_preferences': self.users.cache.get_stats(),
            'error_metrics': self.metrics.cache.get_stats(),
        }


# Global caching layer
_caching_layer = None


def get_caching_layer() -> CachingLayer:
    """Get or create global caching layer."""
    global _caching_layer
    if _caching_layer is None:
        _caching_layer = CachingLayer()
    return _caching_layer


def reset_caching_layer():
    """Reset caching layer for testing."""
    global _caching_layer
    _caching_layer = CachingLayer()
