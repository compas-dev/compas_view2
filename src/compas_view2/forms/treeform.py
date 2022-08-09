from .dockform import DockForm
from qtpy import QtWidgets
from qtpy import QtGui


class TreeForm(DockForm):
    def __init__(self, title="Tree"):
        super().__init__(title)

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Key", "Value"])
        self.setWidget(self.tree)

    def update(self, entries):
        self.tree.clear()
        self.map_entries(entries)

    def map_entries(self, entries, parent=None):
        for entry in entries:
            children = entry.get("children")
            if children:
                item = QtWidgets.QTreeWidgetItem([entry["key"]])
                self.map_entries(children, item)
            else:
                item = QtWidgets.QTreeWidgetItem([entry["key"], str(entry.get("value", ""))])

            if entry.get("color"):
                item.setBackgroundColor(1, QtGui.QColor(*entry.get("color")))

            if parent is not None:
                parent.addChild(item)
            else:
                self.tree.addTopLevelItem(item)
