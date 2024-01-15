# -*- coding: utf-8 -*-
"""Custom model for QTableView objects."""
import platform
from typing import Dict

from PyQt5.QtGui import (
    QStandardItem
)
from PyQt5.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QStorageInfo, 
    pyqtSignal,
    QThread,
    Qt,
    QVariant,
    QByteArray
)

from jester.gui.enums import JesterUserRole


class DriveListLoader(QThread):
    loaded = pyqtSignal(list)

    def run(self):
        drives = []
        if platform.system().lower() == "linux":
            for storage in QStorageInfo.mountedVolumes():
                if not storage.isReady() or not storage.isValid():
                    continue
                if storage.rootPath().startswith(("/snap", "/run", "/boot", "/var")):
                    continue
                drives.append(storage)
        if platform.system().lower() == "windows":
            for storage in QStorageInfo.mountedVolumes():
                if not storage.isReady() or not storage.isValid():
                    continue
                drives.append(storage)
        self.loaded.emit(drives)


class JesterDrivesListModel(QAbstractListModel):

    def __init__(self, *args, **kwargs):
        super(JesterDrivesListModel, self).__init__(*args, **kwargs)
        self.thread = None
        # Initialize an internal list to store drives
        # NOTE: no need to use fancy core logic for data storage here as this is strictly a GUI-only feature
        self._drives = []

    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._drives)):
            return QVariant()

        if role == Qt.DisplayRole:
            return self._drives[index.row()].data(Qt.DisplayRole)
        elif role == JesterUserRole.StorageInfoRole:  # custom role for retreiving original `QStorageInfo`` object
            # Return additional data associated with the item (e.g., QStorageInfo)
            return self._drives[index.row()].data(self.StorageInfoRole)  # Assuming Qt.UserRole contains the additional data

        return QVariant()

    def roleNames(self) -> Dict[int, QByteArray]:
        # Define role names mapping for QML integration (if needed)
        roles = {
            Qt.DisplayRole: b"DisplayRole",
            self.StorageInfoRole: b"StorageInfoRole"
        }
        return roles
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._drives)

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def setData(self, index: QModelIndex, value: QStandardItem, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._drives)):
            return False
        if role == Qt.DisplayRole:
            self._drives[index.row()] = value
            self.dataChanged.emit(index, index)
            return True
        elif role == Qt.EditRole:
            self._drives[index.row()] = value
            self.dataChanged.emit(index, index)
            return True

    def insertRows(self, position: int, rows: int, index=QModelIndex()):
        self.beginInsertRows(index, position, position + rows - 1)
        for row in range(rows):
            self._drives.insert(position, QStandardItem(index.data()))
        self.endInsertRows()
        return True

    def removeRows(self, position: int, rows: int, index=QModelIndex()):
        self.beginRemoveRows(index, position, position + rows - 1)
        for row in range(rows):
            del self._drives[position]
        self.endRemoveRows()
        return True

    # Additional list-like methods

    def append(self, item: QStandardItem):
        self.insertRows(len(self._drives), 1)
        index = self.index(len(self._drives) - 1)
        self.setData(index, item)

    def pop(self, index):
        if 0 <= index < len(self._drives):
            self.removeRows(index, 1)

    def extend(self, values):
        for value in values:
            self.append(value)

    def __getitem__(self, index):
        return self._drives[index]

    def __len__(self):
        return len(self._drives)

    def __iter__(self):
        return iter(self._drives)

    @classmethod
    def fromMountedDrives(cls):
        model = cls()
        model.thread = DriveListLoader()  # Create and attach the thread to the model
        model.thread.loaded.connect(lambda drives: cls.__updateModel(model, drives))
        model.thread.start()
        return model

    @staticmethod
    def __updateModel(model, drives):
        for storage in drives:
            item = QStandardItem(storage.rootPath())
            item.setData(storage, JesterUserRole.StorageInfoRole.value)
            model.append(item)
