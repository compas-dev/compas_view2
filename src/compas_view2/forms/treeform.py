from .dockform import DockForm
from qtpy import QtWidgets
from qtpy import QtGui


class TreeForm(DockForm):
    def __init__(self, title="Tree", data=None, columns=["key", "value"], show_headers=True):
        super().__init__(title)
        self.column_names = list(map(lambda c: c if isinstance(c, str) else c["name"], columns))
        self.column_keys = list(map(lambda c: c if isinstance(c, str) else c["key"], columns))
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(len(columns))
        self.tree.setHeaderLabels(self.column_names)
        self.tree.setHeaderHidden(not show_headers)
        self.setWidget(self.tree)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.tree.itemPressed.connect(self.on_item_pressed)
        if data:
            self.update(data)

    def update(self, entries):
        self.tree.clear()
        self.map_entries(entries)

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
                values.append(str(value))
                colors.append(color)
            item = QtWidgets.QTreeWidgetItem(values)
            item.entry = entry
            if children:
                self.map_entries(children, item)
            if entry.get("color"):
                for i in range(self.tree.columnCount()):
                    item.setBackgroundColor(i, QtGui.QColor(*entry.get("color")))

            if entry.get("on_item_double_clicked"):
                item.on_item_double_clicked = entry.get("on_item_double_clicked")

            if entry.get("on_item_pressed"):
                item.on_item_pressed = entry.get("on_item_pressed")

            for i, color in enumerate(colors):
                if color:
                    item.setBackgroundColor(i, QtGui.QColor(*color))

            if parent is not None:
                parent.addChild(item)
            else:
                self.tree.addTopLevelItem(item)

    def on_item_double_clicked(self, item, column):
        if hasattr(item, "on_item_double_clicked"):
            item.on_item_double_clicked(item.entry)

    def on_item_pressed(self, item, column):
        if hasattr(item, "on_item_pressed"):
            item.on_item_pressed(item.entry)
