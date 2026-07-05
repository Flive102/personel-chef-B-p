"""Production health checks and metrics collection."""

import time
import psutil
from typing import Dict, Any
from datetime import datetime


class HealthCheck:
    """Monitor application health for production deployment."""
    
    def __init__(self):
        self.start_time = time.time()
        self.requests_total = 0
        self.requests_errors = 0
        self.db_queries_total = 0
        self.db_errors = 0
    
    def record_request(self, success: bool = True):
        """Record API request."""
        self.requests_total += 1
        if not success:
            self.requests_errors += 1
    
    def record_db_query(self, success: bool = True):
        """Record database query."""
        self.db_queries_total += 1
        if not success:
            self.db_errors += 1
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive health status.
        
        Returns:
            Dict with status, metrics, and recommendations
        """
        uptime_seconds = time.time() - self.start_time
        error_rate = (
            self.requests_errors / self.requests_total 
            if self.requests_total > 0 else 0
        )
        
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        # Determine health status
        if error_rate > 0.1 or cpu_percent > 90:
            status = "UNHEALTHY"
        elif error_rate > 0.05 or cpu_percent > 75:
            status = "DEGRADED"
        else:
            status = "HEALTHY"
        
        return {
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": uptime_seconds,
            "requests": {
                "total": self.requests_total,
                "errors": self.requests_errors,
                "error_rate": round(error_rate, 4),
            },
            "database": {
                "queries_total": self.db_queries_total,
                "errors": self.db_errors,
            },
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_mb": memory.available / (1024 * 1024),
            },
            "recommendations": get_recommendations(status, error_rate, cpu_percent)
        }


def get_recommendations(status: str, error_rate: float, cpu_percent: float) -> list:
    """Generate recommendations based on health metrics."""
    recommendations = []
    
    if error_rate > 0.1:
        recommendations.append("High error rate detected. Check logs for details.")
    
    if cpu_percent > 90:
        recommendations.append("CPU usage critical. Consider scaling up.")
    
    if cpu_percent > 75:
        recommendations.append("CPU usage elevated. Monitor for increases.")
    
    if not recommendations:
        recommendations.append("System operating normally.")
    
    return recommendations


# Global health monitor
health_check = HealthCheck()


def get_health_status() -> Dict[str, Any]:
    """Get current health status (for /health endpoint)."""
    return health_check.get_status()
