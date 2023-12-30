from NodeGraphQt import (
    Port,
    BaseNode
)

class FileRenameNode(BaseNode):
    NODE_NAME = 'FileRenameNode'
    # unique node identifier.
    __identifier__ = 'jester.core'

    def __init__(self):
        super(FileRenameNode, self).__init__()

        self.add_input("source")
        self.add_output("renamed")