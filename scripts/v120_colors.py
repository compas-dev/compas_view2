import compas

from compas_view2 import app
from compas.datastructures import Mesh
from compas.geometry import Translation, Scale
from random import random

viewer = app.App(width=800, height=500)

mesh = Mesh.from_obj(compas.get('faces.obj'))
T = Translation.from_vector([0, 0, 1])
S = Scale.from_factors([.5, .5, .5])
mesh.transform(T*S)

mesh2 = mesh.transformed(Translation.from_vector([-6, 0, 0]))

facecolors = {k: [random(), random(), random()] for k in mesh.faces()}
linecolors = {k: [random(), random(), random()] for k in mesh.edges()}
pointcolors = {k: [random(), random(), random()] for k in mesh.vertices()}
pointcolors = {k: [0.5, 0, 0] for k in mesh.vertices()}

# viewer.add(mesh, show_points=True, facecolors=facecolors, linecolors=linecolors, pointcolors=pointcolors)
# viewer.add(mesh, show_points=True, facecolors=facecolors, linecolors=linecolors, pointcolors=pointcolors)
viewer.add(mesh, show_points=True, facecolors=facecolors, linecolors=linecolors, pointcolor=[0.3, 0, 0])
# viewer.add(mesh, hide_coplanaredges=False, facecolor=[0.99, 0.0, 0])
# viewer.add(mesh2, hide_coplanaredges=True)

viewer.show()
