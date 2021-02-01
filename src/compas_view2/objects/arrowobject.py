from .shapeobject import ShapeObject


class ArrowObject(ShapeObject):
    def __init__(self, data, **kwargs):
        super().__init__(data, show_edges=False, **kwargs)
