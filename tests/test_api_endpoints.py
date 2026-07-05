"""
Tests for API Endpoints Module

Test coverage for:
- APIEndpoints handlers
- HTTP response formats
- Error handling
"""

import pytest
import json
from mood_to_meal_butler.api_endpoints import APIEndpoints


class TestAPIEndpoints:
    """Test HTTP API endpoints."""
    
    def test_security_check_no_params(self):
        """Test security check without parameters."""
        result = APIEndpoints.security_check()
        
        assert result['success'] == True
        assert 'data' in result
        assert 'timestamp' in result
    
    def test_security_check_sql_injection(self):
        """Test security check for SQL injection."""
        result = APIEndpoints.security_check('sql_injection')
        
        assert result['success'] == True
        assert result['data']['status'] == 'PROTECTED'
    
    def test_security_check_xss(self):
        """Test security check for XSS."""
        result = APIEndpoints.security_check('xss')
        
        assert result['success'] == True
        assert result['data']['status'] == 'PROTECTED'
    
    def test_performance_test_light(self):
        """Test light performance test."""
        result = APIEndpoints.performance_test('light')
        
        assert result['success'] == True
        assert result['data']['scenario'] == 'light'
    
    def test_performance_test_medium(self):
        """Test medium performance test."""
        result = APIEndpoints.performance_test('medium')
        
        assert result['success'] == True
        assert result['data']['scenario'] == 'medium'
    
    def test_compliance_check_all(self):
        """Test compliance check for all frameworks."""
        result = APIEndpoints.compliance_check()
        
        assert result['success'] == True
        assert 'data' in result
    
    def test_compliance_check_gdpr(self):
        """Test GDPR compliance check."""
        result = APIEndpoints.compliance_check('gdpr')
        
        assert result['success'] == True
        assert 'data' in result
    
    def test_system_status_full(self):
        """Test full system status."""
        result = APIEndpoints.system_status(health_only=False)
        
        assert result['success'] == True
        assert 'data' in result
        assert 'timestamp' in result
    
    def test_system_status_health(self):
        """Test health check only."""
        result = APIEndpoints.system_status(health_only=True)
        
        assert result['success'] == True
        assert 'data' in result
    
    def test_cache_status(self):
        """Test cache status endpoint."""
        result = APIEndpoints.cache_operations('status')
        
        assert result['success'] == True
        assert 'data' in result
    
    def test_cache_clear(self):
        """Test cache clear endpoint."""
        result = APIEndpoints.cache_operations('clear')
        
        assert result['success'] == True
        assert 'Caches cleared' in str(result['data'])
    
    def test_database_status(self):
        """Test database status endpoint."""
        result = APIEndpoints.database_status(pool_stats=False)
        
        assert result['success'] == True
        assert 'data' in result
    
    def test_database_pool_stats(self):
        """Test database pool stats endpoint."""
        result = APIEndpoints.database_status(pool_stats=True)
        
        assert result['success'] == True
        assert 'data' in result
    
    def test_fastapi_setup_returns_routes(self):
        """Test FastAPI setup returns valid route definitions."""
        routes = APIEndpoints.get_routes() if hasattr(APIEndpoints, 'get_routes') else None
        # Just verify the class exists and has setup methods
        from mood_to_meal_butler.api_endpoints import FastAPISetup
        
        assert FastAPISetup is not None
        routes = FastAPISetup.get_routes()
        assert '@app.get' in routes
        assert '/api/security' in routes
    
    def test_flask_setup_returns_routes(self):
        """Test Flask setup returns valid route definitions."""
        from mood_to_meal_butler.api_endpoints import FlaskSetup
        
        assert FlaskSetup is not None
        routes = FlaskSetup.get_routes()
        assert '@app.route' in routes
        assert '/api/security' in routes


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
