from PySide2 import QtWidgets


class ObjectsTree(QtWidgets.QTreeWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
