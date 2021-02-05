from compas.datastructures import Mesh

from .meshobject import MeshObject


class ShapeObject(MeshObject):
    """Base object for all COMPAS shapes."""

    def __init__(self, data, *args, **kwargs):
        super().__init__(Mesh.from_shape(data), *args, **kwargs)
        self._data = data
