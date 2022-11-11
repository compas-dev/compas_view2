from qtpy import QtCore


class Mouse:
    """Class representing mouse actions and movements.

    Attributes
    ----------
    pos : QtCore.QPoint
        The current position of the mouse on the screen.
    last_pos : QtCore.QPoint
        The last recorded position of the mouse on the screen.
    buttons : dict
        A dict containing keys "left" and "right"
        with each an associated boolean indicating if the corresponding mouse button is pressed.

    """

    def __init__(self):
        self.pos = QtCore.QPoint()
        self.last_pos = QtCore.QPoint()
        self.buttons = {"left": False, "right": False}

    def dx(self):
        return self.pos.x() - self.last_pos.x()

    def dy(self):
        return self.pos.y() - self.last_pos.y()
