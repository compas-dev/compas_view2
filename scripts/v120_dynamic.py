from compas.geometry import Point
from compas_view2 import app


viewer = app.App()
obj = viewer.add(Point(0, 0, 0))


@viewer.on(interval=1000)
def movepoint(frame):
    print('frame', frame)
    obj._data.x += 1
    obj.update()


viewer.run()
