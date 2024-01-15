import os

from PyQt5.QtCore import (
    pyqtSlot,
    pyqtProperty,
    pyqtSignal,
    QObject
)

from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
    QFileDialog
)

from NodeGraphQt import (
    BaseNode,
    NodeBaseWidget
)

from jester.core import MediaData

from jester.gui.nodes.base import (
    JesterBaseNode,
    BaseNodeHandler
)


class MediaSourceNodeHandler(BaseNodeHandler):

    file_path_changed = pyqtSignal(str)

    def __init__(self, data: MediaData = MediaData(), *args, **kwargs) -> None:
        super().__init__(data, *args, **kwargs)
    
    def get_file_path(self):
        return self.incoming.get("file_path")

    def set_file_path(self, file_path: str):
        if file_path != self.outgoing.get("file_path"):
            self.outgoing.set("file_path", file_path)
            self.file_path_changed.emit(file_path)
    
    @classmethod
    def from_file_path(cls, file_path):
        media_data = MediaData(file_path)
        return cls(media_data)
    
    file_path = pyqtProperty(str, get_file_path, set_file_path, notify=file_path_changed)


class MediaSourceInfoWidget(QWidget):
    def __init__(self, parent_node, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.parent_node = parent_node
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)

        # Label to display file path
        self.file_path_label = QLineEdit(self)
        layout.addWidget(self.file_path_label)
        
        # Button to open file dialog
        self.open_file_btn = QPushButton("open", self)
        self.open_file_btn.clicked.connect(self._open_file_dialog)
        layout.addWidget(self.open_file_btn)

        # size-policies
        self.file_path_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.open_file_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # signals

        self.file_path_label.textChanged.connect(self.parent_node.set_file_path)

    def _open_file_dialog(self):
        # Open file dialog and get the selected file path
        file_path, _ = QFileDialog.getOpenFileName(self, "select source media...")
        if file_path:
            self.parent_node.set_file_path(file_path)

    @pyqtSlot(object, str, object, object)
    def on_outgoing_data_changed(self, data_handler, key, previous_value, new_value):
        # TODO: log this to an outpout console embedded in Jester.
        print(f"{data_handler}.{key} changed from `{previous_value}` to `{new_value}`.")


class MediaSourceInfoWrapper(NodeBaseWidget):
    def __init__(self, parent_node, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_node = parent_node
        self.set_name("media_source_info")
        self.set_label(f"{os.path.basename(self.parent_node.data_handler.file_path)} info:")
        self._setup_ui()
    
    def _setup_ui(self):
        info_widget = MediaSourceInfoWidget(self.parent_node)
        self.set_custom_widget(info_widget)

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


class MediaSourceNode(JesterBaseNode):

    NODE_NAME = 'MediaSourceNode'

    # unique node identifier.
    __identifier__ = 'jester.core'

    def __init__(self, media_file_path: str = ""):
        data_handler = MediaSourceNodeHandler.from_file_path(media_file_path)
        super().__init__(data_handler)

        # Create an output port for the media file path
        self.add_output(multi_output=True)
        self._setup_ui()
    
    def _setup_ui(self):
        media_source_info = MediaSourceInfoWrapper(self, parent=self.view)
        self.add_custom_widget(media_source_info)
        self.data_handler.file_path_changed.connect(media_source_info.set_label)
        self.data_handler.file_path_changed.connect(media_source_info.get_custom_widget().file_path_label.setText)

    def set_file_path(self, file_path: str):
        self.data_handler.file_path = file_path