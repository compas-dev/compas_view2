import random
import math

import compas
from compas.datastructures import Network
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Torus
from compas.geometry import Pointcloud
from compas.geometry import Rotation
from compas.utilities import i_to_rgb

from compas_view2 import app

viewer = app.Window(width=800, height=500, viewmode='ghosted')

mesh = Mesh.from_off(compas.get('tubemesh.off'))
network = Network.from_obj(compas.get('grid_irregular.obj'))

viewer.add(mesh, show_vertices=False)
viewer.add(network)

cloud = Pointcloud.from_bounds(10, 5, 3, 100)
R1 = Rotation.from_axis_and_angle([0, 0, 1], math.radians(180))
R2 = Rotation.from_axis_and_angle([0, 0, 1], math.radians(90))

for point in cloud.transformed(R1):
    box = Box((point, [1, 0, 0], [0, 1, 0]), 0.1, 0.1, 0.1)
    color = i_to_rgb(random.random(), normalize=True)
    viewer.add(box, show_vertices=False, color=color, is_selected=random.choice([0, 1]))

for point in cloud.transformed(R2):
    r1 = 0.1 * random.random()
    r2 = random.random() * r1
    torus = Torus((point, [0, 0, 1]), r1, r2)
    viewer.add(torus, show_vertices=False)

viewer.show()
