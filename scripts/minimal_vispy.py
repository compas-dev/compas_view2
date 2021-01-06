import sys

from vispy import scene

canvas = scene.SceneCanvas(keys="interactive", bgcolor="white", size=(1200, 700), show=True)
view = canvas.central_widget.add_view()
view.camera = "turntable"

axis = scene.visuals.XYZAxis(parent=view.scene)
grid = scene.visuals.GridLines(scale=(1, 1), color=[0, 0, 0, 1.0], parent=view.scene)


if __name__ == '__main__':
    if sys.flags.interactive == 0:
        canvas.app.run()
