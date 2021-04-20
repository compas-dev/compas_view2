from .polylineobject import PolylineObject
from compas.geometry import Frame
import math


class CircleObject(PolylineObject):
    """Object for displaying COMPAS Circle geometry."""

    def __init__(self, circle, u=16, show_edges=True, **kwargs):

        frame = Frame.from_plane(circle.plane)
        circle.points = [
            frame.to_world_coordinates([
                math.cos(i*math.pi*2/u) * circle.radius,
                math.sin(i*math.pi*2/u) * circle.radius,
                0
                ])
            for i in range(u)
        ]

        super().__init__(circle, close=True, show_edges=show_edges, **kwargs)
