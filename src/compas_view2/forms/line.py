from PySide2 import QtWidgets, QtCore

from .form import Form


class LineForm(Form):

    def __init__(self):
        super().__init__(title='Add Line')

    def float_field(self, text, value, layout=None, parent=None):
        if not layout:
            layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(text)
        field = QtWidgets.QDoubleSpinBox()
        field.setValue(value)
        layout.addWidget(label)
        layout.addWidget(field)
        if parent:
            parent.addLayout(layout)
        return field

    def inputs(self):
        inputs = QtWidgets.QVBoxLayout()
        points = QtWidgets.QHBoxLayout()
        # point A
        A_group = QtWidgets.QGroupBox('Point A')
        A_layout = QtWidgets.QVBoxLayout()
        A_group.setLayout(A_layout)
        self.Ax_input = self.float_field('X', 0.0, parent=A_layout)
        self.Ay_input = self.float_field('Y', 0.0, parent=A_layout)
        self.Az_input = self.float_field('Z', 0.0, parent=A_layout)
        # point B
        B_group = QtWidgets.QGroupBox('Point B')
        B_layout = QtWidgets.QVBoxLayout()
        B_group.setLayout(B_layout)
        self.Bx_input = self.float_field('X', 0.0, parent=B_layout)
        self.By_input = self.float_field('Y', 0.0, parent=B_layout)
        self.Bz_input = self.float_field('Z', 0.0, parent=B_layout)
        # show points
        self.show_points_input = QtWidgets.QCheckBox('Show Points')
        self.show_points_input.setCheckState(QtCore.Qt.Checked)
        # combine
        points.addWidget(A_group)
        points.addWidget(B_group)
        inputs.addLayout(points)
        inputs.addWidget(self.show_points_input)
        return inputs

    @property
    def Ax(self):
        return float(self.Ax_input.value())

    @property
    def Ay(self):
        return float(self.Ay_input.value())

    @property
    def Az(self):
        return float(self.Az_input.value())

    @property
    def Bx(self):
        return float(self.Bx_input.value())

    @property
    def By(self):
        return float(self.By_input.value())

    @property
    def Bz(self):
        return float(self.Bz_input.value())

    @property
    def show_points(self):
        return bool(self.show_points_input.checkState())
