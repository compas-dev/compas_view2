from typing import Tuple, Union
from OpenGL import GL

from PySide2 import QtCore, QtGui, QtWidgets

from ..camera import Camera
from ..mouse import Mouse
from ..objects import GridObject
from ..objects import AxisObject


class View(QtWidgets.QOpenGLWidget):
    """Base OpenGL widget."""

    def __init__(self,
                 app,
                 color: Tuple[float, float, float] = (1, 1, 1, 1),
                 selection_color: Tuple[float, float, float] = (1.0, 1.0, 0.0),
                 mode: str = 'shaded'):
        super().__init__()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self._opacity = 1.0
        self.shader = None
        self.app = app
        self.color = color
        self.mode = mode
        self.selection_color = selection_color
        self.camera = Camera()
        self.mouse = Mouse()
        self.objects = {}
        self.grid = GridObject(1, 10, 10)
        self.axis = AxisObject(3)
        self.enable_paint_instances = False
        self.show_grid = True
        self.show_axis = True

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
        # GL.glEnable(GL.GL_POLYGON_SMOOTH) # Disabled to avoid gap between triangles
        self.init()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode
        if mode == 'ghosted':
            self._opacity = 0.7
        else:
            self._opacity = 1.0
        if self.shader:
            self.shader.bind()
            self.shader.uniform1f("opacity", self._opacity)
            self.shader.release()
            self.update()

    @property
    def opacity(self):
        return self._opacity

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

        if event.buttons() & QtCore.Qt.LeftButton:
            self.mouse.buttons['left'] = True
        elif event.buttons() & QtCore.Qt.RightButton:
            self.mouse.buttons['right'] = True

        self.mouse.last_pos = event.pos()
        self.update()

        # Enable painting instance map for pick for next rendered frame
        if self.app.selector.enabled and self.mouse.buttons['left']:
            self.enable_paint_instances = True

    def mouseReleaseEvent(self, event):
        if not self.isActiveWindow() or not self.underMouse():
            return

        self.mouse.buttons['left'] = False
        self.mouse.buttons['right'] = False
        self.update()

    def wheelEvent(self, event):
        if not self.isActiveWindow() or not self.underMouse():
            return
        degrees = event.delta() / 8
        steps = degrees / 15
        self.camera.zoom(steps)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == 16777220 or event.key() == 16777221: # Enter
            if self.app.selector.enabled:
                self.app.selector.finish_selection()