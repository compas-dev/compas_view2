from PySide2 import QtCore, QtGui, QtWidgets


class CollapsibleBox(QtWidgets.QWidget):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)

        self._parent = parent
        self._expanded = False
        self.toggle_button = QtWidgets.QToolButton(
            text=title, checkable=True, checked=False
        )
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon
        )
        self.toggle_button.setIconSize(QtCore.QSize(8, 8))
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.content_area = QtWidgets.QScrollArea(
            maximumHeight=0, minimumHeight=0
        )
        self.content_area.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        # self.content_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

    def update_parent(self):
        if self._parent:
            self._parent.expand()
            self._parent.update_parent()

    def on_pressed(self):
        self._expanded = not self.toggle_button.isChecked()
        if self._expanded:
            self.expand()
        else:
            self.collapse()
        self.update_parent()

    def get_content_height(self):
        return self._layout.sizeHint().height()

    def setContentLayout(self, layout):
        self._layout = layout
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        self._collapsed_height = self.sizeHint().height()

    def expand(self):
        self.toggle_button.setArrowType(QtCore.Qt.DownArrow)
        self.setFixedHeight(self._collapsed_height + self.get_content_height())
        self.content_area.setMaximumHeight(self.get_content_height())

    def collapse(self):
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.setFixedHeight(self._collapsed_height)
        self.content_area.setMaximumHeight(0)


if __name__ == "__main__":
    import sys
    import random

    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QMainWindow()
    w.setCentralWidget(QtWidgets.QWidget())
    dock = QtWidgets.QDockWidget("Collapsible Demo")
    w.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
    scroll = QtWidgets.QScrollArea()
    dock.setWidget(scroll)
    content = QtWidgets.QWidget()
    scroll.setWidget(content)
    scroll.setWidgetResizable(True)
    vlay = QtWidgets.QVBoxLayout(content)

    def create_box(name, parent=None):
        box = CollapsibleBox(name, parent=parent)
        lay = QtWidgets.QVBoxLayout()
        for j in range(8):
            label = QtWidgets.QLabel("{}".format(j))
            color = QtGui.QColor(*[random.randint(0, 255) for _ in range(3)])
            label.setStyleSheet(
                "background-color: {}; color : white;".format(color.name())
            )
            label.setAlignment(QtCore.Qt.AlignCenter)
            lay.addWidget(label)
        box.setContentLayout(lay)
        return box

    box = create_box("Outer box")
    box._layout.addWidget(create_box("Interior box", box))
    vlay.addWidget(box)

    vlay.addStretch()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())
