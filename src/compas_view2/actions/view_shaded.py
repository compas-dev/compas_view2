from .action import Action


class ViewShaded(Action):
    """Swtich to a top view.

    Returns
    -------
    None

    """

    def __init__(self, Controller, keys):
        super().__init__(Controller, keys)

    def pressed_action(self):
        self.controller.app.view.mode = "shaded"
        self.controller.app.view.update()
