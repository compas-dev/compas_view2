from compas.datastructures import Mesh
from .meshobject import MeshObject


class ConeObject(MeshObject):
    """Object for displaying COMPAS cone geometry."""

    def __init__(self, data, u=16, **kwargs):
        super().__init__(Mesh.from_shape(data, u=u), **kwargs)
        self.u = u
        self._data = data

    def update(self):
        self._mesh = Mesh.from_shape(self._data, u=self.u)
        self.init()
        super().update()

    @property
    def properties(self):
        return ["u"]
