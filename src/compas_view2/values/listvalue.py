from .value import Value


class ListValue(Value):
    def __init__(self, value: list, list_value_type: type):
        super().__init__(value, list)
        self._list_value_type = list_value_type
        self._check_list_value_type(value)

    def _check_list_value_type(self, value):
        for i, item in enumerate(value):
            assert isinstance(item, self.list_value_type), "List item {}:{} is not of type {}".format(
                i, item, self.list_value_type
            )

    def check(self, value):
        super().check(value)
        self._check_list_value_type(value)

    @property
    def list_value_type(self):
        return self._list_value_type

    @property
    def data(self):
        data = super().data
        data.update(
            {
                "list_value_type": self.list_value_type.__name__,
            }
        )
        return data

    @data.setter
    def data(self, data):
        super().data = data
        self._list_value_type = eval(data["list_value_type"])
