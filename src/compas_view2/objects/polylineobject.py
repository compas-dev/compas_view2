from .bufferobject import BufferObject


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
        for i in range(len(polyline.points)-1):
            positions.append(list(polyline.points[i]))
            positions.append(list(polyline.points[i+1]))
            colors.append(color)
            colors.append(color)
            elements.append([i*2, i*2+1])
        return positions, colors, elements
