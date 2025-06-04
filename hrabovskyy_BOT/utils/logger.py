import logging
import os
from config import LOG_FILE

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

def log_exception(error: Exception):
    logging.error("🔴 Виняток: %s", str(error), exc_info=True)
