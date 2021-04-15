from .object import Object
from .bufferobject import BufferObject
import numpy as np
from inspect import getargspec


class CollectionObject(BufferObject):
    """Object for displaying COMPAS collection."""

    def __init__(self, collection, color=None, colors=None, **kwargs):

        argspec = getargspec(BufferObject.__init__)
        BufferObject_keywords = argspec.args[-len(argspec.defaults):]
        BufferObject_kwargs = {key: kwargs[key] for key in kwargs if key in BufferObject_keywords}
        super().__init__(collection, **BufferObject_kwargs)

        colors = colors or [color or [0.5, 0.5, 0.5]] * len(self._data.items)
        self._objects = [Object.build(item, color=color, **kwargs) for item, color in zip(self._data.items, colors)]

        # if not given explicitly, use child object default settings
        self.show_points = self.show_points or self._objects[0].show_points
        self.show_lines = self.show_lines or self._objects[0].show_lines
        self.show_faces = self.show_faces or self._objects[0].show_faces

    def _points_data(self):
        positions = []
        colors = []
        elements = []
        for obj in self._objects:
            if hasattr(obj, "_points_data"):
                p, c, e = obj._points_data()
                e = (np.array(e) + len(positions)).tolist()
                positions += p
                colors += c
                elements += e
        return positions, colors, elements

    def _lines_data(self):
        positions = []
        colors = []
        elements = []
        for obj in self._objects:
            if hasattr(obj, "_lines_data"):
                p, c, e = obj._lines_data()
                e = (np.array(e) + len(positions)).tolist()
                positions += p
                colors += c
                elements += e
        return positions, colors, elements

    def _frontfaces_data(self):
        positions = []
        colors = []
        elements = []
        for obj in self._objects:
            if hasattr(obj, "_frontfaces_data"):
                p, c, e = obj._frontfaces_data()
                e = (np.array(e) + len(positions)).tolist()
                positions += p
                colors += c
                elements += e
        return positions, colors, elements

    def _backfaces_data(self):
        positions = []
        colors = []
        elements = []
        for obj in self._objects:
            if hasattr(obj, "_backfaces_data"):
                p, c, e = obj._backfaces_data()
                e = (np.array(e) + len(positions)).tolist()
                positions += p
                colors += c
                elements += e
        return positions, colors, elements
