from PySide2 import QtWidgets

from .form import Form


class TorusForm(Form):

    def __init__(self):
        super().__init__(title='Add Torus')

    def inputs(self):
        # inputs
        inputs = QtWidgets.QVBoxLayout()
        # inputs: radius
        size_layout = QtWidgets.QHBoxLayout()
        # radius
        radius_label = QtWidgets.QLabel('Radius')
        self.radius_input = QtWidgets.QDoubleSpinBox()
        self.radius_input.setValue(1.0)
        size_layout.addWidget(radius_label)
        size_layout.addWidget(self.radius_input)
        # tube
        tube_label = QtWidgets.QLabel('Tube')
        self.tube_input = QtWidgets.QDoubleSpinBox()
        self.tube_input.setValue(1.0)
        size_layout.addWidget(tube_label)
        size_layout.addWidget(self.tube_input)
        inputs.addLayout(size_layout)
        # inputs: UV
        uv_layout = QtWidgets.QHBoxLayout()
        # U
        u_label = QtWidgets.QLabel('U')
        self.u_input = QtWidgets.QSpinBox()
        self.u_input.setValue(16)
        self.u_input.setSingleStep(4)
        uv_layout.addWidget(u_label)
        uv_layout.addWidget(self.u_input)
        # V
        v_label = QtWidgets.QLabel('V')
        self.v_input = QtWidgets.QSpinBox()
        self.v_input.setValue(16)
        self.v_input.setSingleStep(4)
        uv_layout.addWidget(v_label)
        uv_layout.addWidget(self.v_input)
        inputs.addLayout(uv_layout)
        return inputs

    @property
    def radius(self):
        return float(self.radius_input.value())

    @property
    def tube(self):
        return float(self.tube_input.value())

    @property
    def u(self):
        return int(self.u_input.value())

    @property
    def v(self):
        return int(self.v_input.value())
