from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import decompose_matrix
from numpy.linalg import norm
from numpy.linalg import det
from math import atan2
from numpy import pi
from numpy import array
from numpy import asfortranarray
from numpy import dot


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

    def __init__(self, view, fov=45, near=0.1, far=1000, distance=10, target=None):
        self.view = view
        self.fov = fov
        self.near = near
        self.far = far
        self.distance = distance
        self.target = array(target or [0, 0, 0], dtype=float)
        self.rotation = array([0, 0, 0], dtype=float)
        self.zoom_delta = 0.05
        self.rotation_delta = 0.01
        self.pan_delta = 0.05
        self.reset_position()

    @property
    def position(self):
        R = Rotation.from_euler_angles(self.rotation)
        T = Translation.from_vector([0, 0, self.distance])
        M = (R * T).matrix
        vector = [M[i][3] for i in range(3)]
        return self.target + vector

    @position.setter
    def position(self, new_position):
        old_direction = self.position - self.target
        new_direction = new_position - self.target
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

        self.rotation[0] += angle_x
        self.rotation[2] += angle_z

    def reset_position(self):
        if self.view.current == self.view.PERSPECTIVE:
            self.rotation = array([pi/4, 0, -pi/4], dtype=float)
        if self.view.current == self.view.TOP:
            self.rotation = array([0, 0, 0], dtype=float)
        if self.view.current == self.view.FRONT:
            self.rotation = array([pi/2, 0, 0], dtype=float)
        if self.view.current == self.view.RIGHT:
            self.rotation = array([pi/2, 0, pi/2], dtype=float)
        self.target = array([0, 0, 0], dtype=float)

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
            P = perspective(self.fov, aspect, self.near, self.far)
        else:
            left = -self.distance
            right = self.distance
            bottom = -self.distance / aspect
            top = self.distance / aspect
            P = ortho(left, right, bottom, top, self.near, self.far)
        return asfortranarray(P)

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
        return asfortranarray(W.inverted())
