from compas.utilities import flatten
from compas.geometry import is_coplanar

from ..buffers import make_index_buffer, make_vertex_buffer

from .object import Object


class MeshObject(Object):
    """Object for displaying COMPAS mesh data structures.

    Parameters
    ----------
    data : :class: `compas.datastructures.Mesh`
        Mesh for the viewer
    name : string
        name of the object
    show_vertices : bool
        True to show vertices
    show_edges : bool
        True to show edges
    show_faces : bool
        True to show faces
    facecolor : list
        Face color
    linecolor : list
        Line color
    pointcolor : list
        Face color
    linewidth : float
        Line width
    pointsize : float
        Point size
    hide_coplanaredges : bool
        True to hide the coplanar edges

    Attributes
    ----------
    vertices : list
        list of mesh vertices
    edges : list of tuple
        list of mesh edges in tuple
    front : dict
        mesh front face information for the viewer
    back : dict
        mesh back face information for the viewer

    """

    default_color_vertices = [0.2, 0.2, 0.2]
    default_color_edges = [0.4, 0.4, 0.4]
    default_color_front = [0.8, 0.8, 0.8]
    default_color_back = [0.8, 0.8, 0.8]

    def __init__(self, data, name=None, is_selected=False,
                 show_vertices=False, show_edges=True, show_faces=True,
                 facecolor=None, linecolor=None, pointcolor=None,
                 linewidth=1, pointsize=10,
                 hide_coplanaredges=False):
        super().__init__(data, name=name, is_selected=is_selected)
        self._mesh = data
        self._vertices = None
        self._edges = None
        self._front = None
        self._back = None
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces
        self.facecolor = facecolor
        self.linecolor = linecolor
        self.pointcolor = pointcolor
        self.linewidth = linewidth
        self.pointsize = pointsize
        self.hide_coplanaredges = hide_coplanaredges

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
        color = self.pointcolor or self.default_color_vertices
        i = 0
        for vertex in mesh.vertices():
            positions.append(vertex_xyz[vertex])
            colors.append(color)
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
        color = self.linecolor or self.default_color_edges
        i = 0
        for u, v in mesh.edges():

            if self.hide_coplanaredges:
                # hide the edge if neighbor faces are coplanar
                fkeys = mesh.edge_faces(u, v)
                if not mesh.is_edge_on_boundary(u, v):
                    ps = [mesh.face_center(fkeys[0]),
                          mesh.face_center(fkeys[1]),
                          *mesh.edge_coordinates(u, v)]
                    if is_coplanar(ps, tol=1e-5):
                        continue

            positions.append(vertex_xyz[u])
            positions.append(vertex_xyz[v])
            colors.append(color)
            colors.append(color)
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
        color = self.facecolor or self.default_color_front
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
        color = self.facecolor or self.default_color_back
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
            shader.draw_lines(width=self.linewidth, elements=self.edges['elements'], n=self.edges['n'])
        if self.show_vertices:
            shader.bind_attribute('position', self.vertices['positions'])
            shader.bind_attribute('color', self.vertices['colors'])
            shader.draw_points(size=self.pointsize, elements=self.vertices['elements'], n=self.vertices['n'])
        # reset
        shader.disable_attribute('position')
        shader.disable_attribute('color')

    def draw_instance(self, shader):
        shader.enable_attribute('position')
        shader.enable_attribute('color')
        shader.uniform1i('is_instance_mask', 1)
        shader.uniform3f('instance_color', self.instance_color)
        # front
        shader.bind_attribute('position', self.front['positions'])
        shader.draw_triangles(elements=self.front['elements'], n=self.front['n'])
        # back
        shader.bind_attribute('position', self.back['positions'])
        shader.draw_triangles(elements=self.back['elements'], n=self.back['n'])
        # reset
        shader.uniform1i('is_instance_mask', 0)
        shader.uniform3f('instance_color', [0, 0, 0])
        shader.disable_attribute('position')
        shader.disable_attribute('color')
