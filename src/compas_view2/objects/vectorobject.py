from compas_view2.gl import make_index_buffer
from compas_view2.gl import make_vertex_buffer

from .object import Object


class VectorObject(Object):
    """Object for displaying vector as arrow."""

    def __init__(self, data, color=None, position=None, size=1, **kwargs):
        super().__init__(data, **kwargs)
        self.color = color or [0, 0, 0]
        self.position = position or [0, 0, 0]
        self.size = size

    def init(self):
        self.make_buffers()
        self._update_matrix()

    def make_buffers(self):
        self._vector_buffer = {
            "positions": make_vertex_buffer(list(self.position)),
            "directions": make_vertex_buffer(list(self._data)),
            "colors": make_vertex_buffer(self.color),
            "sizes": make_vertex_buffer([self.size]),
            "elements": make_index_buffer([0]),
            "n": 1,
        }

    def draw(self, shader):
        shader.enable_attribute("position")
        shader.enable_attribute("direction")
        shader.enable_attribute("color")
        shader.enable_attribute("size")
        shader.uniform4x4("transform", self.matrix)
        shader.bind_attribute("position", self._vector_buffer["positions"])
        shader.bind_attribute("direction", self._vector_buffer["directions"])
        shader.bind_attribute("color", self._vector_buffer["colors"])
        shader.bind_attribute("size", self._vector_buffer["sizes"], step=1)
        shader.draw_arrows(elements=self._vector_buffer["elements"], n=self._vector_buffer["n"])
        shader.disable_attribute("position")
        shader.disable_attribute("direction")
        shader.disable_attribute("color")
        shader.disable_attribute("size")
