from .bufferobject import BufferObject


class LineObject(BufferObject):
    """Object for displaying COMPAS line geometry."""

    default_color_points = [0.1, 0.1, 0.1]
    default_color_lines = [0.4, 0.4, 0.4]

    def __init__(self, data, show_lines=True, pointcolor=None, linecolor=None, color=None, **kwargs):
        super().__init__(data, show_lines=show_lines, **kwargs)
        self.pointcolor = pointcolor or color
        self.linecolor = linecolor or color

    def _points_data(self):
        line = self._data
        color = self.pointcolor or self.default_color_points
        positions = [line.start, line.end]
        colors = [color, color]
        elements = [[0], [1]]
        return positions, colors, elements

    def _lines_data(self):
        line = self._data
        color = self.linecolor or self.default_color_lines
        positions = [line.start, line.end]
        colors = [color, color]
        elements = [[0, 1]]
        return positions, colors, elements
