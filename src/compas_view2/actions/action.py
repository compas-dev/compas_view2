from qtpy import QtCore


def supported_keys():
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
        ".": QtCore.Qt.Key_Period,
        "placeholder": None,
    }
    return supported_keys


class Action:
    """The main class for all the actions. Actions are some operations that are trigger by the key(s). The `Controller`class invokes all the actions. Typical actions are `zoom_selected`, `view_lighted`, etc."""

    def __init__(self, Controller, keys: list[str]):
        if keys is None:
            keys = "placeholder"

        self.supported_keys = supported_keys()
        for key in keys:
            if key not in self.supported_keys:
                raise KeyError(f"Key {key} is not supported.")

        self.keys = keys
        self.controller = Controller
        self.key_status = Controller.key_status

    def keys_pressed_check(self, event):
        """Check if all the keys are pressed.

        Parameters
        ----------
        event: QKeyEvent.

        Returns
        ----------
        bool:
            If all the keys are pressed.
        """
        for key in self.keys:
            if key not in self.key_status:
                self.key_status[key] = False
            if event.key() == self.supported_keys[key]:
                self.key_status[key] = True
            else:
                if self.key_status[key] is False:
                    return False
        return True

    def keys_released_check(self, event):
        """Check if all the keys are released.

        Parameters
        ----------
        event: QKeyEvent.

        Returns
        ----------
        bool:
            If all the keys are released.
        """
        for key in self.keys:
            if key not in self.key_status:
                self.key_status[key] = True
            if event.key() == self.supported_keys[key]:
                self.key_status[key] = False
            else:
                if self.key_status[key] is True:
                    return True
        return False

    def keys_pressed_action(self):
        self.pressed_action()
        self.to_pressed_status()

    def pressed_action(self):
        pass

    def to_pressed_status(self):
        for key in self.keys:
            self.key_status[key] = True

    def keys_released_action(self):
        self.released_action()
        self.to_released_status()

    def released_action(self):
        pass

    def to_released_status(self):
        for key in self.keys:
            self.key_status[key] = False

    def ui_action(self):
        self.keys_pressed_action()
        self.keys_released_action()
