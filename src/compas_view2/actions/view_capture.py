from qtpy import QtWidgets
from .action import Action
from pathlib import Path


class ViewCapture(Action):
    """Capture a screenshot. A file dialog will be be opened automatically.

    Returns
    -------
    None

    """

    def __init__(self, Controller, keys):
        super().__init__(Controller, keys)

    def pressed_action(self):
        result = QtWidgets.QFileDialog.getSaveFileName(caption="File name", dir="")
        result = result[0]
        filepath = Path(result)
        if not filepath.suffix:
            return
        qimage = self.controller.app.view.grabFramebuffer()
        qimage.save(str(filepath), filepath.suffix[1:])
        print(f"Screenshot saved to {filepath}")

    def keys_pressed_action(self):
        """This is overwriting is specially for this `ViewCapture` action.
        As this action calls external file dialog, and blocks the release event.

        """
        self.pressed_action()
        self.to_released_status()
