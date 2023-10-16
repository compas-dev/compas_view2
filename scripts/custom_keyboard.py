from compas.geometry import Point, Polyline, Bezier
from compas_view2.configs import config_r
from compas_view2.app import App






viewer = App(viewmode="shaded", width=1600, height=900, config=config_r)

curve = Bezier([[0, 0, 0], [3, 6, 0], [5, -3, 0], [10, 0, 0]])
pointobj = viewer.add(Point(* curve.point(0)), pointsize=20, pointcolor=(1, 0, 0))
curveobj = viewer.add(Polyline(curve.locus()), linewidth=2)


viewer.run()
