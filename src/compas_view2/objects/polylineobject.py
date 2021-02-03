from compas.utilities import flatten

from ..buffers import make_index_buffer, make_vertex_buffer

from .object import Object


class PolylineObject(Object):
    """Object for displaying COMPAS Polyline geometry."""

    default_color_points = [0.1, 0.1, 0.1]
    default_color_line = [0.4, 0.4, 0.4]

    def __init__(self,
                 data,
                 name=None,
                 is_selected=False,
                 show_points=False,
                 pointcolor=None,
                 pointsize=10,
                 linecolor=None,
                 linewidth=1):
        super().__init__(data, name=name, is_selected=is_selected)
        self._points = None
        self._polylines = None
        self.show_points = show_points
        self.pointcolor = pointcolor
        self.pointsize = pointsize
        self.linecolor = linecolor
        self.linewidth = linewidth

    @property
    def points(self):
        return self._points

    @property
    def polylines(self):
        return self._polylines

    def init(self):
        polyline = self._data
        # points
        color = self.pointcolor or self.default_color_points
        positions = [point for point in polyline.points]
        colors = [color for i in range(len(positions))]
        elements = [i for i in range(len(positions))]
        self._points = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(elements),
            'n': len(positions)
        }
        # lines
        color = self.linecolor or self.default_color_line
        positions = [list(polyline.points[i]) for i in range(len(polyline.points))]
        colors = list(flatten([[color, color] for i in range(len(positions))]))
        elements = [[i, i + 1] for i in range(len(positions) - 1)]
        self._polylines = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(list(flatten(elements))),
            'n': len(positions) * 2
        }

    def draw(self, shader):
        shader.enable_attribute('position')
        shader.enable_attribute('color')
        shader.uniform1i('is_selected', self.is_selected)

        if self.show_points:
            shader.bind_attribute('position', self.points['positions'])
            shader.bind_attribute('color', self.points['colors'])
            shader.draw_points(size=self.pointsize,
                               elements=self.points['elements'],
                               n=self.points['n'])
        shader.bind_attribute('position', self.polylines['positions'])
        shader.bind_attribute('color', self.polylines['colors'])
        shader.draw_lines(width=self.linewidth,
                          elements=self.polylines['elements'],
                          n=self.polylines['n'])
        shader.disable_attribute('position')
        shader.disable_attribute('color')

    def draw_instance(self, shader):
        shader.enable_attribute('position')
        shader.enable_attribute('color')

        shader.uniform1i('is_instance_mask', 1)
        shader.uniform3f('instance_color', self.instance_color)
        shader.bind_attribute('position', self.polylines['positions'])
        shader.draw_lines(width=self.linewidth, elements=self.polylines['elements'], n=self.polylines['n'])

        if self.show_points:
            shader.bind_attribute('position', self.points['positions'])
            shader.draw_points(size=self.pointsize, elements=self.points['elements'], n=self.points['n'])

        # reset
        shader.uniform1i('is_instance_mask', 0)
        shader.uniform3f('instance_color', [0, 0, 0])
        shader.disable_attribute('position')
        shader.disable_attribute('color')
