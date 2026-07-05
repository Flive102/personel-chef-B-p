"""Constants and configuration values for mood-to-meal-butler."""

# ============================================================================
# EMOTIONS & KEYWORDS
# ============================================================================

EMOTIONS_SUPPORTED = [
    "sad", "happy", "stressed", "tired", "angry", "sick", "bored", 
    "excited", "calm", "anxious", "lonely", "hopeful", "overwhelmed", "motivated"
]

EMOTION_EMOJI = {
    "sad": "💙", "happy": "😊", "stressed": "😰", "tired": "😴",
    "angry": "😠", "sick": "🤒", "bored": "😑", "excited": "🎉",
    "calm": "🧘", "anxious": "😟", "lonely": "💔", "hopeful": "✨",
    "overwhelmed": "😵", "motivated": "💪"
}

# ============================================================================
# SITUATIONS (CONTEXTS)
# ============================================================================

SITUATIONS_SUPPORTED = [
    "breakfast", "lunch", "dinner", "office", "home", "date", "vegan",
    "keto", "budget", "quick-bite", "sick-day", "fine-dining", "party",
    "study-session", "workout", "family-gathering", "romantic", "casual",
    "healthy", "indulgent", "comfort", "celebration", "recovery",
    "travel", "outdoor", "late-night", "weekend", "weekday", "hospital",
    "diet-restricted", "allergic", "special-occasion"
]

# ============================================================================
# MEAL RECOMMENDATIONS
# ============================================================================

DEFAULT_MEAL_COUNT = 4  # Meals to recommend per request
MIN_MEAL_COUNT = 1
MAX_MEAL_COUNT = 10

# Ranking thresholds
PERFECT_MATCH_SCORE = 100
GOOD_MATCH_SCORE = 75
FAIR_MATCH_SCORE = 50

# ============================================================================
# INPUT VALIDATION
# ============================================================================

MAX_INPUT_LENGTH = 500  # Max characters in user message
MIN_INPUT_LENGTH = 2    # Min characters required
MAX_RETRIES = 3         # Max retry attempts on error

# Malicious patterns (security)
INJECTION_PATTERNS = [
    r"ignore.*previous",
    r"dan\s*mode",
    r"jailbreak",
    r"forget.*instructions",
    r"system.*prompt",
]

# ============================================================================
# PERFORMANCE & LIMITS
# ============================================================================

RESPONSE_TIMEOUT_MS = 500      # Target response time
DATABASE_QUERY_TIMEOUT_S = 5   # Database query timeout
MCP_INIT_TIMEOUT_S = 10        # MCP initialization timeout

# ============================================================================
# LOGGING & MONITORING
# ============================================================================

LOG_LEVEL = "INFO"
LOG_DIR = ".logs"
LOG_MAX_BYTES = 10_000_000  # 10MB
LOG_BACKUP_COUNT = 5

# Error tracking
ERROR_LOG_FILE = "errors.log"
ACCESS_LOG_FILE = "access.log"

# ============================================================================
# DATABASE
# ============================================================================

DB_ENCODING = "utf-8"
DB_TIMEOUT = 5.0

# ============================================================================
# RESPONSES (TEMPLATES)
# ============================================================================

RESPONSE_TEMPLATES = {
    "not_found": "I couldn't understand your mood. Could you rephrase? (e.g., 'I am sad')",
    "error": "Sorry, something went wrong. Please try again.",
    "empty_input": "Please tell me how you're feeling.",
    "too_long": "Your message is too long. Please keep it under 500 characters.",
}

# ============================================================================
# VIETNAMESE SUPPORT
# ============================================================================

VIETNAMESE_EMOTIONS = {
    "buồn": "sad", "vui": "happy", "căng": "stressed", "mệt": "tired",
    "giận": "angry", "ốm": "sick", "chán": "bored", "phấn khích": "excited",
    "bình tĩnh": "calm", "lo lắng": "anxious", "cô đơn": "lonely",
    "hy vọng": "hopeful", "quá tải": "overwhelmed", "có động lực": "motivated"
}

# ============================================================================
# RATE LIMITING
# ============================================================================

RATE_LIMIT_ENABLED = True
RATE_LIMIT_REQUESTS_PER_MINUTE = 60  # Per user
RATE_LIMIT_REQUESTS_PER_HOUR = 1000  # Per user
