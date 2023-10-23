from compas_view2.app import App
from compas_view2.values import IntValue
from compas_view2.values import FloatValue
from compas_view2.values import StrValue
from compas_view2.values import ListValue
from compas_view2.values import DictValue

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
    {"column1": "int1", "column2": IntValue(1), "on_item_edited": on_item_edited, "some_binded_obj": {}},
    {"column1": "int2", "column2": IntValue(2, min=0, max=10), "on_item_edited": on_item_edited},
    {"column1": "int3", "column2": IntValue(3, options=[0, 1, 2, 3]), "on_item_edited": on_item_edited},
    {"column1": "float", "column2": FloatValue(0.005), "on_item_edited": on_item_edited},
    {"column1": "str", "column2": StrValue("some texts"), "on_item_edited": on_item_edited},
    {"column1": "list", "column2": ListValue([1, 2, 3], int), "on_item_edited": on_item_edited},
    {"column1": "dict", "column2": DictValue({"a": 1}, int), "on_item_edited": on_item_edited},
]

columns = [
    {"name": "Column 1", "key": "column1"},
    {"name": "Column 2", "key": "column2", "editable": True},
]

tableform = viewer.treeform("Attribute Form Editable", data=data, columns=columns)


viewer.show()
