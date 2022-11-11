from compas.data import Data


class Value(Data):
    def __init__(self, value, value_type: type, options=None):
        super().__init__()
        self._value = value
        self._value_type = value_type
        self._check_type(value)

        self._options = None
        if options is not None:
            self.options = options

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.value)

    def _check_type(self, value):
        assert type(value) == self.value_type, "{} is not of type {}".format(value, self.value_type)

    def _check_options(self, value):
        if self.options is not None:
            assert value in self.options, "Value must be one of {}".format(self.options)

    def check(self, value):
        self._check_type(value)
        self._check_options(value)

    def cast(self, value):
        try:
            return self.value_type(value)
        except ValueError:
            raise ValueError("Cannot cast {} to {}".format(value, self.value_type))

    def set(self, value, raise_error=True, cast=True):
        try:
            if cast:
                value = self.cast(value)
            self.value = value
            return True
        except (AssertionError, ValueError) as e:
            if raise_error:
                raise e
            else:
                return e

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.check(value)
        self._value = value

    @property
    def value_type(self):
        return self._value_type

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options):
        assert type(options) == list, "Options must be a list"
        for option in options:
            self._check_type(option)
        self._options = options

    @property
    def data(self):
        return {
            "value": self.value,
            "value_type": self.value_type.__name__,
            "options": self.options,
        }

    @data.setter
    def data(self, data):
        self._value = data["value"]
        self._value_type = eval(data["value_type"])  # TODO: support imported types
        self._options = data["options"]
