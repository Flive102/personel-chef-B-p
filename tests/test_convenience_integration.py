"""
Integration Tests for User Convenience Features

Tests complete workflows:
- CLI to API to backend
- REPL to functionality
- Export pipelines
- Health monitoring
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
from mood_to_meal_butler.api_endpoints import APIEndpoints
from mood_to_meal_butler.cli_tool import CLICommands
from mood_to_meal_butler.data_export import DataExporter
from mood_to_meal_butler.health_dashboard import (
    get_health_monitor, get_performance_monitor, get_cache_monitor
)


class TestConvenienceIntegration:
    """Integration tests for all convenience features."""
    
    def test_security_workflow(self):
        """Test complete security workflow: CLI -> API -> Result."""
        # Via API
        result = APIEndpoints.security_check('sql_injection')
        assert result['success'] == True
        assert result['data']['status'] == 'PROTECTED'
    
    def test_performance_workflow(self):
        """Test complete performance workflow."""
        result = APIEndpoints.performance_test('light')
        assert result['success'] == True
        assert 'results' in result['data']
    
    def test_compliance_workflow(self):
        """Test complete compliance workflow."""
        # Check all
        result_all = APIEndpoints.compliance_check()
        assert result_all['success'] == True
        
        # Check specific
        result_gdpr = APIEndpoints.compliance_check('gdpr')
        assert result_gdpr['success'] == True
    
    def test_system_status_workflow(self):
        """Test system status workflow."""
        # Full status
        full = APIEndpoints.system_status(health_only=False)
        assert full['success'] == True
        
        # Health check
        health = APIEndpoints.system_status(health_only=True)
        assert health['success'] == True
    
    def test_cache_operations_workflow(self):
        """Test cache operations workflow."""
        # Get status
        status = APIEndpoints.cache_operations('status')
        assert status['success'] == True
        
        # Clear cache
        clear = APIEndpoints.cache_operations('clear')
        assert clear['success'] == True
        
        # Status after clear
        status2 = APIEndpoints.cache_operations('status')
        assert status2['success'] == True
    
    def test_database_workflow(self):
        """Test database operations workflow."""
        # Get status
        status = APIEndpoints.database_status(pool_stats=False)
        assert status['success'] == True
        
        # Get pool stats
        pool = APIEndpoints.database_status(pool_stats=True)
        assert pool['success'] == True


class TestHealthMonitoring:
    """Test health monitoring functionality."""
    
    def test_health_monitor_creation(self):
        """Test health monitor initialization."""
        monitor = get_health_monitor()
        assert monitor is not None
    
    def test_record_and_retrieve_metrics(self):
        """Test recording and retrieving health metrics."""
        monitor = get_health_monitor()
        
        # Record some metrics
        monitor.record_metric('cpu_usage', 45.0, 80.0)
        monitor.record_metric('memory_usage', 65.0, 85.0)
        
        dashboard = monitor.get_dashboard()
        assert 'metrics' in dashboard
        assert 'cpu_usage' in dashboard['metrics']
    
    def test_overall_status_calculation(self):
        """Test overall status calculation."""
        monitor = get_health_monitor()
        
        monitor.record_metric('test_metric', 90.0, 100.0)
        status = monitor._calculate_overall_status()
        assert status in ['HEALTHY', 'WARNING', 'CRITICAL']
    
    def test_alerts_generation(self):
        """Test alerts generation."""
        monitor = get_health_monitor()
        
        monitor.record_metric('warning_metric', 70.0, 80.0)
        alerts = monitor.get_alerts()
        assert isinstance(alerts, list)


class TestPerformanceMonitoring:
    """Test performance monitoring."""
    
    def test_performance_monitor_creation(self):
        """Test performance monitor initialization."""
        monitor = get_performance_monitor()
        assert monitor is not None
    
    def test_record_request(self):
        """Test recording requests."""
        monitor = get_performance_monitor()
        
        monitor.record_request(45.0, True)
        monitor.record_request(52.0, True)
        monitor.record_request(48.0, False)
        
        metrics = monitor.get_metrics()
        assert metrics['total_requests'] >= 1
        assert metrics['error_rate'] >= 0


class TestCacheMonitoring:
    """Test cache monitoring."""
    
    def test_cache_monitor_creation(self):
        """Test cache monitor initialization."""
        monitor = get_cache_monitor()
        assert monitor is not None
    
    def test_record_hits_and_misses(self):
        """Test recording cache hits and misses."""
        monitor = get_cache_monitor()
        
        monitor.record_hit()
        monitor.record_hit()
        monitor.record_miss()
        
        metrics = monitor.get_metrics()
        assert metrics['hits'] >= 1
        assert metrics['total_accesses'] >= 1


class TestDataExport:
    """Test data export functionality."""
    
    def test_export_security_audit(self):
        """Test exporting security audit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'security_audit.json')
            result = DataExporter.export_security_audit(filename)
            
            assert os.path.exists(result)
            assert result.endswith('.json')
    
    def test_export_compliance_audit(self):
        """Test exporting compliance audit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'compliance_audit.json')
            result = DataExporter.export_compliance_audit(filename)
            
            assert os.path.exists(result)
    
    def test_export_performance_metrics(self):
        """Test exporting performance metrics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'performance_metrics.csv')
            result = DataExporter.export_performance_metrics(filename)
            
            assert os.path.exists(result)
            assert result.endswith('.csv')
    
    def test_export_system_report(self):
        """Test exporting full system report."""
        with tempfile.TemporaryDirectory() as tmpdir:
            files = DataExporter.export_system_report(tmpdir)
            
            assert len(files) > 0
            for key, filepath in files.items():
                assert os.path.exists(filepath)


class TestReportGeneration:
    """Test report generation."""
    
    def test_generate_html_report(self):
        """Test generating HTML report."""
        from mood_to_meal_butler.data_export import ReportGenerator
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'report.html')
            result = ReportGenerator.generate_html_summary(filename)
            
            assert os.path.exists(result)
            assert result.endswith('.html')
            
            with open(result, 'r') as f:
                content = f.read()
                assert '<html>' in content
    
    def test_generate_text_report(self):
        """Test generating text report."""
        from mood_to_meal_butler.data_export import ReportGenerator
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'report.txt')
            result = ReportGenerator.generate_text_report(filename)
            
            assert os.path.exists(result)
            assert result.endswith('.txt')


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
