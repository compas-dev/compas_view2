from compas.datastructures import Network
from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Torus

from ..shapes import Arrow
from .object import Object

from .pointobject import PointObject
from .lineobject import LineObject
from .polylineobject import PolylineObject

from .networkobject import NetworkObject
from .meshobject import MeshObject

from .boxobject import BoxObject
from .sphereobject import SphereObject
from .torusobject import TorusObject
from .arrowobject import ArrowObject
from .gridobject import GridObject  # noqa: F401
from .axisobject import AxisObject  # noqa: F401

Object.register(Point, PointObject)
Object.register(Line, LineObject)
Object.register(Polyline, PolylineObject)

Object.register(Network, NetworkObject)
Object.register(Mesh, MeshObject)

Object.register(Box, BoxObject)
Object.register(Sphere, SphereObject)
Object.register(Torus, TorusObject)
Object.register(Arrow, ArrowObject)

try:
    from compas_assembly.datastructures import Block
except ModuleNotFoundError:
    pass
else:
    Object.register(Block, MeshObject)
