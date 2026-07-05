"""
Performance Profiler - Monitor & Debug Performance

Provides:
- Function call profiling
- Timing measurements
- Memory usage tracking
- Performance baselines
- Bottleneck identification
"""

import time
import tracemalloc
from typing import Dict, Callable, Any, Optional, List
from datetime import datetime
from functools import wraps


class FunctionProfile:
    """Profile for a single function."""
    
    def __init__(self, func_name: str):
        self.func_name = func_name
        self.call_count = 0
        self.total_time = 0.0
        self.min_time = float('inf')
        self.max_time = 0.0
        self.total_memory = 0
        self.max_memory = 0
        self.calls = []
    
    def record_call(self, duration: float, memory_used: int = 0):
        """Record a function call."""
        self.call_count += 1
        self.total_time += duration
        self.min_time = min(self.min_time, duration)
        self.max_time = max(self.max_time, duration)
        self.total_memory += memory_used
        self.max_memory = max(self.max_memory, memory_used)
        
        self.calls.append({
            'duration': duration,
            'memory': memory_used,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep last 100 calls
        if len(self.calls) > 100:
            self.calls = self.calls[-100:]
    
    def get_stats(self) -> Dict:
        """Get statistics for this function."""
        avg_time = self.total_time / self.call_count if self.call_count > 0 else 0
        
        return {
            'function': self.func_name,
            'call_count': self.call_count,
            'total_time': round(self.total_time, 4),
            'avg_time': round(avg_time, 4),
            'min_time': round(self.min_time, 4),
            'max_time': round(self.max_time, 4),
            'total_memory_mb': round(self.total_memory / 1024 / 1024, 2),
            'max_memory_mb': round(self.max_memory / 1024 / 1024, 2),
        }


class PerformanceProfiler:
    """Profile system performance."""
    
    def __init__(self):
        self.profiles: Dict[str, FunctionProfile] = {}
        self.enabled = True
    
    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile a function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self.enabled:
                return func(*args, **kwargs)
            
            func_name = func.__name__
            
            # Start timing
            start_time = time.time()
            tracemalloc.start()
            
            try:
                result = func(*args, **kwargs)
            finally:
                # End timing
                duration = time.time() - start_time
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                # Record profile
                if func_name not in self.profiles:
                    self.profiles[func_name] = FunctionProfile(func_name)
                
                self.profiles[func_name].record_call(duration, peak)
            
            return result
        
        return wrapper
    
    def get_profile(self, func_name: str) -> Optional[Dict]:
        """Get profile for a function."""
        if func_name in self.profiles:
            return self.profiles[func_name].get_stats()
        return None
    
    def get_all_profiles(self) -> Dict:
        """Get all profiles."""
        return {
            name: profile.get_stats() 
            for name, profile in self.profiles.items()
        }
    
    def get_top_slowest(self, limit: int = 10) -> List[Dict]:
        """Get slowest functions."""
        profiles = self.get_all_profiles()
        sorted_profiles = sorted(
            profiles.values(),
            key=lambda x: x['avg_time'],
            reverse=True
        )
        return sorted_profiles[:limit]
    
    def get_top_memory_consumers(self, limit: int = 10) -> List[Dict]:
        """Get functions using most memory."""
        profiles = self.get_all_profiles()
        sorted_profiles = sorted(
            profiles.values(),
            key=lambda x: x['max_memory_mb'],
            reverse=True
        )
        return sorted_profiles[:limit]
    
    def get_report(self) -> Dict:
        """Generate performance report."""
        all_profiles = self.get_all_profiles()
        
        if not all_profiles:
            return {'status': 'no_profiles'}
        
        total_time = sum(p['total_time'] for p in all_profiles.values())
        total_calls = sum(p['call_count'] for p in all_profiles.values())
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_functions': len(all_profiles),
            'total_calls': total_calls,
            'total_time': round(total_time, 4),
            'slowest_functions': self.get_top_slowest(5),
            'memory_consumers': self.get_top_memory_consumers(5),
        }
    
    def reset(self):
        """Reset all profiles."""
        self.profiles.clear()
    
    def enable(self):
        """Enable profiling."""
        self.enabled = True
    
    def disable(self):
        """Disable profiling."""
        self.enabled = False


# Global profiler instance
_profiler = None


def get_profiler() -> PerformanceProfiler:
    """Get or create global profiler."""
    global _profiler
    if _profiler is None:
        _profiler = PerformanceProfiler()
    return _profiler
