from random import random

from compas.geometry import Sphere
from compas.geometry import Polyline

from compas_view2.app import App
from compas_view2.collections import Collection

viewer = App()

spheres = []
colors = []

for x in range(5):
    for y in range(5):
        for z in range(5):
            sphere = Sphere([x, y, z], 0.2)
            spheres.append(sphere)
            colors.append((x/5, y/5, z/5))


spherecollection = Collection(spheres)
viewer.add(spherecollection, colors=colors, u=20, v=5, linecolor=(0.2, 0, 0))

lines = []
colors = []
for i in range(100):
    line = Polyline([(random()*5 + 5, random()*5, random()*5), (random()*5 + 5, random()*5, random()*5), (random()*5 + 5, random()*5, random()*5)])
    lines.append(line)
    colors.append((random(), random(), random()))

linecollection = Collection(lines)
viewer.add(linecollection, linewidth=2, colors=colors)


viewer.show()
