from typing import Dict

from PyQt5.QtGui import (
    QStandardItem
)

from PyQt5.QtCore import (
    QAbstractListModel,
    QByteArray,
    Qt,
    QVariant,
    QModelIndex,
    QByteArray
)

from jester.core import (
    JesterCopy
)

from jester.gui.enums import JesterUserRole

class JesterCopyListModel(QAbstractListModel):


    def __init__(self, copy_list: list = list(), *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._copy_object = JesterCopy.from_list(copy_list)

    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._copy_object.list)):
            return QVariant()
        
        data_handler = self._copy_object.list[index.row()]
        if role == Qt.DisplayRole:
            return f"{data_handler.incoming.data.file_path} --> {data_handler.outgoing.data.file_path}"
        elif role == JesterUserRole.CopyOperationRole.value:
            return data_handler
        
        return QVariant()

    def roleNames(self) -> Dict[int, QByteArray]:
        roles = {
            Qt.DisplayRole: b"displayRole",
            JesterUserRole.CopyOperationRole: b"CopyOperationRole"
        }
        return roles
    
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._copy_object.list)
    
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 3
    
    def setData(self, index: QModelIndex, data_handler: object, role=Qt.DisplayRole):
        valid = index.isValid()
        row = index.row()
        in_range = 0 <= index.row() < len(self._copy_object.list)
        if not index.isValid() or not (0 <= index.row() < len(self._copy_object.list)):
            return False
        if role == Qt.DisplayRole:
            self._copy_object.list[index.row()] = data_handler
            self.dataChanged.emit(index, index)
            return True
    
    def insertRows(self, position: int, rows: int, index: QModelIndex = QModelIndex()):
        self.beginInsertRows(index, position, position + rows - 1)
        for row in range(rows):
            self._copy_object.list.insert(position, None)
        self.endInsertRows()
        return True
    
    def removeRows(self, position: int, rows: int, index: QModelIndex = QModelIndex()):
        self.beginRemoveRows(index, position, position + rows - 1)
        for row in range(rows):
            del self._copy_object.list[position]
        self.endRemoveRows()
        return True
    
    # custom methods

    def append(self, handler: "MediaSourceNodeHandler"):
        self.insertRows(len(self._copy_object.list), 1)
        index = self.index(len(self._copy_object.list) - 1)
        self.setData(index, handler)
    
    def remove(self, handler: "MediaSourceNodeHandler"):
        # Find the index of the handler in the list
        row = self._copy_object.list.index(handler)
        self.removeRows(row, 1)