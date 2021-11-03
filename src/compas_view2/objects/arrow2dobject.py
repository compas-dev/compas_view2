from .object import Object
from compas.utilities import flatten
from ..buffers import make_index_buffer, make_vertex_buffer


class Arrow2dObject(Object):
    """Object for displaying text sprites."""

    def __init__(self, data, name=None, color=None, colors=None, opacity=1, size=100):
        super().__init__(data, name=name)
        color = color or [0, 0, 0]
        self.colors = colors or [color for _ in range(len(data.positions))]
        self.opacity = opacity
        self.size = size

    def init(self):
        self.make_buffers()
        self._update_matrix()

    def make_buffers(self):
        self._arrow_buffer = {
            'positions': make_vertex_buffer(list(flatten(self._data.positions))),
            'directions': make_vertex_buffer(list(flatten(self._data.directions))),
            'colors': make_vertex_buffer(list(flatten(self.colors))),
            'elements': make_index_buffer([i for i in range(len(self._data.positions))]),
            'n': len(self._data.positions)
        }

    def draw(self, shader):
        # print('drawing arrow')
        """Draw the object from its buffers"""
        shader.enable_attribute('position')
        shader.enable_attribute('direction')
        shader.enable_attribute('color')
        shader.uniform4x4('transform', self.matrix)
        shader.uniform4x4('size', self.size)
        shader.bind_attribute('position', self._arrow_buffer['positions'])
        shader.bind_attribute('direction', self._arrow_buffer['directions'])
        shader.bind_attribute('color', self._arrow_buffer['colors'])
        shader.draw_arrows(elements=self._arrow_buffer['elements'], n=self._arrow_buffer['n'])
        shader.disable_attribute('position')
        shader.disable_attribute('direction')
        shader.disable_attribute('color')
