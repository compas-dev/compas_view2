from qtpy import QtWidgets

class DockForm(QtWidgets.QDockWidget):
    """
    """

    def __init__(self, title):
        super().__init__(title)

        scroll = QtWidgets.QScrollArea()
        self.setWidget(scroll)
        content = QtWidgets.QWidget()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        vlay = QtWidgets.QVBoxLayout(content)
        self._layout = vlay