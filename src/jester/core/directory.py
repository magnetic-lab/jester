from typing import Union
from enum import Enum, auto


class PathMode(Enum):
    ABSOLUTE = auto()
    RELATIVE = auto()
    RELATIVE_NO_ROOT = auto()


class JesterDirectory:

    ABSOLUTE = PathMode.ABSOLUTE
    RELATIVE = PathMode.RELATIVE
    RELATIVE_NO_ROOT = PathMode.RELATIVE_NO_ROOT

    def __init__(self, name, parent, children=None, type=None):
        self.name = name
        self.parent = parent
        self.type = 0
        self.children = children or list()

    def __repr__(self) -> str:
        return f"<JesterDirectory: {self.path()}>"
    
    def __str__(self) -> str:
        return self.__repr__()

    def append_child(self, child: Union[str, "JesterDirectory"]):
        if isinstance(child, str):
            child = JesterDirectory(child, self)
        self.children.append(child)
        return child
    
    def insert_child(self, index: int, child: Union[str, "JesterDirectory"]):
        if isinstance(child, str):
            child = JesterDirectory(child, self)
        self.children.insert(index, child)
        return child
    
    def path(self, mode=PathMode.ABSOLUTE):
        path_parts = []
        node = self

        # Traverse up the hierarchy to build the path
        while isinstance(node, JesterDirectory):
            path_parts.insert(0, node.name)
            node = node.parent

        # Handle path mode
        if mode == PathMode.RELATIVE:
            return "/".join(path_parts)
        elif mode == PathMode.RELATIVE_NO_ROOT:
            path_parts.pop(0)  # Remove root directory name
            return "/".join(path_parts)
        else:  # Default to ABSOLUTE
            project_dir = self.project().dirname
            return f"{project_dir}/{'/'.join(path_parts)}"

    
    def project(self):
        node = self
        while isinstance(node, JesterDirectory):
            node = node.parent
        return node

    
    def is_root(self):
        return not isinstance(self.parent, JesterDirectory)
    
    def set_name(self, name):
        self.name = name
        return name