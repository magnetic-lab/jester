from NodeGraphQt import (
    Port,
    BaseNode
)

class MetadataNode(BaseNode):
    NODE_NAME = 'MetadataNode'
    # unique node identifier.
    __identifier__ = 'jester.core'

    def __init__(self):
        super(MetadataNode, self).__init__()

        self.add_input("in", multi_input=True)
        self.add_output("out")