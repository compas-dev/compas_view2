from compas.utilities import flatten

from ..buffers import make_index_buffer, make_vertex_buffer

from .object import Object


class LineObject(Object):

    default_color_points = [0.1, 0.1, 0.1]
    default_color_line = [0.4, 0.4, 0.4]

    def __init__(self, data, name=None, is_selected=False, show_points=False, color_points=None, color_line=None):
        super().__init__(data, name=name, is_selected=is_selected)
        self._points = None
        self._lines = None
        self.show_points = show_points
        self.color_points = color_points
        self.color_line = color_line

    @property
    def points(self):
        return self._points

    @property
    def lines(self):
        return self._lines

    def init(self):
        line = self._data
        # nodes
        color = self.color_points or self.default_color_points
        positions = [line.start, line.end]
        colors = [color, color]
        elements = [0, 1]
        self._points = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(elements),
            'n': 2
        }
        # edges
        color = self.color_line or self.default_color_line
        colors = [color, color]
        elements = [0, 1]
        color = self.default_color_edges
        self._lines = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(elements),
            'n': 2
        }

    def draw(self, shader):
        shader.enable_attribute('position')
        shader.enable_attribute('color')
        if self.show_points:
            shader.bind_attribute('position', self.points['positions'])
            shader.bind_attribute('color', self.points['colors'])
            shader.draw_points(size=10, elements=self.points['elements'], n=self.points['n'])
        shader.bind_attribute('position', self.lines['positions'])
        shader.bind_attribute('color', self.lines['colors'])
        shader.draw_lines(elements=self.lines['elements'], n=self.lines['n'])
        shader.disable_attribute('position')
        shader.disable_attribute('color')
