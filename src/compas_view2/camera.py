from math import sin, cos, radians
import numpy as np
from compas.geometry import Translation, Rotation

from .matrices import perspective


class Camera:

    def __init__(self, fov=45, near=0.1, far=100, target=None, distance=10):
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
        self.rx += self.rotation_delta * dy
        self.rz += self.rotation_delta * dx

    def pan(self, dx, dy):
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

    def zoom(self, steps=1):
        self.distance -= steps * self.zoom_delta * self.distance

    def projection(self, width, height):
        P = perspective(self.fov, width / height, self.near, self.far)
        return np.asfortranarray(P, dtype=np.float32)

    def viewworld(self):
        T2 = Translation.from_vector([self.tx, self.ty, -self.distance])
        T1 = Translation.from_vector(self.target)
        Rx = Rotation.from_axis_and_angle([1, 0, 0], radians(self.rx))
        Rz = Rotation.from_axis_and_angle([0, 0, 1], radians(self.rz))
        T0 = Translation.from_vector([-self.target[0], -self.target[1], -self.target[2]])
        W = T2 * T1 * Rx * Rz * T0
        return np.asfortranarray(W, dtype=np.float32)
