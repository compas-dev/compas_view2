from random import random
from compas.geometry import Point
from compas.geometry import Pointcloud
from compas.colors import Color
from compas_view2.app import App

viewer = App()
for i in range(10):
    point = Point(random()*10, random()*10, random()*10)
    viewer.add(point, pointcolor=Color(random(), random(), random()), pointsize=30)

cloud = Pointcloud.from_bounds(5, 5, 5, 1000)
pointcolor = {i: Color(random(), random(), random()) for i in range(1000)}
viewer.add(cloud, pointcolor=pointcolor)

viewer.show()
