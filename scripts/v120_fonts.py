from compas_view2.shapes import Text
from compas_view2.app import App

viewer = App()

# By default, the text is rendered using the FreeSans font from the library.
t = Text("EN", [0, 0, 0], height=50)
viewer.add(t)

# Font specified is possible.
t = Text("EN", [3, 0, 0], height=50, font = "Times New Roman")
viewer.add(t)

# Multi-language text is possible if the machine has the font installed.
t = Text("中文 CN", [3, 3, 0], height=50, font = "DengXian")
viewer.add(t)

viewer.show()
