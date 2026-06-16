"""
config.py — Load và validate cấu hình từ config.yaml.
"""

import os
import yaml
from pathlib import Path

# Giá trị mặc định nếu config.yaml thiếu field
_DEFAULTS = {
    "general": {
        "max_count": 200,
        "delay_between_services": 1.0,
        "delay_between_rounds": 5.0,
        "randomize_order": True,
    },
    "threading": {
        "max_workers": 10,
    },
    "http": {
        "timeout": 15,
        "verify_ssl": False,
        "retry_count": 2,
        "retry_backoff": 1.5,
    },
    "proxy": {
        "enabled": False,
        "file": "proxies.txt",
        "rotate": True,
    },
    "logging": {
        "level": "INFO",
        "file_enabled": True,
        "file_dir": "logs",
    },
}


def _deep_merge(base: dict, override: dict) -> dict:
    """Merge override vào base, giữ lại giá trị base nếu override thiếu."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(config_path: str = None) -> dict:
    """
    Load config từ file YAML, merge với defaults.

    Args:
        config_path: Đường dẫn đến config.yaml.
                     Mặc định: config.yaml trong thư mục project root.

    Returns:
        dict cấu hình đã merge với defaults.
    """
    if config_path is None:
        # Tìm config.yaml ở thư mục gốc project (ngang hàng với main.py)
        project_root = Path(__file__).parent.parent
        config_path = project_root / "config.yaml"

    config_path = Path(config_path)

    if not config_path.exists():
        print(f"[⚠] Không tìm thấy {config_path}, dùng config mặc định.")
        return _DEFAULTS.copy()

    with open(config_path, "r", encoding="utf-8") as f:
        user_config = yaml.safe_load(f) or {}

    config = _deep_merge(_DEFAULTS, user_config)
    _validate(config)
    return config


def _validate(config: dict):
    """Validate các giá trị config cơ bản."""
    assert config["threading"]["max_workers"] > 0, "max_workers phải > 0"
    assert config["http"]["timeout"] > 0, "timeout phải > 0"
    assert config["http"]["retry_count"] >= 0, "retry_count phải >= 0"
    assert config["general"]["max_count"] > 0, "max_count phải > 0"
    assert config["general"]["delay_between_services"] >= 0, "delay_between_services phải >= 0"

    level = config["logging"]["level"].upper()
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    assert level in valid_levels, f"logging.level phải là một trong {valid_levels}"
    config["logging"]["level"] = level
