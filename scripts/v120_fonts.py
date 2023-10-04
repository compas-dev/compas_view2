from compas_view2.shapes import Text
from compas_view2.app import App

viewer = App()

# By default, the font is "FreeSans.ttf" contained in the library.
t = Text("EN", [0, 0, 0], height=50)
viewer.add(t, color = (0,0,1))

# Font specification is possible by indicating the font name.
t = Text("EN", [3, 0, 0], font = "Times New Roman")
viewer.add(t, color = (1, 0, 0))

# Other characters are also possible if the font is installed in the machine.
t = Text("中文 CN", [3,3, 0], font="DengXian")
viewer.add(t, color = (0,1,0))

viewer.show()
