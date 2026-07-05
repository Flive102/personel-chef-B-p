"""Production-ready logging configuration for mood-to-meal-butler."""

import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime


def setup_production_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configure structured logging for production deployment.
    
    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("mood_to_meal_butler")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Create logs directory
    log_dir = Path(".logs")
    log_dir.mkdir(exist_ok=True)
    
    # Formatter with structured output
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # File handler (rotating logs)
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_dir / "app.log",
        maxBytes=10_000_000,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Error file handler (separate error logs)
    error_handler = logging.handlers.RotatingFileHandler(
        filename=log_dir / "errors.log",
        maxBytes=10_000_000,
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    # Console handler (for development/debugging)
    if os.getenv("DEBUG", "false").lower() == "true":
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


# Global logger instance
logger = setup_production_logging(os.getenv("LOG_LEVEL", "INFO"))


def log_request(user_id: str, message: str, emotion: str = None):
    """Log incoming user request."""
    emotion_str = f" emotion={emotion}" if emotion else ""
    logger.info(f"REQUEST user_id={user_id} message_len={len(message)}{emotion_str}")


def log_response(user_id: str, response_time_ms: float, meals_count: int):
    """Log outgoing response."""
    logger.info(f"RESPONSE user_id={user_id} time_ms={response_time_ms:.1f} meals={meals_count}")


def log_error_event(error_type: str, message: str, context: dict = None):
    """Log error with context."""
    ctx_str = f" context={context}" if context else ""
    logger.error(f"ERROR type={error_type} message={message}{ctx_str}")
