from compas_view2 import app
from compas.geometry import Frame

viewer = app.App()

frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])

viewer.add(frame)

viewer.show()
