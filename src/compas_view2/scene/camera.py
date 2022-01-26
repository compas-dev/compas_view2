import numpy as np

from math import sin
from math import cos
from math import radians

from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import decompose_matrix
from compas.geometry import rotate_points
from compas.geometry import Transformation


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

    def __init__(self, view, fov=45, near=0.1, far=1000, position=None, target=None):
        self.view = view
        self.fov = fov
        self.near = near
        self.far = far
        self.position = np.array(position or [0, 0, 10], dtype=float)
        self.target = np.array(target or [0, 0, 0], dtype=float)
        self.rotation = np.array([0, 0, 0], dtype=float)
        self.zoom_delta = 0.05
        self.rotation_delta = 0.01
        self.pan_delta = 0.05
        self.reset_position()

    def _update_position(self):
        R = Rotation.from_euler_angles(self.rotation)
        T = Translation.from_vector([0, 0, self.distance])
        _, _, _, translation, _ = decompose_matrix((R * T).matrix)
        self.position = translation + self.target

    @property
    def distance(self):
        return np.linalg.norm(self.position - self.target)

    @distance.setter
    def distance(self, distacne):
        direction = (self.position - self.target) / self.distance
        self.position = direction * distacne + self.target

    def reset_position(self):
        if self.view.current == self.view.PERSPECTIVE:
            self.position = np.array([-10, -10, 10], dtype=float)
            self.rotation = np.array([np.pi/4, 0, -np.pi/4], dtype=float)
        if self.view.current == self.view.TOP:
            self.position = np.array([0, 0, 10], dtype=float)
            self.rotation = np.array([0, 0, 0], dtype=float)
        if self.view.current == self.view.FRONT:
            self.position = np.array([0, -10, 0], dtype=float)
            self.rotation = np.array([np.pi/2, 0, 0], dtype=float)
        if self.view.current == self.view.RIGHT:
            self.position = np.array([10, 0, 0], dtype=float)
            self.rotation = np.array([np.pi/2, 0, np.pi/2], dtype=float)


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
            self.rotation[0] += self.rotation_delta * dy
            self.rotation[2] += self.rotation_delta * dx

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
        T = Translation.from_vector([-dx * self.pan_delta, dy * self.pan_delta, 0])
        _, _, _, translation, _ = decompose_matrix((R * T).matrix)
        self.target += translation

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
        self._update_position()
        T = Translation.from_vector(self.position)
        R = Rotation.from_euler_angles(self.rotation)
        W = T * R
        return np.asfortranarray(W.inverted(), dtype=np.float32)
