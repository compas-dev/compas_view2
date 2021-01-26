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
                 mode: str = 'shaded',
                 show_grid: bool = True):
        super().__init__()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self._opacity = 1.0
        self.shader = None
        self.app = app
        self.color = color
        self.mode = mode
        self.selection_color = selection_color
        self.show_grid = show_grid
        self.camera = Camera()
        self.mouse = Mouse()
        self.grid = GridObject(1, 10, 10)
        self.objects = {}
        self.keys = {"shift": False, "control": False}

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

        if self.app.selector.paint_instance:
            if self.app.selector.select_from == "pixel":
                self.app.selector.instance_map = self.paint_instances()
            if self.app.selector.select_from == "box":
                self.app.selector.instance_map = self.paint_instances(
                    self.app.selector.box_select_coords)
            self.app.selector.paint_instance = False
            self.clear()

        self.paint()

        if self.app.selector.select_from == "box":
            self.paint_box(self.app.selector.box_select_coords)

    def paint_instances(self):
        pass

    def paint(self):
        pass

    def paint_box(self, box_coords):
        x1, y1, x2, y2 = box_coords
        x1 = (x1/self.app.width - 0.5)*2
        x2 = (x2/self.app.width - 0.5)*2
        y1 = -(y1/self.app.height - 0.5)*2
        y2 = -(y2/self.app.height - 0.5)*2

        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        # GL.glLineStipple(1, 0xAAAA);  # [1]
        # GL.glEnable(GL.GL_LINE_STIPPLE)
        GL.glBegin(GL.GL_LINE_LOOP)
        GL.glColor3f(0, 0, 0)
        GL.glVertex2f(x1, y1)
        GL.glVertex2f(x2, y1)
        GL.glVertex2f(x2, y2)
        GL.glVertex2f(x1, y2)
        GL.glEnd()

    def mouseMoveEvent(self, event):
        if not self.isActiveWindow() or not self.underMouse():
            return
        self.mouse.pos = event.pos()
        dx = self.mouse.dx()
        dy = self.mouse.dy()
        if event.buttons() & QtCore.Qt.LeftButton:
            if self.keys["shift"] or self.keys["control"]:
                self.app.selector.perform_box_selection(
                    self.mouse.pos.x(), self.mouse.pos.y())
            else:
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

    def mouseReleaseEvent(self, event):
        if not self.isActiveWindow() or not self.underMouse():
            return
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouse.buttons['left'] = False
            if self.app.selector.enabled:
                self.app.selector.paint_instance = True

        elif event.button() == QtCore.Qt.MouseButton.RightButton:
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
        key = event.key()
        if self.app.selector.enabled:
            if key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
                self.app.selector.finish_selection()
            if key == QtCore.Qt.Key_Shift:
                self.app.selector.mode = "multi"
                self.keys["shift"] = True
            if key == QtCore.Qt.Key_Control:
                self.app.selector.mode = "deselect"
                self.keys["control"] = True

    def keyReleaseEvent(self, event):
        key = event.key()
        if self.app.selector.enabled:
            if key == QtCore.Qt.Key_Shift:
                self.app.selector.mode = self.app.selector.overwrite_mode or "single"
                self.keys["shift"] = False
            if key == QtCore.Qt.Key_Control:
                self.app.selector.mode = self.app.selector.overwrite_mode or "single"
                self.keys["control"] = False
