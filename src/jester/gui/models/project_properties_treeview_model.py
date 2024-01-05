import os

from PyQt5.QtCore import (
    QAbstractItemModel,
    QModelIndex,
    Qt,
    pyqtSignal,
    pyqtSlot
)

from jester.core import (
    JesterProject
)


class ProjectPropertiesTreeViewModel(QAbstractItemModel):
    location_added = pyqtSignal(str)

    def __init__(self, project=None, columns=1, *args, **kwargs) -> None:
        super(ProjectPropertiesTreeViewModel, self).__init__(*args, **kwargs)
        self._column_count = columns
        self.project = project or JesterProject("jester_project", "jep", "/".join([os.path.expanduser("~"), "jep"]))

    # re-implemented `QAbstractItemModel` methods
        
    def insertRow(self, row: int, parentIndex: QModelIndex = ...) -> bool:
        if not parentIndex.isValid():
            parent_directory = self.project.root
        else:
            parent_directory = parentIndex.internalPointer()
        start, end = len(parent_directory.children), len(parent_directory.children)
        parentIndex = self.createIndex(row, 0, parent_directory)
        self.beginInsertRows(parentIndex, start, end)
        parent_directory.append_child(f"directory_{start}")
        self.endInsertRows()
        return True
    
    def removeRow(self, row: int, parentIndex: QModelIndex = ...) -> bool:
        if row < 0 or row >= self.rowCount(parentIndex):
            return False
        self.beginRemoveRows(parentIndex, row, row)
        if parentIndex.isValid():
            parent_directory = parentIndex.internalPointer()
            parent_directory.children.pop(row)
        else:
            self.project.root.children.pop(row)
        self.endRemoveRows()
        return True

    def rowCount(self, parentIndex=QModelIndex()):
        if not parentIndex.isValid():
            return len(self.project.root.children)
        parentItem = parentIndex.internalPointer()
        return len(parentItem.children)

    def columnCount(self, parentIndex):
        return self._column_count

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        if index.column() > 0:
            return None
        item = index.internalPointer()
        return item.name

    def index(self, row, column, parentIndex=QModelIndex()):
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
        new_location = self.project.add_location(location, qt_callback=self.__update_views_callback)
        self.location_added.emit(location)
        return new_location

    def __update_views_callback(self, target_directory, child_name):
        if target_directory.is_root():
            index = QModelIndex()
        else:
            row = len(target_directory.parent.children) - 1
            index = self.createIndex(row, 0, target_directory)
        start, end = len(target_directory.children), len(target_directory.children)
        self.beginInsertRows(index, start, end)
        new_directory = target_directory.append_child(child_name)
        self.endInsertRows()
        return new_directory
    
    # slots

    @pyqtSlot(str)
    def update_project_code(self, text):
        self.project.code = text

    @pyqtSlot(str)
    def update_project_name(self, text):
        self.project.name = text
