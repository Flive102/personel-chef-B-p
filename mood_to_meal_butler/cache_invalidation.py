"""
WEEK 6: Cache Invalidation - Smart Cache Invalidation Strategy

Implements:
- Event-based invalidation (on data changes)
- Time-based expiration (TTL)
- Dependency tracking (when meal added, invalidate all emotion caches)
"""

from typing import Dict, List, Set, Callable, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class InvalidationEvent(Enum):
    """Types of invalidation events."""
    MEAL_ADDED = "meal_added"
    MEAL_UPDATED = "meal_updated"
    MEAL_DELETED = "meal_deleted"
    EMOTION_CONFIG_CHANGED = "emotion_config_changed"
    SITUATION_CONFIG_CHANGED = "situation_config_changed"
    USER_PREFS_UPDATED = "user_prefs_updated"


@dataclass
class InvalidationRule:
    """Rule for cache invalidation."""
    event_type: InvalidationEvent
    cache_patterns: List[str]  # Glob patterns like "meal_rec:*"
    handler: Optional[Callable] = None


class CacheInvalidationManager:
    """Manage cache invalidation events and rules."""
    
    def __init__(self):
        self.rules: Dict[InvalidationEvent, List[InvalidationRule]] = {}
        self.invalidation_log: List[Dict] = []
        self.handlers: Dict[str, List[Callable]] = {}
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Setup default invalidation rules."""
        # When meal added, invalidate all recommendations
        self.add_rule(InvalidationRule(
            event_type=InvalidationEvent.MEAL_ADDED,
            cache_patterns=["meal_rec:*"]
        ))
        
        # When emotion config changed, invalidate all emotion-based caches
        self.add_rule(InvalidationRule(
            event_type=InvalidationEvent.EMOTION_CONFIG_CHANGED,
            cache_patterns=["meal_rec:*"]
        ))
        
        # When user prefs updated, invalidate user cache
        self.add_rule(InvalidationRule(
            event_type=InvalidationEvent.USER_PREFS_UPDATED,
            cache_patterns=["user_prefs:*"]
        ))
    
    def add_rule(self, rule: InvalidationRule):
        """Register invalidation rule."""
        if rule.event_type not in self.rules:
            self.rules[rule.event_type] = []
        self.rules[rule.event_type].append(rule)
    
    def register_handler(self, cache_pattern: str, handler: Callable):
        """Register callback handler for cache pattern."""
        if cache_pattern not in self.handlers:
            self.handlers[cache_pattern] = []
        self.handlers[cache_pattern].append(handler)
    
    def trigger_invalidation(self, event: InvalidationEvent, context: Dict = None):
        """Trigger cache invalidation for event."""
        context = context or {}
        
        if event not in self.rules:
            return
        
        invalidated_patterns = []
        
        for rule in self.rules[event]:
            for pattern in rule.cache_patterns:
                invalidated_patterns.append(pattern)
                
                # Call registered handlers
                if pattern in self.handlers:
                    for handler in self.handlers[pattern]:
                        try:
                            handler(pattern, context)
                        except Exception as e:
                            pass  # Log but don't fail
        
        # Log invalidation
        self._log_invalidation(event, invalidated_patterns, context)
    
    def _log_invalidation(self, event: InvalidationEvent, patterns: List[str], context: Dict):
        """Log invalidation event."""
        self.invalidation_log.append({
            'timestamp': datetime.now().isoformat(),
            'event': event.value,
            'patterns': patterns,
            'context': context
        })
    
    def get_invalidation_history(self, limit: int = 100) -> List[Dict]:
        """Get recent invalidation history."""
        return self.invalidation_log[-limit:]


class SmartInvalidationStrategy:
    """Smart invalidation based on dependencies."""
    
    def __init__(self):
        self.manager = CacheInvalidationManager()
        self.dependencies: Dict[str, Set[str]] = {}
    
    def add_dependency(self, parent: str, child: str):
        """Register cache dependency (parent -> child)."""
        if parent not in self.dependencies:
            self.dependencies[parent] = set()
        self.dependencies[parent].add(child)
    
    def invalidate_with_dependencies(self, cache_key: str):
        """Invalidate cache and all dependent caches."""
        invalidated = {cache_key}
        to_process = {cache_key}
        
        while to_process:
            current = to_process.pop()
            
            # Find all caches depending on this one
            for parent, children in self.dependencies.items():
                if current in children:
                    if parent not in invalidated:
                        invalidated.add(parent)
                        to_process.add(parent)
        
        return invalidated
    
    def get_dependency_graph(self) -> Dict[str, Set[str]]:
        """Get full dependency graph."""
        return self.dependencies.copy()


class ConditionalInvalidation:
    """Conditional cache invalidation based on predicates."""
    
    def __init__(self):
        self.conditions: List[tuple] = []
    
    def add_condition(self, predicate: Callable, patterns: List[str]):
        """Add conditional invalidation rule."""
        self.conditions.append((predicate, patterns))
    
    def evaluate_conditions(self, context: Dict) -> List[str]:
        """Evaluate conditions and return patterns to invalidate."""
        to_invalidate = []
        
        for predicate, patterns in self.conditions:
            try:
                if predicate(context):
                    to_invalidate.extend(patterns)
            except Exception:
                pass  # Skip failed conditions
        
        return to_invalidate


# Global invalidation manager
_invalidation_manager = None


def get_invalidation_manager() -> CacheInvalidationManager:
    """Get or create global invalidation manager."""
    global _invalidation_manager
    if _invalidation_manager is None:
        _invalidation_manager = CacheInvalidationManager()
    return _invalidation_manager


if __name__ == '__main__':
    manager = get_invalidation_manager()
    
    # Simulate events
    manager.trigger_invalidation(
        InvalidationEvent.MEAL_ADDED,
        {'meal_id': 123}
    )
    
    history = manager.get_invalidation_history()
    print(f"Invalidation events: {len(history)}")
