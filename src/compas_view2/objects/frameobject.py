from .bufferobject import BufferObject


class FrameObject(BufferObject):
    """Object for displaying COMPAS line geometry."""

    def __init__(self,
                 data,
                 name=None,
                 is_selected=False,
                 show_point=True,
                 pointsize=10,
                 linewidth=1):
        super().__init__(data, name=name, is_selected=is_selected, show_points=show_point, show_lines=True, pointsize=pointsize, linewidth=linewidth)

    def init(self):
        frame = self._data
        # points
        color = (0, 0, 0)
        positions = [frame.point]
        colors = [color]
        elements = [0]
        self._point_positions = positions
        self._point_colors = colors
        self._point_elements = elements
        # lines
        color = (1, 0, 0)
        positions = [
            frame.point, frame.point + frame.xaxis,
            frame.point, frame.point + frame.yaxis,
            frame.point, frame.point + frame.zaxis]
        colors = [(1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1)]
        elements = [[0, 1], [2, 3], [4, 5]]
        self._line_positions = positions
        self._line_colors = colors
        self._line_elements = elements
        self.make_buffers()
