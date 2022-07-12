from .dockform import DockForm
from qtpy import QtWidgets


class TreeForm(DockForm):
    def __init__(self, app, title="objects"):
        super().__init__(title)

        self.app = app
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderHidden(True)

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
        self.setWidget(self.tree)
        self.tree.itemPressed.connect(lambda item: self.show_properties(item.obj))

    def map_objects(self, objects, parent=None):

        for obj in objects:
            item = QtWidgets.QTreeWidgetItem([obj["name"]])
            if parent is not None:
                parent.addChild(item)
            else:
                self.tree.addTopLevelItem(item)

            item.obj = obj

            if "children" in obj:
                self.map_objects(obj["children"], item)

    def show_properties(self, obj):
        propertyform = self.app.dock_slots.get("propertyform")
        if propertyform:
            propertyform.tree.clear()
            propertyform.map_properties(obj)