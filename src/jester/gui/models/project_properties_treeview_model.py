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
    
    def insertRow(self, row: int, name: str, parentIndex: QModelIndex = ...) -> bool:
        if row < 0 or row > self.rowCount(parentIndex):
            return False
        # NOTE: It's possible for incoming index's to be from column 1 (when the user clicked a button-group).
        #       This will break the model/view relationship due to our model being hard-coded to 0-columns so,
        #       we hard-set all insertions to be at column 0 regardless of the incoming index.
        parentIndex = self.createIndex(parentIndex.row(), 0, parentIndex.internalPointer())
        self.beginInsertRows(parentIndex, row, row)
        if parentIndex.isValid():
            parent_directory = parentIndex.internalPointer()
            parent_directory.append_child(name)
        else:
            self.project.root.append_child(name)
        self.endInsertRows()
        return True
    
    def removeRow(self, row: int, parentIndex: QModelIndex = ...) -> bool:
        if row < 0 or row >= self.rowCount(parentIndex):
            return False
        # NOTE: all model operations must be on column 0 or the model/view relationships will break
        if parentIndex.column() > 0:
            parentIndex = self.createIndex(parentIndex.row(), 0, parentIndex.internalPointer())
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
        parent_item = parentIndex.internalPointer()
        return len(parent_item.children)

    def columnCount(self, parentIndex):
        return self._column_count

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        # NOTE: this is how we prevent any data populating behind our button-groups in column-1
        if index.column() > 0:
            return None
        item = index.internalPointer()
        return item.name

    def index(self, row, column, parentIndex=QModelIndex()):
        if not self.hasIndex(row, column, parentIndex):
            return QModelIndex()
        if not parentIndex.isValid():
            parent_item = self.project.root
        else:
            parent_item = parentIndex.internalPointer()
        child_item = parent_item.children[row]
        return self.createIndex(row, column, child_item)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        child_item = index.internalPointer()
        parent_item = child_item.parent
        if parent_item == self.project.root:
            return QModelIndex()
        return self.createIndex(parent_item.parent.children.index(parent_item), 0, parent_item)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags

        # Default flags for all items
        defaultFlags = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        # Make specific items editable
        if index.column() == 0:
            return defaultFlags | Qt.ItemIsEditable

        return defaultFlags
    
    def setData(self, index: QModelIndex, value, role: int) -> bool:
        if not index.isValid() or role != Qt.EditRole:
            return False

        if index.column() == 0:
            index.internalPointer().name = value
            self.dataChanged.emit(index, index, [role])
            return True

        return False

    # jester methods

    def append_child_row(self, name: str = None, parent_index: QModelIndex = QModelIndex()):
        row = self.rowCount(parent_index)
        # TODO: this auto-naming doesn't really hold up when removing and re-adding rows. Should be replaced
        #       by a directory naming prompt. I vote for using `jester.gui.nodes.project_properties.AddNewDirectoryWindow`
        name = name or f"directory_{row}"
        return self.insertRow(row, name, parent_index)

    def edit_row(self):
        pass

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
