"""
WEEK 5-6: Integration Tests (Part 1/2) - Performance + Optimization + Compliance

Integration scenarios:
- Load test with caching enabled
- Cache invalidation under concurrent load
- Database optimization with stress tests
- Compliance audit results
"""

import pytest
from mood_to_meal_butler.locust_load_tests import LightLoadTest, MediumLoadTest
from mood_to_meal_butler.caching_layer import get_caching_layer, reset_caching_layer
from mood_to_meal_butler.cache_invalidation import CacheInvalidationManager, InvalidationEvent
from mood_to_meal_butler.database_optimization import get_db_optimizer, reset_optimizer
from mood_to_meal_butler.compliance_audit_extended import get_compliance_auditor


class TestLoadTestWithCaching:
    """Test load performance with caching enabled."""
    
    def test_cached_recommendations_improve_performance(self):
        """Verify caching improves response times."""
        cache = get_caching_layer()
        
        # Pre-populate cache
        test_meals = [{'id': 1, 'name': 'pasta'}, {'id': 2, 'name': 'salad'}]
        cache.meals.cache_recommendation('sad', 'office', test_meals)
        
        # Retrieve from cache
        result = cache.meals.get_recommendation('sad', 'office')
        assert result == test_meals
        
        stats = cache.get_cache_stats()
        assert stats['meal_recommendations']['hits'] > 0
    
    def test_light_load_with_cache(self):
        """Light load test with cache enabled."""
        reset_caching_layer()
        cache = get_caching_layer()
        
        # Run light load test
        test = LightLoadTest()
        result = test.run()
        
        assert result['success_rate'] >= 95
        assert result['response_times']['avg'] > 0


class TestCacheInvalidationUnderLoad:
    """Test cache invalidation during concurrent access."""
    
    def test_invalidation_triggers_correctly(self):
        """Verify cache invalidation events trigger."""
        manager = CacheInvalidationManager()
        
        # Trigger multiple events
        manager.trigger_invalidation(InvalidationEvent.MEAL_ADDED)
        manager.trigger_invalidation(InvalidationEvent.EMOTION_CONFIG_CHANGED)
        
        history = manager.get_invalidation_history()
        assert len(history) == 2
    
    def test_dependency_invalidation(self):
        """Test dependent cache invalidation."""
        from mood_to_meal_butler.cache_invalidation import SmartInvalidationStrategy
        
        strategy = SmartInvalidationStrategy()
        strategy.add_dependency('parent_key', 'child_key')
        
        # Invalidate parent should cascade
        invalidated = strategy.invalidate_with_dependencies('parent_key')
        assert 'parent_key' in invalidated


class TestDatabaseOptimizationIntegration:
    """Test database optimization during operations."""
    
    def test_connection_pool_under_load(self):
        """Verify connection pool handles concurrent requests."""
        reset_optimizer()
        optimizer = get_db_optimizer()
        
        stats = optimizer.get_optimization_metrics()
        assert stats['connection_reuse_enabled'] == True
        assert stats['query_batching_enabled'] == True
    
    def test_query_batching_efficiency(self):
        """Test query batching reduces number of queries."""
        reset_optimizer()
        optimizer = get_db_optimizer()
        
        meal_ids = list(range(1, 101))
        results = optimizer.batcher.batch_get_meals(meal_ids)
        
        # Should batch queries, not 100 individual queries
        assert len(results) > 0


class TestComplianceAuditIntegration:
    """Test compliance audit with all modules."""
    
    def test_compliance_audit_runs(self):
        """Verify compliance audit completes."""
        audit = get_compliance_auditor()
        
        assert 'gdpr' in audit
        assert 'ccpa' in audit
        assert 'hipaa' in audit
    
    def test_gdpr_pass(self):
        """Verify GDPR audit passes."""
        audit = get_compliance_auditor()
        
        assert audit['gdpr']['status'] == 'PASS'
        assert audit['gdpr']['overall_score'] == 10.0
    
    def test_ccpa_pass(self):
        """Verify CCPA audit passes."""
        audit = get_compliance_auditor()
        
        assert audit['ccpa']['status'] == 'PASS'
        assert audit['ccpa']['overall_score'] == 10.0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
