from compas.geometry import Point
from compas_view2 import app
from compas_view2.app.timer import Timer


def movepoint():
    print('test')
    obj._data[0] += 1
    viewer.view.update()


viewer = app.App()
obj = viewer.add(Point(0, 0, 0))
viewer.timer = Timer(interval=1000, callback=movepoint)
viewer.run()
