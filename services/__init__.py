"""
services/__init__.py — Auto-discover tất cả Service subclass.

Scan tất cả file .py trong thư mục services/, import và tìm
class kế thừa từ Service. Thêm service mới = tạo file .py mới.
"""

import importlib
from pathlib import Path

from core.base_service import Service


def discover_services() -> list[type]:
    """
    Auto-discover tất cả Service subclass trong thư mục services/.

    Returns:
        List các class kế thừa Service (chỉ những class có active=True
        sẽ được chạy, nhưng tất cả đều được discover).
    """
    services = []
    services_dir = Path(__file__).parent

    for file in sorted(services_dir.glob("*.py")):
        # Bỏ qua __init__.py và file bắt đầu bằng _
        if file.name.startswith("_"):
            continue

        module_name = f"services.{file.stem}"
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            print(f"[⚠] Không thể import {module_name}: {e}")
            continue

        for attr_name in dir(module):
            obj = getattr(module, attr_name)
            if (
                isinstance(obj, type)
                and issubclass(obj, Service)
                and obj is not Service
                and not getattr(obj, "__abstractmethods__", None)
            ):
                services.append(obj)

    return services


def list_services(services: list[type] = None) -> list[dict]:
    """
    Liệt kê tất cả services với metadata.

    Returns:
        List[dict] với keys: name, category, active, description.
    """
    if services is None:
        services = discover_services()

    return [
        {
            "name": cls.name,
            "category": cls.category,
            "active": cls.active,
            "description": cls.description,
        }
        for cls in services
    ]
