from compas.datastructures import Mesh
from .meshobject import MeshObject


class TorusObject(MeshObject):
    """Object for displaying COMPAS torus geometry."""

    def __init__(self, data, u=16, v=16, **kwargs):
        super().__init__(Mesh.from_shape(data, u=u, v=v), **kwargs)
        self.u = u
        self.v = v
        self._data = data

    def update(self):
        self._mesh = Mesh.from_shape(self._data, u=self.u, v=self.v)
        self.init()
        super().update()

    @property
    def properties(self):
        return ["u", "v"]