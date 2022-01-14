from ..shapes import Arrow
from compas.geometry import Circle
from compas.geometry import Plane
from .arrowobject import ArrowObject
from .circleobject import CircleObject
from .object import Object
import numpy as np


class GimbalObject(Object):
    """Object for displaying the gimbal controller."""

    def __init__(self, app):
        super().__init__({})
        self.app = app
        self.x_axis = ArrowObject(Arrow(position=[0, 0, 0], direction=[1, 0, 0]), u=4, color=(1, 0, 0), is_selectable=False)
        self.y_axis = ArrowObject(Arrow(position=[0, 0, 0], direction=[0, 1, 0]), u=4, color=(0, 1, 0), is_selectable=False)
        self.z_axis = ArrowObject(Arrow(position=[0, 0, 0], direction=[0, 0, 1]), u=4, color=(0, 0, 1), is_selectable=False)

        self.x_rotation = CircleObject(Circle(Plane([0, 0, 0], [1, 0, 0]), radius=1), u=40, color=(1, 0, 0), linewidth=5, is_selectable=False)
        self.y_rotation = CircleObject(Circle(Plane([0, 0, 0], [0, 1, 0]), radius=1), u=40, color=(0, 1, 0), linewidth=5, is_selectable=False)
        self.z_rotation = CircleObject(Circle(Plane([0, 0, 0], [0, 0, 1]), radius=1), u=40, color=(0, 0, 1), linewidth=5, is_selectable=False)

        self.axises = [self.x_axis, self.y_axis, self.z_axis]
        self.rotations = [self.x_rotation, self.y_rotation, self.z_rotation]
        self.components = self.axises + self.rotations
        self.enabled = False
        self._attached_to = None
        self.mode = 'translate'

    def toggle(self):
        self.enabled = not self.enabled
        if self.enabled:
            if self.app.selector.selected:
                self.attach(self.app.selector.selected[0])
        else:
            self.detach()

    def attach(self, obj):
        self._attached_to = obj
        self.matrix = obj.matrix

    def _update_matrix(self):
        super()._update_matrix()
        for component in self.components:
            component.matrix = self.matrix
        if self._attached_to:
            self._attached_to.matrix = self.matrix

    def detach(self):
        self._attached_to = None
        self.translation = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]
        self._update_matrix()

    def init(self):

        def project(pt, transform=None):
            projection = self.app.view.camera.projection(self.app.width, self.app.height)
            viewworld = self.app.view.camera.viewworld()
            pt = np.array([*pt, 1], dtype=float)
            if transform:
                pt = np.matmul(transform, pt)
            pt = np.matmul(viewworld, pt)
            pt = np.matmul(projection, pt)
            pt = pt[:2] / pt[3]
            pt[0] *= self.app.width / 2
            pt[1] *= - self.app.height / 2
            return pt

        def mousedrag(_self, event):
            direction_2d = project(_self._data.direction)
            direction_2d /= np.linalg.norm(direction_2d)
            dis = np.dot([event['dx'], event['dy']], direction_2d)
            self.translate(_self._data.direction * dis * 0.01)
            self._update_matrix()

        for component in self.axises:
            component.background = True
            component.init()
            component.add_event_listener('mousedrag', mousedrag)

        def mousedrag(_self, event):
            rotation_center = project([0, 0, 0], _self.matrix)
            current_pos = np.array([event['x'] - self.app.width/2, event['y'] - self.app.height/2])
            last_pos = np.array([current_pos[0] - event['dx'], current_pos[1] - event['dy']])

            v1 = current_pos - rotation_center
            v2 = last_pos - rotation_center
            v1 /= np.linalg.norm(v1)
            v2 /= np.linalg.norm(v2)
            angle = np.math.atan2(np.linalg.det([v1, v2]), np.dot(v1, v2))

            normal_2d = project(_self._data.normal)
            if normal_2d.dot(v1) > 0:
                angle = -angle

            self.rotate(_self._data.plane.normal * angle)
            print(self.rotation)
            self._update_matrix()

        for component in self.rotations:
            component.background = True
            component.init()
            component.add_event_listener('mousedrag', mousedrag)

    def draw(self, shader):
        if self.mode == 'translate':
            for component in self.axises:
                component.draw(shader)
        elif self.mode == 'rotate':
            for component in self.rotations:
                component.draw(shader)

    def draw_instance(self, shader):
        if self.mode == 'translate':
            for component in self.axises:
                component.draw_instance(shader)
        elif self.mode == 'rotate':
            for component in self.rotations:
                component.draw_instance(shader)
