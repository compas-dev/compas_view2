from compas.datastructures import Network
from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import Pointcloud
from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Frame
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Torus
from compas.geometry import Cylinder
from compas.geometry import Plane
from compas.geometry import Circle
from compas.geometry import Ellipse
from compas.geometry import Polygon
from compas.geometry import Cone
from compas.geometry import Capsule
from compas.geometry import Polyhedron

from ..shapes import Arrow
from ..shapes import Text
from ..collections import Collection

from .object import Object

from .pointobject import PointObject
from .pointcloudobject import PointcloudObject
from .lineobject import LineObject
from .polylineobject import PolylineObject
from .frameobject import FrameObject

from .networkobject import NetworkObject
from .meshobject import MeshObject

from .boxobject import BoxObject
from .sphereobject import SphereObject
from .torusobject import TorusObject
from .arrowobject import ArrowObject
from .textobject import TextObject
from .collectionobject import CollectionObject
from .gridobject import GridObject  # noqa: F401
from .cylinderobject import CylinderObject
from .planeobject import PlaneObject
from .circleobject import CircleObject
from .ellipseobject import EllipseObject
from .polygonobject import PolygonObject
from .coneobject import ConeObject
from .capsuleobject import CapsuleObject
from .polyhedronobject import PolyhedronObject

Object.register(Point, PointObject)
Object.register(Pointcloud, PointcloudObject)
Object.register(Line, LineObject)
Object.register(Polyline, PolylineObject)
Object.register(Frame, FrameObject)

Object.register(Network, NetworkObject)
Object.register(Mesh, MeshObject)

Object.register(Box, BoxObject)
Object.register(Sphere, SphereObject)
Object.register(Torus, TorusObject)
Object.register(Arrow, ArrowObject)
Object.register(Collection, CollectionObject)
Object.register(Cylinder, CylinderObject)
Object.register(Plane, PlaneObject)
Object.register(Circle, CircleObject)
Object.register(Ellipse, EllipseObject)
Object.register(Polygon, PolygonObject)
Object.register(Cone, ConeObject)
Object.register(Capsule, CapsuleObject)
Object.register(Polyhedron, PolyhedronObject)
Object.register(Text, TextObject)

try:
    from compas_assembly.datastructures import Block
except ModuleNotFoundError:
    pass
else:
    Object.register(Block, MeshObject)
