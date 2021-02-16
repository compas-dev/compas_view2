from .bufferobject import BufferObject


class LineObject(BufferObject):
    """Object for displaying COMPAS line geometry."""

    default_color_points = [0.1, 0.1, 0.1]
    default_color_lines = [0.4, 0.4, 0.4]

    def __init__(self,
                 data,
                 name=None,
                 is_selected=False,
                 show_points=False,
                 pointcolor=None,
                 pointsize=10,
                 linecolor=None,
                 linewidth=1):
        super().__init__(data, name=name, is_selected=is_selected, show_lines=True, show_points=show_points, pointsize=pointsize, linewidth=linewidth)
        self.pointcolor = pointcolor
        self.linecolor = linecolor

    def init(self):
        line = self._data
        # points
        color = self.pointcolor or self.default_color_points
        positions = [line.start, line.end]
        colors = [color, color]
        elements = [0, 1]
        self._point_positions = positions
        self._point_colors = colors
        self._point_elements = elements

        # lines
        color = self.linecolor or self.default_color_lines
        positions = [line.start, line.end]
        colors = [color, color]
        elements = [[0, 1]]
        self._line_positions = positions
        self._line_colors = colors
        self._line_elements = elements
        self.make_buffers()
