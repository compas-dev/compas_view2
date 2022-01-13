from ..shapes import Arrow
from .arrowobject import ArrowObject
from .object import Object

class GimbalObject(Object):
    """Object for displaying the gimbal controller."""

    def __init__(self):
        self.x_axis = ArrowObject(Arrow(position=[0, 0, 0], direction=[1, 0, 0]), u=4, color=(1, 0, 0), is_selectable=False)
        self.y_axis = ArrowObject(Arrow(position=[0, 0, 0], direction=[0, 1, 0]), u=4, color=(0, 1, 0), is_selectable=False)
        self.z_axis = ArrowObject(Arrow(position=[0, 0, 0], direction=[0, 0, 1]), u=4, color=(0, 0, 1), is_selectable=False)
        self.components = [self.x_axis, self.y_axis, self.z_axis]
        self.enabled = True
        self._attached_to = None

    def attach(self, obj):
        self._attached_to = obj
        for component in self.components:
            component.translation = obj.translation
            component._update_matrix()
    
    def detach(self):
        self._attached_to = None

    def init(self):

        def on_mousedown(event):
            print("Pressed")
        
        def on_mouserelease(event):
            print("Released")

        def on_mousedrag(event):
            print("Dragging")

        for component in self.components:
            component.background = True
            component.init()
            component.on_mousedown = on_mousedown
            component.on_mousedrag = on_mousedrag
            component.on_mouserelease = on_mouserelease
    
    def draw(self, shader):
        for component in self.components:
            component.draw(shader)

    def draw_instance(self, shader):
        for component in self.components:
            component.draw_instance(shader)