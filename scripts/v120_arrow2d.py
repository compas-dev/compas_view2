from compas_view2 import app
from compas_view2.shapes import Arrow2d
from random import random

viewer = app.App()

arrow = Arrow2d([0, 0, 0], [0, 0, 1], head_portion=0.2, head_width=0.07, body_width=0.02)
viewer.add(arrow, color=(random(), random(), random()))

viewer.show()
