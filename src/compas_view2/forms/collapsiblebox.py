from qtpy import QtCore
from qtpy import QtWidgets


class CollapsibleBox(QtWidgets.QWidget):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)

        self._parent = parent
        self._expanded = False
        self.toggle_button = QtWidgets.QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setIconSize(QtCore.QSize(8, 8))
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.content_area = QtWidgets.QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
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
    pass
