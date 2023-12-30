from NodeGraphQt import (
    Port,
    BaseNode
)

class MediaEncodeNode(BaseNode):
    NODE_NAME = 'MediaEncodeNode'
    # unique node identifier.
    __identifier__ = 'jester.core'

    def __init__(self):
        super(MediaEncodeNode, self).__init__()

        self.add_input("source", multi_input=True)
        self.add_output("encoded")