from PyQt5.QtCore import (
    QModelIndex,
    pyqtSlot
)

from PyQt5.QtWidgets import (
    QFormLayout,
    QVBoxLayout,
    QSizePolicy,
    QWidget,
    QPushButton
)

from NodeGraphQt import (
    BaseNode,
    NodeBaseWidget
)


class FileCopyNodeFormWidget(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._setup_ui()
    
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout(self)
        self.copy_button = QPushButton("Copy")
        main_layout.addLayout(self.form_layout)
        main_layout.addWidget(self.copy_button)


class FileCopyNodeFormWrapper(NodeBaseWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_name("form")
        self.set_label("operations")
        self._setup_ui()
    
    def _setup_ui(self):
        form_widget = FileCopyNodeFormWidget()
        self.set_custom_widget(form_widget)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

    def get_value(self, callback=None):
        widget = self.get_custom_widget()
        if not callback:
            return widget
        return callback(widget)

    def set_value(self, data=None, callback=None):
        if not (data and callback):
            return
        widget = self.get_custom_widget()
        return callback(data, widget)


class FileCopyNode(BaseNode):
    NODE_NAME = 'FileCopyNode'
    # unique node identifier.
    __identifier__ = 'jester.core'

    def __init__(self):
        super(FileCopyNode, self).__init__()

        self.add_input("source", multi_input=True)
        self.add_output("target", multi_output=True)
        self._setup_ui()
    
    def _setup_ui(self):
        form_widget_wrapper = FileCopyNodeFormWrapper(parent=self.view)
        self.add_custom_widget(form_widget_wrapper)

        # signals
        form_widget_wrapper.get_custom_widget().copy_button.clicked.connect(self.copy)
    
    def on_input_connected(self, in_port, out_port):
        connected_node = out_port.node()
        properties = connected_node.properties()
        pass

    def copy(self):
        media_source_nodes = self._find_media_source_nodes()
        pass

    def _find_media_source_nodes(self, node=None, visited=None):
        node = node or self
        visited = visited or set()

        visited.add(node)
        media_source_nodes = []

        if node.type_ == "jester.core.MediaSourceNode":
            # Directly return the current node if it's a MediaSourceNode
            return [node]
        for port, nodes in node.connected_input_nodes().items():
            for node in nodes:
                if node not in visited:
                    # Extend the list with media source nodes found in connected nodes
                    media_source_nodes.extend(self._find_media_source_nodes(node, visited))

        return media_source_nodes