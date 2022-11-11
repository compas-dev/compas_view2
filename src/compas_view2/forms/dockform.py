from qtpy import QtWidgets


class DockForm(QtWidgets.QDockWidget):
    """ """

    def __init__(self, app, title):
        super().__init__(title)
        self.app = app
        self.setMinimumWidth(200)
        scroll = QtWidgets.QScrollArea()
        self.setWidget(scroll)
        content = QtWidgets.QWidget()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        vlay = QtWidgets.QVBoxLayout(content)
        self.content_layout = vlay

    def clear(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
