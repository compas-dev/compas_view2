from compas.geometry import Point, Vector, Plane
from compas.geometry import Box, Cylinder
from compas.datastructures import Mesh
from compas_occ.brep import BRep
from compas_view2.app import App
from compas_view2.flow import Node, FloatNode


P = Point(0, 0, 0)
X = Vector(1, 0, 0)
Y = Vector(0, 1, 0)
Z = Vector(0, 0, 1)
YZ = Plane(P, X)
ZX = Plane(P, Y)
XY = Plane(P, Z)

viewer = App(viewmode="lighted", width=1500, height=1000, show_flow=True, flow_auto_update=True)


@Node(viewer, is_visible=False)
def create_box(size: float) -> Box:
    return Box.from_width_height_depth(size, size, size)


@Node(viewer, opacity=0.2)
def create_cylinder_x(radius: float, height: float) -> Box:
    YZ = Plane(P, X)
    return Cylinder((YZ, radius), height)


@Node(viewer, opacity=0.2)
def create_cylinder_y(radius: float, height: float) -> Box:
    XZ = Plane(P, Y)
    return Cylinder((XZ, radius), height)


@Node(viewer, opacity=0.2)
def create_cylinder_z(radius: float, height: float) -> Box:
    XY = Plane(P, Z)
    return Cylinder((XY, radius), height)


@Node(viewer)
def create_csg_geometry(A: Box, B1: Cylinder, B2: Cylinder, B3: Cylinder) -> Mesh:
    A = BRep.from_box(A)
    B1 = BRep.from_cylinder(B1)
    B2 = BRep.from_cylinder(B2)
    B3 = BRep.from_cylinder(B3)
    C = A - (B1 + B2 + B3)
    return C.to_tesselation()


size = viewer.flow.add_node(FloatNode(title="size", default=2), location=(200, 200))
radius = viewer.flow.add_node(FloatNode(title="radius", default=0.7), location=(200, 400))
height = viewer.flow.add_node(FloatNode(title="height", default=4), location=(200, 600))
box = viewer.flow.add_node(create_box, location=(600, 200))
cylinder_x = viewer.flow.add_node(create_cylinder_x, location=(600, 400))
cylinder_y = viewer.flow.add_node(create_cylinder_y, location=(600, 600))
cylinder_z = viewer.flow.add_node(create_cylinder_z, location=(600, 800))
csg = viewer.flow.add_node(create_csg_geometry, location=(1200, 500))


viewer.flow.add_connection(size.outputs[0], box.inputs[0])
viewer.flow.add_connection(radius.outputs[0], cylinder_x.inputs[0])
viewer.flow.add_connection(height.outputs[0], cylinder_x.inputs[1])
viewer.flow.add_connection(radius.outputs[0], cylinder_y.inputs[0])
viewer.flow.add_connection(height.outputs[0], cylinder_y.inputs[1])
viewer.flow.add_connection(radius.outputs[0], cylinder_z.inputs[0])
viewer.flow.add_connection(height.outputs[0], cylinder_z.inputs[1])
viewer.flow.add_connection(box.outputs[0], csg.inputs[0])
viewer.flow.add_connection(cylinder_x.outputs[0], csg.inputs[1])
viewer.flow.add_connection(cylinder_y.outputs[0], csg.inputs[2])
viewer.flow.add_connection(cylinder_z.outputs[0], csg.inputs[3])


viewer.run()
