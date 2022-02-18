from compas_view2.collections import Collection
from .object import Object
from compas_view2.gl import make_index_buffer, make_vertex_buffer, update_index_buffer, update_vertex_buffer
from compas.utilities import flatten


class VectorCollectionObject(Object):
    """Object for displaying vector as arrow."""

    def __init__(self, collection: Collection, **kwargs):
        super().__init__(collection, **kwargs)

    @property
    def collection(self):
        return self._data

    def init(self):
        self.make_buffers()
        self._update_matrix()

    def update(self):
        self.update_buffers()
        self._update_matrix()

    def make_buffers(self):
        self.positions = [self.collection.item_properties[i].get('position', [0, 0, 0]) for i in range(len(self.collection.item_properties))]
        self.colors = [self.collection.item_properties[i].get('color', [0, 0, 0]) for i in range(len(self.collection.item_properties))]
        self.sizes = [self.collection.item_properties[i].get('size', 1) for i in range(len(self.collection.item_properties))]
        self._vector_buffer = {
            'positions': make_vertex_buffer(list(flatten(self.positions))),
            'directions': make_vertex_buffer(list(flatten(self._data.items))),
            'colors': make_vertex_buffer(list(flatten(self.colors))),
            'sizes': make_vertex_buffer(self.sizes),
            'elements': make_index_buffer([i for i in range(len(self._data.items))]),
            'n': len(self._data.items)
        }

    def update_buffers(self):
        self.positions = [self.collection.item_properties[i].get('position', [0, 0, 0]) for i in range(len(self.collection.item_properties))]
        self.colors = [self.collection.item_properties[i].get('color', [0, 0, 0]) for i in range(len(self.collection.item_properties))]
        self.sizes = [self.collection.item_properties[i].get('size', 1) for i in range(len(self.collection.item_properties))]
        update_vertex_buffer(list(flatten(self.positions)), self._vector_buffer['positions'])
        update_vertex_buffer(list(flatten(self._data.items)), self._vector_buffer['directions'])
        update_vertex_buffer(list(flatten(self.colors)), self._vector_buffer['colors'])
        update_vertex_buffer(self.sizes, self._vector_buffer['sizes'])
        update_index_buffer([i for i in range(len(self._data.items))], self._vector_buffer['elements'])

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
