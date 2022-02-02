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
    T = Translation.from_vector([10, 0, 0])
    R = Rotation.from_axis_and_angle([1, 0, 0], math.radians(90))
    S = Scale.from_factors([100, 100, 100])
    return mesh.transformed(T * R * S)


# # Define the flow graph (Not working yet)
# bunny = load_bunny()
# moved_buuny = move_bunny(bunny)
# save_bunny(moved_buuny)
viewer.run()
