from .object import Object
from ..buffers import make_index_buffer, make_vertex_buffer
from compas.utilities import flatten


class VectorCollectionObject(Object):
    """Object for displaying vector as arrow."""

    def __init__(self, collection, colors=None, positions=None, sizes=None, **kwargs):
        super().__init__(collection, **kwargs)
        self.colors = colors or [[0, 0, 0]] * len(collection.items)
        self.positions = positions or [[0, 0, 0]] * len(collection.items)
        self.sizes = sizes or [1] * len(collection.items)

        print(kwargs)

    def init(self):
        self.make_buffers()
        self._update_matrix()

    def make_buffers(self):
        self._vector_buffer = {
            'positions': make_vertex_buffer(list(flatten(self.positions))),
            'directions': make_vertex_buffer(list(flatten(self._data.items))),
            'colors': make_vertex_buffer(list(flatten(self.colors))),
            'sizes': make_vertex_buffer(self.sizes),
            'elements': make_index_buffer([i for i in range(len(self._data.items))]),
            'n': len(self._data.items)
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
