from NodeGraphQt import (
    BaseNode
)

class TagNode(BaseNode):
    NODE_NAME = 'TagNode'
    # unique node identifier.
    __identifier__ = 'jester.core'

    def __init__(self):
        super(TagNode, self).__init__()

        self.add_input("in1")
        self.add_output("out1")