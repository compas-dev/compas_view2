from .meshobject import MeshObject


class CollectionObject(MeshObject):
    """Object for displaying COMPAS sphere geometry."""

    def __init__(self, collection, color=None, colors=None, **kwargs):
        super().__init__(collection.to_mesh(color=color, colors=colors), **kwargs)
        self._data = collection
