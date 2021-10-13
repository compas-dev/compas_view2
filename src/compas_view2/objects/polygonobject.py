from compas.geometry import centroid_points
from compas.utilities import pairwise
from .polylineobject import PolylineObject


class PolygonObject(PolylineObject):
    """Object for displaying COMPAS Polygon geometry."""

    def __init__(self, polygon, show_face=True, facecolor=None, **kwargs):
        super().__init__(polygon, close=True, facecolor=facecolor, **kwargs)
        self.show_face = show_face

    def _frontfaces_data(self):
        if not self.show_face:
            return
        positions = []
        colors = []
        elements = []
        points = self._data.points
        color = self.facecolor
        if len(points) == 3:
            a, b, c = points
            positions.append(a)
            positions.append(b)
            positions.append(c)
            colors.append(color)
            colors.append(color)
            colors.append(color)
            elements.append([0, 1, 2])
        elif len(points) == 4:
            a, b, c, d = points
            positions.append(a)
            positions.append(b)
            positions.append(c)
            positions.append(a)
            positions.append(c)
            positions.append(d)
            colors.append(color)
            colors.append(color)
            colors.append(color)
            colors.append(color)
            colors.append(color)
            colors.append(color)
            elements.append([0, 1, 2])
            elements.append([3, 4, 5])
        else:
            c = centroid_points(points)
            i = 0
            for a, b in pairwise(points + points[:1]):
                positions.append(a)
                positions.append(b)
                positions.append(c)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                elements.append([i + 0, i + 1, i + 2])
                i += 3
        return positions, colors, elements

    def _backfaces_data(self):
        if not self.show_face:
            return
        positions = []
        colors = []
        elements = []
        points = self._data.points[::-1]
        color = self.facecolor
        if len(points) == 3:
            a, b, c = points
            positions.append(a)
            positions.append(b)
            positions.append(c)
            colors.append(color)
            colors.append(color)
            colors.append(color)
            elements.append([0, 1, 2])
        elif len(points) == 4:
            a, b, c, d = points
            positions.append(a)
            positions.append(b)
            positions.append(c)
            positions.append(a)
            positions.append(c)
            positions.append(d)
            colors.append(color)
            colors.append(color)
            colors.append(color)
            colors.append(color)
            colors.append(color)
            colors.append(color)
            elements.append([0, 1, 2])
            elements.append([3, 4, 5])
        else:
            c = centroid_points(points)
            i = 0
            for a, b in pairwise(points + points[:1]):
                positions.append(a)
                positions.append(b)
                positions.append(c)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                elements.append([i + 0, i + 1, i + 2])
                i += 3
        return positions, colors, elements
