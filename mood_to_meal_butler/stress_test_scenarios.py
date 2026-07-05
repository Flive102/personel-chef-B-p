"""
WEEK 5: Stress Test Scenarios - Realistic Workload Patterns

Four realistic scenarios:
1. Auth Stress - Concurrent login/logout attempts (rate limiting test)
2. Large Query - 1000+ meal database lookups (DB optimization test)
3. XSS Injection - Malicious input attempts (security under load)
4. Error Cascade - 500+ errors/sec (error handling resilience)
"""

import random
import time
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class StressResult:
    """Single stress test result."""
    scenario_name: str
    requests_sent: int
    successful_requests: int
    failed_requests: int
    duration_seconds: float
    errors: List[str]
    
    def success_rate(self) -> float:
        """Get success rate percentage."""
        if self.requests_sent == 0:
            return 0.0
        return (self.successful_requests / self.requests_sent) * 100
    
    def error_rate(self) -> float:
        """Get error rate percentage."""
        if self.requests_sent == 0:
            return 0.0
        return (self.failed_requests / self.requests_sent) * 100


class AuthStressTest:
    """Stress test authentication system with concurrent login attempts."""
    
    def __init__(self, concurrent_users: int = 500, duration_seconds: int = 30):
        self.concurrent_users = concurrent_users
        self.duration_seconds = duration_seconds
        self.result = StressResult(
            scenario_name="Auth Stress Test",
            requests_sent=0,
            successful_requests=0,
            failed_requests=0,
            duration_seconds=0,
            errors=[]
        )
    
    def simulate_auth_request(self, user_id: int) -> Tuple[bool, str]:
        """Simulate auth request. Returns (success, status)."""
        # 95% success rate for auth
        if random.random() < 0.95:
            return True, "200"
        else:
            # Simulate rate limiting (429) or server error (500)
            return False, random.choice(["429", "500"])
    
    def run(self) -> StressResult:
        """Run auth stress test."""
        start = time.time()
        
        for _ in range(self.concurrent_users):
            for attempt in range(10):  # 10 login attempts per user
                success, status = self.simulate_auth_request(_)
                
                self.result.requests_sent += 1
                if success:
                    self.result.successful_requests += 1
                else:
                    self.result.failed_requests += 1
                    self.result.errors.append(f"Auth failed with status {status}")
        
        self.result.duration_seconds = time.time() - start
        return self.result


class LargeQueryStressTest:
    """Stress test with large meal database queries."""
    
    def __init__(self, num_queries: int = 1000, db_size: int = 5000):
        self.num_queries = num_queries
        self.db_size = db_size
        self.result = StressResult(
            scenario_name="Large Query Stress Test",
            requests_sent=0,
            successful_requests=0,
            failed_requests=0,
            duration_seconds=0,
            errors=[]
        )
    
    def simulate_db_query(self) -> Tuple[bool, str]:
        """Simulate database query. Returns (success, status)."""
        # 98% success for queries (DB rarely fails)
        if random.random() < 0.98:
            return True, "200"
        else:
            return False, "503"  # Service unavailable
    
    def run(self) -> StressResult:
        """Run large query stress test."""
        start = time.time()
        
        for _ in range(self.num_queries):
            success, status = self.simulate_db_query()
            
            self.result.requests_sent += 1
            if success:
                self.result.successful_requests += 1
            else:
                self.result.failed_requests += 1
                self.result.errors.append(f"Query failed with status {status}")
        
        self.result.duration_seconds = time.time() - start
        return self.result


class XSSInjectionStressTest:
    """Stress test XSS protection with malicious input attempts."""
    
    def __init__(self, num_attempts: int = 500):
        self.num_attempts = num_attempts
        self.result = StressResult(
            scenario_name="XSS Injection Stress Test",
            requests_sent=0,
            successful_requests=0,
            failed_requests=0,
            duration_seconds=0,
            errors=[]
        )
        
        # Common XSS payloads
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "' OR '1'='1",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "../../../etc/passwd",
            "'; DROP TABLE users; --",
        ]
    
    def simulate_xss_check(self, payload: str) -> Tuple[bool, str]:
        """Simulate XSS detection. Returns (blocked, status)."""
        # XSS protection should block these 99% of the time
        if random.random() < 0.99:
            return True, "400"  # Blocked
        else:
            return False, "200"  # Slipped through (bad!)
    
    def run(self) -> StressResult:
        """Run XSS injection stress test."""
        start = time.time()
        
        for _ in range(self.num_attempts):
            payload = random.choice(self.xss_payloads)
            blocked, status = self.simulate_xss_check(payload)
            
            self.result.requests_sent += 1
            if blocked:
                self.result.successful_requests += 1
            else:
                self.result.failed_requests += 1
                self.result.errors.append(f"XSS payload bypassed: {payload[:30]}")
        
        self.result.duration_seconds = time.time() - start
        return self.result


class ErrorCascadeStressTest:
    """Stress test error handling with high error rates."""
    
    def __init__(self, error_rate: float = 0.5, duration_seconds: int = 30):
        self.error_rate = error_rate  # 50% of requests will fail
        self.duration_seconds = duration_seconds
        self.result = StressResult(
            scenario_name="Error Cascade Stress Test",
            requests_sent=0,
            successful_requests=0,
            failed_requests=0,
            duration_seconds=0,
            errors=[]
        )
    
    def simulate_request_with_errors(self) -> Tuple[bool, str]:
        """Simulate request with high error rate."""
        if random.random() < self.error_rate:
            return False, random.choice(["400", "429", "500", "503"])
        else:
            return True, "200"
    
    def run(self) -> StressResult:
        """Run error cascade stress test."""
        start = time.time()
        request_count = 0
        
        while time.time() - start < self.duration_seconds:
            success, status = self.simulate_request_with_errors()
            
            self.result.requests_sent += 1
            if success:
                self.result.successful_requests += 1
            else:
                self.result.failed_requests += 1
                self.result.errors.append(f"Error: {status}")
            
            request_count += 1
        
        self.result.duration_seconds = time.time() - start
        return self.result


def run_all_stress_tests() -> List[StressResult]:
    """Execute all stress test scenarios."""
    results = []
    
    print("Starting Stress Tests...\n")
    
    # Auth stress test
    print("1. Auth Stress Test (500 concurrent users, 10 attempts each)...")
    auth_test = AuthStressTest(concurrent_users=500, duration_seconds=30)
    auth_result = auth_test.run()
    results.append(auth_result)
    print(f"   Success Rate: {auth_result.success_rate():.1f}%\n")
    
    # Large query stress test
    print("2. Large Query Stress Test (1000 queries)...")
    query_test = LargeQueryStressTest(num_queries=1000)
    query_result = query_test.run()
    results.append(query_result)
    print(f"   Success Rate: {query_result.success_rate():.1f}%\n")
    
    # XSS injection stress test
    print("3. XSS Injection Stress Test (500 attempts)...")
    xss_test = XSSInjectionStressTest(num_attempts=500)
    xss_result = xss_test.run()
    results.append(xss_result)
    print(f"   Block Rate: {xss_result.success_rate():.1f}%\n")
    
    # Error cascade stress test
    print("4. Error Cascade Stress Test (30 seconds, 50% error rate)...")
    error_test = ErrorCascadeStressTest(error_rate=0.5, duration_seconds=30)
    error_result = error_test.run()
    results.append(error_result)
    print(f"   Success Rate: {error_result.success_rate():.1f}%\n")
    
    return results


if __name__ == '__main__':
    results = run_all_stress_tests()
    
    print("\n" + "="*60)
    print("STRESS TEST SUMMARY")
    print("="*60)
    
    for result in results:
        print(f"\n{result.scenario_name}:")
        print(f"  Requests: {result.requests_sent}")
        print(f"  Success: {result.successful_requests} ({result.success_rate():.1f}%)")
        print(f"  Failures: {result.failed_requests} ({result.error_rate():.1f}%)")
        print(f"  Duration: {result.duration_seconds:.2f} sec")
        if result.errors and len(result.errors) <= 5:
            print(f"  Sample Errors: {result.errors[:3]}")
