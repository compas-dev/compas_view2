from compas.geometry import Line
from .bufferobject import BufferObject


class LineObject(BufferObject):
    """Object for displaying COMPAS line geometry."""

    default_color_points = [0.1, 0.1, 0.1]
    default_color_lines = [0.4, 0.4, 0.4]

    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        self.show_lines = True

    def _points_data(self):
        line = self._data
        color = self.pointcolor
        positions = [line.start, line.end]
        colors = [color, color]
        elements = [[0], [1]]
        return positions, colors, elements

    def _lines_data(self):
        line = self._data
        color = self.linecolor
        positions = [line.start, line.end]
        colors = [color, color]
        elements = [[0, 1]]
        return positions, colors, elements

    @classmethod
    def create_default(cls) -> Line:
        return Line([0, 0, 0], [0, 0, 1])
