from PyQt5.QtWidgets import (
    QTreeView,
    QPushButton,
    QStyledItemDelegate,
    QApplication,
    QStyle,
    QStyleOptionButton
)

class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        if index.column() == 1:  # Assuming second column is for buttons
            button = QStyleOptionButton()
            button.rect = option.rect.adjusted(4, 4, -4, -4)  # Adjust margins
            button.text = "+"
            button.state = QStyle.State_Enabled
            QApplication.style().drawControl(QStyle.CE_PushButton, button, painter)
        else:
            super().paint(painter, option, index)

class ProjectPropertiesTreeView(QTreeView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setItemDelegate(ButtonDelegate(self))

    def columnCount(self, index):
        # Return 2 to create a second column
        return 2
    
    def on_rows_inserted(self, parent, first, last):
        # Expand the parent of the newly inserted rows
        pointer = parent.internalPointer()
        self.expand(parent)
        self.scrollTo(parent)
