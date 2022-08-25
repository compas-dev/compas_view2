from math import radians
from unicodedata import name
from compas_view2.app import App
from compas.geometry import Sphere, Circle, Plane, Point
from compas.colors import Color

Sun = Sphere([0, 0, 0], radius=1)
EarthOrbit = Circle(Plane([0, 0, 0], [0, 0, 1]), radius=10)
EarthLocator = Point(0, 0, 0)

EarthContainer = Point(0, 0, 0)
Earth = Sphere([0, 0, 0], radius=0.5)
MoonOrbitContainer = Point(0, 0, 0)
MoonOrbit = Circle(Plane([0, 0, 0], [0, 0, 1]), radius=4)
MoonLocator = Point(0, 0, 0)
MoonContainer = Point(0, 0, 0)
Moon = Sphere([0, 0, 0], radius=0.25)


viewer = App(show_grid=False, enable_sceneform=True)

SunObj = viewer.add(Sun, facecolor=Color.red(), name="Sun")
EarthOrbitObj = viewer.add(EarthOrbit, u=100, name="EarthOrbit")
EarthLocatorObj = EarthOrbitObj.add(EarthLocator, name="EarthLocator")
EarthLocatorObj.translation = [10, 0, 0]

EarthContainerObj = viewer.add(EarthContainer, name="EarthContainer")
EarthContainerObj.rotation = [0, -radians(15), 0]
EarthObj = EarthContainerObj.add(Earth, facecolor=Color.blue(), name="Earth")

MoonOrbitContainerObj = viewer.add(MoonOrbitContainer, name="MoonOrbitContainer")
MoonOrbitContainerObj.rotation = [0, radians(15), 0]

MoonOrbitObj = MoonOrbitContainerObj.add(MoonOrbit, u=100, name="MoonOrbit")
MoonLocatorObj = MoonOrbitObj.add(MoonLocator, name="MoonLocator")
MoonLocatorObj.translation = [4, 0, 0]
MoonContainerObj = viewer.add(MoonContainer, name="MoonContainer")
MoonContainerObj.rotation = [0, -radians(15), 0]
MoonObj = MoonContainerObj.add(Moon, facecolor=Color.white(), name="Moon")


@viewer.on(interval=0.05)
def orbit(frame):

    SunObj.rotation = [0, 0, -radians(frame)/5]
    SunObj._update_matrix()

    EarthOrbitObj.rotation = [0, 0, radians(frame)/5]
    EarthOrbitObj._update_matrix()

    EarthContainerObj.translation = EarthLocatorObj.transformation_world.translation_vector
    EarthContainerObj._update_matrix()
    EarthObj.rotation = [0, 0, -radians(frame)/2]
    EarthObj._update_matrix()

    MoonOrbitContainerObj.translation = EarthLocatorObj.transformation_world.translation_vector
    MoonOrbitContainerObj._update_matrix()
    MoonOrbitObj.rotation = [0, 0, radians(frame)/2]
    MoonOrbitObj._update_matrix()

    MoonContainerObj.translation = MoonLocatorObj.transformation_world.translation_vector
    MoonContainerObj._update_matrix()
    MoonObj.rotation = [0, 0, -radians(frame)/2]
    MoonObj._update_matrix()


viewer.show()
