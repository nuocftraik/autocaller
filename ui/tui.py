"""
tui.py — Interactive TUI menu dùng rich.

Hiển thị menu tương tác khi chạy `python main.py` không có tham số.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm

from core.config import load_config
from core.logger import setup_logger, get_logger
from core.runner import run, health_check
from services import discover_services, list_services


BANNER = """
[bold cyan]
   █████╗ ██╗   ██╗████████╗ ██████╗  ██████╗ █████╗ ██╗     ██╗     ███████╗██████╗
  ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██╔════╝██╔══██╗██║     ██║     ██╔════╝██╔══██╗
  ███████║██║   ██║   ██║   ██║   ██║██║     ███████║██║     ██║     █████╗  ██████╔╝
  ██╔══██║██║   ██║   ██║   ██║   ██║██║     ██╔══██║██║     ██║     ██╔══╝  ██╔══██╗
  ██║  ██║╚██████╔╝   ██║   ╚██████╔╝╚██████╗██║  ██║███████╗███████╗███████╗██║  ██║
  ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
[/bold cyan]
[dim]  v2.0 — Refactored & Enhanced[/dim]
"""


def show_menu(console: Console):
    """Hiển thị menu chính."""
    menu = """
[bold white]  1.[/bold white] 📱  Bắt đầu gửi OTP
[bold white]  2.[/bold white] 📋  Xem danh sách services
[bold white]  3.[/bold white] 🔍  Health check (kiểm tra service)
[bold white]  4.[/bold white] ⚙️   Xem cấu hình hiện tại
[bold white]  5.[/bold white] 📊  Chạy và xuất báo cáo
[bold white]  0.[/bold white] ❌  Thoát
"""
    console.print(Panel(menu, title="[bold]🚀 MENU[/bold]", border_style="bright_blue"))


def show_config(console: Console, config: dict):
    """Hiển thị cấu hình hiện tại."""
    table = Table(title="⚙️ Cấu hình hiện tại", show_lines=True)
    table.add_column("Nhóm", style="bold cyan")
    table.add_column("Tham số", style="bold")
    table.add_column("Giá trị", style="green")

    for group, values in config.items():
        if isinstance(values, dict):
            for key, val in values.items():
                table.add_row(group, key, str(val))

    console.print(table)


def show_services_table(console: Console, service_classes: list):
    """Hiển thị bảng services."""
    table = Table(title=f"📋 Services ({len(service_classes)})", show_lines=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("Tên", style="bold white", min_width=20)
    table.add_column("Nhóm", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Mô tả", max_width=40)

    for i, cls in enumerate(service_classes, 1):
        status = "[green]✅[/green]" if cls.active else "[red]❌[/red]"
        table.add_row(str(i), cls.name, cls.category, status, cls.description)

    console.print(table)

    # Thống kê theo nhóm
    from collections import Counter
    categories = Counter(cls.category for cls in service_classes if cls.active)
    console.print(f"\n[bold]Theo nhóm:[/bold] {dict(categories)}")
    console.print(f"[bold]Active:[/bold] {sum(1 for c in service_classes if c.active)}/{len(service_classes)}\n")


def run_otp_flow(console: Console, config: dict, service_classes: list, export: str = None):
    """Flow chạy OTP chính."""
    # Nhập SĐT
    phone_input = Prompt.ask("[bold]📱 Nhập số điện thoại[/bold] (cách nhau bằng dấu cách)")
    phone_list = phone_input.strip().split()

    if not phone_list:
        console.print("[red]Chưa nhập số điện thoại![/red]")
        return

    # Nhập số vòng
    count = IntPrompt.ask("[bold]🔢 Số vòng lặp[/bold]", default=1)

    # Chọn category
    filter_cat = Confirm.ask("[bold]🏷️  Lọc theo nhóm service?[/bold]", default=False)
    categories = None
    if filter_cat:
        cat_input = Prompt.ask(
            "Nhập nhóm (telecom/ecommerce/fnb/delivery/finance/education/realestate/other)",
            default="all",
        )
        if cat_input != "all":
            categories = cat_input.strip().split()

    # Xác nhận
    console.print(f"\n[bold]📋 Tóm tắt:[/bold]")
    console.print(f"  SĐT: {', '.join(phone_list)}")
    console.print(f"  Vòng lặp: {count}")
    console.print(f"  Nhóm: {categories or 'Tất cả'}")

    if not Confirm.ask("\n[bold]▶️  Bắt đầu?[/bold]", default=True):
        return

    # Chạy
    stats = run(
        phone_list=phone_list,
        count=count,
        service_classes=service_classes,
        config=config,
        categories=categories,
    )

    # Hiển thị kết quả
    stats.display()

    # Export
    if export:
        if export == "json":
            path = stats.export_json()
        else:
            path = stats.export_csv()
        console.print(f"[green]📄 Đã xuất: {path}[/green]")
    elif Confirm.ask("📄 Xuất kết quả ra file?", default=False):
        fmt = Prompt.ask("Định dạng", choices=["json", "csv"], default="json")
        path = stats.export_json() if fmt == "json" else stats.export_csv()
        console.print(f"[green]📄 Đã xuất: {path}[/green]")


def interactive_mode():
    """Chạy chế độ TUI tương tác."""
    console = Console()
    console.print(BANNER)

    config = load_config()
    logger = setup_logger(config)
    service_classes = discover_services()

    console.print(f"[bold green]✅ Đã load {len(service_classes)} services[/bold green]\n")

    while True:
        show_menu(console)
        choice = Prompt.ask("[bold]Chọn[/bold]", default="0")

        if choice == "1":
            run_otp_flow(console, config, service_classes)

        elif choice == "2":
            show_services_table(console, service_classes)

        elif choice == "3":
            phone = Prompt.ask("[bold]📱 SĐT để test[/bold]", default="0000000000")
            health_check(service_classes, config, test_phone=phone)

        elif choice == "4":
            show_config(console, config)

        elif choice == "5":
            fmt = Prompt.ask("Định dạng export", choices=["json", "csv"], default="json")
            run_otp_flow(console, config, service_classes, export=fmt)

        elif choice == "0":
            console.print("[bold yellow]👋 Tạm biệt![/bold yellow]")
            break

        else:
            console.print("[red]Lựa chọn không hợp lệ![/red]")
