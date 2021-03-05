from compas_view2 import app
from compas.geometry import Box
from compas.geometry import Scale

viewer = app.App()

box1 = Box(([0, 0, 0], [1, 0, 0], [0, 1, 0]), 1, 1, 1)
box2 = Box(([0, 0, 0], [1, 0, 0], [0, 1, 0]), 1, 1, 1)
box3 = Box(([0, 0, 0], [1, 0, 0], [0, 1, 0]), 1, 1, 1)
obj1 = viewer.add(box1, color=(1, 0, 0))
obj2 = viewer.add(box2, color=(0, 1, 0))
obj3 = viewer.add(box3, color=(0, 0, 1))

s = 1


@viewer.on(interval=100)
def transform(frame):
    obj1.translation[0] += 0.1
    obj1.rotation[2] += 0.1
    obj1.update()

    obj2.translation[2] += 0.1
    obj2.rotation[0] += 0.1
    obj2.update()

    global s
    s += 0.05
    S = Scale.from_factors([s, s, s])
    obj3.matrix = S.matrix
    obj3.update()


viewer.run()
