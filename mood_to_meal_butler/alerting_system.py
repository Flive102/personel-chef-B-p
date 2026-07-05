"""
Alerting System - Real-time Alert Detection and Notifications

Detects:
- High error rates
- Security events
- Critical errors
- Performance degradation
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Callable, Optional, Any
from collections import deque
from mood_to_meal_butler.error_tracking import (
    ErrorTracker, ErrorCategory, get_error_tracker
)


class AlertLevel:
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    SECURITY = "security"


class Alert:
    """Alert data structure."""
    
    def __init__(
        self,
        alert_id: str,
        level: str,
        title: str,
        message: str,
        category: str,
        context: Optional[Dict] = None
    ):
        self.alert_id = alert_id
        self.timestamp = datetime.utcnow().isoformat()
        self.level = level
        self.title = title
        self.message = message
        self.category = category
        self.context = context or {}
        self.acknowledged = False
        self.acknowledged_by = None
        self.acknowledged_at = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "alert_id": self.alert_id,
            "timestamp": self.timestamp,
            "level": self.level,
            "title": self.title,
            "message": self.message,
            "category": self.category,
            "context": self.context,
            "acknowledged": self.acknowledged,
        }


class AlertingSystem:
    """Real-time alerting and notification system."""
    
    def __init__(self):
        self.alerts: deque = deque(maxlen=1000)  # Keep last 1000 alerts
        self.handlers: List[Callable] = []
        self.error_tracker = get_error_tracker()
        
        # Alert thresholds
        self.high_error_rate_threshold = 0.05  # 5% errors
        self.critical_error_threshold = 10  # 10 errors in 5 min
        self.security_alert_threshold = 5  # 5 security errors in 5 min
        
        # Time windows for metrics
        self.window_size = timedelta(minutes=5)
    
    def register_handler(self, handler: Callable) -> None:
        """Register alert notification handler."""
        self.handlers.append(handler)
    
    def check_high_error_rate(self) -> Optional[Alert]:
        """Check if error rate is too high."""
        metrics = self.error_tracker.get_metrics()
        total_errors = metrics["total_errors"]
        
        if total_errors > 100:
            # Simplified: if total errors > 100, assume high rate
            alert = Alert(
                alert_id=f"alert_{datetime.utcnow().timestamp()}",
                level=AlertLevel.WARNING,
                title="High Error Rate Detected",
                message=f"Error rate exceeded threshold: {total_errors} errors",
                category="performance",
                context={"total_errors": total_errors}
            )
            self._fire_alert(alert)
            return alert
        
        return None
    
    def check_security_events(self) -> List[Alert]:
        """Check for security-related errors."""
        security_errors = self.error_tracker.get_errors_by_category(
            ErrorCategory.SECURITY_ERROR
        )
        
        alerts = []
        recent_count = len([
            e for e in security_errors
            if self._is_recent(e["timestamp"])
        ])
        
        if recent_count >= self.security_alert_threshold:
            alert = Alert(
                alert_id=f"alert_{datetime.utcnow().timestamp()}",
                level=AlertLevel.SECURITY,
                title="Security Event Alert",
                message=f"{recent_count} security errors in last 5 minutes",
                category="security",
                context={"count": recent_count, "type": "security"}
            )
            self._fire_alert(alert)
            alerts.append(alert)
        
        return alerts
    
    def check_critical_errors(self) -> Optional[Alert]:
        """Check for critical/5xx errors."""
        recent_errors = [
            e for e in self.error_tracker.get_recent_errors(limit=100)
            if self._is_recent(e["timestamp"])
            and e["status_code"] >= 500
        ]
        
        if len(recent_errors) >= self.critical_error_threshold:
            alert = Alert(
                alert_id=f"alert_{datetime.utcnow().timestamp()}",
                level=AlertLevel.CRITICAL,
                title="Critical Errors Detected",
                message=f"{len(recent_errors)} server errors in last 5 minutes",
                category="critical",
                context={
                    "count": len(recent_errors),
                    "error_types": list(set(
                        e["exception_type"] for e in recent_errors
                    ))
                }
            )
            self._fire_alert(alert)
            return alert
        
        return None
    
    def check_database_issues(self) -> Optional[Alert]:
        """Check for database connectivity problems."""
        db_errors = self.error_tracker.get_errors_by_category(
            ErrorCategory.DATABASE_ERROR
        )
        
        recent_count = len([
            e for e in db_errors
            if self._is_recent(e["timestamp"])
        ])
        
        if recent_count >= 5:
            alert = Alert(
                alert_id=f"alert_{datetime.utcnow().timestamp()}",
                level=AlertLevel.CRITICAL,
                title="Database Connectivity Issue",
                message=f"{recent_count} database errors in last 5 minutes",
                category="database",
                context={"count": recent_count}
            )
            self._fire_alert(alert)
            return alert
        
        return None
    
    def run_health_checks(self) -> Dict[str, Any]:
        """Run all alert checks and return status."""
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {}
        }
        
        # Run all checks
        error_rate_alert = self.check_high_error_rate()
        results["checks"]["error_rate"] = error_rate_alert.to_dict() if error_rate_alert else None
        
        security_alerts = self.check_security_events()
        results["checks"]["security"] = [a.to_dict() for a in security_alerts]
        
        critical_alert = self.check_critical_errors()
        results["checks"]["critical"] = critical_alert.to_dict() if critical_alert else None
        
        db_alert = self.check_database_issues()
        results["checks"]["database"] = db_alert.to_dict() if db_alert else None
        
        results["alert_count"] = len(self.alerts)
        results["status"] = "healthy" if not any([
            error_rate_alert, security_alerts, critical_alert, db_alert
        ]) else "unhealthy"
        
        return results
    
    def _fire_alert(self, alert: Alert) -> None:
        """Send alert to all registered handlers."""
        self.alerts.append(alert)
        
        for handler in self.handlers:
            try:
                handler(alert)
            except Exception as e:
                print(f"Alert handler failed: {e}")
    
    def _is_recent(self, timestamp: str, minutes: int = 5) -> bool:
        """Check if timestamp is within window."""
        try:
            event_time = datetime.fromisoformat(timestamp)
            cutoff = datetime.utcnow() - timedelta(minutes=minutes)
            return event_time > cutoff
        except:
            return False
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Get recent alerts."""
        return [a.to_dict() for a in list(self.alerts)[-limit:]]
    
    def acknowledge_alert(
        self,
        alert_id: str,
        acknowledged_by: str
    ) -> bool:
        """Mark alert as acknowledged."""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged = True
                alert.acknowledged_by = acknowledged_by
                alert.acknowledged_at = datetime.utcnow().isoformat()
                return True
        return False


# Global alerting system instance
_alerting_system = None


def get_alerting_system() -> AlertingSystem:
    """Get or create global alerting system."""
    global _alerting_system
    if _alerting_system is None:
        _alerting_system = AlertingSystem()
    return _alerting_system
