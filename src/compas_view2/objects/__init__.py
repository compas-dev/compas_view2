from compas.datastructures import Network
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Torus

from .object import Object

from .networkobject import NetworkObject
from .meshobject import MeshObject
from .boxobject import BoxObject
from .sphereobject import SphereObject
from .torusobject import TorusObject

Object.register(Network, NetworkObject)
Object.register(Mesh, MeshObject)
Object.register(Box, BoxObject)
Object.register(Sphere, SphereObject)
Object.register(Torus, TorusObject)
