from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton, QCheckBox


class ExecutionControl(QWidget):
    def __init__(self, params):
        self.node, self.node_item = params
        QWidget.__init__(self)

        layout = QHBoxLayout()
        self.setStyleSheet("background: transparent; color: white;")
        self.setLayout(layout)

        self.checkbox = QCheckBox('Auto Update')
        self.checkbox.setStyleSheet("color: white;")
        self.layout().addWidget(self.checkbox)

        self.button = QPushButton('Run')
        self.button.setStyleSheet("background-color: #0092D2;")
        self.layout().addWidget(self.button)

        if self.node.block_updates:
            self.button.setVisible(True)
            self.checkbox.setChecked(False)
        else:
            self.button.setVisible(False)
            self.checkbox.setChecked(True)

        self.button.clicked.connect(self.button_clicked)
        self.checkbox.stateChanged.connect(self.checkbox_clicked)

    def button_clicked(self):
        self.node.update_event()

    def checkbox_clicked(self):
        if self.checkbox.isChecked():
            self.node.enable_auto_update()
            self.button.setVisible(False)
        else:
            self.node.disable_auto_update()
            self.button.setVisible(True)
        self.node_item.update_shape()

    def get_state(self) -> dict:
        data = {}
        return data

    def set_state(self, data: dict):
        pass

    def remove_event(self):
        pass
