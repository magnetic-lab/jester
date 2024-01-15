from jester.core import MediaData


class JesterCopy:
    def __init__(self) -> None:
        self._list = list()
    
    @property
    def list(self):
        return self._list
    
    @list.setter
    def list(self, copy_list):
        # TODO: create custom list of objects from strings
        self._list = [MediaData(item) for item in copy_list]
    
    @classmethod
    def from_list(cls, copy_list):
        jester_copy_object = cls()
        jester_copy_object.list = copy_list
        return jester_copy_object