from .object import Object
from ..buffers import make_index_buffer, make_vertex_buffer
from compas.utilities import flatten


class VectorGroupObject(Object):
    """Object for displaying vector as arrow sprite."""

    def __init__(self, data, colors=None, color=None, sizes=None, size=None, **kwargs):
        super().__init__(data, **kwargs)
        color = color or [0, 0, 0]
        self.colors = colors or [list(color) for _ in range(len(data.vectors))]
        size = size or 100
        self.sizes = sizes or [size for _ in range(len(data.vectors))]

    def init(self):
        self.make_buffers()
        self._update_matrix()

    def make_buffers(self):
        self._vector_buffer = {
            'positions': make_vertex_buffer(list(flatten(self._data.positions))),
            'directions': make_vertex_buffer(list(flatten(self._data.vectors))),
            'colors': make_vertex_buffer(list(flatten(self.colors))),
            'sizes': make_vertex_buffer(self.sizes),
            'elements': make_index_buffer([i for i in range(len(self._data.vectors))]),
            'n': len(self._data.vectors)
        }

    def draw(self, shader):
        shader.enable_attribute('position')
        shader.enable_attribute('direction')
        shader.enable_attribute('color')
        shader.enable_attribute('size')
        shader.uniform4x4('transform', self.matrix)
        shader.bind_attribute('position', self._vector_buffer['positions'])
        shader.bind_attribute('direction', self._vector_buffer['directions'])
        shader.bind_attribute('color', self._vector_buffer['colors'])
        shader.bind_attribute('size', self._vector_buffer['sizes'], step=1)
        shader.draw_arrows(elements=self._vector_buffer['elements'], n=self._vector_buffer['n'])
        shader.disable_attribute('position')
        shader.disable_attribute('direction')
        shader.disable_attribute('color')
        shader.disable_attribute('size')
