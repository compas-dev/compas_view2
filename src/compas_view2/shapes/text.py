from compas.geometry import Vector
from compas.geometry import Shape


__all__ = ['Text']


class Text(Shape):
    """
    """

    def __init__(
            self, text, position=[0, 0, 0], size=100):
        super().__init__()
        self.text = text
        self.position = Vector(*position)
        self.size = size
