import os
from .directory import JesterDirectory


class JesterProject:
    def __init__(self, name, code, root_path):
        self.name = name
        self.code = code
        self.dirname = os.path.dirname(root_path).replace("\\", "/")
        self.root = JesterDirectory(os.path.basename(root_path), self)

    def __repr__(self):
        return f"<JesterProject: {self.root.path(JesterDirectory.ABSOLUTE)}>"

    def __str__(self) -> str:
        return self.__repr__()

    def add_location(self, target, children=None, qt_callback=None):
        target_directory = self.directory(target, return_existing=True)
        existing_parts = target_directory.path().split("/")
        target_parts = target.split("/")

        for node in [part for part in target_parts if part not in existing_parts]:
            if qt_callback:
                newly_created_directory = qt_callback(target_directory, node)
            else:
                newly_created_directory = target_directory.append_child(node)
            target_directory = newly_created_directory
        return target_directory

    def exists(self, target):
        return bool(self.directory(target, return_existing=False))

    def directory(self, target, location=None, return_existing=False):
        location = location or self.root
        dirnames = target.split("/")
        for child in location.children:
            if dirnames[0] == child.name:
                return self.directory("/".join(dirnames[1:]), location=child, return_existing=return_existing)
        if target and not return_existing:
            return False
        return location

    def rows(self, _directory=None, _count=0):
        _directory = _directory or self.root
        for child in _directory.children:
            _count += (1 + self.rows(child))
        return _count
