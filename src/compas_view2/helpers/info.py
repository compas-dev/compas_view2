import compas_view2
from . import print
from ..actions.action import supported_keys

from compas_view2.app import App


class Info:
    """Prints the info of this version."""

    def __init__(self):
        self.app = App()
        self.info = {
            "author": compas_view2.__author__,
            "version": compas_view2.__version__,
            "email": compas_view2.__email__,
            "license": compas_view2.__license__,
            "copyright": compas_view2.__copyright__,
            "url": compas_view2.__url__,
            "supported_keys": [str(k) for k in supported_keys().keys()],
            "supported_actions": [str(k) for k in self.app.controller.actions.keys()],
        }
        self.config = self.app.all_config

    def show_info(self):
        for i in self.info:
            print(f"[INFO] {i}: {self.info[i]}")

    def show_config(self):
        print(f"[INFO] current configuration: {self.config}")
