from .dockform import DockForm
from qtpy import QtWidgets
from qtpy import QtGui
from qtpy import QtCore
import ast
from compas_view2.values import Value


class ValueDelegate(QtWidgets.QStyledItemDelegate):
    def get_value(self, index):
        treeform = self.parent()
        item = treeform.tree.itemFromIndex(index)
        column = index.column()
        key = treeform.column_keys[column]
        value = item.entry[key]
        return value

    def set_value(self, index, new_value):
        treeform = self.parent()
        item = treeform.tree.itemFromIndex(index)
        column = index.column()
        key = treeform.column_keys[column]
        value = item.entry[key]
        try:
            new_value = ast.literal_eval(new_value)
        except Exception:
            pass
        if isinstance(value, Value):
            value.set(new_value)
            new_value = value.value
        else:
            item.entry[key] = new_value
        return new_value

    def has_options(self, value):
        return isinstance(value, Value) and value.options is not None

    def createEditor(self, parent, option, index):
        value = self.get_value(index)
        if self.has_options(value):
            print("createEditor: has_options")
            editor = QtWidgets.QComboBox(parent)
            editor.addItems([str(o) for o in value.options])
            return editor
        else:
            editor = QtWidgets.QLineEdit(parent)
            return editor

    def setEditorData(self, editor, index):
        value = self.get_value(index)
        if self.has_options(value):
            editor.setCurrentIndex(value.options.index(value.value))
        elif isinstance(value, Value):
            editor.setText(str(value.value))
        else:
            editor.setText(str(value))

    def setModelData(self, editor, model, index):
        value = self.get_value(index)
        if self.has_options(value):
            new_value = value.options[editor.currentIndex()]
        else:
            new_value = editor.text()
        new_value = self.set_value(index, new_value)
        model.setData(index, str(new_value), QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


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
        self.tree.setItemDelegateForColumn(1, ValueDelegate(self))
        self.setWidget(self.tree)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.tree.itemPressed.connect(self.on_item_pressed)
        self.tree.itemChanged.connect(self.on_item_changed)
        self.tree.currentItemChanged.connect(self.on_current_item_changed)
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

    @property
    def entries(self):
        return list(map(lambda i: i.entry, self.items))

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
                # if isinstance(value, dict):
                #     if "color" in value:
                #         color = value["color"]
                #     if "value" in value:
                #         value = value["value"]
                if isinstance(value, Value):
                    value = value.value
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
            key = self.column_keys[column]
            value = item.entry[key]
            if isinstance(value, Value):
                value = value.value
            else:
                value = ast.literal_eval(item.text(column))
        except Exception:
            value = item.text(column)

        item.data_item["values"][column] = value
        if hasattr(item, "on_item_edited"):
            item.on_item_edited(self, item.entry, column, value)

    def on_current_item_changed(self, current_item, privious_item):
        if privious_item:
            for i in range(self.tree.columnCount()):
                self.tree.closePersistentEditor(privious_item, i)

    def select(self, entries):
        all_items = self.tree.findItems("", QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive)
        for item in all_items:
            if item.entry in entries:
                item.setSelected(True)
            else:
                item.setSelected(False)
