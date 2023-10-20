from .action import Action


class ViewGhosted(Action):
    """Switch the view to ghosted.

    Returns
    -------
    None

    """

    def __init__(self, Controller, keys: list[str]):
        super().__init__(Controller, keys)

    def pressed_action(self):
        self.controller.app.view.mode = "ghosted"
        self.controller.app.view.update()
