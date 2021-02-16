from .bufferobject import BufferObject
from compas.utilities import flatten


class PolylineObject(BufferObject):
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
        super().__init__(data, name=name, show_lines=True, is_selected=is_selected, show_points=show_points, linewidth=linewidth, pointsize=pointsize)
        self.pointcolor = pointcolor
        self.linecolor = linecolor

    def init(self):
        polyline = self._data
        # points
        color = self.pointcolor or self.default_color_points
        positions = [point for point in polyline.points]
        colors = [color for i in range(len(positions))]
        elements = [i for i in range(len(positions))]
        self._point_positions = positions
        self._point_colors = colors
        self._point_elements = elements
        # lines
        color = self.linecolor or self.default_color_line
        positions = [list(polyline.points[i]) for i in range(len(polyline.points))]
        colors = list(flatten([[color, color] for i in range(len(positions))]))
        elements = [[i, i + 1] for i in range(len(positions) - 1)]
        self._line_positions = positions
        self._line_colors = colors
        self._line_elements = elements
        self.make_buffers()
