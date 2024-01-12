from NodeGraphQt import BaseNode

from jester.core import Data


class JesterBaseNode(BaseNode):
    def __init__(self, data: Data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._previous_data = data
        self._altered_data = Data()