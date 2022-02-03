import ryvencore_qt as rc
from compas.datastructures import Graph


class Flow(Graph):
    """"A Ryven Flow wrapper."""

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.session = None
        self.script = None
        self.session = rc.Session()
        self.session.design.set_flow_theme(name='pure dark')
        self.script = self.session.create_script(flow_view_size=(800, 500))
        self.flow_view = self.session.flow_views[self.script]

    def show(self):
        self.flow_view.show()

    def add_node(self, node_class, location=(0, 0)):
        # Add ryven node
        ryven_node = self.script.flow.create_node(node_class)
        x, y = location
        self.flow_view.node_items[ryven_node].setX(x)
        self.flow_view.node_items[ryven_node].setY(y)
        data = ryven_node.complete_data(ryven_node.data())

        # Add node in compas graph
        super().add_node(ryven_node.GLOBAL_ID, data)
        return ryven_node

    def add_connection(self, port1, port2):
        # Add ryven connection
        ryven_connection = self.script.flow.connect_nodes(port1, port2)

        # Add connection in compas graph
        node1 = port1.node
        node2 = port2.node
        edge_key = (node1.GLOBAL_ID, node2.GLOBAL_ID)
        if not self.has_edge(*edge_key):
            self.add_edge(*edge_key, {'connections': []})
        connections = self.edge_attribute(edge_key, 'connections')
        connections.append((port1.data(), port2.data()))
        self.edge_attribute(edge_key, 'connections', connections)

        return ryven_connection
