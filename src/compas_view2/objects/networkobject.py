from compas.datastructures import Mesh
from compas.utilities import flatten

from ..buffers import make_index_buffer, make_vertex_buffer

from .object import Object


class NetworkObject(Object):

    default_color_nodes = [0.1, 0.1, 0.1]
    default_color_edges = [0.4, 0.4, 0.4]

    def __init__(self, data, name=None, is_selected=False, show_nodes=True, show_edges=True):
        super().__init__(data, name=name, is_selected=is_selected)
        self._nodes = None
        self._edges = None
        self.show_nodes = show_nodes
        self.show_edges = show_edges

    @property
    def nodes(self):
        return self._nodes

    @property
    def edges(self):
        return self._edges

    def init(self):
        data = self._data
        node_xyz = {node: data.node_attributes(node, 'xyz') for node in data.nodes()}
        # nodes
        positions = []
        colors = []
        elements = []
        color = self.default_color_nodes
        i = 0
        for node in data.nodes():
            positions.append(node_xyz[node])
            colors.append(color)
            elements.append(i)
            i += 1
        self._nodes = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(elements),
            'n': i
        }
        # edges
        positions = []
        colors = []
        elements = []
        color = self.default_color_edges
        i = 0
        for u, v in data.edges():
            positions.append(node_xyz[u])
            positions.append(node_xyz[v])
            colors.append(self.default_color_edges)
            colors.append(self.default_color_edges)
            elements.append([i + 0, i + 1])
            i += 2
        self._edges = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(list(flatten(elements))),
            'n': i
        }

    def draw(self, shader):
        shader.enable_attribute('position')
        shader.enable_attribute('color')
        if self.show_edges:
            shader.bind_attribute('position', self.edges['positions'])
            shader.bind_attribute('color', self.edges['colors'])
            shader.draw_lines(elements=self.edges['elements'], n=self.edges['n'])
        if self.show_nodes:
            shader.bind_attribute('position', self.nodes['positions'])
            shader.bind_attribute('color', self.nodes['colors'])
            shader.draw_points(size=10, elements=self.nodes['elements'], n=self.nodes['n'])
        # reset
        shader.disable_attribute('position')
        shader.disable_attribute('color')
