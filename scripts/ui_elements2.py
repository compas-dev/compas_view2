from compas.geometry import Point, Polyline, Bezier
from compas.colors import Color
from compas_view2.app import App

curve = Bezier([[0, 0, 0], [3, 6, 0], [5, -3, 0], [10, 0, 0]])

viewer = App(viewmode="shaded", enable_sidebar=True, width=1600, height=900)
viewer.view.camera.target = [5, 0, 0]
viewer.view.camera.distance = 20

viewer.add(Polyline(curve.to_points(50)), linewidth=2)

points = []
for i in range(10):
    p = viewer.add(Point(* curve.point_at(0)), pointsize=20, pointcolor=(1, 0, 0))
    points.append(p)


@viewer.slider(title="Slide Point", maxval=100, step=1, bgcolor=Color.white())
def slide(value):
    value = value / 100
    for i, p in enumerate(points):
        p._data = curve.point_at(min(1.0, i * value))
        p.update()
    viewer.view.update()


viewer.run()
