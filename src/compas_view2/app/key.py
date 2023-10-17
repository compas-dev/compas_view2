from qtpy import QtCore

supported_keys = {
    "shift": QtCore.Qt.Key_Shift,
    "control": QtCore.Qt.Key_Control,
    "alt": QtCore.Qt.Key_Alt,
    "space": QtCore.Qt.Key_Space,
    "escape": QtCore.Qt.Key_Escape,
    "delete": QtCore.Qt.Key_Delete,
    "enter": QtCore.Qt.Key_Enter,
    "a": QtCore.Qt.Key_A,
    "b": QtCore.Qt.Key_B,
    "c": QtCore.Qt.Key_C,
    "d": QtCore.Qt.Key_D,
    "e": QtCore.Qt.Key_E,
    "f": QtCore.Qt.Key_F,
    "g": QtCore.Qt.Key_G,
    "h": QtCore.Qt.Key_H,
    "i": QtCore.Qt.Key_I,
    "j": QtCore.Qt.Key_J,
    "k": QtCore.Qt.Key_K,
    "l": QtCore.Qt.Key_L,
    "m": QtCore.Qt.Key_M,
    "n": QtCore.Qt.Key_N,
    "o": QtCore.Qt.Key_O,
    "p": QtCore.Qt.Key_P,
    "q": QtCore.Qt.Key_Q,
    "r": QtCore.Qt.Key_R,
    "s": QtCore.Qt.Key_S,
    "t": QtCore.Qt.Key_T,
    "u": QtCore.Qt.Key_U,
    "v": QtCore.Qt.Key_V,
    "w": QtCore.Qt.Key_W,
    "x": QtCore.Qt.Key_X,
    "y": QtCore.Qt.Key_Y,
    "z": QtCore.Qt.Key_Z,
    "0": QtCore.Qt.Key_0,
    "1": QtCore.Qt.Key_1,
    "2": QtCore.Qt.Key_2,
    "3": QtCore.Qt.Key_3,
    "4": QtCore.Qt.Key_4,
    "5": QtCore.Qt.Key_5,
    "6": QtCore.Qt.Key_6,
    "7": QtCore.Qt.Key_7,
    "8": QtCore.Qt.Key_8,
    "9": QtCore.Qt.Key_9,
    "f1": QtCore.Qt.Key_F1,
    "f2": QtCore.Qt.Key_F2,
    "f3": QtCore.Qt.Key_F3,
    "f4": QtCore.Qt.Key_F4,
    "f5": QtCore.Qt.Key_F5,
    "f6": QtCore.Qt.Key_F6,
    "f7": QtCore.Qt.Key_F7,
    "f8": QtCore.Qt.Key_F8,
    "f9": QtCore.Qt.Key_F9,
    "f10": QtCore.Qt.Key_F10,
    "f11": QtCore.Qt.Key_F11,
    "f12": QtCore.Qt.Key_F12,
    "left": QtCore.Qt.Key_Left,
    "right": QtCore.Qt.Key_Right,
    "up": QtCore.Qt.Key_Up,
    "down": QtCore.Qt.Key_Down,
    "page_up": QtCore.Qt.Key_PageUp,
    "page_down": QtCore.Qt.Key_PageDown,
    "home": QtCore.Qt.Key_Home,
    "end": QtCore.Qt.Key_End,
    "tab": QtCore.Qt.Key_Tab,
    "backtab": QtCore.Qt.Key_Backtab,
    "backspace": QtCore.Qt.Key_Backspace,
    "insert": QtCore.Qt.Key_Insert,
    "return": QtCore.Qt.Key_Return,
}
supported_buttons = {
    "mouse_left": QtCore.Qt.MouseButton.LeftButton,
    "mouse_right": QtCore.Qt.MouseButton.RightButton,
    "mouse_middle": QtCore.Qt.MouseButton.MiddleButton,
}

class Key:
    """
    A class to represent a key.

    References
    ----------
    .. [1] https://doc.qt.io/qtforpython-6/PySide6/QtCore/Qt.html

    """

    def __init__(self) -> None:
        self.dic_keys = supported_keys
        self.dic_buttons = supported_buttons

    # def key_check ( self, )
