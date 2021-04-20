from .polylineobject import PolylineObject
from compas.geometry import Frame
import math


class EllipseObject(PolylineObject):
    """Object for displaying COMPAS Ellipse geometry."""

    def __init__(self, ellipse, u=16, show_edges=True, **kwargs):

        frame = Frame.from_plane(ellipse.plane)
        ellipse.points = [
            frame.to_world_coordinates([
                math.cos(i*math.pi*2/u) * ellipse.major,
                math.sin(i*math.pi*2/u) * ellipse.minor,
                0
            ])
            for i in range(0, u)
        ]

        super().__init__(ellipse, close=True, show_edges=show_edges, **kwargs)
