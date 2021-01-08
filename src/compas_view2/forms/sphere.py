from PySide2 import QtWidgets
from PySide2 import QtGui


class SphereForm(QtWidgets.QDialog):

    def __init__(self):
        super().__init__(f=QtGui.Qt.WindowTitleHint | QtGui.Qt.WindowSystemMenuHint)
        self.setWindowTitle('Add Sphere')
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        # inputs
        inputs = QtWidgets.QVBoxLayout()
        # inputs: radius
        radius_layout = QtWidgets.QHBoxLayout()
        radius_label = QtWidgets.QLabel('Radius')
        self.radius_input = QtWidgets.QLineEdit()
        self.radius_input.setValidator(QtGui.QDoubleValidator())
        self.radius_input.setText('1.0')
        radius_layout.addWidget(radius_label)
        radius_layout.addWidget(self.radius_input)
        inputs.addLayout(radius_layout)
        # inputs: UV
        uv_layout = QtWidgets.QHBoxLayout()
        u_label = QtWidgets.QLabel('U')
        self.u_input = QtWidgets.QLineEdit()
        self.u_input.setValidator(QtGui.QIntValidator())
        self.u_input.setText('16')
        uv_layout.addWidget(u_label)
        uv_layout.addWidget(self.u_input)
        v_label = QtWidgets.QLabel('V')
        self.v_input = QtWidgets.QLineEdit()
        self.v_input.setValidator(QtGui.QIntValidator())
        self.v_input.setText('16')
        uv_layout.addWidget(v_label)
        uv_layout.addWidget(self.v_input)
        inputs.addLayout(uv_layout)
        # buttons
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addLayout(inputs)
        layout.addWidget(buttons)

    def accept(self):
        return super().accept()

    def reject(self):
        return super().reject()

    @property
    def radius(self):
        return float(self.radius_input.text())

    @property
    def u(self):
        return int(self.u_input.text())

    @property
    def v(self):
        return int(self.v_input.text())
