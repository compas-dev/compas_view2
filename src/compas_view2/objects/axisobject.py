from .bufferobject import BufferObject


class AxisObject(BufferObject):
    """Object for displaying XYZ axes at the origin of the world coordinates system."""

    x_axis_color = [1, 0, 0]
    y_axis_color = [0, 1, 0]
    z_axis_color = [0, 0, 1]

    def __init__(self, size):
        super().__init__({}, name="Axis", show_lines=True)
        self.size = size

    def init(self):
        positions = []
        colors = []

        positions.append([0, 0, 0])
        positions.append([self.size, 0, 0])
        colors.append(self.x_axis_color)
        colors.append(self.x_axis_color)

        positions.append([0, 0, 0])
        positions.append([0, self.size, 0])
        colors.append(self.y_axis_color)
        colors.append(self.y_axis_color)

        positions.append([0, 0, 0])
        positions.append([0, 0, self.size])
        colors.append(self.z_axis_color)
        colors.append(self.z_axis_color)

        elements = list(range(6))

        self._line_positions = positions
        self._line_colors = colors
        self._line_elements = elements
        self.make_buffers()
