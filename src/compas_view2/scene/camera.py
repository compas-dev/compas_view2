import numpy as np

from math import sin
from math import cos
from math import radians

from compas.geometry import Translation
from compas.geometry import Rotation

from .matrices import perspective, ortho


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
    target: list[float], optional
        The target location the camera is aimed at.
        Default is None, in which case the origin of the world coordinate system is used.
    distance: float, optional
        The distance from the camera standpoint to the target.

    Attributes
    ----------
    fov : float
        The field of view as an angler in degrees.
    near : float
        The location of the "near" clipping plane.
    far : float
        The locaiton of the "far" clipping plane.
    distance : float
        Distance between the camera position and the viewing target.
    target : :class:`compas.geometry.Point`
        The viewing target.
        Default is the origin of the world coordinate system.
    rx : float
        Rotation of the world around the X axis.
        Default is -60 degrees.
        See Notes for more information.
    rz : float
        Rotation of the world around the Z axis.
        Default is -30 degrees.
        See Notes for more information.
    tx : float
        Translation of the world in the X direction.
    ty : float
        Translation of the world in the Y direction.
    tz : float
        Translation of the world in the Z direction.
    zoom_delta : float
        Size of one zoom increment.
    rotation_delta : float
        Size of one rotation increment.
    pan_delta : float
        Size of one pan increment.

    Notes
    -----
    Under construction...

    """

    def __init__(self, view, fov=45, near=0.1, far=1000, target=None, distance=10):
        self.view = view
        self.fov = fov
        self.near = near
        self.far = far
        self.distance = distance
        self.target = target or [0, 0, 0]
        self.rx = -60
        self.rz = -30
        self.tx = 0
        self.ty = 0
        self.tz = 0
        self.zoom_delta = 0.05
        self.rotation_delta = 1
        self.pan_delta = 0.05

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
            self.rx += self.rotation_delta * dy
            self.rz += self.rotation_delta * dx

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
        if self.view.current == self.view.PERSPECTIVE:
            sinrz = sin(radians(self.rz))
            cosrz = cos(radians(self.rz))
            sinrx = sin(radians(self.rx))
            cosrx = cos(radians(self.rx))
            _dx = dx * cosrz - dy * sinrz * cosrx
            _dy = dy * cosrz * cosrx + dx * sinrz
            _dz = dy * sinrx * self.pan_delta
            _dx *= 0.1 * self.distance
            _dy *= 0.1 * self.distance
            _dz *= 0.1 * self.distance
            self.tx += self.pan_delta * _dx
            self.ty -= self.pan_delta * _dy
            self.target[0] = -self.tx
            self.target[1] = -self.ty
            self.target[2] -= _dz
            self.distance -= _dz

        elif self.view.current == self.view.FRONT:
            _dx = dx * 0.1 * self.distance
            _dz = dy * 0.1 * self.distance
            self.tx += self.pan_delta * _dx
            self.target[2] += 0.01 * _dz

        elif self.view.current == self.view.RIGHT:
            _dx = dx * 0.1 * self.distance
            _dz = dy * 0.1 * self.distance
            self.tx += self.pan_delta * _dx
            self.target[2] += 0.01 * _dz

        elif self.view.current == self.view.TOP:
            self.tx += dx * self.pan_delta * 0.1 * self.distance
            self.ty -= dy * self.pan_delta * 0.1 * self.distance

        else:
            raise NotImplementedError

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
            P = perspective(self.fov, aspect, self.near, self.far)
        else:
            left = -self.distance
            right = self.distance
            bottom = -self.distance / aspect
            top = self.distance / aspect
            P = ortho(left, right, bottom, top, self.near, self.far)
        return np.asfortranarray(P, dtype=np.float32)

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
        T2 = Translation.from_vector([self.tx, self.ty, -self.distance])
        T1 = Translation.from_vector(self.target)
        if self.view.current == self.view.PERSPECTIVE:
            Rx = Rotation.from_axis_and_angle([1, 0, 0], radians(self.rx))
            Rz = Rotation.from_axis_and_angle([0, 0, 1], radians(self.rz))
            R = Rx * Rz
        elif self.view.current == self.view.FRONT:
            R = Rotation.from_axis_and_angle([1, 0, 0], radians(-90))
        elif self.view.current == self.view.RIGHT:
            Rx = Rotation.from_axis_and_angle([1, 0, 0], radians(-90))
            Rz = Rotation.from_axis_and_angle([0, 0, 1], radians(+90))
            R = Rx * Rz
        elif self.view.current == self.view.TOP:
            R = Rotation()
        else:
            raise NotImplementedError
        T0 = Translation.from_vector([-self.target[0], -self.target[1], -self.target[2]])
        W = T2 * T1 * R * T0
        return np.asfortranarray(W, dtype=np.float32)
