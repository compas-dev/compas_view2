from random import random
from math import radians
from math import sin
from math import cos
from compas.geometry import Vector
from compas_view2.app import App
from compas.colors import Color
from compas_view2.collections import Collection

viewer = App()

for i in range(0, 360, 20):
    for j in range(0, 180, 10):
        position = Vector(sin(radians(i)) * sin(radians(j)), cos(radians(i)) * sin(radians(j)), cos(radians(j)))
        vector = Vector(sin(radians(i)), cos(radians(i)), cos(radians(j)))
        viewer.add(vector, position=position, color=[random(), random(), random()], size=1-j / 180)


vectors = []
vector_properties = []

for i in range(0, 360, 20):
    for j in range(0, 180, 10):
        vector = Vector(sin(radians(i)), cos(radians(i)), cos(radians(j)))
        position = Vector(sin(radians(i)) * sin(radians(j)) + 5, cos(radians(i)) * sin(radians(j)), cos(radians(j)))
        color = Color(random(), random(), random())
        size = j / 180

        vectors.append(vector)
        vector_properties.append({'position': position, 'color': color, 'size': size})

collection = Collection(vectors, vector_properties)
viewer.add(collection)

viewer.show()
