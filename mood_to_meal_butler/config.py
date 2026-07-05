# mood_agent/config.py
# Read all config from here — other files import from here, no hardcoding.

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR   = Path(__file__).parent          # mood_agent/
load_dotenv(BASE_DIR.parent / ".env")  # Load .env file with absolute path


# ── Paths ─────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent          # mood_agent/
DATA_DIR   = BASE_DIR / "data"              # mood_agent/data/
DB_PATH    = str(DATA_DIR / "history.db")  # mood_agent/data/history.db
MEALS_PATH = str(DATA_DIR / "meals_200_global.json")  # 274 meals database (updated from 35)

# ── Gemini ────────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME     = "gemini-2.0-flash"        # Use this model, don't change

# ── Language ───────────────────────────────────────────────────
DEFAULT_LANGUAGE = "en"  # English is default
SUPPORTED_LANGUAGES = ["en", "vi"]  # English and Vietnamese

# ── Weather (Open-Meteo, default to US location) ──────────────
DEFAULT_LAT  = float(os.getenv("DEFAULT_LAT", "40.7128"))    # New York latitude
DEFAULT_LON  = float(os.getenv("DEFAULT_LON", "-74.0060"))   # New York longitude
CITY_NAME    = os.getenv("CITY_NAME", "New York")

# ── User ──────────────────────────────────────────────────────
DEFAULT_USER_NAME = os.getenv("USER_NAME", "friend")

# ── System Personality ────────────────────────────────────────
AGENT_NAME = "Empathetic Culinary Butler"
AGENT_TONE = "warm, caring, personalized"

# ── Validation ────────────────────────────────────────────────
if not GEMINI_API_KEY:
    raise EnvironmentError(
        "Missing GEMINI_API_KEY!\n"
        "Get free key at: https://aistudio.google.com/app/apikey\n"
        "Add to .env file: GEMINI_API_KEY=your_key_here"
    )

