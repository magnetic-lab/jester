# -*- coding: utf-8 -*-
"""Custom model for QTableView objects."""
from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtCore import Qt


class JesterFileSystemModel(QFileSystemModel):

    def __init__(self, *args, **kwargs) -> None:
        super(JesterFileSystemModel, self).__init__(*args, **kwargs)

    def update_root_path(self, selected, deselected):
        first_selected_item = selected.first()
        if first_selected_item:
            selected_index = first_selected_item.topLeft()
            selected_data = selected_index.data(role=Qt.DisplayRole)
            self.setRootPath(selected_data)
