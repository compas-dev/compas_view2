from compas.geometry import Vector

__all__ = ['Collection']


class Collection(object):
    """A collection of COMPAS items like meshes or shapes
    """

    def __init__(self, items, **kwargs):
        super().__init__()
        self.items = items or []
        self.kwargs = kwargs

    @property    
    def is_vector(self):
        return isinstance(self.items[0], Vector)
