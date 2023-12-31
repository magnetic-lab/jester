from PyQt5.QtWidgets import (
    QTreeView,
    QPushButton,
    QStyledItemDelegate,
    QApplication,
    QStyle,
    QStyleOptionButton
)

from PyQt5.QtCore import (
    pyqtSlot,
    QModelIndex
)


class ProjectPropertiesTreeView(QTreeView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def columnCount(self, index):
        # Return 2 to create a second column
        return 2

    @pyqtSlot(QModelIndex, int, int)
    def expand_index(self, parent_index, first, last):
        self.expand(parent_index)

    @pyqtSlot(QModelIndex, int, int)
    def scroll_to_index(self, parent_index, first, last):
        self.scrollTo(parent_index)
