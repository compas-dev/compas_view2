import sys
from math import tan, cos, sin, radians

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtOpenGL

from OpenGL import GL

import ctypes as ct
import numpy as np

from compas.geometry import Transformation, Translation, Rotation
from compas.geometry import normalize_vector, subtract_vectors, cross_vectors

from compas.utilities import flatten


DTYPE_OTYPE = {}


VSHADER = """
#version 120

attribute vec3 position;
attribute vec3 color;

uniform mat4 P;
uniform mat4 W;

varying vec4 vertex_color;

void main()
{
    vertex_color = vec4(color, 1.0);

    gl_Position = P * W * vec4(position, 1.0);
}
"""

FSHADER = """
#version 120

varying vec4 vertex_color;

void main()
{
    gl_FragColor = vertex_color;
}
"""


# ==============================================================================
# ==============================================================================
# ==============================================================================
# Helpers
# ==============================================================================
# ==============================================================================
# ==============================================================================


def make_shader_program(vsource, fsource):
    vertex = compile_vertex_shader(vsource)
    fragment = compile_fragment_shader(fsource)
    program = GL.glCreateProgram()
    GL.glAttachShader(program, vertex)
    GL.glAttachShader(program, fragment)
    GL.glLinkProgram(program)
    GL.glValidateProgram(program)
    result = GL.glGetProgramiv(program, GL.GL_LINK_STATUS)
    if not result:
        raise RuntimeError(GL.glGetProgramInfoLog(program))
    GL.glDeleteShader(vertex)
    GL.glDeleteShader(fragment)
    return program


def compile_vertex_shader(source):
    shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
    GL.glShaderSource(shader, source)
    GL.glCompileShader(shader)
    result = GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS)
    if not result:
        raise RuntimeError(GL.glGetShaderInfoLog(shader))
    return shader


def compile_fragment_shader(source):
    shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
    GL.glShaderSource(shader, source)
    GL.glCompileShader(shader)
    result = GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS)
    if not result:
        raise RuntimeError(GL.glGetShaderInfoLog(shader))
    return shader


def make_vertex_buffer(data):
    n = len(data)
    size = n * ct.sizeof(ct.c_float)
    vbo = GL.glGenBuffers(1)
    data = (ct.c_float * n)(* data)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, size, data, GL.GL_STATIC_DRAW)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vbo


def make_index_buffer(data):
    n = len(data)
    size = n * ct.sizeof(ct.c_uint)
    vbo = GL.glGenBuffers(1)
    data = (ct.c_int * n)(* data)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, size, data, GL.GL_STATIC_DRAW)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    return vbo


def ortho(left, right, bottom, top, near, far):
    dx = right - left
    dy = top - bottom
    dz = far - near
    rx = -(right + left) / dx
    ry = -(top + bottom) / dy
    rz = -(far + near) / dz
    matrix = [
        [2.0 / dx,        0,         0, rx],
        [       0, 2.0 / dy,         0, ry],
        [       0,        0, -2.0 / dz, rz],
        [       0,        0,         0,  1]
    ]
    return Transformation.from_matrix(matrix)


def perspective(fov, aspect, near, far):
    sy = 1.0 / tan(radians(fov) / 2.0)
    sx = sy / aspect
    zz = (far + near) / (near - far)
    zw = 2 * far * near / (near - far)
    matrix = [
        [sx,  0,  0,  0],
        [ 0, sy,  0,  0],
        [ 0,  0, zz, zw],
        [ 0,  0, -1,  0]
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
        [    0,     0,    0,       1]
    ]
    return Transformation.from_matrix(matrix)


def gl_info():
    info = """
        Vendor: {0}
        Renderer: {1}
        OpenGL Version: {2}
        Shader Version: {3}
        """.format(
        GL.glGetString(GL.GL_VENDOR),
        GL.glGetString(GL.GL_RENDERER),
        GL.glGetString(GL.GL_VERSION),
        GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION)
    )
    return info


# ==============================================================================
# ==============================================================================
# ==============================================================================
# App & Main Window
# ==============================================================================
# ==============================================================================
# ==============================================================================


class Viewer:

    def __init__(self):
        glFormat = QtGui.QSurfaceFormat()
        glFormat.setVersion(2, 1)
        glFormat.setProfile(QtGui.QSurfaceFormat.CompatibilityProfile)
        glFormat.setDefaultFormat(glFormat)
        QtGui.QSurfaceFormat.setDefaultFormat(glFormat)

        app = QtCore.QCoreApplication.instance()
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
        app.references = set()

        self.app = app
        self.main = QtWidgets.QMainWindow()
        self.app.references.add(self.main)
        self.view = View()
        self.main.setCentralWidget(self.view)
        self.main.setContentsMargins(0, 0, 0, 0)
        self.main.resize(self.view.width, self.view.height)
        desktop = self.app.desktop()
        rect = desktop.availableGeometry()
        x = 0.5 * (rect.width() - self.view.width)
        y = 0.5 * (rect.height() - self.view.height)
        self.main.setGeometry(x, y, self.view.width, self.view.height)

    def add(self, data, **kwargs):
        self.view.objects[data] = DTYPE_OTYPE[type(data)](data, **kwargs)

    def show(self):
        self.main.show()
        self.app.exec_()


# ==============================================================================
# ==============================================================================
# ==============================================================================
# OpenGL View
# ==============================================================================
# ==============================================================================
# ==============================================================================


class PerspectiveCamera:

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

    def P(self, width, height):
        P = perspective(self.fov, width / height, self.near, self.far)
        return np.asfortranarray(P, dtype=np.float32)

    def W(self):
        T2 = Translation.from_vector([self.tx, self.ty, -self.distance])
        T1 = Translation.from_vector(self.target)
        Rx = Rotation.from_axis_and_angle([1, 0, 0], radians(self.rx))
        Rz = Rotation.from_axis_and_angle([0, 0, 1], radians(self.rz))
        T0 = Translation.from_vector([-self.target[0], -self.target[1], -self.target[2]])
        W = T2 * T1 * Rx * Rz * T0
        return np.asfortranarray(W, dtype=np.float32)


class Mouse:

    def __init__(self):
        self.pos = QtCore.QPoint()
        self.last_pos = QtCore.QPoint()
        self.buttons = {'left': False, 'right': False}

    def dx(self):
        return self.pos.x() - self.last_pos.x()

    def dy(self):
        return self.pos.y() - self.last_pos.y()


class View(QtWidgets.QOpenGLWidget):
    width = 800
    height = 500
    opacity = 1.0

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.camera = PerspectiveCamera()
        self.mouse = Mouse()
        self.objects = {}

    def uniform4x4(self, program, name, data):
        loc = GL.glGetUniformLocation(program, name)
        GL.glUniformMatrix4fv(loc, 1, True, data)

    def uniform1f(self, program, name, value):
        loc = GL.glGetUniformLocation(program, name)
        GL.glUniform1f(loc, value)

    def initializeGL(self):
        print(gl_info())
        GL.glClearColor(1, 1, 1, 1)
        GL.glPolygonOffset(1.0, 1.0)
        GL.glEnable(GL.GL_POLYGON_OFFSET_FILL)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glCullFace(GL.GL_BACK)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LESS)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_POINT_SMOOTH)
        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glEnable(GL.GL_POLYGON_SMOOTH)
        # init the buffers
        for guid in self.objects:
            obj = self.objects[guid]
            obj.init()
        # create the program
        self.program = make_shader_program(VSHADER, FSHADER)
        GL.glUseProgram(self.program)
        # GL.glBindAttribLocation(self.program, 0, "position)
        # GL.glBindAttribLocation(self.program, 1, "color")
        self.uniform4x4(self.program, "P", self.camera.P(self.width, self.height))
        self.uniform4x4(self.program, "W", self.camera.W())
        GL.glUseProgram(0)

    def resizeGL(self, width: int, height: int):
        self.width = width
        self.height = height
        GL.glViewport(0, 0, width, height)
        GL.glUseProgram(self.program)
        self.uniform4x4(self.program, "P", self.camera.P(self.width, self.height))
        GL.glUseProgram(0)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glUseProgram(self.program)
        self.uniform4x4(self.program, "W", self.camera.W())
        for guid in self.objects:
            obj = self.objects[guid]
            obj.draw(self.program)
        GL.glUseProgram(0)

    def mouseMoveEvent(self, event):
        if self.isActiveWindow() and self.underMouse():
            self.mouse.pos = event.pos()
            dx = self.mouse.dx()
            dy = self.mouse.dy()
            if event.buttons() & QtCore.Qt.LeftButton:
                self.camera.rotate(dx, dy)
                self.mouse.last_pos = event.pos()
                self.update()
            elif event.buttons() & QtCore.Qt.RightButton:
                self.camera.pan(dx, dy)
                self.mouse.last_pos = event.pos()
                self.update()

    def mousePressEvent(self, event):
        if self.isActiveWindow() and self.underMouse():
            self.mouse.last_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.isActiveWindow() and self.underMouse():
            self.update()

    def wheelEvent(self, event):
        if self.isActiveWindow() and self.underMouse():
            degrees = event.delta() / 8
            steps = degrees / 15
            self.camera.zoom(steps)
            self.update()


# ==============================================================================
# ==============================================================================
# ==============================================================================
# Objects
# ==============================================================================
# ==============================================================================
# ==============================================================================


class MeshObject:

    default_color_vertices = [0.1, 0.1, 0.1]
    default_color_edges = [0.2, 0.2, 0.2]
    default_color_front = [0.8, 0.8, 0.8]
    default_color_back = [1.0, 0.5, 0.7]

    def __init__(self, data, name=None, is_selected=False, show_vertices=True,
                 show_edges=True, show_faces=True):
        self._data = data
        self._mesh = data
        self._vertices = None
        self._edges = None
        self._front = None
        self._back = None
        self.name = name
        self.is_selected = is_selected
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces

    def init(self):
        mesh = self._mesh
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}
        # vertices
        positions = []
        colors = []
        elements = []
        i = 0
        for vertex in mesh.vertices():
            positions.append(vertex_xyz[vertex])
            colors.append(self.default_color_vertices)
            elements.append(i)
            i += 1
        self._vertices = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(elements),
            'n': i
        }
        # edges
        positions = []
        colors = []
        elements = []
        i = 0
        for u, v in mesh.edges():
            positions.append(vertex_xyz[u])
            positions.append(vertex_xyz[v])
            colors.append(self.default_color_edges)
            colors.append(self.default_color_edges)
            elements.append([i + 0, i + 1])
            i += 2
        self._edges = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(list(flatten(elements))),
            'n': i
        }
        # front faces
        positions = []
        colors = []
        elements = []
        color = self.default_color_front
        i = 0
        for face in mesh.faces():
            vertices = mesh.face_vertices(face)
            if len(vertices) == 3:
                a, b, c = vertices
                positions.append(vertex_xyz[a])
                positions.append(vertex_xyz[b])
                positions.append(vertex_xyz[c])
                colors.append(color)
                colors.append(color)
                colors.append(color)
                elements.append([i + 0, i + 1, i + 2])
                i += 3
            elif len(vertices) == 4:
                a, b, c, d = vertices
                positions.append(vertex_xyz[a])
                positions.append(vertex_xyz[b])
                positions.append(vertex_xyz[c])
                positions.append(vertex_xyz[a])
                positions.append(vertex_xyz[c])
                positions.append(vertex_xyz[d])
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                elements.append([i + 0, i + 1, i + 2])
                elements.append([i + 3, i + 4, i + 5])
                i += 6
            else:
                raise NotImplementedError
        self._front = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(list(flatten(elements))),
            'n': i
        }
        # back faces
        positions = []
        colors = []
        elements = []
        color = self.default_color_back
        i = 0
        for face in mesh.faces():
            vertices = mesh.face_vertices(face)[::-1]
            if len(vertices) == 3:
                a, b, c = vertices
                positions.append(vertex_xyz[a])
                positions.append(vertex_xyz[b])
                positions.append(vertex_xyz[c])
                colors.append(color)
                colors.append(color)
                colors.append(color)
                elements.append([i + 0, i + 1, i + 2])
                i += 3
            elif len(vertices) == 4:
                a, b, c, d = vertices
                positions.append(vertex_xyz[a])
                positions.append(vertex_xyz[b])
                positions.append(vertex_xyz[c])
                positions.append(vertex_xyz[a])
                positions.append(vertex_xyz[c])
                positions.append(vertex_xyz[d])
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                elements.append([i + 0, i + 1, i + 2])
                elements.append([i + 3, i + 4, i + 5])
                i += 6
            else:
                raise NotImplementedError
        self._back = {
            'positions': make_vertex_buffer(list(flatten(positions))),
            'colors': make_vertex_buffer(list(flatten(colors))),
            'elements': make_index_buffer(list(flatten(elements))),
            'n': i
        }

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges

    @property
    def front(self):
        return self._front

    @property
    def back(self):
        return self._back

    def draw(self, program):
        position = GL.glGetAttribLocation(program, 'position')
        color = GL.glGetAttribLocation(program, 'color')
        GL.glEnableVertexAttribArray(position)
        GL.glEnableVertexAttribArray(color)
        if self.show_faces:
            # front
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.front['positions'])
            GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, False, 0, None)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.front['colors'])
            GL.glVertexAttribPointer(color, 3, GL.GL_FLOAT, False, 0, None)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.front['elements'])
            GL.glDrawElements(GL.GL_TRIANGLES, self.front['n'], GL.GL_UNSIGNED_INT, None)
            # back
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.back['positions'])
            GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, False, 0, None)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.back['colors'])
            GL.glVertexAttribPointer(color, 3, GL.GL_FLOAT, False, 0, None)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.back['elements'])
            GL.glDrawElements(GL.GL_TRIANGLES, self.back['n'], GL.GL_UNSIGNED_INT, None)
        if self.show_edges:
            # edges
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.edges['positions'])
            GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, False, 0, None)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.edges['colors'])
            GL.glVertexAttribPointer(color, 3, GL.GL_FLOAT, False, 0, None)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.edges['elements'])
            GL.glDrawElements(GL.GL_LINES, self.edges['n'], GL.GL_UNSIGNED_INT, None)
        if self.show_vertices:
            # vertices
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertices['positions'])
            GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, False, 0, None)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertices['colors'])
            GL.glVertexAttribPointer(color, 3, GL.GL_FLOAT, False, 0, None)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.vertices['elements'])
            GL.glPointSize(10)
            GL.glDrawElements(GL.GL_POINTS, self.vertices['n'], GL.GL_UNSIGNED_INT, None)


class ShapeObject(MeshObject):

    default_color_vertices = [0.1, 0.1, 0.1]
    default_color_edges = [0.2, 0.2, 0.2]
    default_color_front = [0.8, 0.8, 0.8]
    default_color_back = [0.4, 0.4, 0.4]

    def __init__(self, data, name=None, is_selected=False,
                 show_vertices=True, show_edges=True, show_faces=True):
        self._data = data
        self._mesh = Mesh.from_shape(data)
        self._vertices = None
        self._edges = None
        self._front = None
        self._back = None
        self.name = name
        self.is_selected = is_selected
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.datastructures import Mesh
    from compas.geometry import Box
    from compas.geometry import Pointcloud

    DTYPE_OTYPE[Box] = ShapeObject
    DTYPE_OTYPE[Mesh] = MeshObject

    # visualisation

    viewer = Viewer()

    for point in Pointcloud.from_bounds(10, 5, 3, 500):
        box = Box((point, [1, 0, 0], [0, 1, 0]), 0.1, 0.1, 0.1)
        viewer.add(box, show_vertices=False)

    viewer.show()
