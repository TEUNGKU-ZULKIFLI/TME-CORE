"""
Logging configuration untuk TME-CORE
Setup: file logging dengan rotating handler + console output
"""

import logging
import logging.handlers
from pathlib import Path


def setup_logger(
    name: str,
    log_dir: str = "data/logs",
    level: str = "INFO",
    log_file: str = None
) -> logging.Logger:
    """
    Setup logger dengan rotating file handler + console handler

    Args:
        name: Nama logger (biasanya __name__)
        log_dir: Directory untuk menyimpan log files
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Nama file log (default: {name}.log)

    Returns:
        Logger object yang siap digunakan

    Example:
        logger = setup_logger(__name__)
        logger.info("Engine started")
    """
    # Buat log directory jika belum ada
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Tentukan nama file
    if log_file is None:
        log_file = f"{name}.log"

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers (prevent duplicate)
    if logger.handlers:
        logger.handlers.clear()

    # File handler dengan rotating (max 10MB per file, keep 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        filename=f"{log_dir}/{log_file}",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Console handler (INFO level only)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Contoh penggunaan:
# if __name__ == "__main__":
#     logger = setup_logger("test_logger")
#     logger.info("This is info message")
#     logger.warning("This is warning message")
#     logger.error("This is error message")