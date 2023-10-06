from compas.geometry import Frame
from compas_view2.app import App

viewer = App()

frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])

viewer.add(frame)

viewer.show()
