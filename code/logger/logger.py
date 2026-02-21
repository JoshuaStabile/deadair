import logging
import os
from logging.handlers import RotatingFileHandler
from config import (
    LOG_LEVEL,
    LOG_DIR,
    LOG_FILE,
    LOG_MAX_BYTES,
    LOG_BACKUP_COUNT,
)

class Logger:
    def __init__(self, name: str = "deadair"):
        self.logger = logging.getLogger(name)

        level = getattr(logging, LOG_LEVEL.upper(), logging.DEBUG)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            self._setup_handlers(level)

    def _setup_handlers(self, level):
        os.makedirs(LOG_DIR, exist_ok=True)

        log_path = os.path.join(LOG_DIR, LOG_FILE)

        # File handler (rotating)
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT
        )
        file_handler.setLevel(level)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get(self):
        return self.logger
