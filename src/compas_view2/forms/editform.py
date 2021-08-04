from PySide2 import QtWidgets
from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh
from .collapsiblebox import CollapsibleBox


class EditForm(QtWidgets.QDockWidget):
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

        scroll = QtWidgets.QScrollArea()
        self.setWidget(scroll)
        content = QtWidgets.QWidget()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        vlay = QtWidgets.QVBoxLayout(content)

        self._inputs = vlay
        self.obj = obj
        self.on_update = on_update

        self.add_label(obj._data.__class__)

        self.map_transform(obj)

        if obj.properties:
            cb = self.add_collapsiblebox("Object")
            v_layout = QtWidgets.QVBoxLayout()
            self.map_dict(obj, keys=obj.properties, layout=v_layout)
            cb.setContentLayout(v_layout)

        if hasattr(obj._data, "data"):
            cb = self.add_collapsiblebox("Data")
            v_layout = QtWidgets.QVBoxLayout()
            v_layout._parent = cb
            self.data = obj._data.data
            if type(obj._data) in [Mesh, Network, VolMesh]:
                self.add_label(type(obj._data).__name__, layout=v_layout)
            else:
                self.map_data(self.data, layout=v_layout)
            cb.setContentLayout(v_layout)

        self._inputs.addStretch()

    def add_label(self, text, layout=None):
        if not layout:
            layout = QtWidgets.QHBoxLayout()
            self._inputs.addLayout(layout)
        # layout.setContentsMargins(0, 0, 0, 0)
        label = QtWidgets.QLabel(str(text))
        layout.addWidget(label)

    def add_collapsiblebox(self, name, layout=None):
        if hasattr(layout, "_parent"):
            cb = CollapsibleBox(name, parent=layout._parent)
        else:
            cb = CollapsibleBox(name)
        layout = layout or self._inputs
        layout.addWidget(cb)
        return cb

    def map_transform(self, obj):

        cb = self.add_collapsiblebox("Transform")
        v_layout = QtWidgets.QVBoxLayout()

        self.add_label("translation", layout=v_layout)
        layout = QtWidgets.QHBoxLayout()
        v_layout.addLayout(layout)
        self.map_number(obj.translation, 0, name="x", layout=layout, update_data=False)
        self.map_number(obj.translation, 1, name="y", layout=layout, update_data=False)
        self.map_number(obj.translation, 2, name="z", layout=layout, update_data=False)

        self.add_label("rotation", layout=v_layout)
        layout = QtWidgets.QHBoxLayout()
        v_layout.addLayout(layout)
        self.map_number(obj.rotation, 0, name="x", layout=layout, update_data=False)
        self.map_number(obj.rotation, 1, name="y", layout=layout, update_data=False)
        self.map_number(obj.rotation, 2, name="z", layout=layout, update_data=False)

        self.add_label("scale", layout=v_layout)
        layout = QtWidgets.QHBoxLayout()
        v_layout.addLayout(layout)
        self.map_number(obj.scale, 0, name="x", layout=layout, update_data=False)
        self.map_number(obj.scale, 1, name="y", layout=layout, update_data=False)
        self.map_number(obj.scale, 2, name="z", layout=layout, update_data=False)

        cb.setContentLayout(v_layout)

    def map_data(self, data, name=None, layout=None):
        if name:
            self.add_label(name, layout=layout)
        if isinstance(data, list):
            if isinstance(data[0], float) or isinstance(data[0], int):
                self.map_list(data, layout=layout)
            elif len(data) <= 10 and (isinstance(data[0][0], float) or isinstance(data[0][0], int)):
                self.map_vector_list(data, layout=layout)
            else:
                self.add_label(f"{data[0].__class__.__name__}[{len(data)}]", layout=layout)
        elif isinstance(data, dict):
            self.map_dict(data, layout=layout)
        else:
            raise TypeError("Un-supported data type")

    def map_dict(self, data, keys=None, layout=None):

        if keys:
            for key in keys:
                self.map_number(data, key, layout=layout)
        else:
            for key in data:
                if isinstance(data[key], int) or isinstance(data[key], float):
                    self.map_number(data, key, layout=layout)
                else:
                    cb = self.add_collapsiblebox(key, layout=layout)
                    v_layout = QtWidgets.QVBoxLayout()
                    v_layout._parent = cb
                    self.map_data(data[key], layout=v_layout)
                    cb.setContentLayout(v_layout)

    def map_vector_list(self, _list, layout=None):
        v_layout = QtWidgets.QVBoxLayout()
        v_layout.setContentsMargins(20, 0, 0, 0)
        layout.addLayout(v_layout)
        for i, vector in enumerate(_list):
            self.map_list(vector, name=i, layout=v_layout)

    def map_list(self, _list, name=None, layout=None):
        h_layout = QtWidgets.QHBoxLayout()
        layout = layout or self._inputs
        layout.addLayout(h_layout)
        if name is not None:
            self.add_label(str(name) + ": ", layout=h_layout)
        for i in range(len(_list)):
            self.map_number(_list, i, layout=h_layout)

    def map_number(self, obj, attribute, name=None, layout=None, update_data=True):
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

        # layout.setContentsMargins(0, 0, 0, 0)
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
        return layout

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
