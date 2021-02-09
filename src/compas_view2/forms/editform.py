from PySide2 import QtWidgets

from .form import Form


class EditForm(Form):

    def map_number(self, obj, attribute):
        """Map number input field to an object attribute
        """
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(attribute)
        _input = QtWidgets.QDoubleSpinBox()
        _input.setValue(0.0)
        layout.addWidget(label)
        layout.addWidget(_input)
        setattr(self, attribute + "_input", _input)

        def set_number(value):
            setattr(obj, attribute, value)
            print("set {} to {}".format(attribute, value))
            # then update object and view

        _input.valueChanged.connect(set_number)
        self._inputs.addLayout(layout)

    def map_color(self, obj, attribute):
        """Map color input field to an object attribute
        """
        raise NotImplementedError()

    def inputs(self):
        return QtWidgets.QVBoxLayout()
