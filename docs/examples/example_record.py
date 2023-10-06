import os
from compas.geometry import Box
from compas.geometry import Scale

import compas_view2
from compas_view2.app import App

viewer = App()

box1 = Box(([0, 0, 0], [1, 0, 0], [0, 1, 0]), 1, 1, 1)
box2 = Box(([0, 0, 0], [1, 0, 0], [0, 1, 0]), 1, 1, 1)
box3 = Box(([0, 0, 0], [1, 0, 0], [0, 1, 0]), 1, 1, 1)
obj1 = viewer.add(box1, facecolor=(1, 0, 0), linecolor=(0, 0, 0))
obj2 = viewer.add(box2, facecolor=(0, 1, 0), linecolor=(0, 0, 0))
obj3 = viewer.add(box3, facecolor=(0, 0, 1), linecolor=(0, 0, 0))

s = 1

FILE = os.path.join(compas_view2.TEMP, 'record2.gif')


# Record 100 frames and save as "record.gif"
@viewer.on(interval=50, record=True, frames=100, record_path=FILE)
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
