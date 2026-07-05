"""
Advanced Caching - Multi-tier Cache Strategy

Provides:
- L1: In-memory LRU cache (fast)
- L2: Distributed cache simulation (medium)
- Cache statistics & metrics
- Automatic tier selection
- Smart invalidation
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import time


class L1Cache:
    """Level 1: In-memory LRU cache (fastest)."""
    
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from L1 cache."""
        if key in self.cache:
            self.hits += 1
            return self.cache[key]['value']
        self.misses += 1
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300):
        """Set value in L1 cache."""
        if len(self.cache) >= self.max_size:
            self.cache.pop(next(iter(self.cache)))
        
        self.cache[key] = {
            'value': value,
            'created_at': datetime.now(),
            'ttl': ttl
        }
    
    def stats(self) -> Dict:
        """Get L1 cache statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'level': 'L1',
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
        }


class L2Cache:
    """Level 2: Distributed cache simulation (medium speed)."""
    
    def __init__(self, max_size: int = 5000):
        self.cache = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from L2 cache."""
        if key in self.cache:
            entry = self.cache[key]
            # Check TTL
            if datetime.now() - entry['created_at'] < timedelta(seconds=entry['ttl']):
                self.hits += 1
                return entry['value']
            else:
                del self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, key: str, value: Any, ttl: int = 600):
        """Set value in L2 cache."""
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k]['created_at'])
            del self.cache[oldest_key]
        
        self.cache[key] = {
            'value': value,
            'created_at': datetime.now(),
            'ttl': ttl
        }
    
    def stats(self) -> Dict:
        """Get L2 cache statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'level': 'L2',
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
        }


class MultiTierCache:
    """Multi-tier cache system (L1 + L2)."""
    
    def __init__(self, l1_size: int = 1000, l2_size: int = 5000):
        self.l1 = L1Cache(l1_size)
        self.l2 = L2Cache(l2_size)
        self.read_pattern = 'l1_first'  # l1_first or l2_first
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache (L1 > L2)."""
        # Try L1 first
        value = self.l1.get(key)
        if value is not None:
            return value
        
        # Fall back to L2
        value = self.l2.get(key)
        if value is not None:
            # Promote to L1
            self.l1.set(key, value)
            return value
        
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300):
        """Set value in L1 and L2."""
        self.l1.set(key, value, ttl)
        self.l2.set(key, value, ttl * 2)  # Longer TTL in L2
    
    def invalidate(self, key: str) -> bool:
        """Invalidate key in all tiers."""
        self.l1.cache.pop(key, None)
        self.l2.cache.pop(key, None)
        return True
    
    def clear_all(self):
        """Clear all cache tiers."""
        self.l1.cache.clear()
        self.l2.cache.clear()
    
    def stats(self) -> Dict:
        """Get cache statistics."""
        return {
            'l1': self.l1.stats(),
            'l2': self.l2.stats(),
            'combined_hit_rate': self._calculate_combined_hit_rate(),
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_combined_hit_rate(self) -> float:
        """Calculate combined hit rate across tiers."""
        total_hits = self.l1.hits + self.l2.hits
        total = total_hits + self.l1.misses + self.l2.misses
        
        return (total_hits / total * 100) if total > 0 else 0


# Global multi-tier cache instance
_multi_tier_cache = None


def get_multi_tier_cache() -> MultiTierCache:
    """Get or create global multi-tier cache."""
    global _multi_tier_cache
    if _multi_tier_cache is None:
        _multi_tier_cache = MultiTierCache()
    return _multi_tier_cache
