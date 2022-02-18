from compas.geometry import Point

from .bufferobject import BufferObject


class PointObject(BufferObject):
    """Object for displaying COMPAS point geometry."""

    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        self.show_points = True

    def _points_data(self):
        positions = [self._data]
        colors = [self.pointcolor]
        elements = [[0]]
        return positions, colors, elements

    @classmethod
    def create_default(cls) -> Point:
        return Point(0, 0, 0)
