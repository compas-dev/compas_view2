import sys
import math

from math import tan, cos, sin, radians

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtOpenGL

from OpenGL import GL

import ctypes as ct
import numpy as np

from compas.geometry import Transformation, Translation, Rotation, Frame
from compas.geometry import normalize_vector, subtract_vectors, scale_vector, cross_vectors, dot_vectors

from compas.utilities import i_to_rgb
from compas.utilities import flatten


DTYPE_OTYPE = {}


VSHADER = """
#version 330

layout(location = 0) in vec3 vertex;
layout(location = 1) in vec3 color;

uniform bool is_selected = false;
uniform float opacity = 1.0;

uniform mat4 P;
uniform mat4 V;
uniform mat4 M;
uniform mat4 O;

out vec4 vertex_color;

void main()
{
    gl_Position = P * V * M * O * vec4(vertex, 1.0);

    if (is_selected) {
        vertex_color = vec4(1.0, 1.0, 0.0, opacity);
    }
    else {
        vertex_color = vec4(color, opacity);
    }
}
"""

FSHADER = """
#version 330

in vec4 vertex_color;
out vec4 frag_color;

void main()
{
    frag_color = vertex_color;
}
"""


# ==============================================================================
# ==============================================================================
# ==============================================================================
# Helpers
# ==============================================================================
# ==============================================================================
# ==============================================================================


def make_shader_program(context, vsource, fsource):
    # vertex = compile_vertex_shader(vsource)
    # fragment = compile_fragment_shader(fsource)
    # program = GL.glCreateProgram()
    # GL.glAttachShader(program, vertex)
    # GL.glAttachShader(program, fragment)
    # GL.glLinkProgram(program)
    # result = GL.glGetProgramiv(program, GL.GL_LINK_STATUS)
    # if not result:
    #     raise RuntimeError(GL.glGetProgramInfoLog(program))
    # return program
    program = QtGui.QOpenGLShaderProgram(context)
    program.addShader(compile_vertex_shader(vsource))
    program.addShader(compile_fragment_shader(fsource))
    program.link()
    return program


def make_vertex_buffer(data):
    # n = len(data)
    # vbo = GL.glGenBuffers(1)
    # cdata = (ct.c_float * n)(* data)
    # fsize = ct.sizeof(ct.c_float)
    # GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    # GL.glBufferData(GL.GL_ARRAY_BUFFER, fsize * n, cdata, GL.GL_STATIC_DRAW)
    # return vbo
    n = len(data)
    fsize = ct.sizeof(ct.c_float)
    cdata = (ct.c_float * n)(* data)
    vbo = QtGui.QOpenGLBuffer(QtGui.QOpenGLBuffer.VertexBuffer)
    vbo.create()
    vbo.bind()
    vbo.allocate(cdata, n * fsize)
    vbo.setUsagePattern(QtGui.QOpenGLBuffer.DynamicDraw)
    return vbo


# def make_index_buffer(data):
#     n = len(data)
#     vbo = GL.glGenBuffers(1)
#     cdata = (ct.c_int * n)(* data)
#     isize = ct.sizeof(ct.c_int)
#     GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, vbo)
#     GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, isize * n, cdata, GL.GL_STATIC_DRAW)
#     return vbo


def compile_vertex_shader(source):
    # shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
    # GL.glShaderSource(shader, source)
    # GL.glCompileShader(shader)
    # result = GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS)
    # if not result:
    #     raise RuntimeError(GL.glGetShaderInfoLog(shader))
    # return shader
    shader = QtGui.QOpenGLShader(QtGui.QOpenGLShader.Vertex)
    is_compiled = shader.compileSourceCode(source)
    if not is_compiled:
        print(shader.log())
        raise ValueError("Vertex shader known as {} is not compiled".format(name))
    return shader


def compile_fragment_shader(source):
    # shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
    # GL.glShaderSource(shader, source)
    # GL.glCompileShader(shader)
    # result = GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS)
    # if not result:
    #     raise RuntimeError(GL.glGetShaderInfoLog(shader))
    # return shader
    shader = QtGui.QOpenGLShader(QtGui.QOpenGLShader.Fragment)
    is_compiled = shader.compileSourceCode(source)
    if not is_compiled:
        print(shader.log())
        raise ValueError("Fragment shader known as {} is not compiled".format(name))
    return shader


# def link_shader_program(vertex, fragment):
#     program = GL.glCreateProgram()
#     GL.glAttachShader(program, vertex)
#     GL.glAttachShader(program, fragment)
#     GL.glLinkProgram(program)
#     result = GL.glGetProgramiv(program, GL.GL_LINK_STATUS)
#     if not result:
#         raise RuntimeError(GL.glGetProgramInfoLog(program))
#     return program


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
        glFormat.setVersion(4, 1)
        glFormat.setProfile(QtGui.QSurfaceFormat.CoreProfile)
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
        self.main.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
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

    def __init__(self, view, fov=45, near=0.1, far=100, target=None, distance=10):
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
        self.pan_delta = 0.1

    def rotate(self):
        dx = self.view.mouse.dx()
        dy = self.view.mouse.dy()
        self.rx += self.rotation_delta * dy
        self.rz += self.rotation_delta * dx

    def pan(self):
        sinrz = sin(radians(self.rz))
        cosrz = cos(radians(self.rz))
        sinrx = sin(radians(self.rx))
        cosrx = cos(radians(self.rx))
        dx = self.view.mouse.dx() * cosrz - self.view.mouse.dy() * sinrz * cosrx
        dy = self.view.mouse.dy() * cosrz * cosrx + self.view.mouse.dx() * sinrz
        dz = self.view.mouse.dy() * sinrx * self.pan_delta
        dx *= self.distance / 10.
        dy *= self.distance / 10.
        dz *= self.distance / 10.
        self.tx += self.pan_delta * dx
        self.ty -= self.pan_delta * dy
        self.target[0] = -self.tx
        self.target[1] = -self.ty
        self.target[2] -= dz
        self.distance -= dz

    def zoom(self, steps=1):
        self.distance -= steps * self.zoom_delta * self.distance

    def P(self):
        P = perspective(self.fov, self.view.aspect(), self.near, self.far)
        return P.list
        # return (ct.c_float * 16)(* P.list)
        # return np.array(P, dtype=np.float32).ravel().tolist()
        # return QtGui.QMatrix4x4(* P.list)

    def V(self):
        V = Transformation()
        return V.list
        # return (ct.c_float * 16)(* V.list)
        # return np.array(V, dtype=np.float32).ravel().tolist()
        # return QtGui.QMatrix4x4(* V.list)

    def M(self):
        T2 = Translation.from_vector([self.tx, self.ty, -self.distance])
        T1 = Translation.from_vector(self.target)
        Rx = Rotation.from_axis_and_angle([1, 0, 0], radians(self.rx))
        Rz = Rotation.from_axis_and_angle([0, 0, 1], radians(self.rz))
        T0 = Translation.from_vector([-self.target[0], -self.target[1], -self.target[2]])
        M = T2 * T1 * Rx * Rz * T0
        return M.list
        # return (ct.c_float * 16)(* M.list)
        # return np.array(M, dtype=np.float32).ravel().tolist()
        # return QtGui.QMatrix4x4(* M.list)


class Mouse:

    def __init__(self, view):
        self.view = view
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
        self.context = QtGui.QOpenGLContext()
        self.keys = {'shift': False}
        self.camera = PerspectiveCamera(self)
        self.mouse = Mouse(self)
        self.objects = {}

    def gl_info(self):
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

    def aspect(self):
        return self.width / self.height

    def initializeGL(self):
        self.context.create()
        # print(self.gl_info())
        f = self.context.functions()
        f.initializeOpenGLFunctions()
        f.glClearColor(0.9, 0.9, 0.9, 1)
        f.glPolygonOffset(1.0, 1.0)
        f.glEnable(GL.GL_POLYGON_OFFSET_FILL)
        f.glEnable(GL.GL_CULL_FACE)
        f.glCullFace(GL.GL_BACK)
        f.glEnable(GL.GL_DEPTH_TEST)
        f.glDepthFunc(GL.GL_LESS)
        f.glEnable(GL.GL_BLEND)
        f.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        # initialize the objects
        for guid in self.objects:
            obj = self.objects[guid]
            obj.init(f)
        # associate programs with object types
        self.program = make_shader_program(self.context, VSHADER, FSHADER)
        self.program.bind()
        self.program.setUniformValueArray("P", self.camera.P(), 1, 4)
        self.program.setUniformValueArray("V", self.camera.V(), 1, 4)
        self.program.setUniformValueArray("O", Transformation().list, 1, 4)
        self.program.release()

    def resizeGL(self, width: int, height: int):
        f = self.context.functions()
        self.width = width
        self.height = height
        f.glViewport(0, 0, width, height)
        self.program.bind()
        self.program.setUniformValueArray("P", self.camera.P(), 1, 4)
        self.program.release()

    def paintGL(self):
        f = self.context.functions()
        f.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        self.program.bind()
        self.program.setUniformValue1f("opacity", self.opacity)
        self.program.setUniformValueArray("M", self.camera.M(), 1, 4)
        for guid in self.objects:
            obj = self.objects[guid]
            obj.draw(f)
        self.program.release()

    def mouseMoveEvent(self, event):
        if self.isActiveWindow() and self.underMouse():
            self.mouse.pos = event.pos()
            if event.buttons() & QtCore.Qt.LeftButton:
                self.camera.rotate()
                self.mouse.last_pos = event.pos()
                self.update()
            elif event.buttons() & QtCore.Qt.RightButton:
                self.camera.pan()
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
            self.program.bind()
            self.program.setUniformValueArray("V", self.camera.V(), 1, 4)
            self.program.release()
            self.update()


# ==============================================================================
# ==============================================================================
# ==============================================================================
# Objects
# ==============================================================================
# ==============================================================================
# ==============================================================================


class NetworkObject:

    default_color_nodes = [0.1, 0.1, 0.1]
    default_color_edges = [0.4, 0.4, 0.4]

    def __init__(self, data, name=None, is_selected=False, show_nodes=True, show_edges=True):
        self._vao = None
        self._data = None
        self._node_xyz = None
        self.data = data
        self.name = name
        self.is_selected = is_selected
        self.show_nodes = show_nodes
        self.show_edges = show_edges

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def node_xyz(self):
        return {node: self.data.node_attributes(node, 'xyz') for node in self.data.nodes()}

    @property
    def nodes(self):
        data = self.data
        node_xyz = self.node_xyz
        color = self.default_color_nodes
        vertices = []
        colors = []
        for node in data.nodes():
            xyz = node_xyz[node]
            vertices.append(xyz)
            colors.append(color)
        return {
            'vertices': make_vertex_buffer(list(flatten(vertices))),
            'colors': make_vertex_buffer(list(flatten(colors)))}

    @property
    def edges(self):
        data = self.data
        node_xyz = self.node_xyz
        color = self.default_color_edges
        edges = []
        colors = []
        for u, v in data.edges():
            edges.append(node_xyz[u])
            edges.append(node_xyz[v])
            colors.append(color)
            colors.append(color)
        return {
            'vertices': make_vertex_buffer(list(flatten(edges))),
            'colors': make_vertex_buffer(list(flatten(colors)))}

    def init(self, f):
        self._vao = {
            'edges': QtGui.QOpenGLVertexArrayObject(),
            'nodes': QtGui.QOpenGLVertexArrayObject()}
        # edges
        self._vao['edges'].create()
        self._vao['edges'].bind()
        f.glEnableVertexAttribArray(0)
        self.edges['vertices'].bind()
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 0, None)
        f.glEnableVertexAttribArray(1)
        self.edges['colors'].bind()
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 0, None)
        self._vao['edges'].release()
        # nodes
        self._vao['nodes'].create()
        self._vao['nodes'].bind()
        f.glEnableVertexAttribArray(0)
        self.nodes['vertices'].bind()
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 0, None)
        f.glEnableVertexAttribArray(1)
        self.nodes['colors'].bind()
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 0, None)
        self._vao['nodes'].release()

    def draw(self, f):
        if self.show_edges:
            self._vao['edges'].bind()
            f.glDrawArrays(GL.GL_LINES, 0, GL.GL_BUFFER_SIZE)
        if self.show_nodes:
            self._vao['nodes'].bind()
            f.glDrawArrays(GL.GL_POINTS, 0, GL.GL_BUFFER_SIZE)


class MeshObject:

    default_color_vertices = [0.1, 0.1, 0.1]
    default_color_edges = [0.2, 0.2, 0.2]
    default_color_front = [0.8, 0.8, 0.8]
    default_color_back = [1.0, 0.5, 0.7]

    def __init__(self, data, name=None, is_selected=False, show_vertices=True, show_edges=True, show_faces=True):
        self._vao = None
        self._data = None
        self._mesh = None
        self._vertex_xyz = None
        self.data = data
        self.name = name
        self.is_selected = is_selected
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self._mesh = data

    @property
    def mesh(self):
        return self._mesh

    @property
    def vertex_xyz(self):
        return {vertex: self.mesh.vertex_attributes(vertex, 'xyz') for vertex in self.mesh.vertices()}

    @property
    def vertices(self):
        mesh = self.mesh
        vertex_xyz = self.vertex_xyz
        color = self.default_color_vertices
        vertices = []
        colors = []
        for vertex in mesh.vertices():
            xyz = vertex_xyz[vertex]
            vertices.append(xyz)
            colors.append(color)
        return {
            'vertices': make_vertex_buffer(list(flatten(vertices))),
            'colors': make_vertex_buffer(list(flatten(colors)))}

    @property
    def edges(self):
        mesh = self.mesh
        vertex_xyz = self.vertex_xyz
        color = self.default_color_edges
        edges = []
        colors = []
        for u, v in mesh.edges():
            edges.append(vertex_xyz[u])
            edges.append(vertex_xyz[v])
            colors.append(color)
            colors.append(color)
        return {
            'vertices': make_vertex_buffer(list(flatten(edges))),
            'colors': make_vertex_buffer(list(flatten(colors)))}

    @property
    def front(self):
        mesh = self.mesh
        vertex_xyz = self.vertex_xyz
        faces = []
        colors = []
        color = self.default_color_front
        for face in mesh.faces():
            vertices = mesh.face_vertices(face)
            if len(vertices) == 3:
                a, b, c = vertices
                faces.append(vertex_xyz[a])
                faces.append(vertex_xyz[b])
                faces.append(vertex_xyz[c])
                colors.append(color)
                colors.append(color)
                colors.append(color)
            elif len(vertices) == 4:
                a, b, c, d = vertices
                faces.append(vertex_xyz[a])
                faces.append(vertex_xyz[b])
                faces.append(vertex_xyz[c])
                faces.append(vertex_xyz[a])
                faces.append(vertex_xyz[c])
                faces.append(vertex_xyz[d])
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
            else:
                raise NotImplementedError
        return {
            'vertices': make_vertex_buffer(list(flatten(faces))),
            'colors': make_vertex_buffer(list(flatten(colors)))}

    @property
    def back(self):
        mesh = self.mesh
        vertex_xyz = self.vertex_xyz
        faces = []
        colors = []
        color = self.default_color_back
        for face in mesh.faces():
            vertices = mesh.face_vertices(face)[::-1]
            if len(vertices) == 3:
                a, b, c = vertices
                faces.append(vertex_xyz[a])
                faces.append(vertex_xyz[b])
                faces.append(vertex_xyz[c])
                colors.append(color)
                colors.append(color)
                colors.append(color)
            elif len(vertices) == 4:
                a, b, c, d = vertices
                faces.append(vertex_xyz[a])
                faces.append(vertex_xyz[b])
                faces.append(vertex_xyz[c])
                faces.append(vertex_xyz[a])
                faces.append(vertex_xyz[c])
                faces.append(vertex_xyz[d])
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
                colors.append(color)
            else:
                raise NotImplementedError
        return {
            'vertices': make_vertex_buffer(list(flatten(faces))),
            'colors': make_vertex_buffer(list(flatten(colors)))}

    def init(self):
        self._vao = {
            'front': GL.glGenVertexArrays(1),
            'back': GL.glGenVertexArrays(1),
            'edges': GL.glGenVertexArrays(1),
            'vertices': GL.glGenVertexArrays(1)}
        # front
        GL.glBindVertexArray(self._vao['front'])
        GL.glEnableVertexAttribArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.front['vertices'])
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 0, None)
        GL.glEnableVertexAttribArray(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.front['colors'])
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, 0, None)
        # back
        GL.glBindVertexArray(self._vao['back'])
        GL.glEnableVertexAttribArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.back['vertices'])
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 0, None)
        GL.glEnableVertexAttribArray(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.back['colors'])
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, 0, None)
        # edges
        GL.glBindVertexArray(self._vao['edges'])
        GL.glEnableVertexAttribArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.edges['vertices'])
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 0, None)
        GL.glEnableVertexAttribArray(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.edges['colors'])
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, 0, None)
        # vertices
        GL.glPointSize(10)
        GL.glBindVertexArray(self._vao['vertices'])
        GL.glEnableVertexAttribArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertices['vertices'])
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 0, None)
        GL.glEnableVertexAttribArray(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertices['colors'])
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, 0, None)
        # release
        GL.glBindVertexArray(0)

    def draw(self, program):
        if self.show_faces:
            GL.glUniform1i(GL.glGetUniformLocation(program, "is_selected"), self.is_selected)
            GL.glBindVertexArray(self._vao['front'])
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, GL.GL_BUFFER_SIZE)
            GL.glBindVertexArray(self._vao['back'])
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, GL.GL_BUFFER_SIZE)
            GL.glUniform1i(GL.glGetUniformLocation(program, "is_selected"), 0)
        if self.show_edges:
            GL.glBindVertexArray(self._vao['edges'])
            GL.glDrawArrays(GL.GL_LINES, 0, GL.GL_BUFFER_SIZE)
        if self.show_vertices:
            GL.glBindVertexArray(self._vao['vertices'])
            GL.glDrawArrays(GL.GL_POINTS, 0, GL.GL_BUFFER_SIZE)


class ShapeObject(MeshObject):

    default_color_vertices = [0.1, 0.1, 0.1]
    default_color_edges = [0.2, 0.2, 0.2]
    default_color_front = [0.6, 0.6, 0.6]
    default_color_back = [0.4, 0.4, 0.4]

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self._mesh = Mesh.from_shape(data)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas
    import random

    from compas.datastructures import Mesh
    from compas.datastructures import Network
    from compas.geometry import Box
    from compas.geometry import Sphere
    from compas.geometry import Torus
    from compas.geometry import Pointcloud
    from compas.geometry import Rotation
    from compas.utilities import print_profile

    DTYPE_OTYPE[Box] = ShapeObject
    DTYPE_OTYPE[Sphere] = ShapeObject
    DTYPE_OTYPE[Torus] = ShapeObject
    DTYPE_OTYPE[Mesh] = MeshObject
    DTYPE_OTYPE[Network] = NetworkObject
    # DTYPE_OTYPE[VolMesh] = VolMeshObject
    # DTYPE_OTYPE[Assembly] = AssemblyObject

    box = Box.from_width_height_depth(1, 1, 1)

    R = Rotation.from_axis_and_angle([0, 0, 1], radians(90))
    pcl1 = Pointcloud.from_bounds(100, 50, 30, 100)
    pcl1.transform(R)

    R = Rotation.from_axis_and_angle([0, 0, 1], radians(180))
    pcl2 = Pointcloud.from_bounds(100, 50, 30, 100)
    pcl2.transform(R)

    mesh = Mesh.from_off(compas.get('tubemesh.off'))
    mesh.flip_cycles()

    network = Network.from_obj(compas.get('grid_irregular.obj'))

    # visualisation

    viewer = Viewer()
    viewer.view.opacity = 0.7
    viewer.view.camera.far = 1000

    viewer.add(network)
    # viewer.add(mesh, show_vertices=False)
    # viewer.add(box, show_vertices=False)

    # for point in pcl1:
    #     sphere = Sphere(point, random.random())
    #     viewer.add(sphere, show_vertices=False)

    # for point in pcl2:
    #     radius = random.random()
    #     scale = random.random()
    #     torus = Torus((point, [0, 0, 1]), radius, scale * radius)
    #     viewer.add(torus, show_vertices=False)

    viewer.show()
