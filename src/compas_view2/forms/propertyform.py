from .dockform import DockForm
from qtpy import QtWidgets


class PropertyForm(DockForm):
    def __init__(self, app, title="Properties"):
        super().__init__(title)

        self.app = app
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Key", "Value"])

        properties = {
            "a": 1,
            "b": 2,
            "c": {
                "c1": 1,
                "c2": 2,
            }
        }

        self.map_properties(properties)
        self.setWidget(self.tree)
        self.tree.clear()

    def map_properties(self, properties, parent=None):

        for key, value in properties.items():
    
            if isinstance(value, dict):
                item = QtWidgets.QTreeWidgetItem([key])
                self.map_properties(value, item)
            else:
                item = QtWidgets.QTreeWidgetItem([key, str(value)])

            if parent is not None:
                parent.addChild(item)
            else:
                self.tree.addTopLevelItem(item)

