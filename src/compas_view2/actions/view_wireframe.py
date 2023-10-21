from .action import Action


class ViewWireframe(Action):
    """Switch the view to wireframe.

    Returns
    -------
    None

    """

    def __init__(self, Controller, keys):
        super().__init__(Controller, keys)

    def pressed_action(self):
        self.controller.app.view.mode = "wireframe"
        self.controller.app.view.update()
