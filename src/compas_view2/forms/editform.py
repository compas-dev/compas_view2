from PySide2 import QtWidgets
from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh
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
            if type(obj._data) in [Mesh, Network, VolMesh]:
                self.add_label("data")
                self.add_label(type(obj._data).__name__, indent=1)
            else:
                self.map_data(self.data)

    def add_label(self, text, indent=0, layout=None):
        if not layout:
            layout = QtWidgets.QHBoxLayout()
            self._inputs.addLayout(layout)
        layout.setContentsMargins(indent*20, 0, 0, 0)
        label = QtWidgets.QLabel(str(text))
        layout.addWidget(label)

    def map_transform(self, obj):
        self.add_label("translation")
        layout = QtWidgets.QHBoxLayout()
        self._inputs.addLayout(layout)
        self.map_number(obj.translation, 0, name="x", layout=layout, update_data=False)
        self.map_number(obj.translation, 1, name="y", layout=layout, update_data=False)
        self.map_number(obj.translation, 2, name="z", layout=layout, update_data=False)

        self.add_label("rotation")
        layout = QtWidgets.QHBoxLayout()
        self._inputs.addLayout(layout)
        self.map_number(obj.rotation, 0, name="x", layout=layout, update_data=False)
        self.map_number(obj.rotation, 1, name="y", layout=layout, update_data=False)
        self.map_number(obj.rotation, 2, name="z", layout=layout, update_data=False)

        self.add_label("scale")
        layout = QtWidgets.QHBoxLayout()
        self._inputs.addLayout(layout)
        self.map_number(obj.scale, 0, name="x", layout=layout, update_data=False)
        self.map_number(obj.scale, 1, name="y", layout=layout, update_data=False)
        self.map_number(obj.scale, 2, name="z", layout=layout, update_data=False)

    def map_data(self, data, name="data", indent=0):
        self.add_label(name, indent=indent)
        if isinstance(data, list):
            if isinstance(data[0], float) or isinstance(data[0], int):
                self.map_list(data, indent=indent+1)
            elif len(data) <= 10 and (isinstance(data[0][0], float) or isinstance(data[0][0], int)):
                self.map_vector_list(data, indent=indent+1)
            else:
                self.add_label(
                    f"{data[0].__class__.__name__}[{len(data)}]",
                    indent=indent + 1)
        elif isinstance(data, dict):
            self.map_dict(data, indent=indent+1)
        else:
            raise TypeError("Un-supported data type")

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

    def map_vector_list(self, _list, indent=1):
        for i, vector in enumerate(_list):
            self.map_list(vector, name=i, indent=indent)

    def map_list(self, _list, name=None, indent=1):
        layout = QtWidgets.QHBoxLayout()
        self._inputs.addLayout(layout)
        if name is not None:
            self.add_label(str(name) + ": ", indent=indent, layout=layout)
        for i in range(len(_list)):
            self.map_number(_list, i, indent=indent, layout=layout)

    def map_number(self, obj, attribute, name=None, indent=1, layout=None, update_data=True):
        """Map number input field to an object attribute

        Parameters
        ----------
        obj: Object
            object to be edited
        attribute: string
            the name of attribute to be mapped

        Returns
        -------
        None
        """
        if not layout:
            layout = QtWidgets.QHBoxLayout()
            self._inputs.addLayout(layout)

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

            if update_data:
                self.obj.update()
            else:
                self.obj._update_matrix()

            if self.on_update:
                self.on_update()

        _input.valueChanged.connect(set_number)

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
