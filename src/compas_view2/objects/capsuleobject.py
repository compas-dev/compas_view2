from compas.datastructures import Mesh
from .meshobject import MeshObject


class CapsuleObject(MeshObject):
    """Object for displaying COMPAS Capsule geometry."""

    def __init__(self, data, u=10, v=10, **kwargs):
        super().__init__(Mesh.from_shape(data, u=u, v=v), **kwargs)
        self._u = u
        self._v = v
        self._data = data
