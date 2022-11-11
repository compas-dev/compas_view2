import numpy as np
from qtpy import QtWidgets

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh
from compas.colors import Color
from .collapsiblebox import CollapsibleBox


class PropertyForm(QtWidgets.QDockWidget):
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

    def __init__(self, title, obj=None, on_update=None):
        super().__init__(title)

        if obj:
            self.set_object(obj, on_update)
        elif on_update:
            self.on_update = on_update

    def set_object(self, obj, on_update=None):
        scroll = QtWidgets.QScrollArea()
        self.setWidget(scroll)
        content = QtWidgets.QWidget()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        self._inputs = QtWidgets.QVBoxLayout(content)
        self.obj = obj
        if on_update:
            self.on_update = on_update

        # Show object class
        self.add_label(obj.name)
        self.add_label(obj._data.__class__)

        # Map object transform
        self.map_transform(obj)

        # Map object visualisation settings
        cb = self.add_collapsiblebox("Visualisation")
        v_layout = QtWidgets.QVBoxLayout()
        v_layout._parent = cb

        cb.setContentLayout(v_layout)
        self.map_object(obj, obj.visualisation, layout=v_layout)

        # Map custom object properties
        if obj.properties:
            cb = self.add_collapsiblebox("Object")
            v_layout = QtWidgets.QVBoxLayout()
            v_layout._parent = cb
            self.map_object(obj, obj.properties, layout=v_layout, update_data=True)
            cb.setContentLayout(v_layout)

        # Map object data
        if hasattr(obj._data, "data"):
            cb = self.add_collapsiblebox("Data")
            v_layout = QtWidgets.QVBoxLayout()
            v_layout._parent = cb
            self.data = obj._data.data
            if type(obj._data) in [Mesh, Network, VolMesh]:
                self.add_label(type(obj._data).__name__, layout=v_layout)
            else:
                self.map_inputs(self.data, layout=v_layout, update_data=True)
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
        """Map the transformation of an object"""
        cb = self.add_collapsiblebox("Transform")
        v_layout = QtWidgets.QVBoxLayout()

        self.add_label("translation", layout=v_layout)
        layout = QtWidgets.QHBoxLayout()
        v_layout.addLayout(layout)
        self.map_number(obj.translation, 0, name="x", layout=layout)
        self.map_number(obj.translation, 1, name="y", layout=layout)
        self.map_number(obj.translation, 2, name="z", layout=layout)

        self.add_label("rotation", layout=v_layout)
        layout = QtWidgets.QHBoxLayout()
        v_layout.addLayout(layout)
        self.map_number(obj.rotation, 0, name="x", layout=layout)
        self.map_number(obj.rotation, 1, name="y", layout=layout)
        self.map_number(obj.rotation, 2, name="z", layout=layout)

        self.add_label("scale", layout=v_layout)
        layout = QtWidgets.QHBoxLayout()
        v_layout.addLayout(layout)
        self.map_number(obj.scale, 0, name="x", layout=layout)
        self.map_number(obj.scale, 1, name="y", layout=layout)
        self.map_number(obj.scale, 2, name="z", layout=layout)

        cb.setContentLayout(v_layout)

    def map_inputs(self, data, name=None, layout=None, update_data=False):
        """Map inputs of supported data type"""
        if name:
            self.add_label(name, layout=layout)
        if isinstance(data, (list, np.ndarray)):
            if isinstance(data[0], (float, int)):
                self.map_list(data, layout=layout, update_data=update_data)
            elif len(data) <= 10 and isinstance(data[0][0], (float, int)):
                self.map_vector_list(data, layout=layout, update_data=update_data)
            else:
                self.add_label(f"{data[0].__class__.__name__}[{len(data)}]", layout=layout)
        elif isinstance(data, Color):
            self.map_color(data, layout=layout, update_data=update_data)
        elif isinstance(data, dict):
            self.map_dict(data, layout=layout, update_data=update_data)
        else:
            raise TypeError("Un-supported data type")

    def map_object(self, data, attrs, layout=None, update_data=False):
        """Map the attributs of an object"""
        for attr in attrs:
            attribute = getattr(data, attr)
            if isinstance(attribute, bool):
                self.map_bool(data, attr, layout=layout, update_data=update_data)
            elif isinstance(attribute, (int, float)):
                self.map_number(data, attr, layout=layout, update_data=update_data)
            else:
                cb = self.add_collapsiblebox(attr, layout=layout)
                v_layout = QtWidgets.QVBoxLayout()
                v_layout._parent = cb
                self.map_inputs(attribute, layout=v_layout, update_data=update_data)
                cb.setContentLayout(v_layout)

    def map_dict(self, data, layout=None, update_data=False):
        """Map a dictionary input"""
        for key in data:
            if isinstance(data[key], (float, int)):
                self.map_number(data, key, layout=layout, update_data=update_data)
            else:
                cb = self.add_collapsiblebox(key, layout=layout)
                v_layout = QtWidgets.QVBoxLayout()
                v_layout._parent = cb
                self.map_inputs(data[key], layout=v_layout, update_data=update_data)
                cb.setContentLayout(v_layout)

    def map_vector_list(self, _list, layout=None, update_data=False):
        """Map a list of vetors"""
        v_layout = QtWidgets.QVBoxLayout()
        v_layout.setContentsMargins(20, 0, 0, 0)
        layout.addLayout(v_layout)
        for i, vector in enumerate(_list):
            self.map_list(vector, name=i, layout=v_layout, update_data=update_data)

    def map_list(self, _list, name=None, layout=None, update_data=False):
        """Map a list of numbers"""
        h_layout = QtWidgets.QHBoxLayout()
        layout = layout or self._inputs
        layout.addLayout(h_layout)
        if name is not None:
            self.add_label(str(name) + ": ", layout=h_layout)
        for i in range(len(_list)):
            self.map_number(_list, i, layout=h_layout, update_data=update_data)

    def map_number(
        self,
        obj,
        attribute,
        name=None,
        layout=None,
        update_data=False,
        minimum=float("-inf"),
        maximum=float("inf"),
        step=None,
    ):
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
        if type(obj) in [list, dict, np.ndarray]:
            value = obj[attribute]
        else:
            value = getattr(obj, attribute)
        if isinstance(value, float):
            _input = QtWidgets.QDoubleSpinBox()
            _input.setSingleStep(0.1)
            _input.setMinimum(minimum)
            _input.setMaximum(maximum)
        elif isinstance(value, int):
            _input = QtWidgets.QSpinBox()
            if minimum == float("-inf"):
                minimum = -(10**9)
            if maximum == float("inf"):
                maximum = 10**9
            _input.setMinimum(minimum)
            _input.setMaximum(maximum)
        else:
            raise ValueError()
        if step:
            _input.setSingleStep(step)
        _input.setValue(value)
        layout.addWidget(label)
        layout.addWidget(_input)

        def set_number(value):
            if type(obj) in [list, dict, np.ndarray]:
                obj[attribute] = value
            else:
                setattr(obj, attribute, value)
            self.update(update_data)

        _input.valueChanged.connect(set_number)
        return layout

    def map_color(self, color, layout=None, update_data=False):
        """Map color input field to an object attribute"""
        h_layout = QtWidgets.QHBoxLayout()
        layout = layout or self._inputs
        layout.addLayout(h_layout)
        for channel in ["r", "g", "b"]:
            self.map_number(color, channel, layout=h_layout, update_data=update_data, minimum=0, maximum=1, step=0.01)

    def map_bool(self, obj, attribute, name=None, layout=None, update_data=False):
        """Map color input field to an object attribute"""
        if not layout:
            layout = QtWidgets.QHBoxLayout()
            self._inputs.addLayout(layout)

        if type(obj) in [list, dict, np.ndarray]:
            value = obj[attribute]
        else:
            value = getattr(obj, attribute)
        _input = QtWidgets.QCheckBox(name or str(attribute))
        _input.setChecked(value)
        layout.addWidget(_input)

        def set_bool(value):
            if type(obj) in [list, dict, np.ndarray]:
                obj[attribute] = value
            else:
                setattr(obj, attribute, value)
            self.update(update_data)

        _input.stateChanged.connect(set_bool)
        return layout

    def update(self, update_data):
        if update_data:
            if hasattr(self, "data"):
                try:
                    self.obj._data.data = self.data
                except Exception as e:
                    print(e)
                    print("Failed to update data of", self.obj)
            self.obj.update()
        else:
            self.obj._update_matrix()

        if self.on_update:
            self.on_update()

    def inputs(self):
        """Creates layout for input fields

        Returns
        -------
        QtWidgets.QVBoxLayout
        """
        return QtWidgets.QVBoxLayout()
