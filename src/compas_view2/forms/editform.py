from PySide2 import QtWidgets

from .form import Form


class EditForm(Form):

    def __init__(self, title, on_update=None):
        super().__init__(title)
        self.on_update = on_update

    def map_number(self, obj, attribute):
        """Map number input field to an object attribute
        """
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(attribute)
        _input = QtWidgets.QDoubleSpinBox()
        _input.setMinimum(float('-inf'))
        _input.setMaximum(float('inf'))
        _input.setValue(getattr(obj, attribute))
        layout.addWidget(label)
        layout.addWidget(_input)
        setattr(self, attribute + "_input", _input)

        def set_number(value):
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
        return QtWidgets.QVBoxLayout()
