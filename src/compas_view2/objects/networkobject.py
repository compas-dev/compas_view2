from .bufferobject import BufferObject


class NetworkObject(BufferObject):
    """Object for displaying COMPAS network data structures."""

    def __init__(self, data, show_points: bool = True, **kwargs):
        super().__init__(data, show_points=show_points, **kwargs)

    @property
    def nodes(self):
        return self._nodes

    @property
    def edges(self):
        return self._edges

    def _points_data(self):
        data = self._data
        node_xyz = {node: data.node_attributes(node, "xyz") for node in data.nodes()}
        # nodes
        positions = []
        colors = []
        elements = []
        for i, node in enumerate(data.nodes()):
            positions.append(node_xyz[node])
            colors.append(self.pointcolors.get(node, self.pointcolor))
            elements.append([i])
        return positions, colors, elements

    def _lines_data(self):
        data = self._data
        node_xyz = {node: data.node_attributes(node, "xyz") for node in data.nodes()}
        positions = []
        colors = []
        elements = []
        i = 0
        for u, v in data.edges():
            positions.append(node_xyz[u])
            positions.append(node_xyz[v])
            color = self.linecolors.get((u, v), self.linecolor)
            colors.append(color)
            colors.append(color)
            elements.append([i + 0, i + 1])
            i += 2
        return positions, colors, elements
