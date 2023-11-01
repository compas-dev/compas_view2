from compas_view2.app import App
from compas.geometry import Box, Frame, Translation

viewer = App()


# Create some boxes and the data
basic_box = Box(Frame.worldXY(), 1, 1, 1)
data = []


# Define the function that will be called when an item is pressed
def select(self, entry):
    # print(self, entry)
    viewer.selector.reset()
    entry["data"][0].is_selected = True
    entry["data"][1].is_selected = True
    viewer.view.update()


# Create the data
for i in range(10):
    obj1 = viewer.add(basic_box.transformed(Translation.from_vector((i, 0, 0))))
    obj2 = viewer.add(basic_box.transformed(Translation.from_vector((i, 1, 0))))
    data.append({"object1": i, "object2": 2 * i, "on_item_pressed": select, "data": [obj1, obj2]})

# Add the treeform
treeform2 = viewer.treeform("Objects", location="right", data=data, show_headers=True, columns=["object1", "object2"])

viewer.show()
