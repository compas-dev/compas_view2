from compas.datastructures import Mesh
from compas_view2 import app
from random import random
import compas

viewer = app.App()

mesh = Mesh.from_off(compas.get('tubemesh.off'))
obj = viewer.add(mesh)


@viewer.on(interval=1000)
def deform_mesh(frame):
    for v in mesh.vertices():
        vertex = mesh.vertex_attributes(v, 'xyz')
        vertex[0] += random()-0.5
        vertex[1] += random()-0.5
        vertex[2] += random()-0.5
        mesh.vertex_attributes(v, 'xyz', vertex)
    obj.update()
    print(frame)


viewer.run()
