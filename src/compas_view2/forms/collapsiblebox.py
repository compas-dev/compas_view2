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
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

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

        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self.content_area, b"maximumHeight")
        )

        self.toggle_animation.finished.connect(self.update_parent)

    def update_parent(self):
        if self._parent:
            self._parent.set_heights()

    def update_animation(self):
        collapsed_height, content_height = self.get_heights()

        self._collapsed_height = collapsed_height
        self._full_hight = collapsed_height + content_height

        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(100)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(self._full_hight)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(100)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)

    @QtCore.Slot()
    def on_pressed(self):

        self._expanded = self.toggle_button.isChecked()

        if not self._expanded:
            self.update_animation()

        self.toggle_button.setArrowType(
            QtCore.Qt.DownArrow if not self._expanded else QtCore.Qt.RightArrow
        )
        self.toggle_animation.setDirection(
            QtCore.QAbstractAnimation.Forward
            if not self._expanded
            else QtCore.QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def get_heights(self):
        collapsed_height = (
            self.sizeHint().height() - self.content_area.maximumHeight()
        )
        content_height = self._layout.sizeHint().height()
        print(collapsed_height, content_height)
        return collapsed_height, content_height

    def set_heights(self):
        collapsed_height, content_height = self.get_heights()
        print("Setting height", collapsed_height, content_height)
        self.setMinimumHeight(content_height + self._collapsed_height)
        self.setMaximumHeight(content_height + self._collapsed_height)
        self.content_area.setMaximumHeight(content_height + self._collapsed_height)

    def setContentLayout(self, layout):
        self._layout = layout
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)

        self.update_animation()


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
