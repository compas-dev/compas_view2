from compas.geometry import Point, Polyline, Bezier
from compas.colors import Color
from matplotlib.pyplot import title
from compas_view2.app import App
from compas_view2.app import Controller

config = {
    "messages":
    {
        "about": "COMPAS View2 is the second generation of standalone viewers for the COMPAS framework."
    },
    "menubar":
    [
        {
            "type": "menu",
            "text": "COMPASVIEW 2",
            "items":
            [
                {"type": "action", "text": "About", "action": "about"},
                {"type": "separator"},
                {"type": "action", "text": "OpenGL Version", "action": "opengl_version"},
                {"type": "action", "text": "GLSL Version", "action": "glsl_version"}
            ]
        },
        {
            "type": "menu",
            "text": "View",
            "items":
            [
                {
                    "type": "radio",
                    "items":
                    [
                        {"type": "action", "text": "Shaded", "checked": False, "action": "view_shaded"},
                        {"type": "action", "text": "Ghosted", "checked": False, "action": "view_ghosted"},
                        {"type": "action", "text": "Wireframe", "checked": False, "action": "view_wireframe"},
                        {"type": "action", "text": "Lighted", "checked": False, "action": "view_lighted"}
                    ]
                },
                {"type": "separator"},
                {"type": "action", "text": "Capture", "action": "view_capture"},
                {"type": "separator"},
                {"type": "action", "text": "Front", "action": "view_front"},
                {"type": "action", "text": "Right", "action": "view_right"},
                {"type": "action", "text": "Top", "action": "view_top"},
                {"type": "action", "text": "Perspective", "action": "view_perspective"}
            ]
        },

        {
            "type": "menu",
            "text": "Custom Menu",
            "items":
            [
                {"type": "action", "text": "Open side dock 1", "action": "open_dock1"},
                {"type": "action", "text": "Open side dock 2", "action": "open_dock2"},
            ]
        },
    ],
    "toolbar":
    [
        {"type": "action", "text": "Capture", "action": "view_capture"},
        {"type": "separator"},
        {"type": "action", "text": "Front", "action": "view_front"},
        {"type": "action", "text": "Right", "action": "view_right"},
        {"type": "action", "text": "Top", "action": "view_top"},
        {"type": "action", "text": "Perspective", "action": "view_perspective"},
        {"type": "separator"},
        {"type": "action", "text": "Open side dock 3", "action": "open_dock3"},
    ]
}


class CustomController(Controller):

    def open_dock1(self):
        viewer = self.app
        dock = viewer.sidedock(title='Menu 1', slot='A', location="right")

        @viewer.checkbox(text="Show Point", checked=True, parent=dock._layout)
        def check(checked):
            pointobj.is_visible = checked
            viewer.view.update()

        dock._layout.addStretch()

    def open_dock2(self):

        viewer = self.app
        dock = viewer.sidedock(title='Menu 2', slot='A', location="right")

        @viewer.slider(title="Slide Point", maxval=100, step=1, bgcolor=Color.white(), parent=dock._layout)
        def slide(value):
            value = value / 100
            pointobj._data = curve.point(value)
            pointobj.update()
            viewer.view.update()

        @viewer.button(text="Reset", parent=dock._layout)
        def click():
            if viewer.confirm('This will reset the point to parameter t=0.'):
                pointobj._data = curve.point(0)
                pointobj.update()
                slide.value = 0
                viewer.view.update()

        dock._layout.addStretch()
    
    def open_dock3(self):
        viewer = self.app
        dock = viewer.sidedock(title='Menu 1', location="left")

        @viewer.checkbox(text="Do nothing", checked=True, parent=dock._layout)
        def check(checked):
            pass
        
        dock._layout.addStretch()


viewer = App(viewmode="shaded", width=1600, height=900, config=config, controller_class=CustomController)

curve = Bezier([[0, 0, 0], [3, 6, 0], [5, -3, 0], [10, 0, 0]])
pointobj = viewer.add(Point(* curve.point(0)), size=20, color=(1, 0, 0))
curveobj = viewer.add(Polyline(curve.locus()), linewidth=2)


viewer.run()
