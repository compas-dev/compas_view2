from random import randint
from compas.utilities import rgb_to_hex
from compas.utilities import hex_to_rgb

class Selector():

    def __init__(self, app):
        self.app = app
        self.color_to_exclude = ['#ffffff', '#000000']
        self.instances = {}
        self.enabled = True

    def get_hex(self):
        while True:
            unique_hex = '#%02x%02x%02x' % (randint(0, 255), randint(0, 255), randint(0, 255))
            if unique_hex not in self.instances and unique_hex not in self.color_to_exclude:
                return unique_hex

    def add(self, obj):
        unique_hex = self.get_hex()
        self.instances[unique_hex] = obj
        obj.instance_color = hex_to_rgb(unique_hex, normalize=True)
        return unique_hex

    def find(self, x, y, instance_map):
        rgb = instance_map[y][x]
        hex_key = rgb_to_hex(rgb)
        if hex_key in self.instances:
            return self.instances[hex_key]
        else:
            return None

    def select(self, obj=None, mode="single"):

        if mode == "single":
            for key in self.instances:
                self.instances[key].is_selected = False
            if obj:
                self.app.statusbar.showMessage("Picked: " + obj.__repr__())
                obj.is_selected = True
                print(self.selected)
            else:
                self.app.statusbar.showMessage("")

    @property
    def selected(self):
        return [self.instances[key] for key in self.instances if self.instances[key].is_selected]