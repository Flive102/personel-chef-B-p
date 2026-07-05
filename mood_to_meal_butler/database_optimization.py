"""
WEEK 6: Database Optimization - Connection Pooling & Query Batching (Part 1/2)

Implements:
- Connection pooling (reuse connections vs creating new ones)
- Query batching (get 50 meals at once instead of N queries)
- Connection lifecycle management
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class ConnectionPoolConfig:
    """Configuration for connection pool."""
    pool_size: int = 20
    max_overflow: int = 40
    pool_timeout: int = 30
    pool_recycle: int = 3600
    echo: bool = False


class Connection:
    """Simulated database connection."""
    
    def __init__(self, connection_id: int):
        self.id = connection_id
        self.created_at = datetime.now()
        self.last_used = datetime.now()
        self.in_use = False
        self.query_count = 0
    
    def execute_query(self, query: str) -> List[Dict]:
        """Execute query on this connection."""
        self.last_used = datetime.now()
        self.query_count += 1
        self.in_use = True
        return self._simulate_query_result()
    
    def _simulate_query_result(self) -> List[Dict]:
        """Simulate query result."""
        return [{'id': 1, 'name': 'meal1'}, {'id': 2, 'name': 'meal2'}]
    
    def close(self):
        """Close connection."""
        self.in_use = False
    
    def is_alive(self) -> bool:
        """Check if connection is still alive."""
        age = (datetime.now() - self.created_at).total_seconds()
        return age < 3600  # 1 hour max age


class ConnectionPool:
    """Database connection pool with lifecycle management."""
    
    def __init__(self, config: Optional[ConnectionPoolConfig] = None):
        self.config = config or ConnectionPoolConfig()
        self.pool = []
        self.available = []
        self.in_use = []
        self.connection_counter = 0
        self._create_initial_pool()
    
    def _create_initial_pool(self):
        """Create initial pool of connections."""
        for _ in range(self.config.pool_size):
            conn = self._create_connection()
            self.pool.append(conn)
            self.available.append(conn)
    
    def _create_connection(self) -> Connection:
        """Create new connection."""
        self.connection_counter += 1
        return Connection(self.connection_counter)
    
    def get_connection(self) -> Connection:
        """Get a connection from pool."""
        # Try to get available connection
        if self.available:
            conn = self.available.pop(0)
            if conn.is_alive():
                self.in_use.append(conn)
                return conn
            else:
                conn.close()
        
        # Create new connection if pool not full
        if len(self.pool) < (self.config.pool_size + self.config.max_overflow):
            conn = self._create_connection()
            self.pool.append(conn)
            self.in_use.append(conn)
            return conn
        
        # Wait for available connection (simulated)
        if self.available:
            conn = self.available.pop(0)
            self.in_use.append(conn)
            return conn
        
        raise RuntimeError("Connection pool exhausted")
    
    def return_connection(self, conn: Connection):
        """Return connection to pool."""
        if conn in self.in_use:
            self.in_use.remove(conn)
        conn.close()
        self.available.append(conn)
    
    def get_pool_stats(self) -> Dict:
        """Get connection pool statistics."""
        return {
            'total_connections': len(self.pool),
            'available': len(self.available),
            'in_use': len(self.in_use),
            'pool_size': self.config.pool_size,
            'max_overflow': self.config.max_overflow,
        }


class QueryBatcher:
    """Batch multiple queries for efficiency."""
    
    def __init__(self, pool: ConnectionPool):
        self.pool = pool
        self.batch_size = 50
    
    def batch_get_meals(self, meal_ids: List[int]) -> List[Dict]:
        """Get multiple meals in batches instead of N queries."""
        results = []
        
        # Split into batches
        for i in range(0, len(meal_ids), self.batch_size):
            batch_ids = meal_ids[i:i + self.batch_size]
            batch_query = f"SELECT * FROM meals WHERE id IN ({','.join(map(str, batch_ids))})"
            
            conn = self.pool.get_connection()
            try:
                batch_results = conn.execute_query(batch_query)
                results.extend(batch_results)
            finally:
                self.pool.return_connection(conn)
        
        return results
    
    def batch_get_by_emotion(self, emotion_ids: List[int]) -> List[Dict]:
        """Get meals by multiple emotions in one query."""
        conn = self.pool.get_connection()
        try:
            query = f"SELECT * FROM meals WHERE emotion_id IN ({','.join(map(str, emotion_ids))})"
            return conn.execute_query(query)
        finally:
            self.pool.return_connection(conn)
    
    def batch_insert_meals(self, meals: List[Dict]) -> int:
        """Insert multiple meals in one batch."""
        conn = self.pool.get_connection()
        try:
            query = f"INSERT INTO meals VALUES ({len(meals)} rows)"
            conn.execute_query(query)
            return len(meals)
        finally:
            self.pool.return_connection(conn)


class DBOptimizer:
    """Main database optimization manager."""
    
    def __init__(self):
        self.config = ConnectionPoolConfig(pool_size=20, max_overflow=40)
        self.pool = ConnectionPool(self.config)
        self.batcher = QueryBatcher(self.pool)
    
    def execute_query(self, query: str) -> List[Dict]:
        """Execute single query."""
        conn = self.pool.get_connection()
        try:
            return conn.execute_query(query)
        finally:
            self.pool.return_connection(conn)
    
    def get_optimization_metrics(self) -> Dict:
        """Get optimization metrics."""
        return {
            'pool_stats': self.pool.get_pool_stats(),
            'batch_size': self.batcher.batch_size,
            'connection_reuse_enabled': True,
            'query_batching_enabled': True,
        }


# Global optimizer instance
_optimizer = None


def get_db_optimizer() -> DBOptimizer:
    """Get or create global DB optimizer."""
    global _optimizer
    if _optimizer is None:
        _optimizer = DBOptimizer()
    return _optimizer


def reset_optimizer():
    """Reset optimizer for testing."""
    global _optimizer
    _optimizer = DBOptimizer()
