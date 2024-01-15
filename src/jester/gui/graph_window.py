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


class JesterGraphWindow(QWidget):
    """This is the main window of the application."""

    def __init__(self, *args, **kwargs):
        super(JesterGraphWindow, self).__init__(*args, **kwargs)
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
        self.graph.port_connected.connect(self.on_port_connected)
        self.graph.port_disconnected.connect(self.on_port_disconnected)
    
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

    def on_port_connected(self, in_port, out_port):
        self._traverse_and_notify_output_nodes(in_port.node(), out_port.node(), "on_upstream_input_connected")

    def on_port_disconnected(self, in_port, out_port):
        in_node = in_port.node()
        out_node = out_port.node()

        self._traverse_and_notify_output_nodes(in_port.node(), out_port.node(), "on_upstream_input_disconnected")

    def _traverse_and_notify_output_nodes(self, in_node, out_node, notify_method, node=None, visited=None):
        if notify_method == "on_upstream_input_connected":
            node = node or out_node
        elif notify_method == "on_upstream_input_disconnected":
            node = node or in_node
        visited = visited or set()

        if node in visited:
            return
        visited.add(node)

        for port, nodes in node.connected_output_nodes().items():
            for connected_node in nodes:
                if connected_node not in visited:
                    # Call the method on the connected node
                    if hasattr(connected_node, notify_method):
                        notify_method_ = getattr(connected_node, notify_method)
                        notify_method_(out_node)

                    # Recursively traverse the output nodes of the connected node
                    self._traverse_and_notify_output_nodes(in_node, out_node, notify_method, connected_node, visited)


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
    def on_filesystem_view_item_double_clicked(self, index, position=[0, 0]):
        model = index.model()
        if model.isDir(index):
            return

        absolute_path = model.filePath(index)
        # Create a new instance of the MediaSourceNode
        media_source_node = nodes.MediaSourceNode()
        media_source_node.set_file_path(absolute_path)
        
        # Set the node's position
        media_source_node.set_pos(position[0], position[1])
        
        # Add the node to the graph
        self.graph.add_node(media_source_node)

        return media_source_node