from .bufferobject import BufferObject


class NetworkObject(BufferObject):
    """Object for displaying COMPAS network data structures."""

    default_color_points = [0.1, 0.1, 0.1]
    default_color_lines = [0.4, 0.4, 0.4]

    def __init__(self, data, name=None, is_selected=False, show_points=True, show_lines=True):
        super().__init__(data, name=name, is_selected=is_selected, show_points=show_points, show_lines=show_lines)

    @property
    def nodes(self):
        return self._nodes

    @property
    def edges(self):
        return self._edges

    def _points_data(self):
        data = self._data
        node_xyz = {node: data.node_attributes(node, 'xyz') for node in data.nodes()}
        # nodes
        positions = []
        colors = []
        elements = []
        color = self.default_color_points
        for i, node in enumerate(data.nodes()):
            positions.append(node_xyz[node])
            colors.append(color)
            elements.append([i])
        return positions, colors, elements

    def _lines_data(self):
        data = self._data
        node_xyz = {node: data.node_attributes(node, 'xyz') for node in data.nodes()}
        positions = []
        colors = []
        elements = []
        color = self.default_color_lines
        i = 0
        for u, v in data.edges():
            positions.append(node_xyz[u])
            positions.append(node_xyz[v])
            colors.append(color)
            colors.append(color)
            elements.append([i + 0, i + 1])
            i += 2
        return positions, colors, elements
