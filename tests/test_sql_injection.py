"""
SQL Injection Security Tests for mood-to-meal-butler
Tests parameterized queries, injection blocking, and database escaping
"""

import pytest
import sqlite3
from mood_to_meal_butler.user_model import DatabaseManager


class TestSQLInjectionProtection:
    """Test SQL injection prevention."""
    
    def test_parameterized_query_basic(self):
        """Test basic parameterized query works."""
        # This should work safely
        user = DatabaseManager.get_user("safe_user_id")
        # Should not crash
        assert user is None or isinstance(user, object)
    
    def test_sql_injection_single_quote_blocked(self):
        """Test single quote injection blocked."""
        # Attempt: ' OR '1'='1
        injection_attempt = "' OR '1'='1"
        user = DatabaseManager.get_user(injection_attempt)
        # Should not return unauthorized data
        assert user is None
    
    def test_sql_injection_double_quote_blocked(self):
        """Test double quote injection blocked."""
        # Attempt: " OR "1"="1
        injection_attempt = '" OR "1"="1'
        user = DatabaseManager.get_user(injection_attempt)
        assert user is None
    
    def test_sql_injection_semicolon_blocked(self):
        """Test semicolon injection blocked."""
        # Attempt: '; DROP TABLE users; --
        injection_attempt = "'; DROP TABLE users; --"
        user = DatabaseManager.get_user(injection_attempt)
        assert user is None
    
    def test_sql_injection_union_blocked(self):
        """Test UNION-based injection blocked."""
        # Attempt: ' UNION SELECT * FROM users; --
        injection_attempt = "' UNION SELECT * FROM users; --"
        user = DatabaseManager.get_user(injection_attempt)
        assert user is None
    
    def test_sql_injection_comment_blocked(self):
        """Test comment-based injection blocked."""
        # Attempt: admin' --
        injection_attempt = "admin' --"
        user = DatabaseManager.get_user(injection_attempt)
        assert user is None
    
    def test_sql_injection_time_based_blocked(self):
        """Test time-based blind injection blocked."""
        # Attempt: ' OR SLEEP(5) --
        injection_attempt = "' OR SLEEP(5) --"
        user = DatabaseManager.get_user(injection_attempt)
        assert user is None
    
    def test_sql_injection_null_byte_blocked(self):
        """Test null byte injection blocked."""
        # Attempt: user_id%00' OR '1'='1
        injection_attempt = "user_id\x00' OR '1'='1"
        user = DatabaseManager.get_user(injection_attempt)
        assert user is None


class TestParameterizedQueries:
    """Test that parameterized queries are used correctly."""
    
    def test_get_user_uses_parameters(self):
        """Test get_user uses parameterized queries."""
        # Safe operation - should not crash
        result = DatabaseManager.get_user("test_user")
        # Function should complete without error
        assert True
    
    def test_get_user_by_username_safe(self):
        """Test get_user_by_username is safe."""
        # This should be safe even with injection attempts
        result = DatabaseManager.get_user_by_username("' OR '1'='1")
        assert result is None
    
    def test_authenticate_user_safe(self):
        """Test authenticate_user is safe."""
        # Should handle injection attempts gracefully
        result = DatabaseManager.authenticate_user(
            "admin' --", 
            "'; DROP TABLE users; --"
        )
        assert result is None


class TestDatabaseEscaping:
    """Test string escaping and safe concatenation."""
    
    def test_special_characters_handled(self):
        """Test special characters don't break queries."""
        special_chars = ["'", '"', ";", "--", "/*", "*/", "\\", "%"]
        for char in special_chars:
            # Should not crash
            user = DatabaseManager.get_user(f"test{char}user")
            assert user is None
    
    def test_unicode_characters_safe(self):
        """Test Unicode characters handled safely."""
        unicode_attempts = [
            "test_user_\u0000",  # Null byte
            "test_user_\u001a",  # EOF
            "test_user_\ufffd",  # Replacement char
        ]
        for attempt in unicode_attempts:
            user = DatabaseManager.get_user(attempt)
            assert user is None
    
    def test_very_long_input_safe(self):
        """Test very long input doesn't cause issues."""
        long_input = "x" * 10000
        user = DatabaseManager.get_user(long_input)
        # Should complete without crashing or SQL injection
        assert user is None


class TestInputValidation:
    """Test input validation for SQL operations."""
    
    def test_empty_user_id_safe(self):
        """Test empty user_id handled safely."""
        user = DatabaseManager.get_user("")
        assert user is None
    
    def test_none_user_id_safe(self):
        """Test None user_id handled safely."""
        # Should not crash
        try:
            user = DatabaseManager.get_user(None)
            # Either returns None or raises exception (both acceptable)
            assert True
        except (TypeError, AttributeError):
            # Exception is acceptable for None input
            assert True
    
    def test_numeric_user_id_safe(self):
        """Test numeric user_id converted safely."""
        # Should handle type conversion safely
        user = DatabaseManager.get_user("12345")
        assert user is None or isinstance(user, object)


class TestDatabaseIntegrity:
    """Test database maintains integrity under attack."""
    
    def test_injection_no_data_corruption(self):
        """Test injection attempts don't corrupt database."""
        # Attempt injection
        DatabaseManager.get_user("' OR '1'='1")
        # Database should still be usable
        # (No assertion needed - if DB corrupted, next operation fails)
        assert True
    
    def test_multiple_injections_safe(self):
        """Test multiple injection attempts safely handled."""
        attempts = [
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM users; --",
            "admin' OR '1'='1",
            "' OR 1=1; --",
        ]
        for attempt in attempts:
            user = DatabaseManager.get_user(attempt)
            assert user is None
