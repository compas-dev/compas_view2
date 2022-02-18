import enum
from random import random
from math import radians
from math import sin
from math import cos
from compas.geometry import Vector
from compas_view2.app import App
from compas.colors import Color
from compas.colors import ColorMap
from compas_view2.collections import Collection

viewer = App()

vectors = []
vector_properties = []

for i in range(0, 360, 20):
    for j in range(0, 180, 10):
        vector = Vector(sin(radians(i)), cos(radians(i)), cos(radians(j)))
        position = Vector(sin(radians(i)) * sin(radians(j)), cos(radians(i)) * sin(radians(j)), cos(radians(j)))
        color = Color(random(), random(), random())
        vectors.append(vector)
        vector_properties.append({'position': position, 'color': color, 'size': 1})

collection = Collection(vectors, vector_properties)
coolectionobj = viewer.add(collection)


flip = 1


@viewer.on(interval=50)
def animate(frame):
    cmap = ColorMap.from_palette('bamako')
    global flip

    if frame % 30 == 0:
        flip *= -1

    parameter = ((frame % 30 / 30) * 2 - 1) * flip

    for property in vector_properties:
        value = 1 - abs(property['position'].z - parameter)
        if value < 0:
            value = 0

        property['size'] = value
        property['color'] = cmap(value)

    coolectionobj.update()
    viewer.view.update()


viewer.show()
