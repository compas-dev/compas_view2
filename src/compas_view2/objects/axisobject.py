from compas.utilities import flatten

from ..buffers import make_index_buffer, make_vertex_buffer

from .object import Object


class AxisObject(Object):
    """Object for displaying XYZ axes at the origin of the world coordinates system."""

    x_axis_color = [1, 0, 0]
    y_axis_color = [0, 1, 0]
    z_axis_color = [0, 0, 1]

    def __init__(self, size):
        super().__init__({}, name="Axis")
        self.size = size

    @property
    def edges(self):
        return self._edges

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

        self._edges = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(elements),
            'n': 6
        }

    def draw(self, shader):
        shader.enable_attribute('position')
        shader.enable_attribute('color')
        shader.uniform1i('is_selected', 0)

        shader.bind_attribute('position', self.edges['positions'])
        shader.bind_attribute('color', self.edges['colors'])
        shader.draw_lines(elements=self.edges['elements'], n=self.edges['n'], width=3)

        # reset
        shader.disable_attribute('position')
        shader.disable_attribute('color')
