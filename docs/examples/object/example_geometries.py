from compas.geometry import Circle
from compas.geometry import Ellipse
from compas.geometry import Plane
from compas.geometry import Polygon
from compas.geometry import Cone
from compas.geometry import Polyhedron
from compas.geometry import Line
from compas.geometry import Capsule

from compas_view2.app import App


viewer = App()

polygon = Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0]])
obj = viewer.add(polygon, linecolor=(0, 0, 1))

plane = Plane([0, 0, 0], [0, 0, 1])
obj = viewer.add(plane, size=0.5, linecolor=(1, 0, 0), facecolor=(0, 0, 1))
obj.translation = (5, 0, 0)

circle = Circle.from_plane_and_radius(plane, 0.8)
obj = viewer.add(circle, linecolor=(0, 1, 0))
obj.translation = (10, 0, 0)

ellipse = Ellipse.from_plane_major_minor(plane, 1.5, 0.5)
obj = viewer.add(ellipse, linecolor=(1, 0, 1))
obj.translation = (0, 5, 0)

cone = Cone.from_circle_and_height(circle, 1.5)
obj = viewer.add(cone, facecolor=(1, 0, 0))
obj.translation = (5, 5, 0)

vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 0, 1]]
faces = [[0, 1, 2], [0, 1, 3], [1, 2, 3], [0, 2, 3]]
polyhedron = Polyhedron(vertices, faces)
obj = viewer.add(polyhedron, facecolor=(0, 1, 0))
obj.translation = (10, 5, 0)

line = Line([0, 0, 0], [1, 1, 1])
capsule = Capsule.from_line_and_radius(line, 0.3)
obj = viewer.add(capsule, facecolor=(0, 0, 1))
obj.translation = (0, 10, 0)

viewer.show()
