from .action import Action


class GridShow(Action):
    """Swtich to a top view.

    Returns
    -------
    None

    """

    def __init__(self, Controller, keys: list[str]):
        super().__init__(Controller, keys)

    def pressed_action(self):
        self.controller.app.view.show_grid = not self.controller.app.view.show_grid
        self.controller.app.view.update()
