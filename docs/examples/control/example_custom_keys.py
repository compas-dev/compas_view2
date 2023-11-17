from compas.geometry import Box, Frame
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

for i in range(0, 5, 2):
    for j in range(0, 5, 2):
        box = Box(Frame([i, j, 0], [1, 0, 0], [0, 1, 0]), 1, 1, 1)
        viewer.add(box)


viewer.run()
