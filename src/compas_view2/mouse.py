from PySide2 import QtCore


class Mouse:

    def __init__(self):
        self.pos = QtCore.QPoint()
        self.last_pos = QtCore.QPoint()
        self.buttons = {'left': False, 'right': False}
        self.pressed_on = None

    def is_pressed(self):
        return self.buttons['left'] or self.buttons['right']

    def dx(self):
        return self.pos.x() - self.last_pos.x()

    def dy(self):
        return self.pos.y() - self.last_pos.y()
