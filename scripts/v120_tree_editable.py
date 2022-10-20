from compas_view2.app import App
from compas_view2.values import IntValue

viewer = App()


def on_item_edited(form, entry, column, value):
    print("form:\n", form)
    print("entry:\n", entry)
    print("column:\n", column)
    print("value:\n", value)
    print("datastore:")
    for row in form.datastore:
        print(row)


data = [
    {"column1": "a", "column2": IntValue(1), "on_item_edited": on_item_edited, "some_binded_obj": {}},
    {"column1": "b", "column2": IntValue(2, min=0, max=10), "on_item_edited": on_item_edited},
    {"column1": "c", "column2": IntValue(3, options=[0, 1, 2, 3]), "on_item_edited": on_item_edited},
]

columns = [
    {"name": "Column 1", "key": "column1"},
    {"name": "Column 2", "key": "column2", "editable": True},
]

tableform = viewer.treeform("Attribute Form Editable", data=data, columns=columns)


viewer.show()
