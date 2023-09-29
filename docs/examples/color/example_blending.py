from compas.geometry import Box
from compas_view2.app import App

viewer = App()


box = Box(frame=([0, 0, 0], [1, 0, 0], [0, 1, 0]))
obj1 = viewer.add(box, facecolor=(1, 0, 0), opacity=0.7)

box = Box(frame=([0, 0, 0], [1, 0, 0], [0, 1, 0]))
obj2 = viewer.add(box, facecolor=(0, 1, 0), opacity=0.7)

box = Box(frame=([0, 0, 0], [1, 0, 0], [0, 1, 0]))
obj3 = viewer.add(box, facecolor=(0, 0, 1), opacity=0.7)


obj2.translation[0] = 2
obj3.translation[0] = 4

viewer.show()
