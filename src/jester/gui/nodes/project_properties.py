from PyQt5.QtCore import (
    QModelIndex,
    pyqtSlot,
    pyqtSignal,
)

from PyQt5.QtWidgets import (
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QSizePolicy,
    QLineEdit,
    QPushButton
)

from NodeGraphQt import (
    BaseNode,
    NodeBaseWidget
)

from jester.gui.views import ProjectPropertiesTreeView
from jester.gui.models import ProjectPropertiesTreeViewModel


# widgets

class AddNewDirectoryWindow(QWidget):
    submitted = pyqtSignal(str)
    def __init__(self, parent: QWidget = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QFormLayout(self)
        self.directory_location_line_edit = QLineEdit()
        self.directory_location_line_edit.setMinimumSize(400, 20)
        self.submit_button = QPushButton("create")
        layout.addRow("location:", self.directory_location_line_edit)
        layout.addWidget(self.submit_button)

        # signal connections
        self.submit_button.clicked.connect(self.submit)
    
    @pyqtSlot(bool)
    def submit(self):
        self.submitted.emit(self.directory_location_line_edit.text())
        self.close()


class ProjectPropertiesFormWidget(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        self.project_code_input = QLineEdit("project-code")
        self.project_name_input = QLineEdit("enter project-name")
        layout.addWidget(self.project_code_input)
        layout.addWidget(self.project_name_input)
        layout.setStretchFactor(self.project_code_input, 1)
        layout.setStretchFactor(self.project_name_input, 3)


class ProjectPropertiesNodeTreeViewWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        tree_view_model = ProjectPropertiesTreeViewModel()
        self.tree_view = ProjectPropertiesTreeView()
        self.tree_view.setModel(tree_view_model)
        add_root_directory_button = QPushButton("+")
        layout.addWidget(add_root_directory_button)
        layout.addWidget(self.tree_view)
        layout.setContentsMargins(0, 0, 0, 0)
        self.add_directory_window = AddNewDirectoryWindow()
        
        # signals
        add_root_directory_button.clicked.connect(self.add_directory_window.show)
        self.add_directory_window.submitted.connect(self.add_location)
        tree_view_model.rowsInserted.connect(self.tree_view.expand_index)
        tree_view_model.rowsInserted.connect(self.tree_view.scroll_to_index)

    @pyqtSlot(str)
    def add_location(self, location: str):
        self.tree_view.model().add_location(location)

# wrappers

class ProjectPropertiesFormWWrapper(NodeBaseWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_name("project_properties_form")
        self.set_label("project properties")
        self._setup_ui()
    
    def _setup_ui(self):
        form_widget = ProjectPropertiesFormWidget()
        self.set_custom_widget(form_widget)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

    def get_value(self, callback=None):
        if not callback:
            return
        widget = self.get_custom_widget()
        return callback(widget)

    def set_value(self, data=None, callback=None):
        if not (data and callback):
            return
        widget = self.get_custom_widget()
        callback(data, widget)


class ProjectPropertiesNodeTreeViewWrapper(NodeBaseWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_name("project_properties_tree")
        self.set_label("project tree")  # not setting label during initializing causes sizing issues.
        self._setup_ui()

    def _setup_ui(self, ):
        treeview_widget = ProjectPropertiesNodeTreeViewWidget()
        self.set_custom_widget(treeview_widget)
        # size-policies
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def get_value(self):
        widget = self.get_custom_widget()
        model = widget.layout().itemAt(1).widget().model()
        return model.project

    def set_value(self, data=None, callback=None):
        if not (data and callback):
            return
        widget = self.get_custom_widget()
        model = widget.layout().itemAt(0).widget().model()
        model.insert_directory(data, model.project.rows() + 1, QModelIndex())
        callback(data)


# base node

class ProjectPropertiesNode(BaseNode):
    NODE_NAME = 'ProjectPropertiesNode'
    # unique node identifier.
    __identifier__ = 'jester.core'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_input("in")
        self.add_output("out")
        self._setup_ui()

    def _setup_ui(self):
        input_form = ProjectPropertiesFormWWrapper(parent=self.view)
        tree_view = ProjectPropertiesNodeTreeViewWrapper(parent=self.view)
        self.add_custom_widget(input_form)
        self.add_custom_widget(tree_view)

        # signals
        input_form.get_custom_widget().project_code_input.textChanged.connect(tree_view.get_custom_widget().tree_view.model().update_project_code)
        input_form.get_custom_widget().project_code_input.textChanged.connect(tree_view.get_custom_widget().tree_view.model().project.root.set_name)
        input_form.get_custom_widget().project_name_input.textChanged.connect(tree_view.get_custom_widget().tree_view.model().update_project_name)
        input_form.get_custom_widget().project_name_input.textChanged.connect(tree_view.set_label)       
