import compas
import math

from compas_view2.flow import Node, Float, String
from compas_view2.app import App
from compas.datastructures import Mesh
from compas.geometry import Scale, Rotation, Translation

viewer = App(viewmode="shaded", width=1500, height=1000, show_flow=True, flow_auto_update=False)


# Wrapping the function to ryven nodes
@Node(viewer)
def load_mesh(path: str) -> Mesh:
    return Mesh.from_ply(compas.get(path))


@Node(viewer)
def move_and_scale(mesh: Mesh, distance: float = 1) -> Mesh:
    T = Translation.from_vector([distance, 0, 0])
    R = Rotation.from_axis_and_angle([1, 0, 0], math.radians(90))
    S = Scale.from_factors([10, 10, 10])
    return mesh.transformed(T * R * S)


# Create the flow graph
node0 = viewer.flow.add_node(String(default='bunny.ply'), location=(300, 150))
node1 = viewer.flow.add_node(load_mesh, location=(700, 250))
node2 = viewer.flow.add_node(move_and_scale, location=(1200, 350))
node3 = viewer.flow.add_node(Float(default=1.0), location=(700, 500))

viewer.flow.add_connection(node0.outputs[0], node1.inputs[0])
viewer.flow.add_connection(node1.outputs[0], node2.inputs[0])
viewer.flow.add_connection(node3.outputs[0], node2.inputs[1])

viewer.run()
