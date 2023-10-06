from compas_view2.app import App
from compas.geometry import Sphere

viewer = App()

center = [0, 0, 5]
viewer.add(Sphere(center, 1))

viewer.view.camera.position = [center[0] + 5, center[1], center[2] + 3]
viewer.view.camera.look_at(center)
viewer.run()
