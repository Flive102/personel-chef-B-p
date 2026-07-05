from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
import json
from datetime import datetime

limiter = Limiter(key_func=get_remote_address)

logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def log_api_call(user_id: str, endpoint: str, mood: str = None, status: str = "success"):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "endpoint": endpoint,
        "mood": mood,
        "status": status
    }
    logger.info(json.dumps(log_entry))
