from compas_view2.app import App

viewer = App()

def on_item_edited(self, entry, column, value):
    print("form", self)
    print("entry", entry)
    print("column", column)
    print("value", value)

data = [
    {"column1": "a", "column2": 1, "on_item_edited": on_item_edited, "some_binded_obj": {}},
    {"column1": "b", "column2": 2, "on_item_edited": on_item_edited},
    {"column1": "c", "column2": 3, "on_item_edited": on_item_edited},
]

columns = [
    {"name": "Column 1", "key": "column1"},
    {"name": "Column 2", "key": "column2", "editable": True},
]

tableform = viewer.treeform("Attribute Form Editable", data=data, columns=columns)


viewer.show()
