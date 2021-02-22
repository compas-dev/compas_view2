from compas.geometry import Shape
from compas.datastructures import Mesh
# import numpy as np

__all__ = ['Collection']


class Collection(Shape):
    """A collection of shapes
    """

    def __init__(self, shapes=[]):
        super().__init__()
        self.shapes = shapes

    def to_mesh(self, color=None, colors=None):
        colors = colors or [color or self.default_color_faces] * len(self.shapes)
        mesh = Mesh()
        for shape, color in zip(self.shapes, colors):
            v, f = shape.to_vertices_and_faces()
            m = Mesh.from_vertices_and_faces(v, f)
            for f in m.faces():
                m.face_attribute(f, 'color', color)
            mesh.join(m)
        return mesh
