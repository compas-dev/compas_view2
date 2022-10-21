from .value import Value
from .dictvalue import DictValue


class Settings(DictValue):
    def __init__(self, settings: dict):
        super().__init__(settings, Value)

    def __getitem__(self, key):
        return self.value[key].value

    def __setitem__(self, key, value):
        self.value[key].value = value
