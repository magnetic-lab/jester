# -*- coding: utf-8 -*-
"""Custom model for QTableView objects."""
from PyQt5.QtCore import QAbstractItemModel


class JesterTurnoverGraphModel(QAbstractItemModel):

    def __init__(self, data) -> None:
        """Construct `SourceModel` from given `data`.

        Args:
            data (dict): department-dictionary.

        Raises:
            ValueError: if data is invalid.
        """
        super(JesterTurnoverGraphModel, self).__init__()
        self._data = data