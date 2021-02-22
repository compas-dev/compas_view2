from .bufferobject import BufferObject


class FrameObject(BufferObject):
    """Object for displaying COMPAS Frame geometry."""

    def __init__(self,
                 data,
                 name=None,
                 is_selected=False,
                 show_point=True,
                 pointsize=10,
                 linewidth=1):
        super().__init__(data, name=name, is_selected=is_selected, show_points=show_point, show_lines=True, pointsize=pointsize, linewidth=linewidth)

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
            frame.point, frame.point + frame.xaxis,
            frame.point, frame.point + frame.yaxis,
            frame.point, frame.point + frame.zaxis]
        colors = [(1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1)]
        elements = [[0, 1], [2, 3], [4, 5]]
        return positions, colors, elements
