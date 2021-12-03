from compas_view2 import app
from compas.geometry import Vector
from compas_view2.shapes import VectorGroup
from random import random
from math import radians, sin, cos

from compas_view2.collections import Collection

viewer = app.App()

# for i in range(0, 360, 20):
#     for j in range(0, 180, 10):
#         position = Vector(sin(radians(i)) * sin(radians(j)), cos(radians(i)) * sin(radians(j)), cos(radians(j)))
#         vector = Vector(sin(radians(i)), cos(radians(i)), cos(radians(j)))
#         viewer.add(vector, position=position, color=[random(), random(), random()], size=1)


vectors = []
positions = []
colors = []
sizes = []

for i in range(0, 360, 20):
    for j in range(0, 180, 10):
        positions.append(Vector(sin(radians(i)) * sin(radians(j)) + 5, cos(radians(i)) * sin(radians(j)), cos(radians(j))))
        vectors.append(Vector(sin(radians(i)), cos(radians(i)), cos(radians(j))))
        colors.append([random(), random(), random()])
        sizes.append(j / 180)

vectorCollection = Collection(vectors, positions=positions, colors=colors, sizes=sizes)
viewer.add(vectorCollection)

viewer.show()