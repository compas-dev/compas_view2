import ryvencore_qt as rc
import ryvencore
from compas.datastructures import Graph
from typing import Union, Tuple


class Flow(Graph):
    """ "A Class that represents maps a Ryven Flow graph.

    Parameters
    ----------
    app : :class:`compas_view2.app.App`
        compas_view app instance.
    flow_auto_update : bool
        Whether to auto update the nodes in graph.
        Defaults to True.
    flow_view_size : Tuple[int, int]
        Window size of the flow view.
        Defaults to (800, 500).

    """

    def __init__(self, app, flow_auto_update: bool = True, flow_view_size: Tuple[int, int] = (800, 500)):
        super().__init__()
        self.app = app
        self.flow_auto_update = flow_auto_update
        self.session = rc.Session()
        self.session.design.set_flow_theme(name="pure dark")
        self.script = self.session.create_script(flow_view_size=flow_view_size)
        self.flow_view = self.session.flow_views[self.script]
        self.script.flow.set_algorithm_mode("data opt")
        self.init_run = False

    def run_all(self):
        """Execute all the ryven nodes in the order of data flow."""
        # print("running all nodes")
        executed = set()
        node_update_states = {node: node.block_updates for node in self.flow_view.node_items}

        def traverse_upwards(node):
            # Traverse upwards to the top of data flow graph
            if node in executed:
                return
            for port in node.inputs:
                for connection in port.connections:
                    traverse_upwards(connection.out.node)
            # print("executing", node)
            node.update_event()
            executed.add(node)

        for node in self.flow_view.node_items:
            node.block_updates = True

        for node in self.flow_view.node_items:
            traverse_upwards(node)

        for node in self.flow_view.node_items:
            node.block_updates = node_update_states[node]
        # print("All nodes executed")

    def show(self):
        """Shows the flow view."""
        if not self.init_run and self.flow_auto_update:
            self.run_all()
            self.init_run = True
        self.flow_view.show()

    def add_node(self, node_class: rc.Node, location: Tuple[int, int] = (0, 0), **kwargs) -> rc.Node:
        """Adds a node to the flow view.

        Parameters
        ----------
        node_class : :class:`ryvencore_qt.Node`
            A ryven node class to be added.
        location : Tuple[int, int]
            The location of the node in the flow view.
            Defaults to (0, 0).
        **kwargs : dict, optional
            Additional keyword arguments to be passed to the node class.

        Returns
        -------
        :class:`ryvencore_qt.Node`
            The created ryven node instance.

        """
        ryven_node = self.script.flow.create_node(node_class, data=kwargs)
        x, y = location
        self.flow_view.node_items[ryven_node].setX(x)
        self.flow_view.node_items[ryven_node].setY(y)
        data = ryven_node.complete_data(ryven_node.data())

        super().add_node(key=ryven_node.GLOBAL_ID, attr_dict={"ryven_data": data})
        return ryven_node

    def add_connection(
        self, port1: ryvencore.NodePort.NodeOutput, port2: ryvencore.NodePort.NodeInput
    ) -> ryvencore.Connection.DataConnection:
        """Adds a connection between two ryven nodes.

        Parameters
        ----------
        port1 : :class:`ryvencore.NodePort.NodeOutput`
            The first port for the connection.
        port2 : :class:`ryvencore.NodePort.NodeInput`
            The second port for the connection.

        Returns
        -------
        :class:`ryvencore.Connection.DataConnection`
            The created ryven connection instance.

        """
        ryven_connection = self.script.flow.connect_nodes(port1, port2)
        if not ryven_connection:
            return

        # Add connection in compas graph
        node1 = port1.node
        node2 = port2.node
        edge_key = (node1.GLOBAL_ID, node2.GLOBAL_ID)
        if not self.has_edge(*edge_key):
            self.add_edge(*edge_key, {"connections": []})
        connections = self.edge_attribute(edge_key, "connections")
        connections.append({"port1": self.get_port_info(port1), "port2": self.get_port_info(port2)})
        self.edge_attribute(edge_key, "connections", connections)

        return ryven_connection

    def get_port_info(self, port: Union[ryvencore.NodePort.NodeOutput, ryvencore.NodePort.NodeInput]) -> dict:
        """Gets the port information.

        Parameters
        ----------
        port : Union[:class:`ryvencore.NodePort.NodeOutput`, :class:`ryvencore.NodePort.NodeInput`]
            The port to get the information from.

        Returns
        -------
        dict
            The port information.

        """
        node = port.node
        data = {}
        if port in node.inputs:
            data["type"] = "input"
            data["index"] = node.inputs.index(port)
        elif port in node.outputs:
            data["type"] = "output"
            data["index"] = node.outputs.index(port)
        else:
            raise ValueError("Port is not in inputs or outputs.")

        data["node"] = node.GLOBAL_ID

        return data
