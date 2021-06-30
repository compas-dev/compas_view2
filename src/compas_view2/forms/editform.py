from PySide2 import QtWidgets

from .form import Form


class EditForm(Form):
    """Form class for real-time editing of objects

    Parameters
    ----------
    title: string
        The title of the form

    Attributes
    ----------
    on_update: function
        the function to be called when object attributes are updated from the form
    """

    def __init__(self, title, obj, on_update=None):
        super().__init__(title)
        self.on_update = on_update
        self.map_transform(obj)

        if obj.properties:
            self.map_dict(obj, keys=obj.properties)

        self.obj = obj
        if hasattr(obj._data, "data"):
            self.data = obj._data.data
            self.map_data(self.data)

    def add_label(self, text, indent=0):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(indent*20, 0, 0, 0)
        label = QtWidgets.QLabel(text)
        layout.addWidget(label)
        self._inputs.addLayout(layout)

    def map_transform(self, obj):
        self.add_label("translation")
        self.map_number(obj.translation, 0, name="x")
        self.map_number(obj.translation, 1, name="y")
        self.map_number(obj.translation, 2, name="z")

        self.add_label("rotation")
        self.map_number(obj.rotation, 0, name="x")
        self.map_number(obj.rotation, 1, name="y")
        self.map_number(obj.rotation, 2, name="z")

        self.add_label("scale")
        self.map_number(obj.scale, 0, name="x")
        self.map_number(obj.scale, 1, name="y")
        self.map_number(obj.scale, 2, name="z")

    def map_data(self, data, name="data", indent=0):
        self.add_label(name, indent=indent)
        if isinstance(data, list):
            if isinstance(data[0], float) or isinstance(data[0], int):
                self.map_list(data, indent=indent+1)
            else:
                self.add_label(f"{data[0].__class__.__name__}[{len(data)}]", indent=indent+1)
        elif isinstance(data, dict):
            if data.get("datatype") and data.get("compas"):
                self.map_schema(data, indent+1)
            else:
                self.map_dict(data, indent=indent+1)

    def map_schema(self, data, indent=0):
        self.add_label(data['datatype'], indent=indent)

    def map_dict(self, data, keys=None, indent=0):

        if keys:
            for key in keys:
                self.map_number(data, key, indent=indent)
        else:
            for key in data:
                if isinstance(data[key], int) or isinstance(data[key], float):
                    self.map_number(data, key, indent=indent)
                else:
                    self.map_data(data[key], name=key, indent=indent)

    def map_list(self, _list, name=None, indent=1):
        if name:
            self.add_label(name)
        for i in range(len(_list)):
            self.map_number(_list, i, indent=indent)

    def map_number(self, obj, attribute, name=None, indent=1):
        """Map number input field to an object attribute

        Parameters
        ----------
        obj: compas_view2.objects.Object
            object to be edited
        attribute: string
            the name of attribute to be mapped

        Returns
        -------
        None
        """
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(indent*20, 0, 0, 0)
        label = QtWidgets.QLabel(name or str(attribute))
        if isinstance(obj, list) or isinstance(obj, dict):
            value = obj[attribute]
        else:
            value = getattr(obj, attribute)
        if isinstance(value, float):
            _input = QtWidgets.QDoubleSpinBox()
            _input.setMinimum(float('-inf'))
            _input.setMaximum(float('inf'))
        elif isinstance(value, int):
            _input = QtWidgets.QSpinBox()
        else:
            raise ValueError()
        _input.setValue(value)
        layout.addWidget(label)
        layout.addWidget(_input)

        def set_number(value):
            if isinstance(obj, list) or isinstance(obj, dict):
                obj[attribute] = value
            else:
                setattr(obj, attribute, value)

            if hasattr(self, "data"):
                self.obj._data.data = self.data

            if self.on_update:
                self.on_update()

        _input.valueChanged.connect(set_number)
        self._inputs.addLayout(layout)

    def map_color(self, obj, attribute):
        """Map color input field to an object attribute
        """
        raise NotImplementedError()

    def inputs(self):
        """Creates layout for input fields

        Returns
        -------
        QtWidgets.QVBoxLayout
        """
        return QtWidgets.QVBoxLayout()
