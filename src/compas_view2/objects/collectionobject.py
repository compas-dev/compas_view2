import numpy as np

from compas_view2.collections import Collection
from .object import Object
from .bufferobject import BufferObject


class CollectionObject(BufferObject):
    """Object for displaying COMPAS collection."""

    def __init__(self, collection: Collection, **kwargs):

        super().__init__(collection, **kwargs)

        self._objects = []
        for item, item_property in zip(collection.items, collection.item_properties):
            _kwargs = dict(kwargs)
            _kwargs.update(item_property)
            self._objects.append(Object.build(item, **_kwargs))

        # if not given explicitly, use child object default settings
        if self._objects:
            self.show_points = self.show_points or self._objects[0].show_points
            self.show_lines = self.show_lines or self._objects[0].show_lines
            self.show_faces = self.show_faces or self._objects[0].show_faces
        self._is_collection = True

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
