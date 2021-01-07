import sys
from math import cos, sin, radians

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtOpenGL

from OpenGL import GL

import ctypes as ct
import numpy as np

from compas.geometry import Transformation, Translation, Rotation

from compas.utilities import flatten
from compas.utilities import i_to_rgb

from utilities.matrices import *
from utilities.shaders import *
from utilities.mouse import *
from utilities.camera import *
from utilities.objects import *


VSHADER = """
#version 120

attribute vec3 position;
attribute vec3 color;

uniform mat4 projection;
uniform mat4 viewworld;

uniform bool is_selected;
uniform float opacity;
uniform vec3 selection_color;

varying vec4 vertex_color;

void main()
{
    if (is_selected) {
        vertex_color = vec4(selection_color, opacity);
    }
    else {
        vertex_color = vec4(color, opacity);
    }

    gl_Position = projection * viewworld * vec4(position, 1.0);
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
# App & Main Window
# ==============================================================================
# ==============================================================================
# ==============================================================================


class Window:
    DTYPE_OTYPE = {}

    def __init__(self, version=(2, 1), core=True):
        glFormat = QtGui.QSurfaceFormat()
        glFormat.setVersion(*version)
        if core:
            glFormat.setProfile(QtGui.QSurfaceFormat.CoreProfile)
        else:
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
        self.view.objects[data] = Window.DTYPE_OTYPE[type(data)](data, **kwargs)

    def show(self):
        self.main.show()
        self.main.raise_()
        self.app.exec_()


# ==============================================================================
# ==============================================================================
# ==============================================================================
# OpenGL View
# ==============================================================================
# ==============================================================================
# ==============================================================================


class View(QtWidgets.QOpenGLWidget):
    width = 800
    height = 500
    opacity = 1.0
    selection_color = [0.0, 0.0, 0.0]

    def __init__(self, parent=None, color=(1, 1, 1, 1)):
        super().__init__(parent=parent)
        self.color = color
        self.camera = PerspectiveCamera()
        self.mouse = Mouse()
        self.objects = {}

    def initializeGL(self):
        GL.glClearColor(* self.color)
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
        self.shader = Shader(VSHADER, FSHADER)
        self.shader.bind()
        self.shader.uniform4x4("projection", self.camera.projection(self.width, self.height))
        self.shader.uniform4x4("viewworld", self.camera.viewworld())
        self.shader.uniform1i("is_selected", 0)
        self.shader.uniform1f("opacity", self.opacity)
        self.shader.uniform3f("selection_color", self.selection_color)
        self.shader.release()

    def resizeGL(self, w: int, h: int):
        GL.glViewport(0, 0, w, h)
        self.width = w
        self.height = h
        self.shader.bind()
        self.shader.uniform4x4("projection", self.camera.projection(w, h))
        self.shader.release()

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        self.shader.bind()
        self.shader.uniform4x4("viewworld", self.camera.viewworld())
        for guid in self.objects:
            obj = self.objects[guid]
            obj.draw(self.shader)
        self.shader.release()

    def mouseMoveEvent(self, event):
        if not self.isActiveWindow() or not self.underMouse():
            return
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
        if not self.isActiveWindow() or not self.underMouse():
            return
        self.mouse.last_pos = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        if not self.isActiveWindow() or not self.underMouse():
            return
        self.update()

    def wheelEvent(self, event):
        if not self.isActiveWindow() or not self.underMouse():
            return
        degrees = event.delta() / 8
        steps = degrees / 15
        self.camera.zoom(steps)
        self.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import random

    from compas.datastructures import Mesh
    from compas.geometry import Box
    from compas.geometry import Pointcloud

    Window.DTYPE_OTYPE[Box] = ShapeObject
    Window.DTYPE_OTYPE[Mesh] = MeshObject

    viewer = Window()
    viewer.view.opacity = 0.7

    for point in Pointcloud.from_bounds(10, 5, 3, 1000):
        box = Box((point, [1, 0, 0], [0, 1, 0]), 0.1, 0.1, 0.1)
        color = i_to_rgb(random.random(), normalize=True)
        viewer.add(box, show_vertices=False, color=color, is_selected=random.choice([0, 1]))

    viewer.show()
