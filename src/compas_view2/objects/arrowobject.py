from compas.datastructures import Mesh
from compas_view2.shapes import Arrow
from .meshobject import MeshObject


class ArrowObject(MeshObject):
    """Object for displaying COMPAS arrow geometry."""

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

    @classmethod
    def create_default(cls) -> Arrow:
        return Arrow([0, 0, 0], [0, 0, 1])
