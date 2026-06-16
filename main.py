#!/usr/bin/env python3
"""
Autocaller v2.0 — Entry point.

Dual-mode:
  - CLI:  python main.py --phone 0357156329 --count 5
  - TUI:  python main.py  (menu tương tác)

Xem help: python main.py --help
"""

import sys
import os

# Thêm project root vào path để import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) > 1:
        # Có tham số → CLI mode
        from ui.cli import cli_mode
        cli_mode()
    else:
        # Không tham số → TUI interactive mode
        from ui.tui import interactive_mode
        interactive_mode()


if __name__ == "__main__":
    main()
