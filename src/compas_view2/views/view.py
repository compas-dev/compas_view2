from typing import Tuple
from OpenGL import GL

from PySide2 import QtCore, QtGui, QtWidgets

from ..camera import Camera
from ..mouse import Mouse


class View(QtWidgets.QOpenGLWidget):
    """Base OpenGL widget."""

    def __init__(self,
                 app,
                 color: Tuple[float, float, float] = (1, 1, 1, 1),
                 opacity: float = 1.0,
                 selection_color: Tuple[float, float, float] = (0.0, 0.0, 0.0)):
        super().__init__()
        self.app = app
        self.color = color
        self.opacity = opacity
        self.selection_color = selection_color
        self.camera = Camera()
        self.mouse = Mouse()
        self.objects = {}

    def clear(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

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
        self.init()

    def init(self):
        pass

    def resizeGL(self, w: int, h: int):
        GL.glViewport(0, 0, w, h)
        self.app.width = w
        self.app.height = h
        self.resize(w, h)

    def resize(self, w: int, h: int):
        pass

    def paintGL(self):
        self.clear()
        self.paint()

    def paint(self):
        pass

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
