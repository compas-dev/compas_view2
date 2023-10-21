from .action import Action


class ZoomSelected(Action):
    def __init__(self, Controller, keys):
        super().__init__(Controller, keys)

    def pressed_action(self):
        if self.controller.app.selector.selected:
            self.controller.app.view.camera.zoom_extents(self.controller.app.selector.selected)
        else:
            self.controller.app.view.camera.zoom_extents(self.controller.app.view.objects)
