from compas.datastructures import Mesh

from .shapeobject import ShapeObject


class SphereObject(ShapeObject):

    def __init__(self, data, *args, u=16, v=16, **kwargs):
        super().__init__(data, *args, **kwargs)
        self._u = u
        self._v = v
        self._mesh = Mesh.from_shape(data, u=u, v=v)
