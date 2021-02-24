from compas.datastructures import Mesh


__all__ = ['Collection']


class Collection(Mesh):
    """A collection of items(inheritances of compas.datastructures.Mesh)
    """

    def __init__(self, items=None):
        super().__init__()
        self.items = items or []

    def to_mesh(self, color=None, colors=None):
        colors = colors or [color or self.default_color_faces] * len(self.items)
        mesh = Mesh()
        for item, color in zip(self.items, colors):
            v, f = item.to_vertices_and_faces()
            m = Mesh.from_vertices_and_faces(v, f)
            for f in m.faces():
                m.face_attribute(f, 'color', color)
            mesh.join(m)
        return mesh
