from .action import Action


class ViewFront(Action):
    """Swtich to a front view.

    Returns
    -------
    None

    """

    def __init__(self, Controller, keys):
        super().__init__(Controller, keys)

    def pressed_action(self):
        self.controller.app.view.current = self.controller.app.view.FRONT
        self.controller.app.view.camera.reset_position()
        self.controller.app.view.update_projection()
        self.controller.app.view.update()
