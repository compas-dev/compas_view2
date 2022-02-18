from random import random
from compas.geometry import Vector
from compas.geometry import Circle
from compas.geometry import Plane
from compas_view2.app import App
from compas.colors import Color
from compas.colors import ColorMap
from compas_view2.collections import Collection

viewer = App(enable_sidebar=True, width=1600, height=1200)

vectors = []
vector_properties = []

for i in range(0, 20):
    for j in range(0, 20):
        vector = Vector(0, 0, 1)
        position = Vector(i, j, 0)
        color = Color(random(), random(), random())
        vectors.append(vector)
        vector_properties.append({'position': position, 'color': color, 'size': 1})

collection = Collection(vectors, vector_properties)
collectionobj = viewer.add(collection)


attractor = Vector(10, 10, 0)
intensity = 1
radius = 10
intensity = 10
cmap = ColorMap.from_palette('bamako')

circle = Circle(Plane(attractor, Vector(0, 0, 1)), radius=radius)
circleobj = viewer.add(circle, u=100, linecolor=Color(1, 0, 0), linewidth=2)


def update_properties(update_objects_buffer=False):
    for properties in vector_properties:
        distance = (attractor - properties['position']).length
        value = 1 - distance / radius
        if value < 0:
            value = 0
        properties['size'] = (value + 0.5) * (intensity / 10)
        properties['color'] = cmap(value)

    circle.radius = radius
    circle.plane.point = attractor
    if update_objects_buffer:
        collectionobj.update()
        circleobj.update()


update_properties()


@viewer.slider(title="attractor_x", value=10, maxval=20, bgcolor=Color.white())
def slide(x):
    global attractor
    attractor.x = x
    update_properties(True)


@viewer.slider(title="attractor_y", value=10, maxval=20, bgcolor=Color.white())
def slide(y):
    global attractor
    attractor.y = y
    update_properties(True)


@viewer.slider(title="attractor_radius", value=10, minval=1, maxval=20, bgcolor=Color.white())
def slide(r):
    global radius
    radius = r
    update_properties(True)


@viewer.slider(title="attractor_intensity", value=10, minval=1, maxval=50, bgcolor=Color.white())
def slide(i):
    global intensity
    intensity = i
    update_properties(True)


viewer.view.camera.target = attractor
viewer.view.camera.distance = 40
viewer.show()
