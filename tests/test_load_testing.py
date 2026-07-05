"""
WEEK 5: Load Testing Verification Tests

Verify that load testing framework itself works correctly:
- Metrics are accurate
- Load scenarios execute properly
- Results are reproducible
- Performance data is valid
"""

import pytest
from mood_to_meal_butler.locust_load_tests import (
    LoadTestMetrics, LoadTestScenario, LightLoadTest,
    MediumLoadTest, HeavyLoadTest
)


class TestLoadTestMetricsAccuracy:
    """Test accuracy of load test metrics."""
    
    def test_metrics_empty_state(self):
        """Verify metrics start empty."""
        metrics = LoadTestMetrics()
        assert metrics.total_requests == 0
        assert metrics.total_errors == 0
        assert len(metrics.response_times) == 0
    
    def test_single_request_recording(self):
        """Verify single request is recorded."""
        metrics = LoadTestMetrics()
        metrics.record_request(50.0, 200, True)
        
        assert metrics.total_requests == 1
        assert metrics.total_errors == 0
        assert metrics.response_times[0] == 50.0
        assert metrics.status_codes[200] == 1
    
    def test_error_request_recording(self):
        """Verify error requests are tracked."""
        metrics = LoadTestMetrics()
        metrics.record_request(100.0, 500, False)
        
        assert metrics.total_requests == 1
        assert metrics.total_errors == 1
        assert len(metrics.errors) == 1
        assert metrics.errors[0]['status_code'] == 500
    
    def test_multiple_status_codes(self):
        """Verify multiple status codes tracked."""
        metrics = LoadTestMetrics()
        metrics.record_request(50.0, 200, True)
        metrics.record_request(60.0, 200, True)
        metrics.record_request(100.0, 429, False)
        metrics.record_request(150.0, 500, False)
        
        assert metrics.status_codes[200] == 2
        assert metrics.status_codes[429] == 1
        assert metrics.status_codes[500] == 1
    
    def test_response_time_percentile_p50(self):
        """Verify p50 percentile calculation."""
        metrics = LoadTestMetrics()
        times = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        for t in times:
            metrics.record_request(float(t), 200, True)
        
        p50 = metrics.get_percentile(50)
        assert 40 < p50 <= 60  # Should be around median
    
    def test_response_time_percentile_p95(self):
        """Verify p95 percentile calculation."""
        metrics = LoadTestMetrics()
        for i in range(100):
            metrics.record_request(float(i + 1), 200, True)
        
        p95 = metrics.get_percentile(95)
        assert 90 < p95 <= 100
    
    def test_response_time_percentile_p99(self):
        """Verify p99 percentile calculation."""
        metrics = LoadTestMetrics()
        for i in range(100):
            metrics.record_request(float(i + 1), 200, True)
        
        p99 = metrics.get_percentile(99)
        assert 95 < p99 <= 100
    
    def test_summary_completeness(self):
        """Verify summary has all required fields."""
        metrics = LoadTestMetrics()
        for i in range(50):
            metrics.record_request(float(50 + i), 200, i % 5 == 0)
        
        summary = metrics.get_summary()
        assert 'total_requests' in summary
        assert 'response_times' in summary
        assert 'status_codes' in summary
        assert summary['response_times']['avg'] > 0
        assert summary['response_times']['min'] > 0
        assert summary['response_times']['max'] > 0


class TestLoadScenarioExecution:
    """Test load scenario execution."""
    
    def test_light_load_scenario_runs(self):
        """Verify light load scenario completes."""
        test = LightLoadTest()
        assert test.num_users == 10
        assert test.duration_seconds == 5
        
        result = test.run()
        assert result['total_requests'] > 0
        assert result['throughput'] > 0
    
    def test_medium_load_scenario_runs(self):
        """Verify medium load scenario completes."""
        test = MediumLoadTest()
        assert test.num_users == 100
        
        result = test.run()
        assert result['total_requests'] > 0
        assert result['success_rate'] >= 80
    
    def test_heavy_load_scenario_runs(self):
        """Verify heavy load scenario completes."""
        test = HeavyLoadTest()
        assert test.num_users == 1000
        
        result = test.run()
        assert result['total_requests'] > 0
    
    def test_scenario_metrics_consistency(self):
        """Verify scenario metrics are internally consistent."""
        test = LightLoadTest()
        result = test.run()
        
        # Total should equal sum of successes and failures
        expected_total = result['total_requests']
        actual_total = sum(result['status_codes'].values())
        assert expected_total == actual_total
    
    def test_response_time_ranges_valid(self):
        """Verify response time ranges are sensible."""
        test = LightLoadTest()
        result = test.run()
        
        times = result['response_times']
        assert times['min'] >= 0
        assert times['avg'] >= times['min']
        assert times['max'] >= times['avg']
        assert times['p50'] >= times['min']
        assert times['p95'] >= times['p50']
        assert times['p99'] >= times['p95']


class TestLoadTestReproducibility:
    """Test that load tests produce consistent results."""
    
    def test_multiple_runs_have_similar_results(self):
        """Verify multiple runs have consistent patterns."""
        results = []
        for _ in range(3):
            test = LightLoadTest()
            result = test.run()
            results.append(result)
        
        # All runs should have similar success rates (within 5%)
        success_rates = [r['success_rate'] for r in results]
        assert max(success_rates) - min(success_rates) < 5
    
    def test_error_distribution_consistent(self):
        """Verify error distribution is consistent."""
        test1 = MediumLoadTest()
        result1 = test1.run()
        
        test2 = MediumLoadTest()
        result2 = test2.run()
        
        # Both should have similar error rates
        error_rate1 = result1['error_rate']
        error_rate2 = result2['error_rate']
        
        assert abs(error_rate1 - error_rate2) < 2


class TestLoadTestValidation:
    """Test validation of load test data."""
    
    def test_summary_has_valid_percentages(self):
        """Verify success/error rates are valid percentages."""
        metrics = LoadTestMetrics()
        for i in range(100):
            metrics.record_request(50.0, 200, i % 10 != 0)
        
        summary = metrics.get_summary()
        assert 0 <= summary['success_rate'] <= 100
        assert 0 <= summary['error_rate'] <= 100
        assert summary['success_rate'] + summary['error_rate'] == 100
    
    def test_throughput_is_positive(self):
        """Verify throughput is positive when requests made."""
        test = LightLoadTest()
        result = test.run()
        
        assert result['throughput'] > 0
    
    def test_status_codes_are_valid_http(self):
        """Verify status codes are valid HTTP codes."""
        test = MediumLoadTest()
        result = test.run()
        
        for status_code in result['status_codes'].keys():
            assert 100 <= status_code < 600


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
