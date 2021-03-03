import compas

from compas_view2 import app
from compas.datastructures import Mesh
from compas.geometry import Translation, Scale

viewer = app.App(width=800, height=500)

mesh = Mesh.from_obj(compas.get('faces.obj'))
T = Translation.from_vector([0, 0, 1])
S = Scale.from_factors([.5, .5, .5])
mesh.transform(T*S)

mesh2 = mesh.transformed(Translation.from_vector([-6, 0, 0]))

viewer.add(mesh, show_vertices=False, hide_coplanaredges=False)
viewer.add(mesh2, show_vertices=False, hide_coplanaredges=True)

viewer.show()
