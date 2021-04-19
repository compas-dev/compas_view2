from .bufferobject import BufferObject


class PolylineObject(BufferObject):
    """Object for displaying COMPAS Polyline geometry."""

    default_color_points = [0.1, 0.1, 0.1]
    default_color_line = [0.4, 0.4, 0.4]

    def __init__(self, data, closed=False, pointcolor=None, linecolor=None, color=None, **kwargs):
        super().__init__(data, show_lines=True, **kwargs)
        self.pointcolor = pointcolor or color
        self.linecolor = linecolor or color
        self.closed = closed

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
        if self.closed:
            indexes = range(len(polyline.points))
        else:
            indexes = range(len(polyline.points)-1)
        for i in indexes:
            positions.append(list(polyline.points[i]))
            positions.append(list(polyline.points[(i+1) % len(polyline.points)]))
            colors.append(color)
            colors.append(color)
            elements.append([i*2, i*2+1])
        return positions, colors, elements
