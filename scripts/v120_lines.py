from compas_view2 import app
from compas.geometry import Line
from random import random

viewer = app.App()

for i in range(10):
    line = Line([random()*20, random()*20, random()*20], [random()*20, random()*20, random()*20])
    viewer.add(line, linecolor=(random(), random(), random()), linewidth=2)

viewer.show()
