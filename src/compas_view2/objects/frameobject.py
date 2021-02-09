from compas.utilities import flatten

from ..buffers import make_index_buffer, make_vertex_buffer
from .object import Object


class FrameObject(Object):
    """Object for displaying COMPAS line geometry."""

    def __init__(self,
                 data,
                 name=None,
                 is_selected=False,
                 show_point=True,
                 pointsize=10,
                 linewidth=1):
        super().__init__(data, name=name, is_selected=is_selected)
        self._points = None
        self._lines = None
        self.show_point = show_point
        self.pointsize = pointsize
        self.linewidth = linewidth

    @property
    def points(self):
        return self._points

    @property
    def lines(self):
        return self._lines

    def init(self):
        frame = self._data
        # points
        color = (0, 0, 0)
        positions = [frame.point]
        colors = [color]
        elements = [0]
        self._points = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(elements),
            'n': 1
        }
        # lines
        color = (1, 0, 0)
        positions = [
            frame.point, frame.point + frame.xaxis,
            frame.point, frame.point + frame.yaxis,
            frame.point, frame.point + frame.zaxis]
        colors = [(1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1)]
        elements = [0, 1, 2, 3, 3, 4]
        self._lines = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(elements),
            'n': 6
        }

    def draw(self, shader):
        shader.enable_attribute('position')
        shader.enable_attribute('color')
        shader.uniform1i('is_selected', self.is_selected)
        if self.show_point:
            shader.bind_attribute('position', self.points['positions'])
            shader.bind_attribute('color', self.points['colors'])
            shader.draw_points(size=self.pointsize, elements=self.points['elements'], n=self.points['n'])
        shader.bind_attribute('position', self.lines['positions'])
        shader.bind_attribute('color', self.lines['colors'])
        shader.draw_lines(width=self.linewidth, elements=self.lines['elements'], n=self.lines['n'])
        shader.uniform1i('is_selected', 0)
        shader.disable_attribute('position')
        shader.disable_attribute('color')

    def draw_instance(self, shader):
        shader.enable_attribute('position')
        shader.enable_attribute('color')
        shader.uniform1i('is_instance_mask', 1)
        shader.uniform3f('instance_color', self.instance_color)
        shader.bind_attribute('position', self.lines['positions'])
        shader.draw_lines(width=self.linewidth, elements=self.lines['elements'], n=self.lines['n'])
        if self.show_point:
            shader.bind_attribute('position', self.points['positions'])
            shader.draw_points(size=self.pointsize, elements=self.points['elements'], n=self.points['n'])
        shader.uniform1i('is_instance_mask', 0)
        shader.uniform3f('instance_color', [0, 0, 0])
        shader.disable_attribute('position')
        shader.disable_attribute('color')
