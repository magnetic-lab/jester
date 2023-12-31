"""Main Window """
import os

from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy
)

from PyQt5.QtCore import (
    pyqtSlot,
    QModelIndex
)

from NodeGraphQt import (
    NodeGraph,
    NodeObject
)

from jester.gui import nodes


class JesterTurnoverWindow(QWidget):
    """This is the main window of the application."""

    def __init__(self, *args, **kwargs):
        super(JesterTurnoverWindow, self).__init__(*args, **kwargs)
        self._setup_ui()
        self._register_nodes()

    def _setup_ui(self):
        self.graph = NodeGraph(self)
        graph_widget = self.graph.widget
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(graph_widget)

        # size-policies
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.context_menu = self.graph.get_context_menu('nodes')
        root = os.path.dirname(os.path.abspath(__file__))
        context_menu = os.path.join(root, "context_menu", "context_menu.json")
        self.graph.set_context_menu_from_file(context_menu)

        # signals
        self.graph.node_created.connect(self.update_node_properties_after_creation)

    
    def _register_nodes(self):
        self.graph.register_nodes(
            [
                nodes.MediaSourceNode,
                nodes.FileCopyNode,
                nodes.MediaEncodeNode,
                nodes.MetadataNode,
                nodes.FileRenameNode,
                nodes.ProjectPropertiesNode,
                nodes.TagNode
            ]
        )
        pass


    @pyqtSlot(NodeObject)
    def update_node_properties_after_creation(self, node=None):
        if node:
            if isinstance(node, nodes.ProjectPropertiesNode):
                project_properties_tree = node.get_widget("project_properties_tree")
                project_properties_tree.set_label(f"{node.name()} project-tree")
                project_properties_form = node.get_widget("project_properties_form")
                project = project_properties_tree.get_custom_widget().tree_view.model().project
                project_properties_form.get_custom_widget().project_code_input.setText(project.root.name)
                project_properties_form.get_custom_widget().project_name_input.setText(project.name)
    
    @pyqtSlot(QModelIndex)
    def create_media_source_node_from_listview_double_click(self, model_index, position=[0, 0]):
        model = model_index.model()
        if model.isDir(model_index):
            return
        # Create a new instance of the MediaSourceNode
        media_source_node = nodes.MediaSourceNode(model_index.data())
        
        # Set the node's position
        media_source_node.set_pos(position[0], position[1])
        
        # Add the node to the graph
        self.graph.add_node(media_source_node)

        return media_source_node