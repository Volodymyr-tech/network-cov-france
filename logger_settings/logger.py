import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(module_name: str, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(module_name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    log_path = os.path.join(LOG_DIR, f"{module_name}.log")

    file_handler = RotatingFileHandler(
        log_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
