from PyQt5.QtWidgets import (
    QTreeView,
    QPushButton,
    QStyledItemDelegate,
    QWidget,
    QHBoxLayout,
    QButtonGroup,
    QSizePolicy
)

from PyQt5.QtCore import (
    pyqtSlot,
    pyqtSignal,
    QModelIndex,
    QRect
)


class ButtonGroupWidget(QWidget):

    add_button_clicked = pyqtSignal(int, QModelIndex)
    remove_button_clicked = pyqtSignal(int, QModelIndex)
    up_button_clicked = pyqtSignal(QModelIndex)
    down_button_clicked = pyqtSignal(QModelIndex)
    edit_button_clicked = pyqtSignal(QModelIndex)

    ADD = 0
    REMOVE = 1
    UP = 2
    DOWN = 3
    EDIT = 4

    def __init__(self, index: QModelIndex, parent: QWidget = None):
        super().__init__(parent)
        self.index = index
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.button_group = self.setup_buttons()
        self.button_group.buttonClicked[int].connect(self.on_button_group_clicked)

    def totalWidth(self):
        if not self.button_group.buttons():
            return 0
        # button_width = self.button_group.buttons()[0].sizeHint().width()
        button_width = 10
        return len(self.button_group.buttons()) * button_width

    def setup_buttons(self):
        button_group = QButtonGroup(self)
        buttons_map = {
            "+": self.ADD,
            "-": self.REMOVE,
            "u": self.UP,
            "d": self.DOWN,
            "e": self.EDIT
        }
        for button_name, constant in buttons_map.items():
            button = QPushButton(button_name, self)
            button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            button_group.addButton(button, constant)
            self.layout().addWidget(button)
        return button_group

    @pyqtSlot(int)
    def on_button_group_clicked(self, id):
        clicked_index = self.button_group.button(id).parent().index
        signal_map = {
            self.ADD: self.add_button_clicked,
            self.REMOVE: self.remove_button_clicked,
            self.UP: self.up_button_clicked,
            self.DOWN: self.down_button_clicked,
            self.EDIT: self.edit_button_clicked,
        }
        args_map = {
            self.ADD: (clicked_index.row(), clicked_index),
            self.REMOVE: (clicked_index.row(), clicked_index.parent()),
            self.UP: self.up_button_clicked,
            self.DOWN: self.down_button_clicked,
            self.EDIT: self.edit_button_clicked
        }
        result = signal_map[id].emit(*args_map[id])
        return result

class ButtonGroupDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        if index.column() == 1:
            treeview_model = self.parent().model()
            button_group = ButtonGroupWidget(index, parent)
            button_group.add_button_clicked.connect(treeview_model.insertRow)
            button_group.remove_button_clicked.connect(treeview_model.removeRow)
            button_group.up_button_clicked.connect(treeview_model.moveRow)
            button_group.down_button_clicked.connect(treeview_model.moveRow)
            button_group.edit_button_clicked.connect(treeview_model.edit_row)
            return button_group
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        # Set data if needed
        pass

    def updateEditorGeometry(self, editor, option, index):
        if index.column() == 1:
            editor.setGeometry(option.rect)
    
    def editorEvent(self, event, model, option, index):
        if index.column() == 1:
            if not self.parent().indexWidget(index):
                self.parent().openPersistentEditor(index)
        return super().editorEvent(event, model, option, index)


class ProjectPropertiesTreeView(QTreeView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setHeaderHidden(True)
        self.setIndentation(5)
        self.setItemDelegateForColumn(1, ButtonGroupDelegate(self))

    def adjustSecondColumnWidth(self):
        # Assuming all ButtonGroupWidgets will have the same width
        if self.model() and self.model().rowCount() > 0:
            temp_widget = ButtonGroupWidget(index=-1)
            column_width = temp_widget.totalWidth()
            self.setColumnWidth(1, column_width)

    def openEditors(self, parent_index):
        if not parent_index.isValid():
            parent = self.model().project.root
        else:
            parent = parent_index.internalPointer()
        for i in range(len(parent.children)):
            child_index = self.model().index(i, 1, parent_index)  # 1 refers to the second column
            self.openPersistentEditor(child_index)
        # adjust the width of the column to fit
        self.adjustSecondColumnWidth()

    def columnCount(self, index):
        # Return 2 to create a second column
        return 2

    @pyqtSlot(QModelIndex, int, int)
    def expand_index(self, parent_index, first, last):
        self.expand(parent_index)

    @pyqtSlot(QModelIndex, int, int)
    def scroll_to_index(self, parent_index, first, last):
        self.scrollTo(parent_index)
    
    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        if index.column() == 1:
            rect = self.visualRect(index)
            button_width = rect.height()  # Assuming square buttons
            total_width = button_width * 5
            start_x = rect.x() + (rect.width() - total_width) // 2  # Centering the button group

            for i in range(5):
                button_rect = QRect(start_x + i * button_width, rect.y(), button_width, button_width)
                if button_rect.contains(event.pos()):
                    print(f"Button {i + 1} in row {index.row()} clicked")
                    break
        super(ProjectPropertiesTreeView, self).mousePressEvent(event)
