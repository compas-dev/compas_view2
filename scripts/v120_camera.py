from compas_view2.app import App
from math import radians


viewer = App(enable_sidebar=True)


@viewer.slider(title="Rotate camera Z", minval=-180, maxval=180, step=1)
def slide(value):
    viewer.view.camera.rotation[2] = radians(value)
    viewer.view.update()


@viewer.slider(title="Rotate camera X", minval=-180, maxval=180, step=1)
def slide(value):
    viewer.view.camera.rotation[0] = radians(value)
    viewer.view.update()


@viewer.slider(title="Move target X", minval=-10, maxval=10)
def slide(value):
    viewer.view.camera.target[0] = value
    viewer.view.update()


@viewer.slider(title="Move target Y", minval=-10, maxval=10)
def slide(value):
    viewer.view.camera.target[1] = value
    viewer.view.update()


@viewer.slider(title="Move camera X", minval=-10, maxval=10, step=0.1)
def slide(value):
    current_pos = viewer.view.camera.position
    viewer.view.camera.position = [value, current_pos[1], current_pos[2]]
    viewer.view.update()


@viewer.slider(title="Move camera Y", minval=-10, maxval=10, step=0.1)
def slide(value):
    current_pos = viewer.view.camera.position
    viewer.view.camera.position = [current_pos[0], value, current_pos[2]]
    viewer.view.update()


@viewer.slider(title="Move camera Z", minval=-10, maxval=10, step=0.1)
def slide(value):
    current_pos = viewer.view.camera.position
    viewer.view.camera.position = [current_pos[0], current_pos[1], value]
    viewer.view.update()


viewer.run()
