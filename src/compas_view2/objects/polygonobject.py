from .polylineobject import PolylineObject


class PolygonObject(PolylineObject):
    """Object for displaying COMPAS Polygon geometry."""

    def __init__(self, polygon, show_edges=True, **kwargs):
        super().__init__(polygon, close=True, show_edges=show_edges, **kwargs)
