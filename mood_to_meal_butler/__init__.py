# Lazy import to avoid breaking on missing dependencies
try:
    from .agent import app
except ImportError:
    # If google.adk is not available, that's okay
    # Other modules like conversation_handler don't need it
    app = None

__all__ = ["app"]
