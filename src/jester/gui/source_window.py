"""Source Window"""
from PyQt5.QtWidgets import (
    QWidget,
    QSplitter,
    QListView,
    QVBoxLayout,
    QSizePolicy
)

from PyQt5.QtCore import (
    QDir
)

from jester.gui.models import (
    JesterFileSystemModel,
    JesterDrivesListModel
)

from jester.gui.views import JesterFileSystemView


class JesterSourceWindow(QWidget):

    def __init__(self, data, *args, **kwargs):
        super(JesterSourceWindow, self).__init__(*args, **kwargs)
        self.setup_ui(data)

    def setup_ui(self, data):
        # create split-view for the drives on the left, and filesystem on the right
        splitter = QSplitter(self)
        self.drives_view = QListView(splitter)
        self.file_system_view = JesterFileSystemView(splitter)

        # drive_list model for drives view
        drives_model = JesterDrivesListModel.fromMountedDrives()
        self.drives_view.setModel(drives_model)
        
        # filesystem model for treeview
        file_system_model = JesterFileSystemModel()
        # file_system_model.setRootPath(file_system_model.data())
        self.file_system_view.setModel(file_system_model)
        self.file_system_view.setRootIndex(file_system_model.index(file_system_model.rootPath()))
       
        # size policies
        splitter.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        # layout-assignment
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(splitter)

        # slots
        self.drives_view.selectionModel().selectionChanged.connect(file_system_model.update_root_path)
        file_system_model.rootPathChanged.connect(self.file_system_view.update_root_index)
