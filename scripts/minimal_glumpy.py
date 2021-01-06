from math import cos, sin, radians

import numpy as np

from glumpy import app, gl, gloo, glm

from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Pointcloud


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
        _dx *= self.distance / 10.
        _dy *= self.distance / 10.
        _dz *= self.distance / 10.
        self.tx += self.pan_delta * _dx
        self.ty -= self.pan_delta * _dy
        self.target[0] = -self.tx
        self.target[1] = -self.ty
        self.target[2] -= _dz
        self.distance -= _dz

    def zoom(self, steps=1):
        self.distance -= steps * self.zoom_delta * self.distance

    def projection(self, width, height):
        return glm.perspective(self.fov, width / height, self.near, self.far)

    def view(self):
        return np.eye(4, dtype=np.float32)

    def world(self):
        world = np.eye(4, dtype=np.float32)
        glm.translate(world, -self.target[0], -self.target[1], -self.target[2])
        glm.rotate(world, self.rz, 0, 0, 1)
        glm.rotate(world, self.rx, 1, 0, 0)
        glm.translate(world, +self.target[0], +self.target[1], +self.target[2])
        glm.translate(world, self.tx, self.ty, -self.distance)
        return world


BOX_VERT_SHADER = """
attribute vec3 position;
attribute vec3 color;

uniform vec4 colormask;
uniform int is_selected;
uniform float opacity;

uniform mat4 projection;
uniform mat4 world;

varying vec4 vertex_color;

void main()
{
    if (is_selected == 1){
        vertex_color = vec4(1.0, 1.0, 0.0, opacity) * colormask;
    }
    else {
        vertex_color = vec4(color, opacity) * colormask;
    }

    gl_Position = projection * world * vec4(position, 1.0);
}
"""

BOX_FRAG_SHADER = """
varying vec4 vertex_color;

void main()
{
    gl_FragColor = vertex_color;
}
"""


window = app.Window(width=800, height=500, title="Minimal Glumpy", color=(1, 1, 1, 1))
camera = Camera()


@window.event
def on_init():
    gl.glPolygonOffset(1.0, 1.0)
    gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
    gl.glEnable(gl.GL_CULL_FACE)
    gl.glCullFace(gl.GL_BACK)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glDepthFunc(gl.GL_LESS)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glEnable(gl.GL_POINT_SMOOTH)
    gl.glEnable(gl.GL_LINE_SMOOTH)
    gl.glEnable(gl.GL_POLYGON_SMOOTH)
    gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)
    gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_NICEST)


@window.event
def on_resize(width, height):
    box_program['projection'] = camera.projection(width, height)


@window.event
def on_draw(dt):
    window.clear()
    box_program['world'] = camera.world()

    for box in box_objects:
        box_program.bind(box['V'])
        box_program['opacity'] = box['opacity']
        box_program['is_selected'] = box['is_selected']
        box_program['colormask'] = [1.0, 1.0, 1.0, 1.0]
        box_program.draw(gl.GL_TRIANGLES, box['F'])
        box_program['colormask'] = [0.0, 0.0, 0.0, 1.0]
        box_program.draw(gl.GL_LINES, box['E'])
        box_program['is_selected'] = 0
        box_program['opacity'] = 1.0


@window.event
def on_mouse_drag(x, y, dx, dy, buttons):
    if buttons == 1:
        camera.rotate(dx, dy)
    elif buttons == 4:
        camera.pan(dx, dy)


@window.event
def on_mouse_scroll(dx, dy):
    pass


box_program = gloo.Program(BOX_VERT_SHADER, BOX_FRAG_SHADER, count=3*2*6)
box_program['projection'] = np.eye(4, dtype=np.float32)
box_program['world'] = np.eye(4, dtype=np.float32)
box_program['is_selected'] = 1
box_program['opacity'] = 1.0

box_objects = []

pcl = Pointcloud.from_bounds(10, 5, 3, 1000)

for point in pcl:
    box = Box((point, [1, 0, 0], [0, 1, 0]), 0.1, 0.1, 0.1)
    mesh = Mesh.from_shape(box)

    i = 0
    vertices = []
    edges = []
    faces = []
    for face in mesh.faces():
        a, b, c, d = mesh.face_coordinates(face)
        vertices.append(a)  # 0
        vertices.append(b)  # 1
        vertices.append(c)  # 2
        vertices.append(a)  # 3
        vertices.append(c)  # 4
        vertices.append(d)  # 5
        faces.append([i + 0, i + 1, i + 2])
        faces.append([i + 3, i + 4, i + 5])
        edges.append([i + 0, i + 1])
        edges.append([i + 1, i + 2])
        edges.append([i + 2, i + 5])
        edges.append([i + 5, i + 0])
        i += 6

    V = np.zeros(len(vertices), dtype=[("position", np.float32, 3), ("color", np.float32, 3)])
    F = np.array(faces, dtype=np.uint32).ravel()
    E = np.array(edges, dtype=np.uint32).ravel()
    V["position"] = vertices
    V["color"] = [(0.7, 0.7, 0.7)] * len(vertices)
    V = V.view(gloo.VertexBuffer)
    F = F.view(gloo.IndexBuffer)
    E = E.view(gloo.IndexBuffer)

    box_objects.append({'V': V, 'F': F, 'E': E, 'is_selected': False, 'opacity': 1.0})

app.run()
