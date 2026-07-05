"""
Tests for API Convenience Layer and CLI Tools

Test coverage for:
- SecurityCheckFacade
- PerformanceFacade
- ComplianceFacade
- CachingFacade
- DatabaseFacade
"""

import pytest
import json
from mood_to_meal_butler.api_convenience import (
    SecurityCheckFacade,
    PerformanceFacade,
    ComplianceFacade,
    CachingFacade,
    DatabaseFacade,
    SystemStatus,
)


class TestSecurityCheckFacade:
    """Test security check convenience methods."""
    
    def test_quick_security_scan(self):
        """Test quick security scan returns valid structure."""
        result = SecurityCheckFacade.quick_security_scan()
        
        assert 'timestamp' in result
        assert 'audit' in result
        assert 'status' in result
        assert result['status'] == 'PASS'
    
    def test_check_sql_injection_vulnerability(self):
        """Test SQL injection check."""
        result = SecurityCheckFacade.check_vulnerability('sql_injection')
        
        assert 'status' in result
        assert result['status'] == 'PROTECTED'
        assert 'method' in result
    
    def test_check_xss_vulnerability(self):
        """Test XSS vulnerability check."""
        result = SecurityCheckFacade.check_vulnerability('xss')
        
        assert result['status'] == 'PROTECTED'
    
    def test_check_auth_vulnerability(self):
        """Test auth vulnerability check."""
        result = SecurityCheckFacade.check_vulnerability('auth')
        
        assert result['status'] == 'PROTECTED'
    
    def test_check_dos_vulnerability(self):
        """Test DoS vulnerability check."""
        result = SecurityCheckFacade.check_vulnerability('dos')
        
        assert result['status'] == 'PROTECTED'
    
    def test_invalid_vulnerability_type(self):
        """Test invalid vulnerability type returns error."""
        result = SecurityCheckFacade.check_vulnerability('invalid')
        
        assert 'error' in result


class TestPerformanceFacade:
    """Test performance testing convenience methods."""
    
    def test_light_load_test(self):
        """Test light load test."""
        result = PerformanceFacade.quick_load_test('light')
        
        assert 'scenario' in result
        assert 'results' in result
        assert result['scenario'] == 'light'
    
    def test_medium_load_test(self):
        """Test medium load test."""
        result = PerformanceFacade.quick_load_test('medium')
        
        assert result['scenario'] == 'medium'
    
    def test_heavy_load_test(self):
        """Test heavy load test."""
        result = PerformanceFacade.quick_load_test('heavy')
        
        assert result['scenario'] == 'heavy'
    
    def test_invalid_scenario(self):
        """Test invalid scenario returns error."""
        result = PerformanceFacade.quick_load_test('invalid')
        
        assert 'error' in result
    
    def test_get_performance_baseline(self):
        """Test getting performance baseline."""
        result = PerformanceFacade.get_performance_baseline()
        
        assert isinstance(result, dict)


class TestComplianceFacade:
    """Test compliance checking convenience methods."""
    
    def test_check_all_compliance(self):
        """Test checking all compliance frameworks."""
        result = ComplianceFacade.check_all_compliance()
        
        assert 'timestamp' in result
        assert 'audits' in result
    
    def test_check_gdpr_compliance(self):
        """Test GDPR compliance check."""
        result = ComplianceFacade.check_compliance('gdpr')
        
        assert 'status' in result or 'error' not in result
    
    def test_check_ccpa_compliance(self):
        """Test CCPA compliance check."""
        result = ComplianceFacade.check_compliance('ccpa')
        
        assert 'status' in result or 'error' not in result
    
    def test_check_hipaa_compliance(self):
        """Test HIPAA compliance check."""
        result = ComplianceFacade.check_compliance('hipaa')
        
        assert 'status' in result or 'error' not in result
    
    def test_invalid_framework(self):
        """Test invalid framework returns error."""
        result = ComplianceFacade.check_compliance('invalid')
        
        assert 'error' in result


class TestCachingFacade:
    """Test caching convenience methods."""
    
    def test_get_cache_status(self):
        """Test getting cache status."""
        result = CachingFacade.get_cache_status()
        
        assert 'timestamp' in result
        assert 'cache_stats' in result
    
    def test_clear_caches(self):
        """Test clearing caches."""
        result = CachingFacade.clear_caches()
        
        assert result['status'] == 'Caches cleared'
        assert 'timestamp' in result


class TestDatabaseFacade:
    """Test database convenience methods."""
    
    def test_get_db_status(self):
        """Test getting database status."""
        result = DatabaseFacade.get_db_status()
        
        assert 'timestamp' in result
        assert 'metrics' in result
    
    def test_pool_statistics(self):
        """Test getting connection pool statistics."""
        result = DatabaseFacade.pool_statistics()
        
        assert isinstance(result, dict)


class TestSystemStatus:
    """Test system status aggregation."""
    
    def test_get_full_status(self):
        """Test getting full system status."""
        result = SystemStatus.get_full_status()
        
        assert 'timestamp' in result
        assert 'security' in result
        assert 'performance' in result
        assert 'compliance' in result
    
    def test_get_health_check(self):
        """Test quick health check."""
        result = SystemStatus.get_health_check()
        
        assert 'status' in result
        assert 'checks' in result
        assert result['status'] in ['HEALTHY', 'UNHEALTHY']


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
