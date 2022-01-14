from ..shapes import Arrow
from .arrowobject import ArrowObject
from .object import Object
import numpy as np


class GimbalObject(Object):
    """Object for displaying the gimbal controller."""

    def __init__(self, app):
        self.app = app
        self.x_axis = ArrowObject(Arrow(position=[0, 0, 0], direction=[1, 0, 0]), u=4, color=(1, 0, 0), is_selectable=False)
        self.y_axis = ArrowObject(Arrow(position=[0, 0, 0], direction=[0, 1, 0]), u=4, color=(0, 1, 0), is_selectable=False)
        self.z_axis = ArrowObject(Arrow(position=[0, 0, 0], direction=[0, 0, 1]), u=4, color=(0, 0, 1), is_selectable=False)
        self.components = [self.x_axis, self.y_axis, self.z_axis]
        self.enabled = False
        self._attached_to = None

    def toggle(self):
        self.enabled = not self.enabled
        if self.enabled:
            if self.app.selector.selected:
                self.attach(self.app.selector.selected[0])
        else:
            self.detach()

    def attach(self, obj):
        self._attached_to = obj
        for component in self.components:
            component.translation = obj.translation
            component._update_matrix()

    def translate(self, vector):
        for component in self.components:
            component.translate(vector)
            component._update_matrix()

        if self._attached_to:
            self._attached_to.translate(vector)
            self._attached_to._update_matrix()

    def detach(self):
        self._attached_to = None
        for component in self.components:
            component.translation = [0, 0, 0]
            component._update_matrix()

    def init(self):

        def mousedrag(_self, event):
            projection = self.app.view.camera.projection(self.app.width, self.app.height)
            viewworld = self.app.view.camera.viewworld()
            direction = np.matmul(viewworld, np.array([*_self._data.direction, 1], dtype=float))
            direction = np.matmul(projection, direction)[:2]
            direction[1] *= - self.app.height / self.app.width
            dis = np.dot([event['dx'], event['dy']], direction)
            self.translate(_self._data.direction * dis * 0.01)

        for component in self.components:
            component.background = True
            component.init()
            component.add_event_listener('mousedrag', mousedrag)

    def draw(self, shader):
        for component in self.components:
            component.draw(shader)

    def draw_instance(self, shader):
        for component in self.components:
            component.draw_instance(shader)
