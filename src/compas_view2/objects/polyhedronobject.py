from compas.datastructures import Mesh
from .meshobject import MeshObject


class PolyhedronObject(MeshObject):
    """Object for displaying COMPAS Polyhedron geometry."""

    def __init__(self, data, **kwargs):
        super().__init__(Mesh.from_shape(data), **kwargs)
        self._data = data
