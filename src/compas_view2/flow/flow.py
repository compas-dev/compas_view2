import ryvencore_qt as rc


class Flow():
    """"A Ryven Flow wrapper."""
    def __init__(self, app):
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
        node = self.script.flow.create_node(node_class)
        x, y = location
        self.flow_view.node_items[node].setX(x)
        self.flow_view.node_items[node].setY(y)
        return node

    def add_connection(self, port1, port2):
        return self.script.flow.connect_nodes(port1, port2)
