"""
Health Dashboard - Real-time System Monitoring

Tracks:
- System health status
- Performance metrics
- Error rates
- Cache hit rates
- Database connection pool status
"""

from typing import Dict, List
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class HealthMetric:
    """Single health metric snapshot."""
    name: str
    status: str  # HEALTHY, WARNING, CRITICAL
    value: float
    threshold: float
    timestamp: datetime


class HealthMonitor:
    """Centralized health monitoring system."""
    
    def __init__(self):
        self.metrics: Dict[str, HealthMetric] = {}
        self.history: List[Dict] = []
        self.alert_threshold = 0.8  # 80% threshold
    
    def record_metric(self, name: str, value: float, threshold: float):
        """Record health metric."""
        if value <= threshold * 0.5:
            status = 'CRITICAL'
        elif value <= threshold * 0.8:
            status = 'WARNING'
        else:
            status = 'HEALTHY'
        
        metric = HealthMetric(
            name=name,
            status=status,
            value=value,
            threshold=threshold,
            timestamp=datetime.now()
        )
        
        self.metrics[name] = metric
    
    def get_dashboard(self) -> Dict:
        """Get full health dashboard."""
        overall_status = self._calculate_overall_status()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'overall_status': overall_status,
            'metrics': {
                name: {
                    'status': m.status,
                    'value': m.value,
                    'threshold': m.threshold,
                }
                for name, m in self.metrics.items()
            }
        }
    
    def _calculate_overall_status(self) -> str:
        """Calculate overall system status."""
        if not self.metrics:
            return 'UNKNOWN'
        
        statuses = [m.status for m in self.metrics.values()]
        
        if 'CRITICAL' in statuses:
            return 'CRITICAL'
        elif 'WARNING' in statuses:
            return 'WARNING'
        else:
            return 'HEALTHY'
    
    def get_alerts(self) -> List[Dict]:
        """Get current alerts."""
        alerts = []
        
        for name, metric in self.metrics.items():
            if metric.status != 'HEALTHY':
                alerts.append({
                    'metric': name,
                    'status': metric.status,
                    'message': f'{name} is {metric.status}',
                    'timestamp': metric.timestamp.isoformat()
                })
        
        return alerts


class PerformanceMonitor:
    """Monitor performance metrics."""
    
    def __init__(self):
        self.response_times = []
        self.error_count = 0
        self.request_count = 0
    
    def record_request(self, duration_ms: float, success: bool):
        """Record request for monitoring."""
        self.response_times.append(duration_ms)
        self.request_count += 1
        if not success:
            self.error_count += 1
    
    def get_metrics(self) -> Dict:
        """Get performance metrics."""
        if not self.response_times:
            return {'status': 'No data'}
        
        times = sorted(self.response_times)
        error_rate = (self.error_count / self.request_count * 100) if self.request_count > 0 else 0
        
        return {
            'avg_response_ms': sum(times) / len(times),
            'p95_response_ms': times[int(len(times) * 0.95)] if len(times) > 0 else 0,
            'error_rate': error_rate,
            'total_requests': self.request_count,
        }


class CacheMonitor:
    """Monitor cache performance."""
    
    def __init__(self):
        self.hits = 0
        self.misses = 0
    
    def record_hit(self):
        """Record cache hit."""
        self.hits += 1
    
    def record_miss(self):
        """Record cache miss."""
        self.misses += 1
    
    def get_metrics(self) -> Dict:
        """Get cache metrics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'total_accesses': total,
        }


# Global monitors
_health_monitor = None
_performance_monitor = None
_cache_monitor = None


def get_health_monitor() -> HealthMonitor:
    """Get or create global health monitor."""
    global _health_monitor
    if _health_monitor is None:
        _health_monitor = HealthMonitor()
    return _health_monitor


def get_performance_monitor() -> PerformanceMonitor:
    """Get or create global performance monitor."""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor


def get_cache_monitor() -> CacheMonitor:
    """Get or create global cache monitor."""
    global _cache_monitor
    if _cache_monitor is None:
        _cache_monitor = CacheMonitor()
    return _cache_monitor
