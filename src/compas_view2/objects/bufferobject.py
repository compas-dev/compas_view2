from compas.utilities import flatten

from ..buffers import make_index_buffer, make_vertex_buffer

from .object import Object


class BufferObject(Object):
    """Object for displaying COMPAS mesh data structures.
    """

    default_color_points = [0.2, 0.2, 0.2]
    default_color_lines = [0.4, 0.4, 0.4]
    default_color_frontfaces = [0.8, 0.8, 0.8]
    default_color_backfaces = [0.8, 0.8, 0.8]

    def __init__(self, data, name=None, is_selected=False, show_points=False,
                 show_lines=False, show_faces=False):
        super().__init__(data, name=name, is_selected=is_selected)
        self._data = data
        self._points_buffer = None
        self._lines_buffer = None
        self._frontfaces_buffer = None
        self._backfaces_buffer = None
        self.show_points = show_points
        self.show_lines = show_lines
        self.show_faces = show_faces
        self.linewidth = 1
        self.pointsize = 10

    def make_buffers(self):

        if hasattr(self, '_points'):
            self._points_buffer = {
                'positions': make_vertex_buffer(list(flatten(self._points))),
                'colors': make_vertex_buffer(list(flatten(self._pointcolors))),
                'elements': make_index_buffer([i for i in range(len(self._pointelements))]),
                'n': len(self._points)
            }

        if hasattr(self, '_linevertices'):
            self._lines_buffer = {
                'positions': make_vertex_buffer(list(flatten(self._linevertices))),
                'colors': make_vertex_buffer(list(flatten(self._linevertexcolors))),
                'elements': make_index_buffer(list(flatten(self._lineelements))),
                'n': len(self._linevertices)
            }

        if hasattr(self, '_frontfacevertices'):
            self._frontfaces_buffer = {
                'positions': make_vertex_buffer(list(flatten(self._frontfacevertices))),
                'colors': make_vertex_buffer(list(flatten(self._frontfacevertexcolors))),
                'elements': make_index_buffer(list(flatten(self._frontfacevertexelements))),
                'n': len(self._frontfacevertices)
            }

        if hasattr(self, '_backfacevertices'):
            self._backfaces_buffer = {
                'positions': make_vertex_buffer(list(flatten(self._backfacevertices))),
                'colors': make_vertex_buffer(list(flatten(self._backfacevertexcolors))),
                'elements': make_index_buffer(list(flatten(self._backfacevertexelements))),
                'n': len(self._backfacevertices)
            }

    def draw(self, shader):
        shader.enable_attribute('position')
        shader.enable_attribute('color')
        shader.uniform1i('is_selected', self.is_selected)
        if self.show_points:
            shader.bind_attribute('position', self._points_buffer['positions'])
            shader.bind_attribute('color', self._points_buffer['colors'])
            shader.draw_points(size=self.pointsize, elements=self._points_buffer['elements'], n=self._points_buffer['n'])
        if self.show_lines:
            shader.bind_attribute('position', self._lines_buffer['positions'])
            shader.bind_attribute('color', self._lines_buffer['colors'])
            shader.draw_lines(width=self.linewidth, elements=self._lines_buffer['elements'], n=self._lines_buffer['n'])
        if self.show_faces:
            shader.bind_attribute('position', self._frontfaces_buffer['positions'])
            shader.bind_attribute('color', self._frontfaces_buffer['colors'])
            shader.draw_triangles(elements=self._frontfaces_buffer['elements'], n=self._frontfaces_buffer['n'])
            shader.bind_attribute('position', self._backfaces_buffer['positions'])
            shader.bind_attribute('color', self._backfaces_buffer['colors'])
            shader.draw_triangles(elements=self._backfaces_buffer['elements'], n=self._backfaces_buffer['n'])
        shader.uniform1i('is_selected', 0)
        shader.disable_attribute('position')
        shader.disable_attribute('color')

    def draw_instance(self, shader):
        shader.enable_attribute('position')
        shader.uniform1i('is_instance_mask', 1)
        shader.uniform3f('instance_color', self.instance_color)
        if self.show_points:
            shader.bind_attribute('position', self._points_buffer['positions'])
            shader.draw_points(size=self.pointsize, elements=self._points_buffer['elements'], n=self._points_buffer['n'])
        if self.show_lines:
            shader.bind_attribute('position', self._lines_buffer['positions'])
            shader.draw_lines(width=self.linewidth, elements=self._lines_buffer['elements'], n=self._lines_buffer['n'])
        if self.show_faces:
            shader.bind_attribute('position', self._frontfaces_buffer['positions'])
            shader.draw_triangles(elements=self._frontfaces_buffer['elements'], n=self._frontfaces_buffer['n'])
            shader.bind_attribute('position', self._backfaces_buffer['positions'])
            shader.draw_triangles(elements=self._backfaces_buffer['elements'], n=self._backfaces_buffer['n'])
        shader.uniform1i('is_instance_mask', 0)
        shader.uniform3f('instance_color', [0, 0, 0])
        shader.disable_attribute('position')
