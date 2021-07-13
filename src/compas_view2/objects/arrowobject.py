from .bufferobject import BufferObject


class ArrowObject(BufferObject):
    """Object for displaying COMPAS arrow geometry."""

    def __init__(self, data, u=16, color=None, facecolor=None, linecolor=None, **kwargs):
        super().__init__(data, **kwargs)
        self._u = u
        self.facecolor = facecolor or color
        self.linecolor = linecolor or color
        self._vertices = None
        self._faces = None

    @property
    def vertices(self):
        if not self._vertices:
            self._data.to_vertices_and_faces(u=self._u)
            self._vertices = self._data.vertices
            self._faces = self._data.faces
        return self._vertices

    @property
    def faces(self):
        if not self._faces:
            self._data.to_vertices_and_faces(u=self._u)
            self._vertices = self._data.vertices
            self._faces = self._data.faces
        return self._faces

    @classmethod
    def from_other(cls, other, **kwargs):
        arrow = cls(other._data, **kwargs)
        arrow._vertices = other._vertices
        arrow._faces = other._faces
        return arrow

    def _points_data(self):
        color = self.pointcolor or self.default_color_points
        positions = []
        colors = []
        elements = []
        i = 0
        for vertex in self.vertices:
            positions.append(vertex)
            colors.append(color)
            elements.append([i])
            i += 1
        return positions, colors, elements

    def _frontfaces_data(self):
        color = self.facecolor or self.default_color_faces
        positions = []
        colors = []
        elements = []
        i = 0
        for face in self.faces:
            if len(face) == 3:
                positions.append(self.vertices[face[0]])
                positions.append(self.vertices[face[1]])
                positions.append(self.vertices[face[2]])
                colors.append(color)
                colors.append(color)
                colors.append(color)
                elements.append([i + 0, i + 1, i + 2])
                i += 3
            else:
                positions.append(self.vertices[face[0]])
                positions.append(self.vertices[face[1]])
                positions.append(self.vertices[face[2]])
                positions.append(self.vertices[face[0]])
                positions.append(self.vertices[face[2]])
                positions.append(self.vertices[face[3]])
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                elements.append([i + 0, i + 1, i + 2])
                elements.append([i + 3, i + 4, i + 5])
                i += 6
        return positions, colors, elements

    def _backfaces_data(self):
        color = self.facecolor or self.default_color_faces
        positions = []
        colors = []
        elements = []
        i = 0
        for face in self.faces:
            face = face[::-1]
            if len(face) == 3:
                positions.append(self.vertices[face[0]])
                positions.append(self.vertices[face[1]])
                positions.append(self.vertices[face[2]])
                colors.append(color)
                colors.append(color)
                colors.append(color)
                elements.append([i + 0, i + 1, i + 2])
                i += 3
            else:
                positions.append(self.vertices[face[0]])
                positions.append(self.vertices[face[1]])
                positions.append(self.vertices[face[2]])
                positions.append(self.vertices[face[0]])
                positions.append(self.vertices[face[2]])
                positions.append(self.vertices[face[3]])
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                elements.append([i + 0, i + 1, i + 2])
                elements.append([i + 3, i + 4, i + 5])
                i += 6
        return positions, colors, elements
