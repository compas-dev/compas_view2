from compas_view2 import app
from compas_view2.shapes import Arrow2d
from random import random
from math import radians, sin, cos

viewer = app.App()

positions = []
directions = []
colors = []

for i in range(0, 360, 20):
    for j in range(0, 180, 10):
        positions.append([sin(radians(i)) * sin(radians(j)), cos(radians(i)) * sin(radians(j)), cos(radians(j))])
        directions.append([sin(radians(i)), cos(radians(i)), cos(radians(j))])
        colors.append([random(), random(), random()])

arrow=Arrow2d(positions, directions)
viewer.add(arrow, colors=colors)

viewer.show()
