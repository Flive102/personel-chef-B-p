"""
WEEK 5: Performance Tests - Verify Load Testing & Metrics

Tests verify:
- Load test scenarios execute correctly
- Performance metrics are calculated accurately
- Stress tests detect issues properly
- Performance improvements are measurable
"""

import pytest
import time
from mood_to_meal_butler.locust_load_tests import (
    LoadTestMetrics, LoadTestScenario, LightLoadTest, 
    MediumLoadTest, HeavyLoadTest, run_all_load_tests
)
from mood_to_meal_butler.performance_metrics import (
    PerformanceTracker, PerformanceProfile, BenchmarkComparison,
    get_performance_tracker, reset_tracker
)
from mood_to_meal_butler.stress_test_scenarios import (
    AuthStressTest, LargeQueryStressTest, XSSInjectionStressTest,
    ErrorCascadeStressTest, run_all_stress_tests
)


class TestLoadTestMetrics:
    """Test load test metrics collection."""
    
    def test_metrics_initialization(self):
        """Verify metrics initialized correctly."""
        metrics = LoadTestMetrics()
        assert metrics.total_requests == 0
        assert metrics.total_errors == 0
        assert len(metrics.response_times) == 0
    
    def test_record_request(self):
        """Verify request recording."""
        metrics = LoadTestMetrics()
        metrics.record_request(50.0, 200, True)
        metrics.record_request(100.0, 200, True)
        metrics.record_request(75.0, 500, False)
        
        assert metrics.total_requests == 3
        assert metrics.total_errors == 1
        assert len(metrics.response_times) == 3
    
    def test_percentile_calculation(self):
        """Verify percentile calculations."""
        metrics = LoadTestMetrics()
        for i in range(100):
            metrics.record_request(float(i + 1), 200, True)
        
        p50 = metrics.get_percentile(50)
        p95 = metrics.get_percentile(95)
        p99 = metrics.get_percentile(99)
        
        assert 40 < p50 < 60  # Should be around 50
        assert 90 < p95 < 100  # Should be around 95
        assert 95 < p99 <= 100  # Should be around 99
    
    def test_summary_generation(self):
        """Verify metrics summary generation."""
        metrics = LoadTestMetrics()
        for i in range(50):
            metrics.record_request(50.0 + i, 200, i % 10 == 0)
        
        summary = metrics.get_summary()
        assert summary['total_requests'] == 50
        assert summary['error_rate'] > 0
        assert 'response_times' in summary
        assert summary['response_times']['avg'] > 0


class TestPerformanceTracking:
    """Test performance tracking functionality."""
    
    def test_tracker_initialization(self):
        """Verify tracker initializes correctly."""
        tracker = PerformanceTracker()
        assert tracker.start_time is None
        assert tracker.end_time is None
        assert tracker.request_count == 0
    
    def test_start_stop_tracking(self):
        """Verify tracking lifecycle."""
        tracker = PerformanceTracker()
        tracker.start_tracking()
        assert tracker.start_time is not None
        
        tracker.record_response(50.0)
        tracker.record_response(75.0)
        assert tracker.request_count == 2
        
        tracker.end_tracking()
        assert tracker.end_time is not None
    
    def test_response_recording(self):
        """Verify response recording."""
        tracker = PerformanceTracker()
        tracker.start_tracking()
        
        for i in range(10):
            tracker.record_response(50.0 + i * 5)
        
        tracker.end_tracking()
        
        avg = tracker.get_average_response_time()
        assert 50 < avg < 100
        assert tracker.get_throughput() > 0
    
    def test_baseline_comparison(self):
        """Verify baseline comparison."""
        tracker = PerformanceTracker()
        tracker.start_tracking()
        
        for i in range(20):
            tracker.record_response(100.0)
        
        tracker.end_tracking()
        baseline = tracker.set_baseline()
        
        assert baseline['avg_response_ms'] == 100.0
        
        # Simulate improvement
        tracker.start_tracking()
        for i in range(20):
            tracker.record_response(50.0)
        tracker.end_tracking()
        
        summary = tracker.get_summary()
        assert summary['baseline_comparison'] is not None
        assert summary['baseline_comparison']['response_time_improvement_percent'] > 0


class TestLoadTestScenarios:
    """Test load test scenario execution."""
    
    def test_light_load_test(self):
        """Verify light load test runs."""
        test = LightLoadTest()
        result = test.run()
        
        assert result['total_requests'] > 0
        assert 'response_times' in result
        assert result['response_times']['avg'] > 0
        assert result['success_rate'] >= 95  # Should have high success
    
    def test_medium_load_test(self):
        """Verify medium load test runs."""
        test = MediumLoadTest()
        result = test.run()
        
        assert result['total_requests'] > result['total_errors']
        assert result['throughput'] > 0
        assert result['success_rate'] >= 90
    
    def test_heavy_load_test(self):
        """Verify heavy load test runs."""
        test = HeavyLoadTest()
        result = test.run()
        
        assert result['total_requests'] > 0
        # Under heavy load, some errors expected
        assert result['success_rate'] >= 80
    
    def test_response_time_increases_with_load(self):
        """Verify response times increase with concurrent users."""
        light = LightLoadTest()
        light_result = light.run()
        
        heavy = HeavyLoadTest()
        heavy_result = heavy.run()
        
        # Heavy load should have higher response times
        assert heavy_result['response_times']['avg'] >= light_result['response_times']['avg']


class TestStressScenarios:
    """Test stress test scenarios."""
    
    def test_auth_stress_test(self):
        """Verify auth stress test."""
        test = AuthStressTest(concurrent_users=100, duration_seconds=5)
        result = test.run()
        
        assert result.requests_sent > 0
        assert result.success_rate() > 90
        assert result.error_rate() < 10
    
    def test_large_query_stress_test(self):
        """Verify large query stress test."""
        test = LargeQueryStressTest(num_queries=200)
        result = test.run()
        
        assert result.requests_sent == 200
        assert result.success_rate() > 95
    
    def test_xss_injection_stress_test(self):
        """Verify XSS protection under stress."""
        test = XSSInjectionStressTest(num_attempts=100)
        result = test.run()
        
        assert result.requests_sent == 100
        # Should block 99%+ of XSS attempts
        assert result.success_rate() >= 95
    
    def test_error_cascade_stress_test(self):
        """Verify error handling under cascade."""
        test = ErrorCascadeStressTest(error_rate=0.5, duration_seconds=5)
        result = test.run()
        
        assert result.requests_sent > 0
        # Error rate should match configured rate (50%)
        assert 40 < result.error_rate() < 60


class TestLoadTestIntegration:
    """Integration tests for performance framework."""
    
    def test_all_load_tests_complete(self):
        """Verify all load tests run to completion."""
        results = run_all_load_tests()
        
        assert len(results) == 3
        assert "Light Load" in results
        assert "Medium Load" in results
        assert "Heavy Load" in results
    
    def test_all_stress_tests_complete(self):
        """Verify all stress tests run to completion."""
        results = run_all_stress_tests()
        
        assert len(results) == 4
        assert results[0].scenario_name == "Auth Stress Test"
        assert results[1].scenario_name == "Large Query Stress Test"
        assert results[2].scenario_name == "XSS Injection Stress Test"
        assert results[3].scenario_name == "Error Cascade Stress Test"
    
    def test_performance_baselines_established(self):
        """Verify performance baselines can be established."""
        tracker = PerformanceTracker()
        tracker.start_tracking()
        
        for i in range(50):
            tracker.record_response(75.0 + i)
        
        tracker.end_tracking()
        baseline = tracker.set_baseline()
        
        assert baseline is not None
        assert 'avg_response_ms' in baseline
        assert 'p95_response_ms' in baseline


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
