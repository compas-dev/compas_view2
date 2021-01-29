from math import tan, radians

from compas.geometry import Transformation
from compas.geometry import normalize_vector, subtract_vectors, cross_vectors


def ortho(left, right, bottom, top, near, far):
    dx = right - left
    dy = top - bottom
    dz = far - near
    rx = -(right + left) / dx
    ry = -(top + bottom) / dy
    rz = -(far + near) / dz
    matrix = [
        [2.0 / dx,        0,         0, rx],
        [       0, 2.0 / dy,         0, ry],  # noqa: E201
        [       0,        0, -2.0 / dz, rz],  # noqa: E201
        [       0,        0,         0,  1]   # noqa: E201
    ]
    return Transformation.from_matrix(matrix)


def perspective(fov, aspect, near, far):
    sy = 1.0 / tan(radians(fov) / 2.0)
    sx = sy / aspect
    zz = (far + near) / (near - far)
    zw = 2 * far * near / (near - far)
    matrix = [
        [sx,  0,  0,  0],
        [ 0, sy,  0,  0],  # noqa: E201
        [ 0,  0, zz, zw],  # noqa: E201
        [ 0,  0, -1,  0]   # noqa: E201
    ]
    return Transformation.from_matrix(matrix)


def lookat(eye, target, up):
    d = normalize_vector(subtract_vectors(target, eye))
    r = cross_vectors(d, normalize_vector(up))
    u = cross_vectors(r, d)
    matrix = [
        [+r[0], +r[1], +r[2], -eye[0]],
        [+u[0], +u[1], +u[2], -eye[1]],
        [-d[0], -d[1], -d[2], -eye[2]],
        [    0,     0,    0,       1]  # noqa: E201
    ]
    return Transformation.from_matrix(matrix)
