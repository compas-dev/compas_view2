from compas.utilities import flatten

from ..buffers import make_index_buffer, make_vertex_buffer

from .object import Object


class GridObject(Object):
    """Object for displaying a grid of lines in the XY plane of the world coordinate system."""

    default_color_edges = [0.75, 0.75, 0.75]

    def __init__(self, cell_size, x_cells, y_cells):
        super().__init__({}, name="Grid")
        self.cell_size = cell_size
        self.x_cells = x_cells
        self.y_cells = y_cells

    @property
    def edges(self):
        return self._edges

    def init(self):
        positions = []
        colors = []
        elements = []
        color = self.default_color_edges
        n = 0

        for x in range(- self.x_cells, self.x_cells + 1):
            if x == 0:
                positions.append([x * self.cell_size, -self.x_cells * self.cell_size, 0])
                positions.append([x * self.cell_size, 0, 0])
                colors.append(color)
                colors.append(color)
                positions.append([x * self.cell_size, 0, 0])
                positions.append([x * self.cell_size, self.x_cells * self.cell_size, 0])
                colors.append([0, 1, 0])
                colors.append([0, 1, 0])
                n = len(elements)
                elements.extend([n + 0, n + 1])
                elements.extend([n + 2, n + 3])
            else:
                positions.append([x * self.cell_size, -self.x_cells * self.cell_size, 0])
                positions.append([x * self.cell_size, self.x_cells * self.cell_size, 0])
                colors.append(color)
                colors.append(color)
                n = len(elements)
                elements.extend([n, n + 1])

        for y in range(- self.y_cells, self.y_cells + 1):
            if y == 0:
                positions.append([-self.y_cells * self.cell_size, y * self.cell_size, 0])
                positions.append([0, y * self.cell_size, 0])
                colors.append(color)
                colors.append(color)
                positions.append([0, y * self.cell_size, 0])
                positions.append([self.y_cells * self.cell_size, y * self.cell_size, 0])
                colors.append([1, 0, 0])
                colors.append([1, 0, 0])
                n = len(elements)
                elements.extend([n + 0, n + 1])
                elements.extend([n + 2, n + 3])
            else:
                positions.append([-self.y_cells * self.cell_size, y * self.cell_size, 0])
                positions.append([self.y_cells * self.cell_size, y * self.cell_size, 0])
                colors.append(color)
                colors.append(color)
                n = len(elements)
                elements.extend([n, n + 1])

        make_vertex_buffer(list(flatten(positions)))

        self._edges = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(elements),
            'n': len(elements)
        }

        x_size = self.x_cells * self.cell_size
        y_size = self.y_cells * self.cell_size
        positions = [[-x_size, -y_size, 0], [x_size, -y_size, 0], [x_size, y_size, 0], [-x_size, y_size, 0]]
        color = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
        elements = [[0, 1, 3], [1, 2, 3], [1, 0, 3], [2, 1, 3]]

        self._uvplane = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(color))),
            'elements': make_index_buffer(list(flatten(elements))),
            'n': len(list(flatten(elements))),
        }

    def draw(self, shader):
        shader.enable_attribute('position')
        shader.enable_attribute('color')
        shader.uniform1i('is_selected', 0)

        shader.bind_attribute('position', self.edges['positions'])
        shader.bind_attribute('color', self.edges['colors'])
        shader.draw_lines(elements=self.edges['elements'], n=self.edges['n'], background=True)

        # reset
        shader.disable_attribute('position')
        shader.disable_attribute('color')

    def draw_plane(self, shader):
        shader.enable_attribute('position')
        shader.enable_attribute('color')

        shader.bind_attribute('position', self._uvplane['positions'])
        shader.bind_attribute('color', self._uvplane['colors'])
        shader.draw_triangles(elements=self._uvplane['elements'], n=self._uvplane['n'])

        shader.disable_attribute('position')
        shader.disable_attribute('color')
