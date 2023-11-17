from compas.geometry import Point, Polyline, Bezier
from compas_view2.app import App

# If you input incomplete configuration, the rest will be filled by the default values.
# The default controller configuration is more Rhino-user friendly.
# Below we provide a more ***Blender-user friendly*** configuration.


config = {
    "controller": {
        "actions": {
            "mouse_key": {
                "pan": {"mouse": "middle", "key": "shift"},
                "rotate": {"mouse": "middle", "key": ""},
                "box_selection": {"mouse": "left", "key": ""},
                "box_deselection": {"mouse": "left", "key": "control"},
                "selection": {"mouse": "left", "multi_selection": "shift", "deselect": "control"},
            },
            "keys": {
                "zoom_selected": ["control","."]
            },
        },
    }
}

viewer = App(config=config)

curve = Bezier([[0, 0, 0], [3, 6, 0], [5, -3, 0], [10, 0, 0]])
pointobj = viewer.add(Point(*curve.point(0)), pointsize=20, pointcolor=(1, 0, 0))
curveobj = viewer.add(Polyline(curve.locus()), linewidth=2)


viewer.run()
