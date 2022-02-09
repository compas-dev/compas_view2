import ryvencore_qt as rc
from compas.datastructures import Graph


class Flow(Graph):
    """"A Ryven Flow wrapper."""

    def __init__(self, app, flow_auto_update=True, flow_view_size=(800, 500)):
        super().__init__()
        self.app = app
        self.flow_auto_update = flow_auto_update
        self.session = rc.Session()
        self.session.design.set_flow_theme(name='pure dark')
        self.script = self.session.create_script(flow_view_size=flow_view_size)
        self.flow_view = self.session.flow_views[self.script]

    def show(self):
        self.flow_view.show()

    def add_node(self, node_class, location=(0, 0), **kwargs):
        # Add ryven node
        ryven_node = self.script.flow.create_node(node_class, data=kwargs)
        x, y = location
        self.flow_view.node_items[ryven_node].setX(x)
        self.flow_view.node_items[ryven_node].setY(y)
        data = ryven_node.complete_data(ryven_node.data())

        # Add node in compas graph
        super().add_node(key=ryven_node.GLOBAL_ID, attr_dict={'ryven_data': data})
        return ryven_node

    def add_connection(self, port1, port2):
        # Add ryven connection
        ryven_connection = self.script.flow.connect_nodes(port1, port2)
        if not ryven_connection:
            return

        # Add connection in compas graph
        node1 = port1.node
        node2 = port2.node
        edge_key = (node1.GLOBAL_ID, node2.GLOBAL_ID)
        if not self.has_edge(*edge_key):
            self.add_edge(*edge_key, {'connections': []})
        connections = self.edge_attribute(edge_key, 'connections')
        connections.append({'port1': self.get_port_info(port1), 'port2': self.get_port_info(port2)})
        self.edge_attribute(edge_key, 'connections', connections)

        return ryven_connection

    def get_port_info(self, port):
        node = port.node
        data = {}
        if port in node.inputs:
            data['type'] = 'input'
            data['index'] = node.inputs.index(port)
        elif port in node.outputs:
            data['type'] = 'output'
            data['index'] = node.outputs.index(port)
        else:
            raise ValueError('Port is not in inputs or outputs.')

        data['node'] = node.GLOBAL_ID

        return data
