from compas_view2 import app
from compas.geometry import Box
from compas.geometry import Frame

viewer = app.App()

f = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
box = Box(f, 1, 1, 1)

obj1 = viewer.add(box)
# obj1.translation = [2, 0, 0]

obj2 = viewer.add(box)
obj2.translation = [0, 2, 0]

viewer.show()