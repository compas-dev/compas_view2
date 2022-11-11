from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import Vector
from numpy.linalg import norm
from numpy.linalg import det
from math import atan2
from numpy import pi
from numpy import array
from numpy import asfortranarray
from numpy import dot
from numpy import float32
from compas_view2.objects import Object
from typing import List

from .matrices import perspective, ortho


class Position(Vector):
    def __init__(self, vector, on_update=None):
        super().__init__(*vector)
        self.pause_update = False
        if on_update:
            self.on_update = on_update

    def set(self, x, y, z, pause_update=False):
        pause_update = pause_update or self.pause_update
        if hasattr(self, "on_update") and not pause_update:
            self.on_update([x, y, z])
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if hasattr(self, "on_update") and not self.pause_update:
            self.on_update([x, self.y, self.z])
        self._x = float(x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if hasattr(self, "on_update") and not self.pause_update:
            self.on_update([self.x, y, self.z])
        self._y = float(y)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        if hasattr(self, "on_update") and not self.pause_update:
            self.on_update([self.x, self.y, z])
        self._z = float(z)


class RotationEuler(Position):
    pass


class Camera:
    """Camera object for the default view.

    Parameters
    ----------
    view: :class:`compas_view2.views.View`,
        The parent view of the camera.
    fov: float, optional
        The field-of-view of the camera in degrees.
    near: float, optional
        Distance to the near clipping plane.
    far: float, optional
        Distance to the far clipping plane.
    position: list[float], optional
        The location the camera.
    target: list[float], optional
        The target location the camera is aimed at.
        Default is None, in which case the origin of the world coordinate system is used.
    scale: float, optional
        The scale factor for camera's near, far and pan_delta.
        Default is 1.0.

    Attributes
    ----------
    fov : float
        The field of view as an angler in degrees.
    near : float
        The location of the "near" clipping plane.
    far : float
        The locaiton of the "far" clipping plane.
    position : :class:`compas_view2.scene.camera.Position`
        The location the camera.
    rotation : :class:`compas_view2.scene.camera.RotationEuler`
        The euler rotation of camera.
    target : :class:`compas_view2.scene.camera.Position`
        The viewing target.
        Default is the origin of the world coordinate system.
    distance : float
        The distance from the camera standpoint to the target.
    zoom_delta : float
        Size of one zoom increment.
    rotation_delta : float
        Size of one rotation increment.
    pan_delta : float
        Size of one pan increment.
    scale : float
        The scale factor for camera's near, far and pan_delta.

    Notes
    -----
    Under construction...

    """

    def __init__(self, view, fov=45, near=0.1, far=1000, position=None, target=None, scale=1.0):
        self.view = view
        self.fov = fov
        self.near = near
        self.far = far
        self.scale = scale
        self._position = Position([0, 0, 10 * scale], on_update=self._on_position_update)
        self._rotation = RotationEuler([0, 0, 0], on_update=self._on_rotation_update)
        self._target = Position([0, 0, 0], on_update=self._on_target_update)
        self.zoom_delta = 0.05
        self.rotation_delta = 0.01
        self.pan_delta = 0.05
        self.reset_position()
        if target:
            self.target = target
        if position:
            self.position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position.set(*position)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation.set(*rotation)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        self._target.set(*target)

    def look_at(self, target):
        """Set the target of the camera, while keeping the current position."""
        position = list(self.position)
        self.target = target
        self.position = position

    @property
    def distance(self):
        return (self.position - self.target).length

    @distance.setter
    def distance(self, distance):
        """Update the position based on the distance."""
        direction = self.position - self.target
        direction.unitize()
        new_position = self.target + direction * distance
        self.position.set(*new_position, pause_update=True)

    def _on_position_update(self, new_position):
        """Update camera rotation to keep pointing the target."""
        old_direction = array(self.position - self.target)
        new_direction = array(Vector(*new_position) - self.target)
        old_distance = norm(old_direction)
        new_distance = norm(new_direction)
        self.distance *= new_distance / old_distance

        old_direction_xy = old_direction[:2]
        new_direction_xy = new_direction[:2]
        old_direction_xy_distance = norm(old_direction_xy)
        new_direction_xy_distance = norm(new_direction_xy)

        old_direction_pitch = array([old_direction_xy_distance, old_direction[2]])
        new_direction_pitch = array([new_direction_xy_distance, new_direction[2]])
        old_direction_pitch_distance = norm(old_direction_pitch)
        new_direction_pitch_distance = norm(new_direction_pitch)

        old_direction_xy /= old_direction_xy_distance
        new_direction_xy /= new_direction_xy_distance
        old_direction_pitch /= old_direction_pitch_distance
        new_direction_pitch /= new_direction_pitch_distance

        angle_z = atan2(det([old_direction_xy, new_direction_xy]), dot(old_direction_xy, new_direction_xy))
        angle_x = -atan2(det([old_direction_pitch, new_direction_pitch]), dot(old_direction_pitch, new_direction_pitch))

        new_rotation = self.rotation + [angle_x or 0, 0, angle_z or 0]
        self.rotation.set(*new_rotation, pause_update=True)

    def _on_rotation_update(self, rotation):
        """Update camera position when rotation around target."""
        R = Rotation.from_euler_angles(rotation)
        T = Translation.from_vector([0, 0, self.distance])
        M = (R * T).matrix
        vector = [M[i][3] for i in range(3)]
        position = self.target + vector

        self.position.set(*position, pause_update=True)

    def _on_target_update(self, target):
        """Update camera position when target changes."""
        R = Rotation.from_euler_angles(self.rotation)
        T = Translation.from_vector([0, 0, self.distance])
        M = (R * T).matrix
        vector = [M[i][3] for i in range(3)]
        position = Vector(*target) + Vector(*vector)

        self.target.set(*target, pause_update=True)
        self.position.set(*position, pause_update=True)

    def reset_position(self):
        """Reset the position of the camera based current view type."""
        self.target.set(0, 0, 0)
        if self.view.current == self.view.PERSPECTIVE:
            self.rotation.set(pi / 4, 0, -pi / 4)
        if self.view.current == self.view.TOP:
            self.rotation.set(0, 0, 0)
        if self.view.current == self.view.FRONT:
            self.rotation.set(pi / 2, 0, 0)
        if self.view.current == self.view.RIGHT:
            self.rotation.set(pi / 2, 0, pi / 2)

    def rotate(self, dx, dy):
        """Rotate the camera based on current mouse movement.

        Parameters
        ----------
        dx : float
            Number of rotation increments around the Z axis, with each increment the size of :attr:`Camera.rotation_delta`.
        dy: float
            Number of rotation increments around the X axis, with each increment the size of :attr:`Camera.rotation_delta`.

        Returns
        -------
        None

        Notes
        -----
        Camera rotations are only available if the current view is a perspective view (``camera.view.current == camera.view.PERSPECTIVE``).

        """
        if self.view.current == self.view.PERSPECTIVE:
            self.rotation += [-self.rotation_delta * dy, 0, -self.rotation_delta * dx]

    def pan(self, dx, dy):
        """Pan the camera based on current mouse movement.

        Parameters
        ----------
        dx : float
            Number of "pan" increments in the "X" direction of the current view, with each increment the size of :attr:`Camera.pan_delta`.
        dy : float
            Number of "pan" increments in the "Y" direction of the current view, with each increment the size of :attr:`Camera.pan_delta`.

        Returns
        -------
        None

        """
        R = Rotation.from_euler_angles(self.rotation)
        T = Translation.from_vector([-dx * self.pan_delta * self.scale, dy * self.pan_delta * self.scale, 0])
        M = (R * T).matrix
        vector = [M[i][3] for i in range(3)]
        self.target += vector

    def zoom(self, steps=1):
        """Zoom in or out.

        Parameters
        ----------
        steps : int
            The number of zoom increments, with each increment the zsize of :attr:`Camera.zoom_delta`.

        Returns
        -------
        None

        """
        self.distance -= steps * self.zoom_delta * self.distance

    def projection(self, width, height):
        """Compute the projection matrix corresponding to the current camera settings.

        Parameters
        ----------
        width : float
            Width of the viewer.
        height : float
            Height of the viewer.

        Returns
        -------
        4x4 np.array
            The transformation matrix as a `numpy` array in column-major order.

        Notes
        -----
        The projection matrix transforms the scene from camera coordinates to screen coordinates.

        """
        aspect = width / height
        if self.view.current == self.view.PERSPECTIVE:
            P = perspective(self.fov, aspect, self.near * self.scale, self.far * self.scale)
        else:
            left = -self.distance
            right = self.distance
            bottom = -self.distance / aspect
            top = self.distance / aspect
            P = ortho(left, right, bottom, top, self.near * self.scale, self.far * self.scale)
        return asfortranarray(P, dtype=float32)

    def viewworld(self):
        """Compute the view-world matrix corresponding to the current camera settings.

        Returns
        -------
        4x4 np.array
            The transformation matrix in column-major order.

        Notes
        -----
        The view-world matrix transforms the scene from world coordinates to camera coordinates.

        """
        T = Translation.from_vector(self.position)
        R = Rotation.from_euler_angles(self.rotation)
        W = T * R
        return asfortranarray(W.inverted(), dtype=float32)

    def zoom_extents(self, objects: List[Object] = None):

        objects = objects or self.view.objects.values()

        extents = []

        for obj in objects:
            if not obj.is_visible:
                continue

            if obj.bounding_box is None and hasattr(obj, "_update_bounding_box"):
                obj._update_bounding_box()

            if obj.bounding_box is not None:
                extents.append(obj.bounding_box)

        extents = array([obj.bounding_box for obj in objects if obj.bounding_box is not None])

        if len(extents) == 0:
            return

        extents = extents.reshape(-1, 3)
        max_corner = extents.max(axis=0)
        min_corner = extents.min(axis=0)
        center = (max_corner + min_corner) / 2
        distance = norm(max_corner - min_corner)

        self.target = center
        self.position = center + self.position
        self.distance = distance * 1.5
