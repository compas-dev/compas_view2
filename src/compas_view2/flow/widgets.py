from qtpy.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QCheckBox, QLabel


class ExecutionControl(QWidget):
    """Main widget to control and monitor the execution of node."""

    def __init__(self, params):
        self.node, self.node_item = params
        QWidget.__init__(self)

        layout = QVBoxLayout()
        self.setStyleSheet("background: transparent; color: white;")
        self.setLayout(layout)

        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        self.checkbox = QCheckBox("Auto Update")
        self.checkbox.setStyleSheet("color: white;")
        h_layout.addWidget(self.checkbox)

        self.button = QPushButton("Run")
        self.button.setStyleSheet("background-color: #0092D2;")
        h_layout.addWidget(self.button)

        self.message = QLabel()
        self.message.setMaximumWidth(200)
        layout.addWidget(self.message)
        self.set_message()

        self.pause_event = False

        if self.node.block_updates:
            self.button.setVisible(True)
            self.checkbox.setChecked(False)
        else:
            self.button.setVisible(False)
            self.checkbox.setChecked(True)

        self.button.clicked.connect(self.update_node)
        self.checkbox.stateChanged.connect(self.set_auto_update)

    def set_message(self, message=None):
        if message:
            self.message.setText(message)
            self.message.setVisible(True)
        else:
            self.message.setVisible(False)

    def set_auto_update(self, _, value=None, update_node=True):

        if self.pause_event:
            return

        if value is not None:
            self.pause_event = True
            self.checkbox.setChecked(value)
            self.pause_event = False

        auto_update = self.checkbox.isChecked()
        self.node.block_updates = not auto_update
        self.button.setVisible(not auto_update)
        self.node_item.update_shape()

        if update_node and auto_update:
            self.update_node()

    def update_node(self):
        self.node.update_event()

    def get_state(self) -> dict:
        data = {}
        return data

    def set_state(self, data: dict):
        pass

    def remove_event(self):
        pass
