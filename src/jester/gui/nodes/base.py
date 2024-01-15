from PyQt5.QtCore import (
    QObject,
    pyqtSignal,
    pyqtSlot
)

from NodeGraphQt import BaseNode

from jester.core import Data


class DataHandler(QObject):

    data_changed = pyqtSignal(QObject, str, object, object)

    def __init__(self, data: Data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._data = data
    
    def get(self, key):
        if hasattr(self._data, key):
            return getattr(self._data, key)
    
    def set(self, key, value):
        if hasattr(self._data, key):
            previous_value = getattr(self._data, key)
            setattr(self._data, key, value)
            # emit signal
            self.data_changed.emit(self, key, previous_value, value)
    
    @property
    def data(self):
        return self._data


class BaseNodeHandler(QObject):

    incoming_data_changed = pyqtSignal(object, str, object, object)
    outgoing_data_changed = pyqtSignal(object, str, object, object)

    def __init__(self, data: Data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._incomming_data = DataHandler(data)
        self._outgoing_data = DataHandler(data)

        # signals
        self._incomming_data.data_changed.connect(self.emit_incoming_data_changed)
        self._outgoing_data.data_changed.connect(self.emit_outgoing_data_changed)

    @pyqtSlot(QObject, str, object, object)
    def emit_incoming_data_changed(self, data_handler, key, previous_value, new_value):
        self.incoming_data_changed.emit(data_handler.data, key, previous_value, new_value)

    @pyqtSlot(QObject, str, object, object)
    def emit_outgoing_data_changed(self, data_handler, key, previous_value, new_value):
        self.outgoing_data_changed.emit(data_handler.data, key, previous_value, new_value)

    @property
    def incoming(self):
        return self._incomming_data
    
    @property
    def outgoing(self):
        return self._outgoing_data


class JesterBaseNode(BaseNode):
    def __init__(self, data_handler: BaseNodeHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_handler = data_handler
