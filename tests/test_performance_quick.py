"""
WEEK 5: Quick Performance Tests (Lightweight, No Timeout)

Faster tests that verify framework logic without running full scenarios.
"""

import pytest
from mood_to_meal_butler.locust_load_tests import LoadTestMetrics
from mood_to_meal_butler.performance_metrics import PerformanceTracker
from mood_to_meal_butler.stress_test_scenarios import (
    AuthStressTest, LargeQueryStressTest, XSSInjectionStressTest
)


class TestMetricsCore:
    """Test core metrics functionality."""
    
    def test_metrics_init(self):
        """Metrics initialize empty."""
        m = LoadTestMetrics()
        assert m.total_requests == 0
        assert m.total_errors == 0
    
    def test_record_single(self):
        """Record single request."""
        m = LoadTestMetrics()
        m.record_request(50.0, 200, True)
        assert m.total_requests == 1
        assert m.status_codes[200] == 1
    
    def test_error_tracking(self):
        """Track errors correctly."""
        m = LoadTestMetrics()
        m.record_request(100.0, 500, False)
        assert m.total_errors == 1
        assert len(m.errors) == 1
    
    def test_percentile_basic(self):
        """Percentile calculation works."""
        m = LoadTestMetrics()
        for i in range(10):
            m.record_request(float(i * 10), 200, True)
        
        p50 = m.get_percentile(50)
        assert p50 > 0


class TestPerformanceTracker:
    """Test performance tracker."""
    
    def test_tracker_init(self):
        """Tracker initializes."""
        t = PerformanceTracker()
        assert t.request_count == 0
    
    def test_record_responses(self):
        """Record responses."""
        t = PerformanceTracker()
        t.start_tracking()
        t.record_response(50.0)
        t.record_response(75.0)
        assert t.request_count == 2
    
    def test_average_calculation(self):
        """Calculate average correctly."""
        t = PerformanceTracker()
        t.start_tracking()
        t.record_response(50.0)
        t.record_response(100.0)
        avg = t.get_average_response_time()
        assert avg == 75.0


class TestStressQuick:
    """Quick stress test checks."""
    
    def test_auth_stress_init(self):
        """Auth stress test initializes."""
        test = AuthStressTest(concurrent_users=10, duration_seconds=1)
        assert test.result.scenario_name == "Auth Stress Test"
    
    def test_query_stress_init(self):
        """Query stress test initializes."""
        test = LargeQueryStressTest(num_queries=10)
        assert test.result.scenario_name == "Large Query Stress Test"
    
    def test_xss_stress_init(self):
        """XSS stress test initializes."""
        test = XSSInjectionStressTest(num_attempts=10)
        assert test.result.scenario_name == "XSS Injection Stress Test"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
