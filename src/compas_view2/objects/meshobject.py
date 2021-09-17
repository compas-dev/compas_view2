from compas.utilities import pairwise
from compas.geometry import is_coplanar, centroid_points

from .bufferobject import BufferObject


class MeshObject(BufferObject):
    """Object for displaying COMPAS mesh data structures.

    Parameters
    ----------
    data : :class: `compas.datastructures.Mesh`
        Mesh for the viewer
    vertices : list
        Subset of vertices to be displayed
    edges : list
        Subset of edges to be displayed
    faces : list
        Subset of faces to be displayed
    hide_coplanaredges : bool
        True to hide the coplanar edges

    Parameters[kwargs]
    ------------------
    name : string
        Name of the object.
    is_selected : bool
        Whether the object is selected.
    is_visible : bool
        Whether the object is visible.
    show_vertices : bool
        True to show vertices/points.
    show_points : bool
        True to show vertices/points.
    show_edges : bool
        True to show edges/lines.
    show_lines : bool
        True to show edges/lines.
    show_faces : bool
        True to show faces.
    color : list
        Color all points lines and faces.
    pointcolor : list
        Color for all points.
    linecolor : list
        Color for all lines.
    facecolor : list
        Color for all faces.
    pointcolors : list
        List of colors for each points.
    linecolors : list
        List of colors for each lines.
    facecolors : list
        List of colors for each faces.
    linewidth : float
        The line width to be drawn on screen.
    pointsize : float
        The line width to be drawn on screen.
    opacity : float
        The point size to be drawn on screen.

    Attributes
    ----------
    hide_coplanaredges : bool
        True to hide the coplanar edges
    vertices : list
        Subset of vertices to be displayed
    edges : list
        Subset of edges to be displayed
    faces : list
        Subset of faces to be displayed

    """

    def __init__(self, data, vertices=None, edges=None, faces=None,
                 hide_coplanaredges=False, **kwargs):
        super().__init__(data,  **kwargs)
        self._mesh = data
        self.hide_coplanaredges = hide_coplanaredges
        self.vertices = vertices
        self.edges = edges
        self.faces = faces

    def _points_data(self):
        mesh = self._mesh
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}
        positions = []
        colors = []
        elements = []
        i = 0
        vertices = self.vertices or mesh.vertices()
        for vertex in vertices:
            positions.append(vertex_xyz[vertex])
            colors.append(self.pointcolors.get(vertex, self.pointcolor))
            elements.append([i])
            i += 1
        return positions, colors, elements

    def _lines_data(self):
        mesh = self._mesh
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}
        positions = []
        colors = []
        elements = []
        i = 0
        edges = self.edges or mesh.edges()
        for u, v in edges:
            color = self.linecolors.get((u, v), self.linecolor)
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
        positions = []
        colors = []
        elements = []
        i = 0
        faces = self.faces or mesh.faces()
        for face in faces:
            vertices = mesh.face_vertices(face)
            color = self.facecolors.get(face, self.facecolor)
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
        positions = []
        colors = []
        elements = []
        i = 0
        faces = self.faces or mesh.faces()
        for face in faces:
            vertices = mesh.face_vertices(face)[::-1]
            color = self.facecolors.get(face, self.facecolor)
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
