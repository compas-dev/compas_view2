import compas
import math
from compas_view2.flow import Node
from compas_view2.app import App
from compas.datastructures import Mesh
from compas.geometry import Scale, Rotation, Translation

viewer = App(viewmode="shaded", show_flow=True, width=800, height=500)


# Wrapping the function to workflow nodes
@Node(viewer)
def load_bunny() -> Mesh:
    return Mesh.from_ply(compas.get('bunny.ply'))


@Node(viewer)
def move_bunny(mesh: Mesh) -> Mesh:
    if not mesh:
        return
    T = Translation.from_vector([1, 0, 0])
    R = Rotation.from_axis_and_angle([1, 0, 0], math.radians(90))
    S = Scale.from_factors([10, 10, 10])
    return mesh.transformed(T * R * S)


# Create the flow graph
node1 = viewer.flow.add_node(load_bunny, location=(300, 150))
node2 = viewer.flow.add_node(move_bunny, location=(500, 350))
viewer.flow.add_connection(node1.outputs[0], node2.inputs[0])


print("Flow graph:", viewer.flow)
print("\n Nodes:")
for key, attr in viewer.flow.node.items():
    print('    key:', key, 'attr:', attr)

print("\n Edges:")
for key in viewer.flow.edges():
    print('    key:', key, 'attr:', viewer.flow.edge_attribute(key, 'connections'))

viewer.run()
