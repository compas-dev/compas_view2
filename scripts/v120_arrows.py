from compas_view2 import app
from compas_view2.shapes import Arrow
from random import random

viewer = app.App()

for x in range(5):
    for y in range(5):
        arrow = Arrow([x, y, 0], [0, 0, 1])
        viewer.add(arrow, color=(random(), random(), random()))

viewer.show()
