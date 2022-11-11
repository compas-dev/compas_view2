from .value import Value


class StrValue(Value):
    def __init__(self, value: str, options: list = None):
        super().__init__(value, str, options=options)
