# -*- coding: utf-8 -*-
"""Main interface"""
import argparse
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import (
    QCoreApplication,
    Qt
)

from jester.gui import (
    JesterMainWindow,
    nodes
)

def debug(main_window):
    pp_node = main_window.turnover_window.graph.create_node("jester.core.ProjectPropertiesNode", "The Amazing First Project!")
    pass

def show_command(*args, **kwargs):
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_window = JesterMainWindow()
    main_window.adjustSize()
    debug(main_window)
    sys.exit(app.exec_())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="Sub-Commands")
    show_parser = subparsers.add_parser("gui", help="Launch Jester GUI")
    show_parser.set_defaults(func=show_command)

    args = parser.parse_args()
    args.func(args)
