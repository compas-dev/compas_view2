from .bufferobject import BufferObject


class FrameObject(BufferObject):
    """Object for displaying COMPAS Frame geometry."""

    def __init__(self, data, show_point=True, show_lines=True, size=1.0, **kwargs):
        super().__init__(data, show_points=show_point, show_lines=show_lines, **kwargs)
        self.size = size

    def _points_data(self):
        frame = self._data
        # points
        color = (0, 0, 0)
        positions = [frame.point]
        colors = [color]
        elements = [[0]]
        return positions, colors, elements

    def _lines_data(self):
        frame = self._data
        positions = [
            frame.point, frame.point + (frame.xaxis * self.size),
            frame.point, frame.point + (frame.yaxis * self.size),
            frame.point, frame.point + (frame.zaxis * self.size)]
        colors = [(1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1)]
        elements = [[0, 1], [2, 3], [4, 5]]
        return positions, colors, elements
