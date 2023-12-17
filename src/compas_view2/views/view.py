import time

from OpenGL import GL
from qtpy import QtCore
from qtpy import QtWidgets

from compas_view2.objects import GridObject
from compas_view2.scene import Camera


class View(QtWidgets.QOpenGLWidget):
    """Base OpenGL view widget.

    Parameters
    ----------
    app: :class:`compas_view2.app.App`
        The parent application of the view.
    view_config: dict
        The view configuration.
    """

    VIEWPORTS = {"front": 1, "right": 2, "top": 3, "perspective": 4}

    def __init__(self, app, view_config):
        super().__init__()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self._opacity = 1.0
        self._current = self.VIEWPORTS[view_config["viewport"]]
        self.shader_model = None
        self.app = app
        self.color = view_config["background_color"]
        self.mode = view_config["viewmode"]
        self.selection_color = view_config["selection_color"]
        self.show_grid = view_config["show_grid"]
        self.camera = Camera(self, **view_config["camera"])
        self.grid = GridObject(1, 10, 10)
        self.objects = {}
        self.keys = {"shift": False, "control": False, "f": False}
        self._frames = 0
        self._now = time.time()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode
        if mode == "ghosted":
            self._opacity = 0.7
        else:
            self._opacity = 1.0
        if self.shader_model:
            self.shader_model.bind()
            self.shader_model.uniform1f("opacity", self._opacity)
            self.shader_model.release()
            self.update()

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, current):
        self._current = current
        if self.shader_model:
            self.shader_model.bind()
            self.shader_model.uniform4x4("projection", self.camera.projection(self.app.width, self.app.height))
            self.shader_model.release()
            self.update()

    @property
    def opacity(self):
        return self._opacity

    def clear(self):
        """Clear the view."""
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    def initializeGL(self):
        """Initialize the OpenGL canvas.

        This implements the virtual funtion of the OpenGL widget.
        See the PySide2 docs [1]_ for more info.
        It sets the clear color of the view,
        and enables culling, depth testing, blending, point smoothing, and line smoothing.

        To extend the behaviour of this function,
        you can implement :meth:`~compas_view2.views.View.init`.

        References
        ----------
        .. [1] https://doc.qt.io/qtforpython-5.12/PySide2/QtWidgets/QOpenGLWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QOpenGLWidget.initializeGL

        """
        GL.glClearColor(*self.color)
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
        GL.glEnable(GL.GL_FRAMEBUFFER_SRGB)
        self.init()

    def init(self):
        pass

    def resizeGL(self, w, h):
        """Resize the OpenGL canvas.

        This implements the virtual funtion of the OpenGL widget.
        See the PySide2 docs [1]_ for more info.

        To extend the behaviour of this function,
        you can implement :meth:`~compas_view2.views.View.resize`.

        Parameters
        ----------
        w: float
            The width of the canvas.
        h: float
            The height of the canvas.

        References
        ----------
        .. [1] https://doc.qt.io/qtforpython-5.12/PySide2/QtWidgets/QOpenGLWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QOpenGLWidget.resizeGL

        """
        GL.glViewport(0, 0, w, h)
        self.app.width = w
        self.app.height = h
        self.resize(w, h)

    def resize(self, w, h):
        pass

    def paintGL(self):
        """Paint the OpenGL canvas.

        This implements the virtual funtion of the OpenGL widget.
        See the PySide2 docs [1]_ for more info.

        To extend the behaviour of this function,
        you can implement :meth:`~compas_view2.views.View.paint`.

        Notes
        -----
        This method also paints the instance map used by the selector to identify selected objects.
        The instance map is immediately cleared again, after which the real scene objects are drawn.

        References
        ----------
        .. [1] https://doc.qt.io/qtforpython-5.12/PySide2/QtWidgets/QOpenGLWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QOpenGLWidget.paintGL

        """
        self.clear()
        self.paint()
        self._frames += 1
        if time.time() - self._now > 1:
            self._now = time.time()
            self.app.fps(self._frames)
            self._frames = 0

    def paint(self):
        pass

    def paint_instances(self):
        pass

    def paint_plane(self):
        pass

    def mouseMoveEvent(self, event):
        """Callback for the mouse move event.

        This method registers selections, if the left button is pressed,
        and modifies the view (pan/rotate), if the right button is pressed.

        Parameters
        ----------
        event : PySide2.QtGui.QMouseEvent
            The Qt event.
        """
        if not self.isActiveWindow() or not self.underMouse():
            return
        else:
            self.app.controller.mouse_move_action(event)

    def mousePressEvent(self, event):
        """Callback for the mouse press event.

        Parameters
        ----------
        event : PySide2.QtGui.QMouseEvent
            The Qt event.
        """
        if not self.isActiveWindow() or not self.underMouse():
            return
        else:
            self.app.controller.mouse_press_action(event)

    def mouseReleaseEvent(self, event):
        """Callback for the release press event.

        Parameters
        ----------
        event : PySide2.QtGui.QMouseEvent
            The Qt event.
        """
        if not self.isActiveWindow() or not self.underMouse():
            return
        else:
            self.app.controller.mouse_release_action(event)

        self.update()

    def wheelEvent(self, event):
        """Callback for the mouse wheel event.

        Parameters
        ----------
        event : PySide2.QtGui.QMouseEvent
            The Qt event.
        """
        if not self.isActiveWindow() or not self.underMouse():
            return
        else:
            self.app.controller.wheel_action(event)

    def keyPressEvent(self, event):
        """Callback for the key press event.

        Parameters
        ----------
        event : PySide2.QtGui.QMouseEvent
            The Qt event.
        """
        self.app.controller.key_press_action(event)

    def keyReleaseEvent(self, event):
        """Callback for the key release event.

        Parameters
        ----------
        event : PySide2.QtGui.QMouseEvent
            The Qt event.
        """
        self.app.controller.key_release_action(event)
