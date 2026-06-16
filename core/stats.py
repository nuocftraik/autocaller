"""
stats.py — Thu thập và hiển thị thống kê kết quả.
"""

import threading
import json
import csv
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional

from rich.table import Table
from rich.console import Console
from rich.panel import Panel

from core.base_service import ServiceResult


class Stats:
    """Thread-safe thống kê kết quả chạy autocaller."""

    def __init__(self):
        self._lock = threading.Lock()
        self._results: list[ServiceResult] = []
        self._per_service: dict[str, dict] = defaultdict(
            lambda: {"success": 0, "fail": 0, "total_time_ms": 0.0, "errors": []}
        )
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None

    def record(self, result: ServiceResult):
        """Ghi nhận 1 kết quả (thread-safe)."""
        with self._lock:
            self._results.append(result)
            entry = self._per_service[result.service_name]
            if result.success:
                entry["success"] += 1
            else:
                entry["fail"] += 1
                if result.error:
                    entry["errors"].append(result.error)
            entry["total_time_ms"] += result.response_time_ms

    def start_timer(self):
        """Bắt đầu đo thời gian tổng."""
        import time
        self._start_time = time.perf_counter()

    def stop_timer(self):
        """Kết thúc đo thời gian tổng."""
        import time
        self._end_time = time.perf_counter()

    @property
    def total_success(self) -> int:
        return sum(e["success"] for e in self._per_service.values())

    @property
    def total_fail(self) -> int:
        return sum(e["fail"] for e in self._per_service.values())

    @property
    def total_requests(self) -> int:
        return self.total_success + self.total_fail

    @property
    def success_rate(self) -> float:
        total = self.total_requests
        if total == 0:
            return 0.0
        return (self.total_success / total) * 100

    @property
    def elapsed_seconds(self) -> float:
        if self._start_time and self._end_time:
            return self._end_time - self._start_time
        return 0.0

    def display(self):
        """Hiển thị bảng thống kê bằng rich."""
        console = Console()

        # --- Bảng chi tiết per-service ---
        table = Table(
            title="📊 Thống Kê Chi Tiết",
            show_lines=True,
            header_style="bold cyan",
        )
        table.add_column("Service", style="bold white", min_width=20)
        table.add_column("✅ OK", justify="center", style="green")
        table.add_column("❌ Fail", justify="center", style="red")
        table.add_column("Tỷ lệ", justify="center")
        table.add_column("Avg (ms)", justify="center", style="yellow")

        for name, data in sorted(self._per_service.items()):
            total = data["success"] + data["fail"]
            rate = (data["success"] / total * 100) if total > 0 else 0
            avg_ms = (data["total_time_ms"] / total) if total > 0 else 0

            rate_style = "green" if rate >= 80 else ("yellow" if rate >= 50 else "red")
            rate_str = f"[{rate_style}]{rate:.0f}%[/{rate_style}]"

            table.add_row(
                name,
                str(data["success"]),
                str(data["fail"]),
                rate_str,
                f"{avg_ms:.0f}",
            )

        console.print(table)

        # --- Tóm tắt tổng ---
        elapsed = f"{self.elapsed_seconds:.1f}s" if self.elapsed_seconds else "N/A"
        summary = (
            f"[bold]Tổng requests:[/bold] {self.total_requests}  |  "
            f"[green]Thành công: {self.total_success}[/green]  |  "
            f"[red]Thất bại: {self.total_fail}[/red]  |  "
            f"[cyan]Tỷ lệ: {self.success_rate:.1f}%[/cyan]  |  "
            f"[yellow]Thời gian: {elapsed}[/yellow]"
        )
        console.print(Panel(summary, title="📈 Tổng Kết", border_style="bright_blue"))

    def export_json(self, filepath: str = None):
        """Xuất kết quả ra file JSON."""
        if filepath is None:
            Path("logs").mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"logs/results_{timestamp}.json"

        data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": self.total_requests,
                "success": self.total_success,
                "fail": self.total_fail,
                "success_rate": round(self.success_rate, 2),
                "elapsed_seconds": round(self.elapsed_seconds, 2),
            },
            "per_service": dict(self._per_service),
            "results": [
                {
                    "service": r.service_name,
                    "success": r.success,
                    "phone": r.phone,
                    "status_code": r.status_code,
                    "response_time_ms": round(r.response_time_ms, 1),
                    "error": r.error,
                }
                for r in self._results
            ],
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return filepath

    def export_csv(self, filepath: str = None):
        """Xuất kết quả ra file CSV."""
        if filepath is None:
            Path("logs").mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"logs/results_{timestamp}.csv"

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Service", "Success", "Phone", "StatusCode", "ResponseTimeMs", "Error"])
            for r in self._results:
                writer.writerow([
                    r.service_name, r.success, r.phone,
                    r.status_code, round(r.response_time_ms, 1), r.error or "",
                ])

        return filepath
