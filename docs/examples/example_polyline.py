import random
from compas.geometry import Polyline

from compas_view2.app import App

viewer = App()

pts = []
for i in range(10):
    pts.append([random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10)])

polyline = Polyline(pts)
viewer.add(polyline)

pts = []
for i in range(5):
    pts.append([random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10)])

polyline = Polyline(pts)
viewer.add(polyline, show_points=True, pointcolor=(0, 0, 1), linecolor=(1, 0, 0), linewidth=5)

viewer.show()
