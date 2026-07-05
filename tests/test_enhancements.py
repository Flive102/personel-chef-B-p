"""
Tests for Enhancement Modules - All 5 Features

Comprehensive test coverage for:
- WebSocket real-time updates
- Slack integration
- Advanced multi-tier caching
- Alert rules engine
- Performance profiler
"""

import pytest


class TestWebSocket:
    """Test WebSocket real-time updates."""
    
    def test_websocket_manager_import(self):
        """Test WebSocket manager can be imported."""
        from mood_to_meal_butler.websocket_realtime import WebSocketManager
        manager = WebSocketManager()
        assert manager is not None
    
    def test_websocket_register_client(self):
        """Test registering WebSocket client."""
        from mood_to_meal_butler.websocket_realtime import WebSocketManager
        manager = WebSocketManager()
        client = manager.register_client('test_client')
        assert client['id'] == 'test_client'
    
    def test_websocket_client_count(self):
        """Test client connection count."""
        from mood_to_meal_butler.websocket_realtime import WebSocketManager
        manager = WebSocketManager()
        manager.register_client('c1')
        manager.register_client('c2')
        assert manager.get_connected_clients() == 2
    
    def test_websocket_subscribe(self):
        """Test client subscription."""
        from mood_to_meal_butler.websocket_realtime import WebSocketManager
        manager = WebSocketManager()
        manager.register_client('client1')
        result = manager.subscribe_client('client1', 'health')
        assert result['status'] == 'subscribed'


class TestSlackIntegration:
    """Test Slack integration."""
    
    def test_slack_notifier_import(self):
        """Test Slack notifier can be imported."""
        from mood_to_meal_butler.slack_integration import SlackNotifier
        notifier = SlackNotifier()
        assert notifier is not None
    
    def test_slack_not_configured(self):
        """Test Slack when not configured."""
        from mood_to_meal_butler.slack_integration import SlackNotifier
        notifier = SlackNotifier()
        assert notifier.is_configured() == False
    
    def test_slack_alert_manager_import(self):
        """Test Slack alert manager."""
        from mood_to_meal_butler.slack_integration import SlackAlertManager
        manager = SlackAlertManager()
        assert 'security' in manager.alert_routing


class TestAdvancedCaching:
    """Test multi-tier caching."""
    
    def test_l1_cache_import(self):
        """Test L1 cache can be imported."""
        from mood_to_meal_butler.advanced_caching import L1Cache
        cache = L1Cache()
        assert cache is not None
    
    def test_l1_cache_operations(self):
        """Test L1 cache set/get."""
        from mood_to_meal_butler.advanced_caching import L1Cache
        cache = L1Cache()
        cache.set('key1', 'value1')
        assert cache.get('key1') == 'value1'
    
    def test_l2_cache_operations(self):
        """Test L2 cache set/get."""
        from mood_to_meal_butler.advanced_caching import L2Cache
        cache = L2Cache()
        cache.set('key1', 'value1')
        assert cache.get('key1') == 'value1'
    
    def test_multi_tier_cache(self):
        """Test multi-tier cache."""
        from mood_to_meal_butler.advanced_caching import MultiTierCache
        cache = MultiTierCache()
        cache.set('key1', 'value1')
        assert cache.get('key1') == 'value1'
    
    def test_cache_stats(self):
        """Test cache statistics."""
        from mood_to_meal_butler.advanced_caching import MultiTierCache
        cache = MultiTierCache()
        cache.set('test', 'data')
        stats = cache.stats()
        assert 'l1' in stats
        assert 'l2' in stats


class TestAlertRulesEngine:
    """Test alert rules engine."""
    
    def test_alert_rule_import(self):
        """Test AlertRule can be imported."""
        from mood_to_meal_butler.alert_rules_engine import AlertRule
        rule = AlertRule('test', 'Test', lambda: False, lambda: 'action')
        assert rule is not None
    
    def test_alert_engine_import(self):
        """Test AlertRulesEngine can be imported."""
        from mood_to_meal_butler.alert_rules_engine import AlertRulesEngine
        engine = AlertRulesEngine()
        assert engine is not None
    
    def test_add_rule(self):
        """Test adding alert rule."""
        from mood_to_meal_butler.alert_rules_engine import (
            AlertRule,
            AlertRulesEngine
        )
        engine = AlertRulesEngine()
        rule = AlertRule('test', 'Test', lambda: False, lambda: 'ok')
        result = engine.add_rule(rule)
        assert result['status'] == 'added'
    
    def test_rule_enable_disable(self):
        """Test enabling/disabling rules."""
        from mood_to_meal_butler.alert_rules_engine import (
            AlertRule,
            AlertRulesEngine
        )
        engine = AlertRulesEngine()
        rule = AlertRule('test', 'Test', lambda: False, lambda: 'ok')
        engine.add_rule(rule)
        engine.disable_rule('test')
        assert engine.rules['test'].enabled == False


class TestPerformanceProfiler:
    """Test performance profiler."""
    
    def test_profiler_import(self):
        """Test PerformanceProfiler can be imported."""
        from mood_to_meal_butler.performance_profiler import PerformanceProfiler
        profiler = PerformanceProfiler()
        assert profiler is not None
    
    def test_profile_function_decorator(self):
        """Test profiling function decorator."""
        from mood_to_meal_butler.performance_profiler import PerformanceProfiler
        profiler = PerformanceProfiler()
        
        @profiler.profile_function
        def test_func():
            return 42
        
        result = test_func()
        assert result == 42
    
    def test_get_profile(self):
        """Test getting profile data."""
        from mood_to_meal_butler.performance_profiler import PerformanceProfiler
        profiler = PerformanceProfiler()
        
        @profiler.profile_function
        def test_func():
            return 42
        
        test_func()
        profile = profiler.get_profile('test_func')
        assert profile is not None
        assert profile['call_count'] >= 1
    
    def test_profiler_report(self):
        """Test generating profiler report."""
        from mood_to_meal_butler.performance_profiler import PerformanceProfiler
        profiler = PerformanceProfiler()
        
        @profiler.profile_function
        def test_func():
            return 42
        
        test_func()
        report = profiler.get_report()
        assert 'total_functions' in report


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
