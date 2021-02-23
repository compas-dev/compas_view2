from compas_view2 import app
from compas.geometry import Point
from random import random

viewer = app.App()

for i in range(10):
    point = Point(random()*10, random()*10, random()*10)
    viewer.add(point, color=(random(), random(), random()), size=10)

viewer.show()
