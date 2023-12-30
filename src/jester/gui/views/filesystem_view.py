from PyQt5.QtWidgets import (
    QTreeView
)

from PyQt5.QtCore import (
    pyqtSlot
)


class JesterFileSystemView(QTreeView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    @pyqtSlot(str)
    def update_root_index(self, root_path):
        self.setRootIndex(self.model().index(root_path))