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
        if obj.editables:
            self.add_label("data")
            for key in obj.editables:
                if obj.editables[key]["type"] == "number":
                    self.map_number(obj._data, key)

    def add_label(self, text):
        layout = QtWidgets.QHBoxLayout()
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

    def map_number(self, obj, attribute, name=None):
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
        layout.setContentsMargins(20, 0, 0, 0)
        label = QtWidgets.QLabel(name or str(attribute))
        _input = QtWidgets.QDoubleSpinBox()
        _input.setMinimum(float('-inf'))
        _input.setMaximum(float('inf'))
        if isinstance(obj, list):
            _input.setValue(obj[attribute])
        else:
            _input.setValue(getattr(obj, attribute))
        layout.addWidget(label)
        layout.addWidget(_input)

        def set_number(value):
            if isinstance(obj, list):
                obj[attribute] = value
            else:
                setattr(obj, attribute, value)
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
