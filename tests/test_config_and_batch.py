"""
Tests for Configuration Manager and Batch Operations

Test coverage for:
- ConfigurationManager
- BatchOperations
- Configuration persistence
- Batch job execution
"""

import pytest
import json
import tempfile
import os
from mood_to_meal_butler.config_manager import (
    ConfigurationManager,
    get_config,
    reset_config,
    SecurityConfig,
    PerformanceConfig,
)
from mood_to_meal_butler.batch_operations import (
    BatchOperations,
    get_batch_operations,
)


class TestConfigurationManager:
    """Test configuration management."""
    
    def test_default_config_creation(self):
        """Test creating default configuration."""
        reset_config()
        config = get_config()
        
        assert config is not None
        assert config.security is not None
        assert config.performance is not None
    
    def test_security_config_defaults(self):
        """Test security configuration defaults."""
        reset_config()
        config = get_config()
        
        assert config.security.rate_limit_per_minute == 60
        assert config.security.https_required == True
        assert config.security.tls_version == "1.2"
    
    def test_performance_config_defaults(self):
        """Test performance configuration defaults."""
        reset_config()
        config = get_config()
        
        assert config.performance.cache_size == 10000
        assert config.performance.db_pool_size == 20
        assert config.performance.query_batch_size == 50
    
    def test_compliance_config_defaults(self):
        """Test compliance configuration defaults."""
        reset_config()
        config = get_config()
        
        assert config.compliance.gdpr_retention_days == 30
        assert config.compliance.sla_uptime_target == 99.9
    
    def test_save_and_load_config(self):
        """Test saving and loading configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = os.path.join(tmpdir, 'test_config.json')
            
            # Create and save config
            config1 = ConfigurationManager(config_file)
            config1.update_security_config(rate_limit_per_minute=120)
            config1.save_config()
            
            # Load config
            config2 = ConfigurationManager(config_file)
            assert config2.security.rate_limit_per_minute == 120
    
    def test_update_security_config(self):
        """Test updating security configuration."""
        reset_config()
        config = get_config()
        
        config.update_security_config(rate_limit_per_minute=100)
        assert config.security.rate_limit_per_minute == 100
    
    def test_update_performance_config(self):
        """Test updating performance configuration."""
        reset_config()
        config = get_config()
        
        config.update_performance_config(cache_size=20000)
        assert config.performance.cache_size == 20000
    
    def test_get_all_config(self):
        """Test getting all configuration."""
        reset_config()
        config = get_config()
        
        all_config = config.get_all_config()
        assert 'security' in all_config
        assert 'performance' in all_config
        assert 'compliance' in all_config
        assert 'export' in all_config
    
    def test_generate_config_template(self):
        """Test generating configuration template."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ConfigurationManager()
            template_file = os.path.join(tmpdir, 'template.json')
            
            result = config.generate_config_template(template_file)
            assert os.path.exists(result)
            
            with open(result, 'r') as f:
                template = json.load(f)
                assert 'security' in template
    
    def test_validate_config(self):
        """Test configuration validation."""
        reset_config()
        config = get_config()
        
        validation = config.validate_config()
        assert 'valid' in validation
        assert 'issues' in validation


class TestBatchOperations:
    """Test batch operation execution."""
    
    def test_batch_security_audits(self):
        """Test batch security audits."""
        batch = get_batch_operations()
        
        result = batch.batch_security_audits(['sql_injection', 'xss'])
        
        assert result['operation'] == 'batch_security_audits'
        assert result['total'] == 2
        assert result['successful'] >= 1
    
    def test_batch_compliance_checks(self):
        """Test batch compliance checks."""
        batch = get_batch_operations()
        
        result = batch.batch_compliance_checks(['gdpr', 'ccpa'])
        
        assert result['operation'] == 'batch_compliance_checks'
        assert result['total'] == 2
    
    def test_batch_performance_tests(self):
        """Test batch performance tests."""
        batch = get_batch_operations()
        
        result = batch.batch_performance_tests(['light'])
        
        assert result['operation'] == 'batch_performance_tests'
        assert result['total'] == 1
        assert 'duration_seconds' in result
    
    def test_batch_export_data(self):
        """Test batch data export."""
        batch = get_batch_operations()
        
        result = batch.batch_export_data(['security', 'compliance'])
        
        assert result['operation'] == 'batch_export_data'
        assert 'exports' in result
    
    def test_batch_full_audit(self):
        """Test full system audit."""
        batch = get_batch_operations()
        
        result = batch.batch_full_audit()
        
        assert 'security' in result
        assert 'compliance' in result
        assert 'performance' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
