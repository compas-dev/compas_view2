from .value import Value


class BoolValue(Value):
    def __init__(self, value: bool):
        super().__init__(value, bool)
