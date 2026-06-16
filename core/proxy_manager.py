"""
proxy_manager.py — Quản lý proxy rotating.

Load proxy từ file, hỗ trợ round-robin và random selection.
"""

import random
import threading
from pathlib import Path

from core.logger import get_logger


class ProxyManager:
    """Quản lý danh sách proxy với rotation."""

    def __init__(self, proxy_file: str = "proxies.txt"):
        self._lock = threading.Lock()
        self._proxies: list[str] = []
        self._index = 0
        self._load(proxy_file)

    def _load(self, proxy_file: str):
        """Load proxy từ file, bỏ qua dòng trống và comment."""
        path = Path(proxy_file)
        if not path.exists():
            get_logger().warning(f"Không tìm thấy file proxy: {proxy_file}")
            return

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    self._proxies.append(line)

        if self._proxies:
            get_logger().info(f"Đã load {len(self._proxies)} proxy từ {proxy_file}")
        else:
            get_logger().warning(f"File {proxy_file} không chứa proxy nào.")

    @property
    def available(self) -> bool:
        """Có proxy nào khả dụng không."""
        return len(self._proxies) > 0

    @property
    def count(self) -> int:
        return len(self._proxies)

    def get_next(self) -> dict:
        """
        Lấy proxy tiếp theo theo round-robin.
        
        Returns:
            dict dạng {"http": proxy_url, "https": proxy_url}
            hoặc {} nếu không có proxy.
        """
        if not self._proxies:
            return {}

        with self._lock:
            proxy = self._proxies[self._index % len(self._proxies)]
            self._index += 1

        return {"http": proxy, "https": proxy}

    def get_random(self) -> dict:
        """
        Lấy proxy ngẫu nhiên.

        Returns:
            dict dạng {"http": proxy_url, "https": proxy_url}
            hoặc {} nếu không có proxy.
        """
        if not self._proxies:
            return {}

        proxy = random.choice(self._proxies)
        return {"http": proxy, "https": proxy}

    def remove_dead(self, proxy_url: str):
        """Loại bỏ proxy chết khỏi danh sách."""
        with self._lock:
            self._proxies = [p for p in self._proxies if p != proxy_url]
            get_logger().info(f"Đã loại proxy chết: {proxy_url} (còn {len(self._proxies)})")
