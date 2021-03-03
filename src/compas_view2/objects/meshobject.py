from compas.utilities import pairwise
from compas.geometry import is_coplanar, centroid_points

from .bufferobject import BufferObject


class MeshObject(BufferObject):
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
    opacity : float
        The opacity of mesh
    vertices : list
        Subset of vertices to be displayed
    edges : list
        Subset of edges to be displayed
    faces : list
        Subset of faces to be displayed

    Attributes
    ----------
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
    opacity : float
        The opacity of mesh
    vertices : list
        Subset of vertices to be displayed
    edges : list
        Subset of edges to be displayed
    faces : list
        Subset of faces to be displayed

    """

    default_color_points = [0.2, 0.2, 0.2]
    default_color_lines = [0.4, 0.4, 0.4]
    default_color_faces = [0.8, 0.8, 0.8]

    def __init__(self, data, name=None, is_selected=False,
                 show_vertices=False, show_edges=True, show_faces=True,
                 facecolor=None, linecolor=None, pointcolor=None,
                 color=None,
                 linewidth=1, pointsize=10,
                 hide_coplanaredges=False, opacity=1,
                 vertices=None, edges=None, faces=None):
        super().__init__(
            data, name=name, is_selected=is_selected, show_points=show_vertices,
            show_lines=show_edges, show_faces=show_faces, linewidth=linewidth,
            pointsize=pointsize, opacity=opacity)
        self._mesh = data
        self._pointcolor = None
        self._linecolor = None
        self._facecolor = None
        self.facecolor = color or facecolor
        self.linecolor = color or linecolor
        self.pointcolor = color or pointcolor
        self.hide_coplanaredges = hide_coplanaredges
        self.vertices = vertices
        self.edges = edges
        self.faces = faces

    @property
    def pointcolor(self):
        if not self._pointcolor:
            self._pointcolor = {vertex: self._mesh.vertex_attribute(vertex, 'color') or self.default_color_points for vertex in self._mesh.vertices()}
        return self._pointcolor

    @pointcolor.setter
    def pointcolor(self, color):
        if color:
            if isinstance(color, dict):
                self.pointcolor.update(color)
            else:
                pointcolor = self.pointcolor
                color = color or self.default_color_points
                for vertex in pointcolor:
                    pointcolor[vertex] = color

    @property
    def linecolor(self):
        if not self._linecolor:
            self._linecolor = {edge: self._mesh.edge_attribute(edge, 'color') or self.default_color_lines for edge in self._mesh.edges()}
        return self._linecolor

    @linecolor.setter
    def linecolor(self, color):
        if color:
            if isinstance(color, dict):
                self.linecolor.update(color)
            else:
                linecolor = self.linecolor
                color = color or self.default_color_lines
                for edge in linecolor:
                    linecolor[edge] = color

    @property
    def facecolor(self):
        if not self._facecolor:
            self._facecolor = {face: self._mesh.face_attribute(face, 'color') or self.default_color_faces for face in self._mesh.faces()}
        return self._facecolor

    @facecolor.setter
    def facecolor(self, color):
        if color:
            if isinstance(color, dict):
                self.facecolor.update(color)
            else:
                facecolor = self.facecolor
                color = color or self.default_color_faces
                for face in facecolor:
                    facecolor[face] = color

    def _points_data(self):
        mesh = self._mesh
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}
        vertex_color = self.pointcolor
        positions = []
        colors = []
        elements = []
        i = 0
        vertices = self.vertices or mesh.vertices()
        for vertex in vertices:
            positions.append(vertex_xyz[vertex])
            colors.append(vertex_color[vertex])
            elements.append([i])
            i += 1
        return positions, colors, elements

    def _lines_data(self):
        mesh = self._mesh
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}
        linecolor = self.linecolor
        positions = []
        colors = []
        elements = []
        i = 0
        edges = self.edges or mesh.edges()
        for u, v in edges:
            color = linecolor[u, v]
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
        return positions, colors, elements

    def _frontfaces_data(self):
        mesh = self._mesh
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}
        face_color = self.facecolor
        positions = []
        colors = []
        elements = []
        i = 0
        faces = self.faces or mesh.faces()
        for face in faces:
            color = face_color[face]
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
                points = [vertex_xyz[vertex] for vertex in vertices]
                c = centroid_points(points)
                for a, b in pairwise(points + points[:1]):
                    positions.append(a)
                    positions.append(b)
                    positions.append(c)
                    colors.append(color)
                    colors.append(color)
                    colors.append(color)
                    elements.append([i + 0, i + 1, i + 2])
                    i += 3

        return positions, colors, elements

    def _backfaces_data(self):
        mesh = self._mesh
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}
        face_color = self.facecolor
        positions = []
        colors = []
        elements = []
        i = 0
        faces = self.faces or mesh.faces()
        for face in faces:
            color = face_color[face]
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
                points = [vertex_xyz[vertex] for vertex in vertices]
                c = centroid_points(points)
                for a, b in pairwise(points + points[:1]):
                    positions.append(a)
                    positions.append(b)
                    positions.append(c)
                    colors.append(color)
                    colors.append(color)
                    colors.append(color)
                    elements.append([i + 0, i + 1, i + 2])
                    i += 3
        return positions, colors, elements
