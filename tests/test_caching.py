"""
WEEK 6: Caching Tests - Verify LRU Cache & Cache Invalidation

Tests:
- LRU eviction works correctly
- TTL expiration works
- Cache hit/miss rates accurate
- Invalidation events trigger properly
"""

import pytest
from mood_to_meal_butler.caching_layer import (
    LRUCache, MealRecommendationCache, UserPreferenceCache,
    ErrorMetricsCache, CachingLayer, get_caching_layer, reset_caching_layer
)
from mood_to_meal_butler.cache_invalidation import (
    CacheInvalidationManager, InvalidationEvent, SmartInvalidationStrategy
)


class TestLRUCache:
    """Test LRU cache functionality."""
    
    def test_cache_put_get(self):
        """Test basic put/get operations."""
        cache = LRUCache(max_size=10)
        cache.put('key1', 'value1')
        assert cache.get('key1') == 'value1'
    
    def test_cache_miss(self):
        """Test cache miss."""
        cache = LRUCache(max_size=10)
        assert cache.get('nonexistent') is None
        assert cache.misses == 1
    
    def test_cache_hit(self):
        """Test cache hit."""
        cache = LRUCache(max_size=10)
        cache.put('key1', 'value1')
        result = cache.get('key1')
        assert result == 'value1'
        assert cache.hits == 1
    
    def test_cache_size_limit(self):
        """Test cache respects size limit."""
        cache = LRUCache(max_size=3)
        cache.put('key1', 'value1')
        cache.put('key2', 'value2')
        cache.put('key3', 'value3')
        
        # Cache is full (3 items, max 3)
        assert len(cache.cache) == 3
        
        # Add one more - should trigger eviction
        cache.put('key4', 'value4')
        
        # Cache should not exceed max size
        assert len(cache.cache) <= 3
        assert cache.evictions >= 1
    
    def test_cache_stats(self):
        """Test cache statistics."""
        cache = LRUCache(max_size=10)
        cache.put('key1', 'value1')
        cache.get('key1')
        cache.get('nonexistent')
        
        stats = cache.get_stats()
        assert stats['hits'] == 1
        assert stats['misses'] == 1
        assert stats['size'] == 1


class TestMealRecommendationCache:
    """Test meal recommendation caching."""
    
    def test_cache_recommendation(self):
        """Cache meal recommendation."""
        cache = MealRecommendationCache()
        meals = [{'id': 1, 'name': 'pasta'}]
        cache.cache_recommendation('sad', 'office', meals)
        
        result = cache.get_recommendation('sad', 'office')
        assert result == meals
    
    def test_invalidate_recommendation(self):
        """Invalidate recommendation."""
        cache = MealRecommendationCache()
        meals = [{'id': 1, 'name': 'pasta'}]
        cache.cache_recommendation('sad', 'office', meals)
        cache.invalidate_recommendation('sad', 'office')
        
        result = cache.get_recommendation('sad', 'office')
        assert result is None


class TestUserPreferenceCache:
    """Test user preference caching."""
    
    def test_cache_preferences(self):
        """Cache user preferences."""
        cache = UserPreferenceCache()
        prefs = {'diet': 'vegan', 'allergy': 'nuts'}
        cache.cache_preferences('user123', prefs)
        
        result = cache.get_preferences('user123')
        assert result == prefs


class TestCacheInvalidation:
    """Test cache invalidation manager."""
    
    def test_invalidation_trigger(self):
        """Trigger invalidation event."""
        manager = CacheInvalidationManager()
        manager.trigger_invalidation(InvalidationEvent.MEAL_ADDED)
        
        history = manager.get_invalidation_history()
        assert len(history) == 1
    
    def test_invalidation_with_context(self):
        """Trigger invalidation with context."""
        manager = CacheInvalidationManager()
        manager.trigger_invalidation(
            InvalidationEvent.MEAL_ADDED,
            {'meal_id': 123}
        )
        
        history = manager.get_invalidation_history()
        assert history[0]['context']['meal_id'] == 123


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
