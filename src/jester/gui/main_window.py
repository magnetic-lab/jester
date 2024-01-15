# -*- coding: utf-8 -*-
"""Main Window """
import os

from PyQt5.QtCore import (
    QFile,
    pyqtSlot,
    QModelIndex
)

from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QSplitter,
    QSizePolicy
)
from jester.gui.source_window import JesterSourceWindow
from jester.gui.graph_window import JesterGraphWindow
from jester.gui import nodes


class JesterMainWindow(QMainWindow):
    """This is the main window of the application."""

    def __init__(self):
        super().__init__()
        self._setup_ui()
        self.show()

    def _setup_ui(self):
        # Load the main application stylesheet
        self._load_stylesheet("main.css")
        
        # Collect and store package metadata
        # self._package_metadata = utils.get_package_metadata()
        
        # Build the file menu for the main window
        self._build_file_menu()
        
        # Set the main window title based on package metadata
        # self.setWindowTitle(
            # f"{self._package_metadata._headers[1][1]}-{self._package_metadata._headers[2][1]}")

        # Create a central splitter widget for the main window
        central_splitter_widget = QSplitter(self)
        self.setCentralWidget(central_splitter_widget)

        # Create the source window and turnover window widgets
        self.source_window = JesterSourceWindow(central_splitter_widget)
        self.graph_window = JesterGraphWindow(central_splitter_widget)
        
        # Add the source and turnover windows to the central splitter
        central_splitter_widget.addWidget(self.source_window)
        central_splitter_widget.addWidget(self.graph_window)
        
        # Set the stretch factors for the widgets in the splitter
        central_splitter_widget.setStretchFactor(0, 1)
        central_splitter_widget.setStretchFactor(1, 2)

        # signal connections
        self.source_window.file_system_view.doubleClicked.connect(self.graph_window.on_filesystem_view_item_double_clicked)

    def _load_stylesheet(self, stylesheet_name):
        # Determine the path to the CSS stylesheet file
        root = os.path.dirname(os.path.abspath(__file__))
        css_file = os.path.join(root, "static", "css", "main.css")
        
        # Read and apply the CSS file as the main window's stylesheet
        file = QFile(css_file)
        file.open(QFile.ReadOnly | QFile.Text)
        self.setStyleSheet(str(file.readAll(), 'utf-8'))

    def _build_file_menu(self):
        # Create a 'File' menu in the menu bar
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        
        # Add actions to the 'File' menu (e.g., "Injest Target Directory")
        # The second argument (None) should be replaced with the action handler function
        # that should be executed when the menu item is selected.
        # file_menu.addAction("Injest Target Directory", None)
