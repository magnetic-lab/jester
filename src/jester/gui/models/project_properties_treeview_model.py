import os

from PyQt5.QtCore import (
    QAbstractItemModel,
    QModelIndex,
    Qt
)

from jester.core import (
    JesterProject,
    JesterDirectory,
    LOGGER
)


class ProjectPropertiesTreeViewModel(QAbstractItemModel):

    def __init__(self, project=None, *args, **kwargs) -> None:
        super(ProjectPropertiesTreeViewModel, self).__init__(*args, **kwargs)
        self.project = project or JesterProject("JesterProject", "/".join([os.path.expanduser("~"), "jester_project"]))

    def rowCount(self, parentIndex):
        if not parentIndex.isValid():
            return len(self.project.root.children)
        parentItem = parentIndex.internalPointer()
        return len(parentItem.children)

    def columnCount(self, parentIndex):
        return 1  # We have a single column in this example

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.name

    def index(self, row, column, parentIndex):
        if not self.hasIndex(row, column, parentIndex):
            return QModelIndex()
        if not parentIndex.isValid():
            parentItem = self.project.root
        else:
            parentItem = parentIndex.internalPointer()
        childItem = parentItem.children[row]
        return self.createIndex(row, column, childItem)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent
        if parentItem == self.project.root:
            return QModelIndex()
        return self.createIndex(parentItem.children.index(childItem), 0, parentItem)
    
    def insert_directory(self, name: str, row: int, parent: QModelIndex = ...) -> JesterDirectory:
        self.beginInsertRows(parent, row, row + 1)
        if not parent.isValid():
            parent = self.project.root
        else:
            parent = parent.internalPointer()
        new_directory = parent.insert_child(row, name)
        self.endInsertRows()
        return new_directory

    def add_location(self, location: str):
        """add location

        the for-loop loops over each 'part' in the given location-string and defines `location_` as:
        ```
        [i=0]: assets
        [i=1]: assets/scenes
        [i=2]: assets/scenes/{scene}
        [i=3]: assets/scenes/{scene}/{shot}
        [i=4]: assets/scenes/{scene}/{shot}/{version}
        [i=5]: assets/scenes/{scene}/{shot}/{version}/{dcc}
        ```

        Args:
            location (str): location-string. (example: `assets/scenes/{scene}/{shot}/{version}/{dcc}`)

        Returns:
            _type_: _description_
        """
        # TODO: this method is awful - please simplify
        existing_directory = self.project.directory(location, return_existing=True)
        self.project.add_location(location)
        existing_target = existing_directory.path(relative=True, include_root=False)
        if existing_target:
            existing_parts = existing_target.split("/")
        else:
            existing_parts = []
        parts = location.split("/")
        new_parts = [part if part not in existing_parts else None for part in location.split("/")]


        for i in range(len(parts)):
            if not new_parts[i]:
                continue
            parent_location = "/".join(parts[0:i])
            # Find or create the directory at this level
            if i == 0:
                parent = self.project.root
                index = QModelIndex()  # Start with an invalid index for the root
            else:
                parent = self.project.directory(parent_location)
                row = len(parent.children) - 1
                index = self.createIndex(row, 0, parent)
            # If the directory doesn't exist, insert it
            self.beginInsertRows(index, len(parent.children) - 1, len(parent.children) - 1)
            new_directory = parent.children[len(parent.children) - 1]
            print(f"informing views that {new_directory} was created...")
            self.endInsertRows()
        return new_directory
