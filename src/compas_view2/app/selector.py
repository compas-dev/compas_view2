from random import randint
from compas.utilities import rgb_to_hex
from compas.utilities import hex_to_rgb


class Selector:

    def __init__(self, app):
        self.app = app
        self.color_to_exclude = ['#ffffff', '#000000']
        self.instances = {}
        self.enabled = True
        self.mode = "single"
        self.overwrite_mode = None
        self.types = []
        self.on_finish_selection = None

    def reset(self):
        self.enabled = True
        self.mode = "single"
        self.overwrite_mode = None
        self.types = []
        self.on_finish_selection = None
        self.deselect()

    @property
    def selected(self):
        return [self.instances[key] for key in self.instances if self.instances[key].is_selected]

    def get_hex(self):
        while True:
            unique_hex = '#%02x%02x%02x' % (
                randint(0, 255), randint(0, 255), randint(0, 255))
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

    def select(self, obj=None, mode=None, types=None, update=False):
        mode = mode or self.mode
        types = types or self.types
        if mode == 'single':
            if obj:
                self.deselect()
                obj.is_selected = True
        elif mode == 'multi':
            if not obj:
                return
            if types:
                for _type in types:
                    if isinstance(obj._data, _type):
                        obj.is_selected = True
            else:
                obj.is_selected = True
        elif mode == 'deselect':
            self.deselect(obj)
        else:
            raise NotImplementedError
        if update:
            self.app.view.update()

    def deselect(self, obj=None, update=False):
        if obj:
            obj.is_selected = False
        else:
            for key in self.instances:
                self.instances[key].is_selected = False
        if update:
            self.app.view.update()

    def start_selection(self, types=None, on_finish_selection=None, mode="multi"):
        if not isinstance(types, list):
            types = [types]
        self.enabled = True
        self.deselect(update=True)
        self.mode = self.overwrite_mode = mode
        self.types = types
        self.on_finish_selection = on_finish_selection

    def finish_selection(self):
        if self.on_finish_selection:
            selected_data = [obj._data for obj in self.selected]
            self.on_finish_selection(selected_data)
        self.reset()
