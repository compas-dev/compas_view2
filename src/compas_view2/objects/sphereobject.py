from compas.datastructures import Mesh
from .meshobject import MeshObject


class SphereObject(MeshObject):
    """Object for displaying COMPAS sphere geometry."""

    def __init__(self, data, u=16, v=16, **kwargs):
        super().__init__(Mesh.from_shape(data, u=u, v=v), **kwargs)
        self._u = u
        self._v = v
        self._data = data
