from .action import Action


class SelectAll(Action):
    """Swtich to a top view.

    Returns
    -------
    None

    """

    def __init__(self, Controller, keys):
        super().__init__(Controller, keys)

    def pressed_action(self):
        raise NotImplementedError
