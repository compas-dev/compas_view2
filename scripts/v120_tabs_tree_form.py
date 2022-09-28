from compas_view2.app import App

viewer = App()

tabs = [
    {
        "name": "tab1",
        "data": [
            {
                "name": "a",
                "value": 1,
            },
            {
                "name": "b",
                "value": 2,
            },
            {
                "name": "c",
                "value": 3,
            },

        ]
    },
    {
        "name": "tab2",
        "data": [
            {
                "name": "d",
                "value": 4,
            },
            {
                "name": "e",
                "value": 5,
            },
            {
                "name": "f",
                "value": 6,
            },

        ]
    }
]
treeform2 = viewer.tabsform("Tabs Form", location="right", tabs=tabs, show_headers=True, columns=["name", "value"], striped_rows=True)

viewer.show()
