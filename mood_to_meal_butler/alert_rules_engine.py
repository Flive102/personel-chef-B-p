"""
Alert Rules Engine - Custom Alert Rules

Provides:
- Define custom alert rules
- Trigger alerts based on conditions
- Rule evaluation & execution
- Alert history & logging
"""

from typing import Dict, List, Callable, Any, Optional
from datetime import datetime
import json


class AlertRule:
    """Define a single alert rule."""
    
    def __init__(self, rule_id: str, name: str, condition: Callable, 
                 action: Callable, enabled: bool = True):
        self.rule_id = rule_id
        self.name = name
        self.condition = condition  # Returns bool
        self.action = action  # Executes when condition is true
        self.enabled = enabled
        self.triggered_count = 0
        self.last_triggered = None
    
    def evaluate(self) -> bool:
        """Evaluate rule condition."""
        try:
            return self.condition()
        except Exception as e:
            print(f"Error evaluating rule {self.name}: {e}")
            return False
    
    def execute(self) -> Dict:
        """Execute rule action."""
        if not self.enabled:
            return {'status': 'disabled'}
        
        try:
            result = self.action()
            self.triggered_count += 1
            self.last_triggered = datetime.now().isoformat()
            return {'status': 'executed', 'result': result}
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
    
    def to_dict(self) -> Dict:
        """Convert rule to dictionary."""
        return {
            'rule_id': self.rule_id,
            'name': self.name,
            'enabled': self.enabled,
            'triggered_count': self.triggered_count,
            'last_triggered': self.last_triggered,
        }


class AlertRulesEngine:
    """Manage and evaluate alert rules."""
    
    def __init__(self):
        self.rules: Dict[str, AlertRule] = {}
        self.history: List[Dict] = []
        self.max_history = 1000
    
    def add_rule(self, rule: AlertRule) -> Dict:
        """Add alert rule."""
        self.rules[rule.rule_id] = rule
        return {'status': 'added', 'rule_id': rule.rule_id}
    
    def remove_rule(self, rule_id: str) -> Dict:
        """Remove alert rule."""
        if rule_id in self.rules:
            del self.rules[rule_id]
            return {'status': 'removed', 'rule_id': rule_id}
        return {'error': 'Rule not found'}
    
    def enable_rule(self, rule_id: str) -> Dict:
        """Enable alert rule."""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = True
            return {'status': 'enabled', 'rule_id': rule_id}
        return {'error': 'Rule not found'}
    
    def disable_rule(self, rule_id: str) -> Dict:
        """Disable alert rule."""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = False
            return {'status': 'disabled', 'rule_id': rule_id}
        return {'error': 'Rule not found'}
    
    def evaluate_all(self) -> Dict:
        """Evaluate all rules."""
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_rules': len(self.rules),
            'triggered': [],
            'evaluated': 0
        }
        
        for rule_id, rule in self.rules.items():
            if rule.enabled and rule.evaluate():
                exec_result = rule.execute()
                results['triggered'].append({
                    'rule_id': rule_id,
                    'name': rule.name,
                    'result': exec_result
                })
                
                # Add to history
                self._add_to_history({
                    'rule_id': rule_id,
                    'name': rule.name,
                    'timestamp': datetime.now().isoformat(),
                    'triggered': True
                })
            
            results['evaluated'] += 1
        
        return results
    
    def _add_to_history(self, event: Dict):
        """Add event to history."""
        self.history.append(event)
        
        # Keep history size bounded
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_rules(self) -> List[Dict]:
        """Get all rules."""
        return [rule.to_dict() for rule in self.rules.values()]
    
    def get_history(self, limit: int = 100) -> List[Dict]:
        """Get alert history."""
        return self.history[-limit:]
    
    def get_stats(self) -> Dict:
        """Get alert statistics."""
        triggered = sum(1 for r in self.rules.values() if r.triggered_count > 0)
        total_triggers = sum(r.triggered_count for r in self.rules.values())
        
        return {
            'total_rules': len(self.rules),
            'enabled_rules': sum(1 for r in self.rules.values() if r.enabled),
            'rules_with_triggers': triggered,
            'total_triggers': total_triggers,
            'history_size': len(self.history),
        }


# Predefined alert rules
def create_high_error_rate_rule() -> AlertRule:
    """Create rule for high error rates."""
    def check_errors():
        # Simulated check
        return False
    
    def on_error():
        return "High error rate detected"
    
    return AlertRule('high_error_rate', 'High Error Rate', check_errors, on_error)


def create_low_cache_hit_rule() -> AlertRule:
    """Create rule for low cache hit rates."""
    def check_cache():
        # Simulated check
        return False
    
    def on_cache_miss():
        return "Low cache hit rate"
    
    return AlertRule('low_cache_hit', 'Low Cache Hit Rate', check_cache, on_cache_miss)


# Global alert engine instance
_alert_engine = None


def get_alert_rules_engine() -> AlertRulesEngine:
    """Get or create global alert rules engine."""
    global _alert_engine
    if _alert_engine is None:
        _alert_engine = AlertRulesEngine()
    return _alert_engine
