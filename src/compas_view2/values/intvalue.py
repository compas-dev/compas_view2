from .value import Value


class IntValue(Value):
    def __init__(self, value: int, min: int = None, max: int = None, options: list = None):
        super().__init__(value, int, options=options)
        if min is not None:
            self._check_type(min)
        if max is not None:
            self._check_type(max)
        self._min = min
        self._max = max
        self._check_bounds(value)

    def _check_bounds(self, value):
        if self.min is not None:
            assert value >= self.min, "Value must be greater than {}".format(self.min)
        if self.max is not None:
            assert value <= self.max, "Value must be less than {}".format(self.max)

    def check(self, value):
        super().check(value)
        self._check_bounds(value)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        self._check_type(value)
        self._min = value

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        self._check_type(value)
        self._max = value

    @property
    def data(self):
        data = super().data
        data.update({"min": self.min, "max": self.max})
        return data

    @data.setter
    def data(self, data):
        super().data = data
        self._min = data["min"]
        self._max = data["max"]
