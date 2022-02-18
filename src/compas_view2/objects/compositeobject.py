import numpy as np

from .bufferobject import BufferObject


class CompositeObject(BufferObject):
    """Object for displaying a composition of View2 objects."""

    def __init__(self, objects, **kwargs):
        self.objects = objects
        super().__init__([obj._data for obj in objects], **kwargs)

    def _points_data(self):
        positions, colors, elements = [], [], []
        for obj in self.objects:
            if hasattr(obj, "_points_data"):
                p, c, e = obj._points_data()
                positions += p
                colors += c
                elements += e
        return positions, colors, elements

    def _lines_data(self):
        positions, colors, elements = [], [], []
        for obj in self.objects:
            if hasattr(obj, "_lines_data"):
                p, c, e = obj._lines_data()
                elements += (np.array(e) + len(positions)).tolist()
                positions += p
                colors += c
        return positions, colors, elements

    def _frontfaces_data(self):
        positions, colors, elements = [], [], []
        for obj in self.objects:
            if hasattr(obj, "_frontfaces_data"):
                p, c, e = obj._frontfaces_data()
                elements += (np.array(e) + len(positions)).tolist()
                positions += p
                colors += c
        return positions, colors, elements

    def _backfaces_data(self):
        positions, colors, elements = [], [], []
        for obj in self.objects:
            if hasattr(obj, "_backfaces_data"):
                p, c, e = obj._backfaces_data()
                elements += (np.array(e) + len(positions)).tolist()
                positions += p
                colors += c
        return positions, colors, elements
