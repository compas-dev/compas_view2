from compas.datastructures import Mesh

from .viewmesh import ViewMesh


class ViewShape(ViewMesh):

    default_color_vertices = [0.2, 0.2, 0.2]
    default_color_edges = [0.4, 0.4, 0.4]
    default_color_front = [0.8, 0.8, 0.8]
    default_color_back = [0.8, 0.8, 0.8]

    def __init__(self, data, name=None, is_selected=False,
                 show_vertices=False, show_edges=True, show_faces=True, color=None):
        self._data = data
        self._mesh = Mesh.from_shape(data)
        self._vertices = None
        self._edges = None
        self._front = None
        self._back = None
        self.name = name
        self.is_selected = is_selected
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces
        if color:
            self.default_color_front = color
            self.default_color_back = color
