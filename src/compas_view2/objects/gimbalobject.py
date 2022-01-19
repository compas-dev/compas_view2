from ..shapes import Arrow
from compas.geometry import Circle
from compas.geometry import Plane
from compas.geometry import Line
from compas.geometry import Transformation
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import Scale
from compas.geometry import Vector
from .arrowobject import ArrowObject
from .circleobject import CircleObject
from .lineobject import LineObject
from .object import Object
import numpy as np


class GimbalObject(Object):
    """Object for displaying the gimbal controller."""

    def __init__(self, app):
        super().__init__({})
        self.app = app
        self.x_translation = ArrowObject(Arrow(position=[0, 0, 0], direction=[1, 0, 0]), u=4, color=(1, 0, 0), is_selectable=False)
        self.y_translation = ArrowObject(Arrow(position=[0, 0, 0], direction=[0, 1, 0]), u=4, color=(0, 1, 0), is_selectable=False)
        self.z_translation = ArrowObject(Arrow(position=[0, 0, 0], direction=[0, 0, 1]), u=4, color=(0, 0, 1), is_selectable=False)
        self.x_rotation = CircleObject(Circle(Plane([0, 0, 0], [1, 0, 0]), radius=1), u=40, color=(1, 0, 0), linewidth=5, is_selectable=False)
        self.y_rotation = CircleObject(Circle(Plane([0, 0, 0], [0, 1, 0]), radius=1), u=40, color=(0, 1, 0), linewidth=5, is_selectable=False)
        self.z_rotation = CircleObject(Circle(Plane([0, 0, 0], [0, 0, 1]), radius=1), u=40, color=(0, 0, 1), linewidth=5, is_selectable=False)
        self.x_scale = LineObject(Line([0, 0, 0], [1, 0, 0]), color=(1, 0, 0), linewidth=5, is_selectable=False)
        self.y_scale = LineObject(Line([0, 0, 0], [0, 1, 0]), color=(0, 1, 0), linewidth=5, is_selectable=False)
        self.z_scale = LineObject(Line([0, 0, 0], [0, 0, 1]), color=(0, 0, 1), linewidth=5, is_selectable=False)

        self.translations = [self.x_translation, self.y_translation, self.z_translation]
        self.rotations = [self.x_rotation, self.y_rotation, self.z_rotation]
        self.scales = [self.x_scale, self.y_scale, self.z_scale]
        self.components = self.translations + self.rotations + self.scales
        self.enabled = False
        self._attached_to = None
        self.mode = 'translate'
        self.coordinate_system = 'local'

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

        if self.coordinate_system == 'world':
            for component in self.components:
                component.translation = self.translation
                component._update_matrix()
        elif self.coordinate_system == 'local':
            for component in self.components:
                component.translation = self.translation
                component.rotation = self.rotation
                component._update_matrix()

        if self._attached_to:
            self._attached_to.matrix = self.matrix

    def detach(self):
        self._attached_to = None
        self.translation = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]
        self._update_matrix()

    def switch_coordinate_system(self):
        if self.coordinate_system == 'world':
            self.coordinate_system = 'local'
            if self._attached_to:
                self.matrix = self._attached_to.matrix

        else:
            self.coordinate_system = 'world'
            for component in self.components:
                component.rotation = [0, 0, 0]
                component.scale = [1, 1, 1]
                component._update_matrix()

        print("Switched to {} coordinate system".format(self.coordinate_system))
        self._update_matrix()

    def init(self):

        def _project(pt, transform=None):
            projection = self.app.view.camera.projection(self.app.width, self.app.height)
            viewworld = self.app.view.camera.viewworld()
            pt = np.array([*pt, 1], dtype=float)
            if transform:
                pt = np.matmul(transform, pt)
            pt = np.matmul(viewworld, pt)
            pt = np.matmul(projection, pt)
            pt = pt / pt[3]
            pt[0] *= self.app.width / 2
            pt[1] *= - self.app.height / 2
            return pt

        def translate(_self, event):
            if self.coordinate_system == 'world':
                direction = _self._data.direction
            elif self.coordinate_system == 'local':
                R = Rotation.from_euler_angles(self.rotation)
                direction = Vector(*_self._data.direction).transformed(R)
            else:
                raise Exception("Unknown coordinate system")

            direction_2d = _project(direction)[:2]
            direction_2d /= np.linalg.norm(direction_2d)
            dis = np.dot([event['dx'], event['dy']], direction_2d)
            self.translate(direction * dis * 0.01)
            self._update_matrix()

        def rotate(_self, event):
            projected_center = _project([0, 0, 0], _self.matrix)
            current_pos = np.array([event['x'] - self.app.width/2, event['y'] - self.app.height/2])
            last_pos = np.array([current_pos[0] - event['dx'], current_pos[1] - event['dy']])

            v1 = current_pos - projected_center[:2]
            v2 = last_pos - projected_center[:2]
            v1 /= np.linalg.norm(v1)
            v2 /= np.linalg.norm(v2)
            angle = np.math.atan2(np.linalg.det([v1, v2]), np.dot(v1, v2))

            if self.coordinate_system == 'world':
                normal = _self._data.plane.normal
            elif self.coordinate_system == 'local':
                R = Rotation.from_euler_angles(self.rotation)
                normal = Vector(*_self._data.plane.normal).transformed(R)
            else:
                raise Exception("Unknown coordinate system")

            projected_normal = _project(normal, _self.matrix)
            if projected_normal[2] > projected_center[2]:
                angle *= -1

            Rd = Rotation.from_axis_and_angle(normal, angle)
            T1 = Translation.from_vector(self.translation)
            R1 = Rotation.from_euler_angles(self.rotation)
            S1 = Scale.from_factors(self.scale)
            M = T1 * Rd * R1 * S1
            self.matrix = M.matrix

        def scale(_self, event):
            if self.coordinate_system == 'world':
                direction = _self._data.end
                direction_2d = _project(direction)[:2]
                direction_2d /= np.linalg.norm(direction_2d)
                dis = np.dot([event['dx'], event['dy']], direction_2d)
                scale_factor = _self._data.end * dis * 0.01 + np.array([1, 1, 1])
                S = Scale.from_factors(scale_factor)
                M = S * Transformation(self.matrix)
                self.matrix = M.matrix
            elif self.coordinate_system == 'local':
                R = Rotation.from_euler_angles(self.rotation)
                direction = Vector(*_self._data.end).transformed(R)
                direction_2d = _project(direction)[:2]
                direction_2d /= np.linalg.norm(direction_2d)
                dis = np.dot([event['dx'], event['dy']], direction_2d)
                scale_factor = _self._data.end * dis * 0.01 + np.array([1, 1, 1])
                S = Scale.from_factors(scale_factor)
                M = Transformation(self.matrix) * S
                self.matrix = M.matrix
            else:
                raise Exception("Unknown coordinate system")


        for component in self.translations:
            component.background = True
            component.init()
            component.add_event_listener('mousedrag', translate)

        for component in self.rotations:
            component.background = True
            component.init()
            component.add_event_listener('mousedrag', rotate)

        for component in self.scales:
            component.background = True
            component.init()
            component.add_event_listener('mousedrag', scale)

    def draw(self, shader):
        if self.mode == 'translate':
            for component in self.translations:
                component.draw(shader)
        elif self.mode == 'rotate':
            for component in self.rotations:
                component.draw(shader)
        elif self.mode == 'scale':
            for component in self.scales:
                component.draw(shader)

    def draw_instance(self, shader):
        if self.mode == 'translate':
            for component in self.translations:
                component.draw_instance(shader)
        elif self.mode == 'rotate':
            for component in self.rotations:
                component.draw_instance(shader)
        elif self.mode == 'scale':
            for component in self.scales:
                component.draw_instance(shader)
