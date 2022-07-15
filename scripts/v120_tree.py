from random import random

from compas_view2.app import App
from compas_view2.shapes import Arrow

viewer = App(enable_sceneform=True, enable_propertyform=True)

arrow1 = Arrow([0, 0, 0], [0, 0, 1], head_portion=0.2, head_width=0.07, body_width=0.02)
arrow1_obj = viewer.add(arrow1, name="arrow1", u=16, show_edges=False, color=(random(), random(), random()))
arrow1_obj.translation = [0, 1, 0]

arrow2 = Arrow([0, 0, 0], [0, 0, 1], head_portion=0.2, head_width=0.07, body_width=0.02)
arrow2_obj = arrow1_obj.add(arrow2, name="arrow2", u=16, show_edges=False, color=(random(), random(), random()))
arrow2_obj.translation = [1, 0, 0]

treeform = viewer.treeform()
treeform.update([
    {"key": "a", "value": "1"},
    {"key": "b", "children": [
        {"key": "c", "value": "2"},
    ]},
])

viewer.show()
