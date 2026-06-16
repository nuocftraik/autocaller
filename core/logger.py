"""
logger.py — Logging thống nhất cho Autocaller.

Ghi log ra console (với màu sắc qua rich) + file (nếu bật).
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from rich.logging import RichHandler


_logger = None


def setup_logger(config: dict) -> logging.Logger:
    """
    Khởi tạo logger với config từ config.yaml.

    Args:
        config: dict config (dùng config["logging"]).

    Returns:
        logging.Logger đã cấu hình.
    """
    global _logger
    if _logger is not None:
        return _logger

    log_config = config["logging"]
    level = getattr(logging, log_config["level"], logging.INFO)

    logger = logging.getLogger("autocaller")
    logger.setLevel(level)
    logger.handlers.clear()

    # --- Console handler (rich) ---
    console_handler = RichHandler(
        level=level,
        show_time=True,
        show_path=False,
        markup=True,
        rich_tracebacks=True,
    )
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(console_handler)

    # --- File handler ---
    if log_config.get("file_enabled", False):
        log_dir = Path(log_config.get("file_dir", "logs"))
        log_dir.mkdir(parents=True, exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"autocaller_{today}.log"

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(file_handler)

    _logger = logger
    return logger


def get_logger() -> logging.Logger:
    """Lấy logger đã khởi tạo. Nếu chưa setup, trả về logger mặc định."""
    global _logger
    if _logger is None:
        # Fallback: logger console đơn giản
        _logger = logging.getLogger("autocaller")
        if not _logger.handlers:
            _logger.addHandler(logging.StreamHandler())
            _logger.setLevel(logging.INFO)
    return _logger
