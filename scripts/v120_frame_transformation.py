from compas_view2.app import App
from compas.datastructures import Mesh
from compas.geometry import Frame
import compas

viewer = App(enable_sceneform=True)

mesh = Mesh.from_obj(compas.get('faces.obj'))

visual_frame = Frame.worldXY()
frame1 = Frame([1, 0, 1], [1, 0, 0], [0, 1, 0])
frame2 = Frame([0, 0, 2], [1, 0, 0], [0, 0, 1])

obj1 = viewer.add(mesh, frame=frame1, show_lines=False, name="obj1")
obj1.add(visual_frame, name="frame of obj1")

obj2 = obj1.add(mesh, frame=frame2, show_lines=False, name="obj2")
obj2.add(visual_frame, name="frame of obj2")

print(obj1.frame_transformation)
print(obj2.frame_transformation)

viewer.show()
