from compas.datastructures import Mesh


__all__ = ['Collection']


class Collection(Mesh):
    """A collection of items(inheritances of compas.datastructures.Mesh)
    """

    def __init__(self, items=None):
        super().__init__()
        self.items = items or []
