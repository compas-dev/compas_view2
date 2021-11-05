from compas_view2 import app
from compas.geometry import Vector
from compas_view2.shapes import VectorGroup
from random import random
from math import radians, sin, cos

viewer = app.App()

for i in range(0, 360, 20):
    for j in range(0, 180, 10):
        position = Vector(sin(radians(i)) * sin(radians(j)), cos(radians(i)) * sin(radians(j)), cos(radians(j)))
        vector = Vector(sin(radians(i)), cos(radians(i)), cos(radians(j)))
        viewer.add(vector, position=position, color=[random(), random(), random()], size=random()*100)


vectors = []
positions = []
colors = []
sizes = []
for i in range(0, 360, 20):
    for j in range(0, 180, 10):
        position = Vector(sin(radians(i)) * sin(radians(j)) + 3, cos(radians(i)) * sin(radians(j)), cos(radians(j)))
        vector = Vector(sin(radians(i)), cos(radians(i)), cos(radians(j)))
        vectors.append(vector)
        positions.append(position)
        colors.append([random(), random(), random()])
        sizes.append(random()*100)

vectorgroup = VectorGroup(vectors, positions)
viewer.add(vectorgroup, colors=colors, sizes=sizes)

viewer.show()
