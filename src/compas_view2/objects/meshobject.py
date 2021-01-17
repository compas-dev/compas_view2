from compas.datastructures import Mesh
from compas.utilities import flatten

from ..buffers import make_index_buffer, make_vertex_buffer

from .object import Object


class MeshObject(Object):

    default_color_vertices = [0.2, 0.2, 0.2]
    default_color_edges = [0.4, 0.4, 0.4]
    default_color_front = [0.8, 0.8, 0.8]
    default_color_back = [0.8, 0.8, 0.8]

    def __init__(self, data, name=None, is_selected=False, show_vertices=False,
                 show_edges=True, show_faces=True):
        super().__init__(data, name=name, is_selected=is_selected)
        self._mesh = data
        self._vertices = None
        self._edges = None
        self._front = None
        self._back = None
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges

    @property
    def front(self):
        return self._front

    @property
    def back(self):
        return self._back

    def init(self):
        mesh = self._mesh
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}
        # vertices
        positions = []
        colors = []
        elements = []
        i = 0
        for vertex in mesh.vertices():
            positions.append(vertex_xyz[vertex])
            colors.append(self.default_color_vertices)
            elements.append(i)
            i += 1
        self._vertices = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(elements),
            'n': i
        }
        # edges
        positions = []
        colors = []
        elements = []
        i = 0
        for u, v in mesh.edges():
            positions.append(vertex_xyz[u])
            positions.append(vertex_xyz[v])
            colors.append(self.default_color_edges)
            colors.append(self.default_color_edges)
            elements.append([i + 0, i + 1])
            i += 2
        self._edges = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(list(flatten(elements))),
            'n': i
        }
        # front faces
        positions = []
        colors = []
        elements = []
        color = self.default_color_front
        i = 0
        for face in mesh.faces():
            vertices = mesh.face_vertices(face)
            if len(vertices) == 3:
                a, b, c = vertices
                positions.append(vertex_xyz[a])
                positions.append(vertex_xyz[b])
                positions.append(vertex_xyz[c])
                colors.append(color)
                colors.append(color)
                colors.append(color)
                elements.append([i + 0, i + 1, i + 2])
                i += 3
            elif len(vertices) == 4:
                a, b, c, d = vertices
                positions.append(vertex_xyz[a])
                positions.append(vertex_xyz[b])
                positions.append(vertex_xyz[c])
                positions.append(vertex_xyz[a])
                positions.append(vertex_xyz[c])
                positions.append(vertex_xyz[d])
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                elements.append([i + 0, i + 1, i + 2])
                elements.append([i + 3, i + 4, i + 5])
                i += 6
            else:
                raise NotImplementedError
        self._front = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(list(flatten(elements))),
            'n': i
        }
        # back faces
        positions = []
        colors = []
        elements = []
        color = self.default_color_back
        i = 0
        for face in mesh.faces():
            vertices = mesh.face_vertices(face)[::-1]
            if len(vertices) == 3:
                a, b, c = vertices
                positions.append(vertex_xyz[a])
                positions.append(vertex_xyz[b])
                positions.append(vertex_xyz[c])
                colors.append(color)
                colors.append(color)
                colors.append(color)
                elements.append([i + 0, i + 1, i + 2])
                i += 3
            elif len(vertices) == 4:
                a, b, c, d = vertices
                positions.append(vertex_xyz[a])
                positions.append(vertex_xyz[b])
                positions.append(vertex_xyz[c])
                positions.append(vertex_xyz[a])
                positions.append(vertex_xyz[c])
                positions.append(vertex_xyz[d])
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                elements.append([i + 0, i + 1, i + 2])
                elements.append([i + 3, i + 4, i + 5])
                i += 6
            else:
                raise NotImplementedError
        self._back = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(list(flatten(elements))),
            'n': i
        }

    def draw(self, shader):
        shader.enable_attribute('position')
        shader.enable_attribute('color')
        if self.show_faces:
            shader.uniform1i('is_selected', self.is_selected)
            # front
            shader.bind_attribute('position', self.front['positions'])
            shader.bind_attribute('color', self.front['colors'])
            shader.draw_triangles(elements=self.front['elements'], n=self.front['n'])
            # back
            shader.bind_attribute('position', self.back['positions'])
            shader.bind_attribute('color', self.back['colors'])
            shader.draw_triangles(elements=self.back['elements'], n=self.back['n'])
            # reset
            shader.uniform1i('is_selected', 0)
        if self.show_edges:
            shader.bind_attribute('position', self.edges['positions'])
            shader.bind_attribute('color', self.edges['colors'])
            shader.draw_lines(elements=self.edges['elements'], n=self.edges['n'])
        if self.show_vertices:
            shader.bind_attribute('position', self.vertices['positions'])
            shader.bind_attribute('color', self.vertices['colors'])
            shader.draw_points(size=10, elements=self.vertices['elements'], n=self.vertices['n'])
        # reset
        shader.disable_attribute('position')
        shader.disable_attribute('color')
