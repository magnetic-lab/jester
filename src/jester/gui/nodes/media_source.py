from PyQt5.QtCore import (
    pyqtSlot,
    QModelIndex
)

from NodeGraphQt import (
    NodeObject,
    BaseNode
)

class MediaSourceNode(BaseNode):
    NODE_NAME = 'MediaSourceNode'
    # unique node identifier.
    __identifier__ = 'jester.core'

    def __init__(self, media_file_path=""):
        super(MediaSourceNode, self).__init__()
        self._media_file_path = media_file_path  # Store the media file path as an instance variable

        # Create an output port for the media file path
        self.add_output(media_file_path)

    def eval_output(self):
        # Return the stored media file path
        return self._media_file_path
