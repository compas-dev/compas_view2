from compas_view2.app import App
from compas.geometry import Sphere


viewer = App()
viewer.add(Sphere(0.01, [0, 0, 0]))
viewer.view.camera.scale = 0.01
viewer.view.camera.zoom_extents()

viewer.run()
