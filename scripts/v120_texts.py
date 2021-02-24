from compas_view2.shapes import Text
from compas_view2 import app


viewer = app.App()

# for i in range(10):
#     point = Point(random()*10, random()*10, random()*10)
#     viewer.add(point, color=(random(), random(), random()), size=10)

t = Text("123321")
viewer.add(t)
viewer.show()
