from compas_view2.app import App
from math import radians


viewer = App(enable_sidebar=True)
viewer.view.camera.position = (10, 10, 10)
viewer.view.camera.target = (5, 0, 0)


@viewer.slider(title="Rotate camera Z", minval=-180, maxval=180, step=1)
def slide(value):
    viewer.view.camera.rotation.z = radians(value)
    viewer.view.update()


@viewer.slider(title="Rotate camera X", minval=-180, maxval=180, step=1)
def slide(value):
    viewer.view.camera.rotation.x = radians(value)
    viewer.view.update()


@viewer.slider(title="Move target X", minval=-10, maxval=10)
def slide(value):
    viewer.view.camera.target.x = value
    viewer.view.update()


@viewer.slider(title="Move target Y", minval=-10, maxval=10)
def slide(value):
    viewer.view.camera.target.y = value
    viewer.view.update()


@viewer.slider(title="Move camera X", minval=-10, maxval=10, step=0.1)
def slide(value):
    viewer.view.camera.position.x = value
    viewer.view.update()


@viewer.slider(title="Move camera Y", minval=-10, maxval=10, step=0.1)
def slide(value):
    viewer.view.camera.position.y = value
    viewer.view.update()


@viewer.slider(title="Move camera Z", minval=-10, maxval=10, step=0.1)
def slide(value):
    viewer.view.camera.position.z = value
    viewer.view.update()


viewer.run()
