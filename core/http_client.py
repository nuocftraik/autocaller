"""
http_client.py — Factory tạo requests.Session với retry và proxy.
"""

import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from core.proxy_manager import ProxyManager

# Tắt cảnh báo SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_session(
    config: dict,
    proxy_manager: ProxyManager = None,
) -> requests.Session:
    """
    Tạo requests.Session đã cấu hình retry, proxy, timeout.

    Args:
        config: dict config từ config.yaml.
        proxy_manager: ProxyManager instance (optional).

    Returns:
        requests.Session sẵn sàng dùng.
    """
    http_config = config["http"]
    proxy_config = config["proxy"]

    session = requests.Session()

    # --- Retry strategy ---
    retry = Retry(
        total=http_config["retry_count"],
        backoff_factor=http_config["retry_backoff"],
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
    )
    adapter = HTTPAdapter(
        max_retries=retry,
        pool_maxsize=config["threading"]["max_workers"] + 5,
        pool_connections=config["threading"]["max_workers"] + 5,
    )
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    # --- SSL ---
    session.verify = http_config["verify_ssl"]

    # --- Proxy ---
    if proxy_config["enabled"] and proxy_manager and proxy_manager.available:
        if proxy_config.get("rotate", True):
            session.proxies = proxy_manager.get_random()
        else:
            session.proxies = proxy_manager.get_next()

    return session
