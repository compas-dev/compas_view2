from random import random

import compas

from compas.datastructures import Mesh
from compas.geometry import Translation, Scale
from compas.colors import Color

from compas_view2.app import App

viewer = App(width=800, height=500)

mesh = Mesh.from_obj(compas.get('faces.obj'))
T = Translation.from_vector([0, 0, 1])
S = Scale.from_factors([.5, .5, .5])
mesh.transform(T*S)

mesh2 = mesh.transformed(Translation.from_vector([-6, 0, 0]))

facecolors = {k: Color(random(), random(), random()) for k in mesh.faces()}
linecolors = {k: Color(random(), random(), random()) for k in mesh.edges()}
pointcolors = {k: Color(random(), random(), random()) for k in mesh.vertices()}

viewer.add(mesh, name="mesh1", show_points=True, facecolors=facecolors, linecolors=linecolors, pointcolors=pointcolors)
viewer.add(mesh2, name="mesh2", show_points=True, facecolor=Color(1, 0, 0), linecolor=Color(0, 1, 0), pointcolor=Color(0, 0, 1))

viewer.show()
