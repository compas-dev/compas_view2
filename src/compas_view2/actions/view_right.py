from .action import Action


class ViewRight(Action):
    """Swtich to a right view.

    Returns
    -------
    None

    """

    def __init__(self, Controller, keys: list[str]):
        super().__init__(Controller, keys)

    def pressed_action(self):
        self.controller.app.view.current = self.controller.app.view.RIGHT
        self.controller.app.view.camera.reset_position()
        self.controller.app.view.update_projection()
        self.controller.app.view.update()
