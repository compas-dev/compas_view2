from compas_view2 import app
from compas.geometry import Sphere
from compas.geometry import Line
from compas_view2.collections import Collection
from random import random

viewer = app.App()

spheres = []
colors = []

for x in range(5):
    for y in range(5):
        for z in range(5):
            sphere = Sphere([x, y, z], 0.2)
            spheres.append(sphere)
            colors.append((x/5, y/5, z/5))


spherecollection = Collection(spheres)
viewer.add(spherecollection, colors=colors)

lines = []
colors = []
for i in range(1000):
    line = Line((random()*5 + 5, random()*5, random()*5), (random()*5 + 5, random()*5, random()*5))
    lines.append(line)
    colors.append((random(), random(), random()))

linecollection = Collection(lines)
viewer.add(linecollection, linewidth=2, colors=colors)


viewer.show()
