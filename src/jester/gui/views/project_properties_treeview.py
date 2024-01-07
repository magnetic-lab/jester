from enum import Enum, auto

from PyQt5.QtWidgets import (
    QTreeView,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QButtonGroup,
    QSizePolicy
)

from PyQt5.QtCore import (
    QSize,
    pyqtSlot,
    pyqtSignal,
    QModelIndex
)


class ButtonAction(Enum):

    ADD = auto()
    REMOVE = auto()

class ButtonGroupWidget(QWidget):

    add_button_clicked = pyqtSignal(str, QModelIndex)
    remove_button_clicked = pyqtSignal(int, QModelIndex)
    edit_button_clicked = pyqtSignal(QModelIndex)

    ADD = ButtonAction.ADD
    REMOVE = ButtonAction.REMOVE

    def __init__(self, index: QModelIndex = QModelIndex(), parent: QWidget = None):
        super().__init__(parent)
        self.index = index
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.button_group = self.setup_buttons()
        self.button_group.setExclusive(False)  # remove toggle-behavior
        self.button_group.buttonClicked[int].connect(self.on_button_group_clicked)

    def setup_buttons(self):
        button_group = QButtonGroup(self)
        buttons_map = {
            "+": self.ADD,
            "-": self.REMOVE
        }
        for button_name, enum in buttons_map.items():
            button = QPushButton(button_name, self)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            button_group.addButton(button, enum.value)
            self.layout().addWidget(button)
        return button_group
    
    @pyqtSlot(QModelIndex, int, int)
    def handle_rows_inserted(self, parent, first, last):
        # not adjustments needed for rows inserted in other parents or, rows below current
        if self.index.parent() != parent or self.index.row() < first:
            return
        # calculate and apply the offset for insertion
        offset = last - first + 1
        self.index = self.index.model().index(self.index.row() + offset, self.index.column(), parent)

    @pyqtSlot(QModelIndex, int, int)
    def handle_rows_removed(self, parent, first, last):
        # no adjustments needed for rows deleted from other parents or, rows below current
        if self.index.parent() != parent or self.index.row() <= first:
            return
        # calculate and apply the offset for removal
        offset = last - first + 1
        self.index = self.index.model().createIndex(self.index.row() - offset, self.index.column(), self.index.internalPointer())

    @pyqtSlot(int)
    def on_button_group_clicked(self, id):
        clicked_index = self.button_group.button(id).parent().index
        signal_map = {
            self.ADD: self.add_button_clicked,
            self.REMOVE: self.remove_button_clicked
        }
        args_map = {
            self.ADD: (None, clicked_index),  # TODO: this is where we would include the name for newly created directories
            self.REMOVE: (clicked_index.row(), clicked_index.parent())
        }
        result = signal_map[ButtonAction(id)].emit(*args_map[ButtonAction(id)])
        return result


class ProjectPropertiesTreeView(QTreeView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setHeaderHidden(True)
        self.setIndentation(5)

    # re-implemented `QTreeView` methods

    def columnCount(self, index):
        # Return 2 to create a second column
        return 2

    # slots

    @pyqtSlot(QModelIndex, int, int)
    def show_button_group(self, parent_index, row, column):
        treeview_model = self.model()
        button_group_index = treeview_model.index(row, 1, parent_index)
        if button_group_index.isValid():
            # this is where we associate a `QModelIndex` to the `ButtonGroupWidget`
            button_group = ButtonGroupWidget(button_group_index, self)
            button_group.add_button_clicked.connect(treeview_model.append_child_row)
            button_group.remove_button_clicked.connect(treeview_model.removeRow)
            treeview_model.rowsAboutToBeInserted.connect(button_group.handle_rows_inserted)
            treeview_model.rowsAboutToBeRemoved.connect(button_group.handle_rows_removed)
            self.setIndexWidget(button_group_index, button_group)
        
    @pyqtSlot(QModelIndex, int, int)
    def expand_index(self, parent_index, first, last):
        self.expand(parent_index)

    @pyqtSlot(QModelIndex, int, int)
    def scroll_to_index(self, parent_index, first, last):
        self.scrollTo(parent_index)
