import compas
from compas.geometry import Sphere
from compas.colors import Color

from compas_view2.app import App

sphere = Sphere([0, 0, 0], 1.0)

# =============================================================================
# Visualization
# =============================================================================

viewer = App(width=960, height=540)
viewer.view.camera.rx = -60
viewer.view.camera.rz = 0
viewer.view.camera.distance = 5

viewer.add(sphere, u=128, v=128, facecolor=Color.cyan(), linecolor=Color.blue())


@viewer.on(interval=50, frames=180, record=True, record_path="docs/_images/example_orbiting.gif")
def orbit(f):
    viewer.view.camera.rz += 1


viewer.show()
