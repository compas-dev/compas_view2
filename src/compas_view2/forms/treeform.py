from .dockform import DockForm
from qtpy import QtWidgets


class TreeForm(DockForm):
    def __init__(self, title="objects"):
        super().__init__(title)

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Name", "Type"])

        objects = [
            {"name": "A", "children": []},
            {"name": "B", "children": [
                {"name": "B1", "children": []},
                {"name": "B2", "children": []},
            ]},
            {"name": "C", "children": [
                {"name": "C1", "children": [
                    {"name": "C1.1", "children": []},
                    {"name": "C1.2", "children": []},
                ]},
                {"name": "C2", "children": []},
            ]},
        ]

        self.map_objects(objects)

        self.content_layout.addWidget(self.tree)

    def map_objects(self, objects, parent=None):

        for obj in objects:
            item = QtWidgets.QTreeWidgetItem([obj["name"]])
            if parent is not None:
                parent.addChild(item)
            else:
                self.tree.addTopLevelItem(item)

            button = Button("Inspect", obj)
            self.tree.setItemWidget(item, 1, button)

            if "children" in obj:
                self.map_objects(obj["children"], item)

class Button(QtWidgets.QPushButton):
    def __init__(self, text, obj):
        super().__init__(text)
        self.clicked.connect(lambda: print(obj))