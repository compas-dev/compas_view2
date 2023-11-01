from .dockform import DockForm
from qtpy import QtWidgets
from qtpy import QtCore
from qtpy.QtWidgets import QAbstractItemView


class SceneForm(DockForm):
    def __init__(self, app, title="Scene"):
        super().__init__(app, title)
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderHidden(True)
        self.setWidget(self.tree)
        self.tree.itemPressed.connect(self.display_selected)
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def update(self):
        self.tree.clear()
        root_objects = filter(lambda obj: obj.parent is None, self.app.view.objects.values())
        self.map_objects(root_objects)

    def map_objects(self, objects, parent=None):
        for obj in objects:
            item = QtWidgets.QTreeWidgetItem([obj.name])
            if parent is not None:
                parent.addChild(item)
            else:
                self.tree.addTopLevelItem(item)

            item.obj = obj

            self.map_objects(obj.children, item)

    def display_selected(self):
        selected = self.tree.selectedItems()
        self.app.selector.deselect()

        if len(selected) == 0:
            return
        else:
            self.app.selector.mode = "multi"
            [self.app.selector.select(s.obj, update=True, mode="multi") for s in selected]
        self.show_properties(selected[0].obj)

    def show_properties(self, obj):
        propertyform = self.app.dock_slots.get("propertyform")
        if propertyform:
            propertyform.set_object(obj)

    def select(self, objs):
        all_items = self.tree.findItems("", QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive)
        for item in all_items:
            if item.obj in objs:
                item.setSelected(True)
            else:
                item.setSelected(False)
