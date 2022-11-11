import math

from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Circle

from .polylineobject import PolylineObject


class CircleObject(PolylineObject):
    """Object for displaying COMPAS Circle geometry."""

    def __init__(self, circle, u=16, **kwargs):
        self.u = u
        self.calculate_circle_points(circle)
        super().__init__(circle, close=True, **kwargs)

    def calculate_circle_points(self, circle):
        frame = Frame.from_plane(circle.plane)
        circle.points = [
            frame.to_world_coordinates(
                [
                    math.cos(i * math.pi * 2 / self.u) * circle.radius,
                    math.sin(i * math.pi * 2 / self.u) * circle.radius,
                    0,
                ]
            )
            for i in range(self.u)
        ]

    def update(self):
        self.calculate_circle_points(self._data)
        self.init()
        super().update()

    @property
    def properties(self):
        return ["u"]

    @classmethod
    def create_default(cls) -> Circle:
        return Circle(Plane([0, 0, 0], [0, 0, 1]), 1)
