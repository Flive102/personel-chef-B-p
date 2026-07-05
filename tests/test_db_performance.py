"""
WEEK 6: Database Performance Tests (Part 1/2) - Connection Pool & Batching

Tests:
- Connection pool creation and reuse
- Query batching efficiency
- Connection lifecycle management
"""

import pytest
from mood_to_meal_butler.database_optimization import (
    Connection, ConnectionPool, ConnectionPoolConfig, QueryBatcher,
    DBOptimizer, get_db_optimizer, reset_optimizer
)


class TestConnectionPooling:
    """Test connection pool functionality."""
    
    def test_pool_initialization(self):
        """Verify pool initializes with correct size."""
        config = ConnectionPoolConfig(pool_size=10, max_overflow=5)
        pool = ConnectionPool(config)
        
        assert len(pool.pool) == 10
        assert len(pool.available) == 10
        assert len(pool.in_use) == 0
    
    def test_get_connection(self):
        """Get connection from pool."""
        pool = ConnectionPool()
        conn = pool.get_connection()
        
        assert conn is not None
        assert conn in pool.in_use
        assert len(pool.available) < len(pool.pool)
    
    def test_return_connection(self):
        """Return connection to pool."""
        pool = ConnectionPool()
        conn = pool.get_connection()
        initial_in_use = len(pool.in_use)
        
        pool.return_connection(conn)
        
        assert conn in pool.available
        assert len(pool.in_use) == initial_in_use - 1
    
    def test_pool_stats(self):
        """Get pool statistics."""
        pool = ConnectionPool()
        stats = pool.get_pool_stats()
        
        assert 'total_connections' in stats
        assert 'available' in stats
        assert 'in_use' in stats
        assert stats['pool_size'] == 20


class TestQueryBatching:
    """Test query batching efficiency."""
    
    def test_batch_get_meals(self):
        """Batch meal retrieval."""
        pool = ConnectionPool()
        batcher = QueryBatcher(pool)
        
        meal_ids = list(range(1, 101))
        results = batcher.batch_get_meals(meal_ids)
        
        assert len(results) > 0
    
    def test_batch_size_configuration(self):
        """Verify batch size setting."""
        pool = ConnectionPool()
        batcher = QueryBatcher(pool)
        
        assert batcher.batch_size == 50
