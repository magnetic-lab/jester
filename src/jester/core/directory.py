from typing import Union


class JesterDirectory:
    def __init__(self, name, parent=None, children=None, type=None):
        self.name = name
        self.parent = parent
        self.type = 0
        self.children = children or list()

    def __repr__(self) -> str:
        parent = self.parent
        if not isinstance(parent, JesterDirectory):
            # project directory-root
            return self.name
        return f"{parent}/{self.name}"
    
    def __str__(self) -> str:
        return self.__repr__()

    def append_child(self, child: Union[str, "JesterDirectory"]):
        if isinstance(child, str):
            child = JesterDirectory(child)
        self.children.append(child)
        child.parent = self
        return child
    
    def path(self, relative=False, include_root=False, _node=None):
        if relative:
            if include_root:
                parts = self.__str__().split("/")
            else:
                parts = self.__str__().split("/")
                subtract_str = self.project().root.name
                parts.pop(parts.index(subtract_str))
            result = "/".join(parts) if len(parts) else ""
            return result
        node = _node or self
        if isinstance(node, JesterDirectory):
            return self.path(relative=relative, include_root=include_root, _node=node.parent)
        return "/".join([node.dirname, self.__str__()])
    
    def project(self, _node=None):
        node = _node or self
        if isinstance(node, JesterDirectory):
            return self.project(node.parent)
        return node
    
    def is_root(self):
        return not isinstance(self.parent, JesterDirectory)
    
    def set_name(self, name):
        self.name = name
        return name