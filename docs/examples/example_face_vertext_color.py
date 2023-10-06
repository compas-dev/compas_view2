import compas

from compas.datastructures import Mesh
from compas.colors import Color
from random import random

from compas_view2.app import App

viewer = App(width=800, height=500)

mesh = Mesh.from_obj(compas.get('faces.obj'))

for vertex in mesh.vertices():
    mesh.vertex_attribute(vertex, 'color', Color.from_i(random()))

viewer.add(mesh, use_vertex_color=True)

viewer.show()
