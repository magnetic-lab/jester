from PyQt5.QtCore import Qt

from enum import (
    Enum
)


class JesterUserRole(Enum):

    StorageInfoRole = Qt.UserRole + 1
    CopyOperationRole = Qt.UserRole + 2
