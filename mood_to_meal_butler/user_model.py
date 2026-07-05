"""
User Model and Database Schema for mood-to-meal-butler
SQLite-based user storage with password hashing
"""

from datetime import datetime
from typing import Optional, Dict
import sqlite3
import hashlib
import os


# Database configuration
DB_PATH = os.environ.get("DB_PATH", "mood_butler.db")


class UserModel:
    """User data model with password hashing."""
    
    def __init__(self, user_id: str, username: str, email: str, 
                 password_hash: str, created_at: datetime = None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary (safe - no password)."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }


class DatabaseManager:
    """Manage SQLite database for users and API keys."""
    
    @staticmethod
    def init_database():
        """Create tables if they don't exist."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # API keys table (for service accounts)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                key_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                api_key TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Rate limit tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rate_limits (
                user_id TEXT PRIMARY KEY,
                request_count INTEGER DEFAULT 0,
                window_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify password against hash."""
        return hashlib.sha256(password.encode()).hexdigest() == password_hash
    
    @staticmethod
    def create_user(user_id: str, username: str, email: str, 
                   password: str) -> bool:
        """
        Create new user in database.
        
        Args:
            user_id: Unique user identifier
            username: Display name
            email: User email
            password: Plain text password (will be hashed)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            password_hash = DatabaseManager.hash_password(password)
            
            cursor.execute("""
                INSERT INTO users (user_id, username, email, password_hash)
                VALUES (?, ?, ?, ?)
            """, (user_id, username, email, password_hash))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    @staticmethod
    def get_user(user_id: str) -> Optional[UserModel]:
        """Retrieve user by ID."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT user_id, username, email, password_hash, created_at
                FROM users WHERE user_id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            return UserModel(
                user_id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                created_at=datetime.fromisoformat(row[4])
            )
        except Exception:
            return None
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[UserModel]:
        """Retrieve user by username."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT user_id, username, email, password_hash, created_at
                FROM users WHERE username = ?
            """, (username,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            return UserModel(
                user_id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                created_at=datetime.fromisoformat(row[4])
            )
        except Exception:
            return None
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[str]:
        """
        Authenticate user and return user_id if valid.
        
        Args:
            username: User's username
            password: User's password (plain text)
        
        Returns:
            user_id if authenticated, None otherwise
        """
        user = DatabaseManager.get_user_by_username(username)
        
        if not user:
            return None
        
        if not DatabaseManager.verify_password(password, user.password_hash):
            return None
        
        return user.user_id
