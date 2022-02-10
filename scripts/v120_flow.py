import compas
import math

from compas_view2.flow import Node, StringNode, VectorNode
from compas_view2.app import App
from compas.datastructures import Mesh
from compas.geometry import Vector
from compas.geometry import Scale, Rotation, Translation

viewer = App(viewmode="shaded", width=1500, height=1000, show_flow=True, flow_auto_update=False)


# Wrapping the function to ryven nodes
@Node(viewer)
def load_mesh(path: str) -> Mesh:
    file_format = path.split(".")[-1]
    if hasattr(Mesh, f"from_{file_format}"):
        return getattr(Mesh, f"from_{file_format}")(compas.get(path))
    else:
        raise ValueError(f"File format {file_format} is not supported")


@Node(viewer)
def transform_mesh(mesh: Mesh, translation: Vector, rotation: Vector, scale: Vector) -> Mesh:
    T = Translation.from_vector(translation)
    R = Rotation.from_axis_angle_vector(rotation)
    S = Scale.from_factors(scale)
    return mesh.transformed(T * R * S)


# Create the flow graph
path_node = viewer.flow.add_node(StringNode(default='bunny.ply'), location=(300, 150))
load_node = viewer.flow.add_node(load_mesh, location=(700, 150))
translation_node = viewer.flow.add_node(VectorNode(title='translation', default=[1, 0, 0]), location=(700, 400))
rotation_node = viewer.flow.add_node(VectorNode(title='rotation', default=[math.radians(90), 0, 0]), location=(700, 600))
scale_node = viewer.flow.add_node(VectorNode(title='scale', default=[10, 10, 10]), location=(700, 800))
transform_node = viewer.flow.add_node(transform_mesh, location=(1200, 350))


viewer.flow.add_connection(path_node.outputs[0], load_node.inputs[0])
viewer.flow.add_connection(load_node.outputs[0], transform_node.inputs[0])
viewer.flow.add_connection(translation_node.outputs[0], transform_node.inputs[1])
viewer.flow.add_connection(rotation_node.outputs[0], transform_node.inputs[2])
viewer.flow.add_connection(scale_node.outputs[0], transform_node.inputs[3])

viewer.run()
