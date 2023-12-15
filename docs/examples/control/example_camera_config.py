from compas.geometry import Box
from compas.geometry import Frame
from compas_view2.app import App

# If you input incomplete configuration, the rest will be filled by the default values.

config = {
    "view": {
        "show_grid": True,
        "view_mode": "shaded",
        "background_color": [1, 1, 1, 1],
        "selection_color": [1.0, 1.0, 0.0],
        "view_port": "TOP",
        "camera": {
            "fov": 45,
            "near": 0.1,
            "far": 1000,
            "position": [-15, -15, 15],
            "target": [1,1, 1],
            "scale": 1,
        },
    }
}

viewer_default = App()
viewer_custom = App(config=config)


box = Box(Frame([0, 0, 0], [1, 0, 0], [0, 1, 0]), 1, 1, 1)

viewer_default.add(box)
viewer_custom.add(box)


viewer_default.run()
viewer_custom.run()
