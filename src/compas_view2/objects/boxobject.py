from compas.datastructures import Mesh
from .meshobject import MeshObject


class BoxObject(MeshObject):
    """Object for displaying COMPAS box geometry."""

    def __init__(self, data, **kwargs):
        super().__init__(Mesh.from_shape(data), **kwargs)
        self._data = data
