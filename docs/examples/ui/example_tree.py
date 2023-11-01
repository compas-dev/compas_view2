from random import random

from compas_view2.app import App
from compas_view2.shapes import Arrow
from compas.colors import Color

viewer = App(enable_sceneform=True, enable_propertyform=True)

arrow1 = Arrow([0, 0, 0], [0, 0, 1], head_portion=0.2, head_width=0.07, body_width=0.02)
arrow1_obj = viewer.add(arrow1, name="arrow1", u=16, show_lines=False, facecolor=(0,0,0))
arrow1_obj.translation = [0, 1, 0]

arrow2 = Arrow([0, 0, 0], [0, 0, 1], head_portion=0.2, head_width=0.07, body_width=0.02)
arrow2_obj = arrow1_obj.add(arrow2, name="arrow2", u=16, show_lines=False, facecolor=(0,0,0))
arrow2_obj.translation = [1, 0, 0]

arrow3 = Arrow([0, 0, 0], [0, 0, 1], head_portion=0.2, head_width=0.07, body_width=0.02)
arrow3_obj = arrow1_obj.add(arrow3, name="arrow3", u=16, show_lines=False, facecolor=(0,0,0))
arrow3_obj.translation = [2, 0, 0]

arrow4 = Arrow([0, 0, 0], [0, 0, 1], head_portion=0.2, head_width=0.07, body_width=0.02)
arrow4_obj = arrow1_obj.add(arrow4, name="arrow4", u=16, show_lines=False, facecolor=(0,0,0))
arrow4_obj.translation = [3, 0, 0]

arrow5 = Arrow([0, 0, 0], [0, 0, 1], head_portion=0.2, head_width=0.07, body_width=0.02)
arrow5_obj = arrow1_obj.add(arrow5, name="arrow5", u=16, show_lines=False, facecolor=(0,0,0))
arrow5_obj.translation = [4, 0, 0]

treeform = viewer.treeform("Custom Tree Form")
treeform.update([
    {"key": "a", "value": "1"},
    {"key": "b", "children": [
        {"key": "c", "value": "2"},
        {"key": "d", "value": "3"},
        {"key": "e", "value": "4"},
        {"key": "f", "value": "5"}
    ]},
])

viewer.show()
