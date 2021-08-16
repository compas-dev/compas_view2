from compas.utilities.itertools import flatten
from .meshobject import MeshObject


class NurbsSurfaceObject(MeshObject):
    """Object for displaying COMPAS NurbsSurface geometry."""

    def __init__(self, surface, u=10, v=10, show_edges=False, **kwargs):
        self.u = u
        self.v = v
        self._mesh = surface.to_mesh(u=self.u, v=self.v)
        super().__init__(self._mesh, show_edges=show_edges, **kwargs)
        self._data = surface

    def update(self):
        self._mesh = self._data.to_mesh(u=self.u, v=self.v)
        self.init()
        super().update()

    def _points_data(self):
        positions = [list(pt) for pt in flatten(self._data.points)]
        colors = [self.pointcolor or self.default_color_points for _ in positions]
        elements = [[i] for i in range(len(positions))]
        return positions, colors, elements

    def _lines_data(self):
        positions = [list(pt) for pt in flatten(self._data.points)]
        colors = [self.linecolor or self.default_color_lines for _ in positions]
        count = 0
        indexes = []
        for row in self._data.points:
            row_i = []
            for _ in range(len(row)):
                row_i.append(count)
                count += 1
            indexes.append(row_i)
        elements = []
        for row in indexes:
            for i in range(len(row) - 1):
                elements.append([row[i], row[i + 1]])
        for col in zip(*indexes):
            for i in range(len(col) - 1):
                elements.append([col[i], col[i + 1]])
        return positions, colors, elements

    @property
    def properties(self):
        return ["u", "v"]
