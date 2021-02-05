from compas.datastructures import Mesh
from .shapeobject import ShapeObject


class ArrowObject(ShapeObject):
    """Object for displaying COMPAS arrow geometry."""

    def __init__(self, data, *args, u=16, **kwargs):
        super().__init__(data, *args, **kwargs)
        self._u = u
        self._mesh = Mesh.from_shape(data, u=u)
