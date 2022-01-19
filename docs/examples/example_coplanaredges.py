import compas
from compas.datastructures import Mesh
from compas.geometry import Translation
from compas.geometry import Scale

from compas_view2.app import App

mesh = Mesh.from_obj(compas.get('faces.obj'))
mesh.transform(Translation.from_vector([0.5, 0, 0.1]))

mesh2 = mesh.transformed(Translation.from_vector([-11, 0, 0]))

# =============================================================================
# Visualization
# =============================================================================

viewer = App(width=1600, height=900)
viewer.view.camera.rx = -60
viewer.view.camera.rz = 0
viewer.view.camera.ty = -2
viewer.view.camera.distance = 10

viewer.add(mesh, hide_coplanaredges=False)
viewer.add(mesh2, hide_coplanaredges=True)
viewer.show()
