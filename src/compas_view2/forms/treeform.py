from .dockform import DockForm
from qtpy import QtWidgets
from qtpy import QtGui
import ast


class TreeForm(DockForm):
    def __init__(self, app, title="Tree", data=None, columns=["key", "value"], show_headers=True, striped_rows=False):
        super().__init__(app, title)
        self.column_names = list(map(lambda c: c if isinstance(c, str) else c["name"], columns))
        self.column_keys = list(map(lambda c: c if isinstance(c, str) else c["key"], columns))
        self.column_editable = list(map(lambda c: c.get("editable") if isinstance(c, dict) else False, columns))
        self.striped_rows = striped_rows
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(len(columns))
        self.tree.setHeaderLabels(self.column_names)
        self.tree.setHeaderHidden(not show_headers)
        # self.tree.setStyleSheet("QTreeWidget::item { height:35px; }")
        self.setWidget(self.tree)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.tree.itemPressed.connect(self.on_item_pressed)
        self.tree.itemChanged.connect(self.on_item_changed)
        self.datastore = []
        if data:
            self.update(data)

    def update(self, entries):
        self.tree.clear()
        self.item_count = 0
        self.map_entries(entries)
        for item in self.items:
            if item.entry.get("expanded"):
                item.setExpanded(True)
        self.tree.resizeColumnToContents(0)

    @property
    def items(self):
        items = []

        def traverseNode(item):
            for i in range(item.childCount()):
                items.append(item.child(i))
                traverseNode(item.child(i))

        for i in range(self.tree.topLevelItemCount()):
            items.append(self.tree.topLevelItem(i))
            traverseNode(self.tree.topLevelItem(i))

        return items

    def map_entries(self, entries, parent=None):

        # automatically convert dict to list of key, value pairs
        if isinstance(entries, dict):
            _entries = []
            for key, value in entries.items():
                _entries.append({"key": key, "value": value})
            entries = _entries

        for entry in entries:
            children = entry.get("children")
            values = []
            colors = []
            for key in self.column_keys:
                value = entry.get(key, "")
                color = None
                if isinstance(value, dict):
                    if "color" in value:
                        color = value["color"]
                    if "value" in value:
                        value = value["value"]
                values.append(value)
                colors.append(color)
            item = QtWidgets.QTreeWidgetItem([str(v) for v in values])
            item.entry = entry
            item.data_item = {"values": values, "children": []}
            if children:
                self.map_entries(children, item)
            if entry.get("color"):
                for i in range(self.tree.columnCount()):
                    item.setBackgroundColor(i, QtGui.QColor(*entry.get("color")))
            elif self.striped_rows and self.item_count % 2 == 1:
                for i in range(self.tree.columnCount()):
                    item.setBackgroundColor(i, QtGui.QColor(240, 240, 240))

            if entry.get("on_item_double_clicked"):
                item.on_item_double_clicked = entry.get("on_item_double_clicked")

            if entry.get("on_item_pressed"):
                item.on_item_pressed = entry.get("on_item_pressed")

            if entry.get("on_item_edited"):
                item.on_item_edited = entry.get("on_item_edited")

            for i, color in enumerate(colors):
                if color:
                    item.setBackgroundColor(i, QtGui.QColor(*color))

            self.item_count += 1

            if parent is not None:
                parent.addChild(item)
                parent.data_item["children"].append(item.data_item)
            else:
                self.tree.addTopLevelItem(item)
                self.datastore.append(item.data_item)

    def on_item_double_clicked(self, item, column):
        if self.column_editable[column]:
            self.tree.openPersistentEditor(item, column)
        if hasattr(item, "on_item_double_clicked"):
            item.on_item_double_clicked(self, item.entry)

    def on_item_pressed(self, item, column):
        if hasattr(item, "on_item_pressed"):
            item.on_item_pressed(self, item.entry)

    def on_item_changed(self, item, column):
        self.tree.closePersistentEditor(item, column)

        try:
            value = ast.literal_eval(item.text(column))
        except Exception:
            value = item.text(column)

        item.data_item["values"][column] = value
        if hasattr(item, "on_item_edited"):
            item.on_item_edited(self, item.entry, column, value)
