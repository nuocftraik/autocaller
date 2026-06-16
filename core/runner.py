"""
runner.py — Orchestrator chạy tất cả service với ThreadPoolExecutor.
"""

import random
import time
import concurrent.futures
from typing import Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from core.base_service import Service, ServiceResult
from core.config import load_config
from core.http_client import create_session
from core.logger import get_logger, setup_logger
from core.proxy_manager import ProxyManager
from core.stats import Stats


def normalize_phone(phone: str) -> str:
    """Chuẩn hóa SĐT: 0xxx → +84xxx."""
    if phone.startswith("0"):
        return "+84" + phone[1:]
    if phone.startswith("84") and not phone.startswith("+84"):
        return "+" + phone
    return phone


def run(
    phone_list: list[str],
    count: int,
    service_classes: list[type],
    config: dict,
    categories: Optional[list[str]] = None,
    service_names: Optional[list[str]] = None,
    dry_run: bool = False,
):
    """
    Vòng lặp chính: chạy tất cả service cho mỗi SĐT.

    Args:
        phone_list: Danh sách SĐT gốc (e.g. ["0357156329"]).
        count: Số vòng lặp.
        service_classes: Danh sách class Service đã discover.
        config: Config dict.
        categories: Lọc theo nhóm (None = tất cả).
        service_names: Lọc theo tên service (None = tất cả).
        dry_run: Nếu True, chỉ hiển thị mà không gọi thật.
    """
    logger = get_logger()
    console = Console()
    stats = Stats()

    # --- Giới hạn count ---
    max_count = config["general"]["max_count"]
    if count > max_count:
        logger.warning(f"count={count} vượt max_count={max_count}, giới hạn lại.")
        count = max_count

    # --- Setup proxy ---
    proxy_config = config["proxy"]
    proxy_manager = None
    if proxy_config["enabled"]:
        proxy_manager = ProxyManager(proxy_config["file"])

    # --- Lọc service ---
    filtered_classes = []
    for cls in service_classes:
        if not getattr(cls, "active", True):
            continue
        if categories and getattr(cls, "category", "other") not in categories:
            continue
        if service_names and getattr(cls, "name", "") not in service_names:
            continue
        filtered_classes.append(cls)

    if not filtered_classes:
        logger.error("Không có service nào phù hợp để chạy!")
        return stats

    logger.info(f"Sẽ chạy {len(filtered_classes)} services × {len(phone_list)} SĐT × {count} vòng")

    # --- Dry run ---
    if dry_run:
        console.print("[bold yellow]🔍 DRY RUN — không gửi request thật[/bold yellow]")
        for cls in filtered_classes:
            console.print(f"  → {cls.name} [{cls.category}]")
        return stats

    delay_services = config["general"]["delay_between_services"]
    delay_rounds = config["general"]["delay_between_rounds"]
    max_workers = config["threading"]["max_workers"]
    randomize = config["general"]["randomize_order"]

    stats.start_timer()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:

        total_tasks = count * len(phone_list) * len(filtered_classes)
        overall = progress.add_task("[cyan]Tổng tiến độ", total=total_tasks)

        for round_idx in range(count):
            round_label = f"Vòng {round_idx + 1}/{count}"
            logger.info(f"===== {round_label} =====")

            for phone in phone_list:
                phone_intl = normalize_phone(phone)
                logger.info(f"📱 SĐT: {phone_intl}")

                # Tạo session cho mỗi SĐT (mỗi session có thể có proxy khác)
                session = create_session(config, proxy_manager)

                # Tạo instances
                service_instances = [cls(session, config) for cls in filtered_classes]

                if randomize:
                    random.shuffle(service_instances)

                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = {}
                    for svc in service_instances:
                        future = executor.submit(svc.safe_execute, phone, phone_intl)
                        futures[future] = svc
                        time.sleep(delay_services)

                    for future in concurrent.futures.as_completed(futures):
                        svc = futures[future]
                        result = future.result()
                        stats.record(result)
                        progress.advance(overall)

                        # Log kết quả
                        if result.success:
                            logger.info(f"  ✅ {result.service_name} | {result.response_time_ms:.0f}ms")
                        else:
                            err = result.error or result.message
                            logger.warning(f"  ❌ {result.service_name} | {err}")

                session.close()

            # Delay giữa các vòng
            if round_idx < count - 1 and delay_rounds > 0:
                logger.info(f"⏳ Chờ {delay_rounds}s trước vòng tiếp...")
                time.sleep(delay_rounds)

    stats.stop_timer()
    return stats


def health_check(service_classes: list[type], config: dict, test_phone: str = "0000000000"):
    """
    Kiểm tra tất cả service, báo cáo active/inactive song song bằng ThreadPoolExecutor.

    Args:
        service_classes: Danh sách class Service.
        config: Config dict.
        test_phone: SĐT dùng để test (mặc định dummy).
    """
    logger = get_logger()
    console = Console()
    phone_intl = normalize_phone(test_phone)

    console.print(f"\n[bold]🔍 Health Check Song Song — {len(service_classes)} services[/bold]\n")

    # Tạo bản sao config dành riêng cho health check để tránh hang lâu
    hc_config = config.copy()
    if "http" in config:
        hc_config["http"] = config["http"].copy()
    else:
        hc_config["http"] = {}
    
    # Ép buộc timeout ngắn (5s) và không retry khi test health check
    hc_config["http"]["retry_count"] = 0
    hc_config["http"]["timeout"] = 5

    session = create_session(hc_config)
    results = []
    max_workers = config.get("threading", {}).get("max_workers", 10)

    # Hàm wrapper để log chi tiết quá trình chạy từng service
    def check_service_wrapper(cls_type):
        svc_instance = cls_type(session, hc_config)
        logger.debug(f"[Health Check] Bắt đầu kiểm tra: {svc_instance.name}")
        start_time = time.perf_counter()
        try:
            res = svc_instance.safe_execute(test_phone, phone_intl)
            duration = (time.perf_counter() - start_time) * 1000
            logger.debug(f"[Health Check] Hoàn thành: {svc_instance.name} | Success: {res.success} | {duration:.0f}ms")
            return svc_instance, res
        except Exception as e:
            duration = (time.perf_counter() - start_time) * 1000
            logger.error(f"[Health Check] Lỗi nghiêm trọng tại {svc_instance.name}: {e}")
            from core.base_service import ServiceResult
            return svc_instance, ServiceResult(
                success=False,
                service_name=svc_instance.name,
                phone=phone_intl,
                error=str(e),
                response_time_ms=duration
            )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Đang chuẩn bị kiểm tra...", total=len(service_classes))

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Gửi tất cả các task kiểm tra
            futures = {executor.submit(check_service_wrapper, cls): cls for cls in service_classes}
            
            progress.update(task, description="Đang kiểm tra các dịch vụ...")

            for future in concurrent.futures.as_completed(futures):
                try:
                    svc, result = future.result()
                    results.append((svc, result))
                    status_indicator = "✅" if result.success else "❌"
                    progress.update(task, description=f"Đang kiểm tra... (Vừa xong: {status_indicator} {svc.name})", advance=1)
                except Exception as e:
                    logger.error(f"Lỗi khi nhận kết quả từ future: {e}")
                    progress.advance(task)

    # Sắp xếp kết quả theo bảng chữ cái để hiển thị đẹp mắt
    results.sort(key=lambda x: x[0].name)

    # Hiển thị kết quả
    from rich.table import Table
    table = Table(title="🏥 Health Check Results", show_lines=True)
    table.add_column("Service", style="bold", min_width=20)
    table.add_column("Category", style="dim")
    table.add_column("Status", justify="center")
    table.add_column("Time (ms)", justify="center")
    table.add_column("Details", max_width=50)

    for svc, result in results:
        status = "[green]✅ Active[/green]" if result.success else "[red]❌ Inactive[/red]"
        detail = (result.error or result.message or "").strip().replace('\n', ' ')[:50]
        table.add_row(
            svc.name,
            svc.category,
            status,
            f"{result.response_time_ms:.0f}",
            detail,
        )

    console.print(table)
    session.close()

    active = sum(1 for _, r in results if r.success)
    console.print(f"\n[bold]Kết quả: {active}/{len(results)} services active[/bold]\n")

    return results

