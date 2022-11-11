from compas.utilities import pairwise
from .bufferobject import BufferObject


class PolylineObject(BufferObject):
    """Object for displaying COMPAS Polyline geometry."""

    def __init__(self, data, close=False, **kwargs):
        super().__init__(data, **kwargs)
        self.close = close
        self.show_lines = True

    def _points_data(self):
        polyline = self._data
        positions = [point for point in polyline.points]
        colors = [self.pointcolors.get(i, self.pointcolor) for i, _ in enumerate(polyline.points)]
        elements = [[i] for i in range(len(positions))]
        return positions, colors, elements

    def _lines_data(self):
        polyline = self._data
        positions = []
        colors = []
        elements = []
        if self.close:
            lines = pairwise(polyline.points + [polyline.points[0]])
        else:
            lines = pairwise(polyline.points)
        count = 0
        for i, (pt1, pt2) in enumerate(lines):
            positions.append(pt1)
            positions.append(pt2)
            color = self.linecolors.get(i, self.linecolor)
            colors.append(color)
            colors.append(color)
            elements.append([count, count + 1])
            count += 2
        return positions, colors, elements
