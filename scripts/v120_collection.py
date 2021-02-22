from compas_view2 import app
from compas.geometry import Sphere
from compas_view2.shapes import Collection

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

viewer.add(spherecollection, show_lines=False, colors=colors)
viewer.show()
