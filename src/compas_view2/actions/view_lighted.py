from .action import Action


class ViewLighted(Action):
    """Switch the view to lighted.

    Returns
    -------
    None

    """

    def __init__(self, Controller, keys: list[str]):
        super().__init__(Controller, keys)

    def pressed_action(self):
        self.controller.app.view.mode = "lighted"
        self.controller.app.view.update()
