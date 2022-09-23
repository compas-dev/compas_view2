from compas.datastructures import Network
from compas.datastructures import Mesh
from compas.geometry import Vector
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
from compas.geometry import NurbsSurface
from compas.robots import RobotModel

from compas_view2.shapes import Arrow
from compas_view2.shapes import Text
from compas_view2.collections import Collection

from .object import Object
from .bufferobject import BufferObject  # noqa : F401

from .vectorobject import VectorObject
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
from .gridobject import GridObject  # noqa : F401
from .cylinderobject import CylinderObject
from .planeobject import PlaneObject
from .circleobject import CircleObject
from .ellipseobject import EllipseObject
from .polygonobject import PolygonObject
from .coneobject import ConeObject
from .capsuleobject import CapsuleObject
from .polyhedronobject import PolyhedronObject

from .nurbssurfaceobject import NurbsSurfaceObject
from .robotobject import RobotObject

try:
    from compas_occ.brep import BRep
    from .brepobject import BRepObject
except ImportError:
    BRep = None
    BRepObject = None

from .object import DATA_OBJECT  # noqa : F401

Object.register(Point, PointObject)
Object.register(Vector, VectorObject)
Object.register(Plane, PlaneObject)
Object.register(Frame, FrameObject)

Object.register(Pointcloud, PointcloudObject)

Object.register(Line, LineObject)
Object.register(Polyline, PolylineObject)

Object.register(Circle, CircleObject)
Object.register(Ellipse, EllipseObject)
Object.register(Polygon, PolygonObject)

Object.register(Box, BoxObject)
Object.register(Sphere, SphereObject)
Object.register(Torus, TorusObject)
Object.register(Cylinder, CylinderObject)
Object.register(Cone, ConeObject)
Object.register(Capsule, CapsuleObject)
Object.register(Polyhedron, PolyhedronObject)

Object.register(Arrow, ArrowObject)
Object.register(Text, TextObject)

Object.register(NurbsSurface, NurbsSurfaceObject)

Object.register(Network, NetworkObject)
Object.register(Mesh, MeshObject)

Object.register(Collection, CollectionObject)
Object.register(RobotModel, RobotObject)

if BRep and BRepObject:
    Object.register(BRep, BRepObject)
