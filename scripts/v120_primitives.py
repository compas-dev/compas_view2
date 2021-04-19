from compas_view2 import app
from compas.geometry import Plane

viewer = app.App()

plane = Plane([0, 0, 1], [1, 0, 1])
viewer.add(plane, linecolor=(1, 0, 0), facecolor=(0, 0, 1))


viewer.show()
