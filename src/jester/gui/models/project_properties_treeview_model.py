import os

from PyQt5.QtCore import (
    QAbstractItemModel,
    QModelIndex,
    Qt,
    pyqtSignal,
    pyqtSlot
)

from jester.core import (
    JesterProject,
    LOGGER
)


class ProjectPropertiesTreeViewModel(QAbstractItemModel):
    directory_added = pyqtSignal(QModelIndex)

    def __init__(self, project=None, *args, **kwargs) -> None:
        super(ProjectPropertiesTreeViewModel, self).__init__(*args, **kwargs)
        self.project = project or JesterProject("jester_project", "/".join([os.path.expanduser("~"), "jester_project_root"]))

    # re-implemented `QAbstractItemModel` methods

    def rowCount(self, parentIndex):
        if not parentIndex.isValid():
            return len(self.project.root.children)
        parentItem = parentIndex.internalPointer()
        return len(parentItem.children)

    def columnCount(self, parentIndex):
        return 1  # We have a single column in this example

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.name

    def index(self, row, column, parentIndex):
        if not self.hasIndex(row, column, parentIndex):
            return QModelIndex()
        if not parentIndex.isValid():
            parentItem = self.project.root
        else:
            parentItem = parentIndex.internalPointer()
        childItem = parentItem.children[row]
        return self.createIndex(row, column, childItem)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent
        if parentItem == self.project.root:
            return QModelIndex()
        return self.createIndex(parentItem.children.index(childItem), 0, parentItem)
    
    # jester methods

    def add_location(self, location: str):
        return self.project.add_location(location, qt_callback=self.__update_views_callback)

    def __update_views_callback(self, target_directory, child_name):
        if target_directory.is_root():
            index = QModelIndex()
        else:
            row = len(target_directory.parent.children) - 1
            index = self.createIndex(row, 0, target_directory)
        self.beginInsertRows(index, len(target_directory.children), len(target_directory.children))
        new_directory = target_directory.append_child(child_name)
        self.endInsertRows()
        self.directory_added.emit(index)
        return new_directory
    
    # slots

    @pyqtSlot(str)
    def update_project_code(self, text):
        self.project.code = text

    @pyqtSlot(str)
    def update_project_name(self, text):
        self.project.name = text
