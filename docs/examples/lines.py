from random import random
from compas.geometry import Line
from compas_view2.app import App

viewer = App()

for i in range(10):
    line = Line([random()*20, random()*20, random()*20], [random()*20, random()*20, random()*20])
    viewer.add(line, linecolor=(random(), random(), random()), linewidth=2)

viewer.show()
