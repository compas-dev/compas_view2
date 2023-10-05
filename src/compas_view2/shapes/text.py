from compas.geometry import Vector
from compas.geometry import Shape


class Text(Shape):
    """ """

    def __init__(self, text, position=[0, 0, 0], height=50, absolute_height=False, font=None):
        super().__init__()
        self.text = text
        self.position = Vector(*position)
        self.height = height
        self.absolute_height = absolute_height
        self.font = font
