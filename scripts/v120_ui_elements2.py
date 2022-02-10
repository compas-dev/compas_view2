from compas.geometry import Point, Polyline, Bezier
from compas.colors import Color
from compas_view2.app import App

curve = Bezier([[0, 0, 0], [3, 6, 0], [5, -3, 0], [10, 0, 0]])

viewer = App(viewmode="shaded", enable_sidebar=True, width=1600, height=900)
viewer.view.camera.tx = -5.0
viewer.view.camera.rz = 0
viewer.view.camera.rx = -20

viewer.add(Polyline(curve.locus()), linewidth=2)

points = []
for i in range(10):
    p = viewer.add(Point(* curve.point(0)), size=20, color=(1, 0, 0))
    points.append(p)


@viewer.slider(title="Slide Point", maxval=100, step=1, bgcolor=Color.white())
def slide(value):
    value = value / 100
    for i, p in enumerate(points):
        p._data = curve.point(min(1.0, i * value))
        p.update()
    viewer.view.update()


viewer.run()
