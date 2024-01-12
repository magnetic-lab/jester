# -*- coding: utf-8 -*-
"""Main interface"""
import argparse
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout
)

from PyQt5.QtCore import (
    QCoreApplication,
    Qt
)

from jester.gui import (
    JesterMainWindow,
    models,
    views
)

def debug(main_window):
    graph = main_window.turnover_window.graph
    pp_node = graph.create_node("jester.core.ProjectPropertiesNode", "The Amazing First Project!")
    pp_node.set_pos(500, 400)
    fc_node = graph.create_node("jester.core.FileCopyNode")
    fc_node.set_pos(1200, 400)
    pp_node.set_output(0, fc_node.input(0))
    for i in range(10):
        source_node = graph.create_node("jester.core.MediaSourceNode", f"media_source_{i}")
        source_node.set_pos(10, i * 100)
        source_node.set_output(0, pp_node.input(0))

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
    gui_parser = subparsers.add_parser("gui", help="Launch Jester GUI")
    gui_parser.set_defaults(func=show_command)

    args = parser.parse_args()
    args.func(args)
