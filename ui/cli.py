"""
cli.py — CLI mode dùng argparse.

Sử dụng:
    python main.py --phone 0357156329 --count 5
    python main.py --phone 0357156329 0901234567 --count 3 --category telecom
    python main.py --list-services
    python main.py --health-check --phone 0357156329
"""

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="autocaller",
        description="🚀 Autocaller v2.0 — Gửi OTP hàng loạt đến nhiều dịch vụ",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  python main.py --phone 0357156329 --count 5
  python main.py --phone 0357156329 0901234567 --count 3 --category telecom fnb
  python main.py --list-services
  python main.py --health-check --phone 0357156329
  python main.py --phone 0357156329 --count 1 --dry-run
        """,
    )

    parser.add_argument(
        "--phone", "-p",
        nargs="+",
        help="Danh sách số điện thoại (cách nhau bằng dấu cách)",
    )
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=1,
        help="Số vòng lặp (mặc định: 1)",
    )
    parser.add_argument(
        "--category",
        nargs="+",
        choices=["telecom", "ecommerce", "fnb", "delivery", "finance", "education", "realestate", "other"],
        help="Lọc theo nhóm service",
    )
    parser.add_argument(
        "--service",
        nargs="+",
        help="Lọc theo tên service cụ thể",
    )
    parser.add_argument(
        "--list-services", "-l",
        action="store_true",
        help="Liệt kê tất cả services",
    )
    parser.add_argument(
        "--health-check",
        action="store_true",
        help="Kiểm tra tất cả services hoạt động hay không",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Chỉ hiển thị service sẽ chạy, không gửi request thật",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Đường dẫn config.yaml (mặc định: config.yaml)",
    )
    parser.add_argument(
        "--export",
        choices=["json", "csv"],
        help="Xuất kết quả ra file",
    )

    return parser


def cli_mode():
    """Chạy chế độ CLI."""
    from rich.console import Console
    from rich.table import Table

    from core.config import load_config
    from core.logger import setup_logger
    from core.runner import run, health_check
    from services import discover_services, list_services

    parser = build_parser()
    args = parser.parse_args()
    console = Console()

    # Load config
    config = load_config(args.config)
    logger = setup_logger(config)

    # Discover services
    service_classes = discover_services()

    # --- List services ---
    if args.list_services:
        services_info = list_services(service_classes)
        table = Table(title=f"📋 Danh sách Services ({len(services_info)})", show_lines=True)
        table.add_column("Tên", style="bold", min_width=20)
        table.add_column("Nhóm", style="cyan")
        table.add_column("Trạng thái", justify="center")
        table.add_column("Mô tả", max_width=40)

        for svc in services_info:
            status = "[green]✅ Active[/green]" if svc["active"] else "[red]❌ Inactive[/red]"
            table.add_row(svc["name"], svc["category"], status, svc["description"])

        console.print(table)
        return

    # --- Health check ---
    if args.health_check:
        if not args.phone:
            console.print("[red]Cần cung cấp --phone để health check[/red]")
            sys.exit(1)
        health_check(service_classes, config, test_phone=args.phone[0])
        return

    # --- Run ---
    if not args.phone:
        console.print("[red]Cần cung cấp --phone. Dùng --help để xem hướng dẫn.[/red]")
        sys.exit(1)

    stats = run(
        phone_list=args.phone,
        count=args.count,
        service_classes=service_classes,
        config=config,
        categories=args.category,
        service_names=args.service,
        dry_run=args.dry_run,
    )

    # Hiển thị thống kê
    stats.display()

    # Export nếu cần
    if args.export == "json":
        path = stats.export_json()
        console.print(f"[green]📄 Đã xuất JSON: {path}[/green]")
    elif args.export == "csv":
        path = stats.export_csv()
        console.print(f"[green]📄 Đã xuất CSV: {path}[/green]")
