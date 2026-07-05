"""
END-TO-END WORKFLOW TESTS - Full System Validation

Tests complete workflows:
- Security audit → Export → Alert
- Performance test → Monitor → Export
- Compliance check → Slack notification → Export
- Configuration → Batch operations → Monitor
- Cache operations → Statistics → Profiling
"""

import pytest


class TestSecurityWorkflow:
    """Test complete security workflow."""
    
    def test_security_audit_to_export(self):
        """Test security audit and export."""
        from mood_to_meal_butler.api_convenience import SecurityCheckFacade
        from mood_to_meal_butler.data_export import DataExporter
        
        # Run security check
        result = SecurityCheckFacade.quick_security_scan()
        assert result['status'] == 'PASS'
        
        # Export audit
        filename = DataExporter.export_security_audit()
        assert filename is not None
    
    def test_security_alert_flow(self):
        """Test security alert to Slack."""
        from mood_to_meal_butler.api_convenience import SecurityCheckFacade
        from mood_to_meal_butler.slack_integration import SlackAlertManager
        
        # Run security check
        result = SecurityCheckFacade.check_vulnerability('sql_injection')
        assert result is not None
        
        # Send alert
        manager = SlackAlertManager()
        alert_result = manager.route_alert('security', 'Test alert')
        assert alert_result is not None


class TestPerformanceWorkflow:
    """Test complete performance workflow."""
    
    def test_performance_test_to_profiling(self):
        """Test performance test and profiling."""
        from mood_to_meal_butler.api_convenience import PerformanceFacade
        from mood_to_meal_butler.performance_profiler import PerformanceProfiler
        
        # Run performance test
        result = PerformanceFacade.quick_load_test('light')
        assert result is not None
        
        # Create profiler and profile a function
        profiler = PerformanceProfiler()
        
        @profiler.profile_function
        def test_func():
            return 42
        
        test_func()
        report = profiler.get_report()
        assert report is not None
    
    def test_performance_monitoring_workflow(self):
        """Test performance monitoring."""
        from mood_to_meal_butler.health_dashboard import get_health_monitor
        from mood_to_meal_butler.data_export import DataExporter
        
        # Get health monitor
        monitor = get_health_monitor()
        assert monitor is not None
        
        # Export metrics
        filename = DataExporter.export_performance_metrics()
        assert filename is not None


class TestComplianceWorkflow:
    """Test complete compliance workflow."""
    
    def test_compliance_check_to_export(self):
        """Test compliance audit and export."""
        from mood_to_meal_butler.api_convenience import ComplianceFacade
        from mood_to_meal_butler.data_export import DataExporter
        
        # Check compliance
        result = ComplianceFacade.check_compliance('gdpr')
        assert result is not None
        
        # Export compliance audit
        filename = DataExporter.export_compliance_audit()
        assert filename is not None
    
    def test_compliance_alert_workflow(self):
        """Test compliance alert to Slack."""
        from mood_to_meal_butler.api_convenience import ComplianceFacade
        from mood_to_meal_butler.slack_integration import SlackNotifier
        
        # Check compliance
        result = ComplianceFacade.check_compliance('ccpa')
        assert result is not None
        
        # Send Slack notification
        notifier = SlackNotifier()
        message_result = notifier.send_compliance_status('CCPA', 'PASS', 9.5)
        assert message_result is not None


class TestCacheWorkflow:
    """Test caching workflow."""
    
    def test_cache_set_get_stats(self):
        """Test cache operations and statistics."""
        from mood_to_meal_butler.advanced_caching import get_multi_tier_cache
        
        cache = get_multi_tier_cache()
        
        # Set values
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        
        # Get values
        assert cache.get('key1') == 'value1'
        assert cache.get('key2') == 'value2'
        
        # Get stats
        stats = cache.stats()
        assert 'l1' in stats
        assert 'l2' in stats
    
    def test_cache_invalidation(self):
        """Test cache invalidation."""
        from mood_to_meal_butler.advanced_caching import MultiTierCache
        
        cache = MultiTierCache()
        cache.set('key1', 'value1')
        assert cache.get('key1') == 'value1'
        
        cache.invalidate('key1')
        assert cache.get('key1') is None


class TestBatchWorkflow:
    """Test batch operations workflow."""
    
    def test_full_audit_workflow(self):
        """Test full system audit."""
        from mood_to_meal_butler.batch_operations import get_batch_operations
        
        batch = get_batch_operations()
        result = batch.batch_full_audit()
        
        assert 'security' in result
        assert 'compliance' in result
        assert 'performance' in result
    
    def test_batch_export_workflow(self):
        """Test batch export operations."""
        from mood_to_meal_butler.batch_operations import get_batch_operations
        
        batch = get_batch_operations()
        result = batch.batch_export_data(['security', 'compliance'])
        
        assert result['operation'] == 'batch_export_data'
        assert 'exports' in result


class TestConfigurationWorkflow:
    """Test configuration management workflow."""
    
    def test_config_load_modify_save(self):
        """Test loading, modifying, and saving config."""
        from mood_to_meal_butler.config_manager import ConfigurationManager
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = os.path.join(tmpdir, 'test.json')
            
            # Create config
            config = ConfigurationManager(config_file)
            
            # Modify
            config.update_security_config(rate_limit_per_minute=100)
            
            # Save
            config.save_config()
            
            # Load in new instance
            config2 = ConfigurationManager(config_file)
            assert config2.security.rate_limit_per_minute == 100
    
    def test_config_validation(self):
        """Test configuration validation."""
        from mood_to_meal_butler.config_manager import get_config
        
        config = get_config()
        validation = config.validate_config()
        
        assert 'valid' in validation
        assert 'issues' in validation


class TestAlertRulesWorkflow:
    """Test alert rules workflow."""
    
    def test_rule_creation_and_evaluation(self):
        """Test creating and evaluating rules."""
        from mood_to_meal_butler.alert_rules_engine import (
            AlertRule,
            AlertRulesEngine
        )
        
        engine = AlertRulesEngine()
        
        # Create rule
        rule = AlertRule('test', 'Test Rule', lambda: False, lambda: 'OK')
        engine.add_rule(rule)
        
        # Evaluate
        result = engine.evaluate_all()
        assert result['total_rules'] == 1
    
    def test_rule_history_tracking(self):
        """Test rule history."""
        from mood_to_meal_butler.alert_rules_engine import get_alert_rules_engine
        
        engine = get_alert_rules_engine()
        history = engine.get_history(limit=10)
        
        assert isinstance(history, list)


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
