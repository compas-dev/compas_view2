import compas

from compas.datastructures import Mesh
from compas.geometry import Translation
from compas.geometry import Scale

from compas_view2.app import App

viewer = App()

mesh = Mesh.from_obj(compas.get('faces.obj'))
T = Translation.from_vector([0, 0, 1])
S = Scale.from_factors([.5, .5, .5])
mesh.transform(T*S)

mesh2 = mesh.transformed(Translation.from_vector([-6, 0, 0]))

viewer.add(mesh, hide_coplanaredges=False)
viewer.add(mesh2, hide_coplanaredges=True)

viewer.show()
