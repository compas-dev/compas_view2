from compas_view2 import app
from compas.geometry import Point
from compas.geometry import Pointcloud
from random import random

viewer = app.App()
for i in range(10):
    point = Point(random()*10, random()*10, random()*10)
    viewer.add(point, color=(random(), random(), random()), size=10)

cloud = Pointcloud.from_bounds(5, 5, 5, 1000)
viewer.add(cloud, color=(random(), random(), random()), size=10)

viewer.show()