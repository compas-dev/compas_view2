from compas.datastructures import Network
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Torus

from .viewobject import ViewObject

from .viewnetwork import ViewNetwork
from .viewmesh import ViewMesh
from .viewshape import ViewShape
from .viewsphere import ViewSphere

ViewObject.register(Network, ViewNetwork)
ViewObject.register(Mesh, ViewMesh)
ViewObject.register(Box, ViewShape)
ViewObject.register(Sphere, ViewSphere)
ViewObject.register(Torus, ViewShape)
