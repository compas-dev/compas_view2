from PySide2 import QtWidgets

from .form import Form


class PointForm(Form):

    def __init__(self):
        super().__init__(title='Add Point')

    def inputs(self):
        inputs = QtWidgets.QVBoxLayout()
        # inputs: X
        x_layout = QtWidgets.QHBoxLayout()
        x_label = QtWidgets.QLabel('X')
        self.x_input = QtWidgets.QDoubleSpinBox()
        self.x_input.setValue(0.0)
        x_layout.addWidget(x_label)
        x_layout.addWidget(self.x_input)
        inputs.addLayout(x_layout)
        # inputs: Y
        y_layout = QtWidgets.QHBoxLayout()
        y_label = QtWidgets.QLabel('Y')
        self.y_input = QtWidgets.QDoubleSpinBox()
        self.y_input.setValue(0.0)
        y_layout.addWidget(y_label)
        y_layout.addWidget(self.y_input)
        inputs.addLayout(y_layout)
        # inputs: Z
        z_layout = QtWidgets.QHBoxLayout()
        z_label = QtWidgets.QLabel('Z')
        self.z_input = QtWidgets.QDoubleSpinBox()
        self.z_input.setValue(0.0)
        z_layout.addWidget(z_label)
        z_layout.addWidget(self.z_input)
        inputs.addLayout(z_layout)
        return inputs

    @property
    def x(self):
        return float(self.x_input.value())

    @property
    def y(self):
        return float(self.y_input.value())

    @property
    def z(self):
        return float(self.z_input.value())
