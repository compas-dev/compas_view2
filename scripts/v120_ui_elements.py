from compas.geometry import Point, Polyline, Bezier
from compas_view2.app import App

curve = Bezier([[0, 0, 0], [3, 6, 0], [5, -3, 0], [10, 0, 0]])

viewer = App(viewmode="ghosted", enable_sidebar=True)

pointobj = viewer.add(Point(* curve.point(0)), size=20, color=(1, 0, 0))
curveobj = viewer.add(Polyline(curve.locus()), linewidth=2)


@viewer.checkbox(text="Show Point", checked=True)
def check(checked):
    pointobj.is_visible = checked
    viewer.view.update()


@viewer.slider(text="Slide Point", maxval=100, step=1)
def slide(value):
    value = value / 100
    pointobj._data = curve.point(value)
    pointobj.update()
    viewer.view.update()


viewer.run()
