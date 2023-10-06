from compas_view2.shapes import Text
from compas_view2.app import App

viewer = App()

t = Text("a", [0, 0, 0], height=50)
viewer.add(t)

t = Text("123", [3, 0, 0], height=50)
viewer.add(t)

t = Text("ABC", [3, 3, 0], height=20, absolute_height=True)
viewer.add(t, color=(1, 0, 0))

viewer.show()
