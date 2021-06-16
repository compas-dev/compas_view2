from compas.datastructures import Mesh
from .meshobject import MeshObject


class SphereObject(MeshObject):
    """Object for displaying COMPAS sphere geometry."""

    def __init__(self, data, u=16, v=16, **kwargs):
        super().__init__(Mesh.from_shape(data, u=u, v=v), **kwargs)
        self._u = u
        self._v = v
        self._data = data

    def update(self):
        self._mesh = Mesh.from_shape(self._data, u=self._u, v=self._v)
        super().update()

    @property
    def editables(self):
        return {
            "radius": {"type": "number"}
        }