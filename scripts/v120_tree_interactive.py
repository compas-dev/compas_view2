from compas_view2.app import App

viewer = App()


def show_attributes_form(self, entry):
    print(self, self.app)
    # when data is a dict, it is automatically converted to a list of key, value pairs
    attributeform = viewer.treeform("Attribute Form", data=entry["attributes"], floating=True)


data = [
    {
        "key": "a",
        "on_item_double_clicked": show_attributes_form,
        "attributes": {"attribute1": 1, "attribute2": 2, "attribute3": 3}

    },
    {
        "key": "b",
        "on_item_double_clicked": show_attributes_form,
        "attributes": {"attribute4": 4, "attribute5": 5, "attribute6": 6},
        "children": [
            {
                "key": "c",
                "on_item_double_clicked": show_attributes_form,
                "attributes": {"attribute7": 7, "attribute8": 8, "attribute9": 9},
                "color": (100, 100, 0)  # This assigns a color to the entrie row of this entry
            },
        ]
    },
]
treeform = viewer.treeform("Content Form", data=data, show_headers=False, columns=["key"])


def show_table_form(self, entry):
    print(self, self.app)
    # columns can also be a list of name (the header label to show), key pairs.
    columns = [
        {"name": "Column 1", "key": "column1"},
        {"name": "Column 2", "key": "column2"},
        {"name": "Column 3", "key": "column3"},
    ]
    # assigning a desginated slot ensures only one form is shown at a time.
    tableform = viewer.treeform("Table Form", data=entry["table_data"], columns=columns, location="right", slot="focus_table")


data2 = [
    {
        "name": "a",
        "on_item_pressed": show_table_form,  # triggered by single click
        "table_data": [
            {"column1": 1, "column2": 2, "column3": 3},
            {"column1": 4, "column2": 5, "column3": 6},
            {"column1": 7, "column2": 8, "column3": 9},
        ],
        "children": [
            {
                "name": "b",
                "on_item_pressed": show_table_form,  # triggered by single click
                "table_data": [
                    {"column1": 11, "column2": 22, "column3": 33},
                    {"column1": 44, "column2": 55, "column3": 66},
                    {"column1": 77, "column2": 88, "column3": {"value": 99, "color": (255, 0, 0)}},  # the value can also be a dict with a cell color and a value.
                ],
            },
        ]
    },

]
treeform2 = viewer.treeform("Content Form 2", location="right", data=data2, show_headers=False, columns=["name"])

viewer.show()
