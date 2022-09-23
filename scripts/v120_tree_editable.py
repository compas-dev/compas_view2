from compas_view2.app import App

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
