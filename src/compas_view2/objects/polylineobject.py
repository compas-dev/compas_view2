from .bufferobject import BufferObject
from compas.utilities import pairwise


class PolylineObject(BufferObject):
    """Object for displaying COMPAS Polyline geometry."""

    default_color_points = [0.1, 0.1, 0.1]
    default_color_line = [0.4, 0.4, 0.4]

    def __init__(self, data, close=False, pointcolor=None, linecolor=None, color=None, **kwargs):
        super().__init__(data, show_lines=True, **kwargs)
        self.pointcolor = pointcolor or color
        self.linecolor = linecolor or color
        self.close = close

    def _points_data(self):
        polyline = self._data
        color = self.pointcolor or self.default_color_points
        positions = [point for point in polyline.points]
        colors = [color for i in range(len(positions))]
        elements = [[i] for i in range(len(positions))]
        return positions, colors, elements

    def _lines_data(self):
        polyline = self._data
        color = self.linecolor or self.default_color_line
        positions = []
        colors = []
        elements = []
        if self.close:
            lines = pairwise(polyline.points + [polyline.points[0]])
        else:
            lines = pairwise(polyline.points)
        count = 0
        for pt1, pt2 in lines:
            positions.append(pt1)
            positions.append(pt2)
            colors.append(color)
            colors.append(color)
            elements.append([count, count+1])
            count += 2
        return positions, colors, elements
