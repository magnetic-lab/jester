from NodeGraphQt import (
    BaseNode
)

class FileCopyNode(BaseNode):
    NODE_NAME = 'FileCopyNode'
    # unique node identifier.
    __identifier__ = 'jester.core'

    def __init__(self):
        super(FileCopyNode, self).__init__()

        self.add_input("source", multi_input=True)
        self.add_output("target")

