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
        point color
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

    def __init__(self, data, color=None,
                 facecolor=None, linecolor=None, pointcolor=None,
                 vertices=None, edges=None, faces=None,
                 hide_coplanaredges=False, **kwargs):
        super().__init__(data,  **kwargs)
        self._mesh = data
        self.facecolor = facecolor or color
        self.linecolor = linecolor or color
        self.pointcolor = pointcolor or color
        self.hide_coplanaredges = hide_coplanaredges
        self.vertices = vertices
        self.edges = edges
        self.faces = faces

    def _points_data(self):
        mesh = self._mesh
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}
        vertex_color = {
            vertex: self._mesh.vertex_attribute(vertex, 'color') or self.pointcolor or self.default_color_points
            for vertex in self._mesh.vertices()
        }
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
        linecolor = {
            edge: self._mesh.edge_attribute(edge, 'color') or self.linecolor or self.default_color_lines
            for edge in self._mesh.edges()
        }
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
        face_color = {
            face: self._mesh.face_attribute(face, 'color') or self.facecolor or self.default_color_faces
            for face in self._mesh.faces()
        }
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
        face_color = {
            face: self._mesh.face_attribute(face, 'color') or self.facecolor or self.default_color_faces
            for face in self._mesh.faces()
        }
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
