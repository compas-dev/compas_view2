import random

from compas.geometry import Polyline

from compas_view2 import app

viewer = app.App()

for j in range(1):
    pts = []
    for i in range(10):
        pts.append([random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10)])

    polyline = Polyline(pts)
    viewer.add(polyline)

pts = []
for i in range(5):
    pts.append([random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10)])

polyline = Polyline(pts)
viewer.add(polyline, show_points=True, color_lines=(1, 0, 0), width_lines=5)

viewer.show()
