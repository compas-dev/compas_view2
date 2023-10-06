from random import random
from math import radians
from math import sin
from math import cos
from compas.geometry import Vector
from compas_view2.app import App
from compas_view2.shapes import VectorGroup

viewer = App()

for i in range(0, 360, 20):
    for j in range(0, 180, 10):
        position = Vector(sin(radians(i)) * sin(radians(j)), cos(radians(i)) * sin(radians(j)), cos(radians(j)))
        vector = Vector(sin(radians(i)), cos(radians(i)), cos(radians(j)))
        viewer.add(vector, position=position, color=[random(), random(), random()], size=1)

viewer.show()