from compas.datastructures import Mesh
from .meshobject import MeshObject


class CylinderObject(MeshObject):
    """Object for displaying COMPAS cylinder geometry."""

    def __init__(self, data, u=16, **kwargs):
        super().__init__(Mesh.from_shape(data, u=u), **kwargs)
        self._u = u
        self._data = data
