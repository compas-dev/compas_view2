import sys

from OpenGL import GL
from PySide2 import QtCore, QtGui, QtWidgets

from ..gl import gl_info
from ..views import View120
from ..views import View330
from ..objects import ViewObject
from ..forms.sphere import SphereForm
from ..forms.torus import TorusForm


VERSIONS = {'120': (2, 1), '330': (3, 3)}


class Window:
    """Viewer app and main window.

    Attributes
    ----------
    main : :class:`compas_view2.MainWindow`
        The main window of the application.
        This window contains the view and any other UI components
        such as the menu, toolbar, statusbar, ...
    view : :class:`compas_view2.View`
        Instance of OpenGL view.
        This view is the central widget of the main window.

    Methods
    -------
    add
    show

    Examples
    --------
    >>>

    """

    def __init__(self, version: str = '120', width=800, height=500, viewmode='shaded'):
        if version not in VERSIONS:
            raise Exception("Only these versions are currently supported: {}".format(VERSIONS))

        glFormat = QtGui.QSurfaceFormat()
        glFormat.setVersion(* VERSIONS[version])

        if version == '330':
            View = View330
            glFormat.setProfile(QtGui.QSurfaceFormat.CoreProfile)
        elif version == '120':
            View = View120
            glFormat.setProfile(QtGui.QSurfaceFormat.CompatibilityProfile)
        else:
            raise NotImplementedError

        glFormat.setDefaultFormat(glFormat)
        QtGui.QSurfaceFormat.setDefaultFormat(glFormat)

        app = QtCore.QCoreApplication.instance()
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
        app.references = set()

        self.width = width
        self.height = height

        self.app = app
        self.main = QtWidgets.QMainWindow()
        self.app.references.add(self.main)

        self.view = View(self, mode=viewmode)

        self.main.setCentralWidget(self.view)
        self.main.setContentsMargins(0, 0, 0, 0)

        statusbar = self.main.statusBar()
        statusbar.setContentsMargins(0, 0, 0, 0)
        statusbar.showMessage('Ready')

        menubar = self.main.menuBar()
        menubar.setContentsMargins(0, 0, 0, 0)
        menubar.setNativeMenuBar(True)

        viewmenu = menubar.addMenu('View')
        radio = QtWidgets.QActionGroup(self.main, exclusive=True)
        action = viewmenu.addAction('Shaded', self.to_shaded)
        action.setCheckable(True)
        action.setChecked(self.view.mode == 'shaded')
        radio.addAction(action)
        action = viewmenu.addAction('Ghosted', self.to_ghosted)
        action.setCheckable(True)
        action.setChecked(self.view.mode == 'ghosted')
        radio.addAction(action)

        scenemenu = menubar.addMenu('Scene')
        scenemenu.addAction('Load Scene', lambda: statusbar.showMessage('Load scene...'))
        scenemenu.addAction('Save Scene', lambda: statusbar.showMessage('Save scene...'))
        scenemenu.addSeparator()
        scenemenu.addAction('Undo', lambda: statusbar.showMessage('Undo scene change...'))
        scenemenu.addAction('Redo', lambda: statusbar.showMessage('Redo scene change...'))
        scenemenu.addAction('Clear', lambda: statusbar.showMessage('Clear scene...'))
        scenemenu.addAction('Redraw', lambda: statusbar.showMessage('Redraw scene...'))

        primenu = menubar.addMenu('Primitives')
        primenu.addAction('Point', lambda: statusbar.showMessage('Add point'))
        primenu.addAction('Vector', lambda: statusbar.showMessage('Add vector'))
        primenu.addAction('Line', lambda: statusbar.showMessage('Add line'))
        primenu.addAction('Circle', lambda: statusbar.showMessage('Add circle'))

        shapemenu = menubar.addMenu('Shapes')
        shapemenu.addAction('Box', self.add_box)
        shapemenu.addAction('Spere', self.add_sphere)
        shapemenu.addAction('Torus', self.add_torus)

        netmenu = menubar.addMenu('Networks')
        meshmenu = menubar.addMenu('Meshes')

        openglmenu = menubar.addMenu('OpenGL')
        openglmenu.addAction('OpenGL Version', self.opengl_version)
        openglmenu.addAction('GLSL Version', self.glsl_version)

        # toolbar = self.main.addToolBar('Tools')
        # toolbar.setMovable(False)
        # toolbar.setObjectName('Tools')
        # toolbar.setIconSize(QtCore.QSize(24, 24))
        # toolbar.setContentsMargins(0, 0, 0, 0)

        self.resize(width, height)

    def resize(self, width, height):
        self.main.resize(width, height)
        desktop = self.app.desktop()
        rect = desktop.availableGeometry()
        x = 0.5 * (rect.width() - width)
        y = 0.5 * (rect.height() - height)
        self.main.setGeometry(x, y, width, height)

    def add(self, data, **kwargs):
        obj = ViewObject.build(data, **kwargs)
        self.view.objects[obj] = obj
        if self.view.isValid():
            obj.init()

    def opengl_version(self):
        value = "OpenGL {}".format(GL.glGetString(GL.GL_VERSION).decode('ascii'))
        QtWidgets.QMessageBox.information(self.main, 'Info', value)

    def glsl_version(self):
        value = "GLSL {}".format(GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode('ascii'))
        QtWidgets.QMessageBox.information(self.main, 'Info', value)

    def to_shaded(self):
        self.view.mode = 'shaded'

    def to_ghosted(self):
        self.view.mode = 'ghosted'

    def add_box(self):
        from compas.geometry import Box
        r = QtWidgets.QInputDialog.getDouble(self.main, 'Add Box', 'size', 1)
        if r[1] and r[0] > 0:
            size = r[0]
            box = Box.from_width_height_depth(size, size, size)
            self.add(box)

    def add_sphere(self):
        from compas.geometry import Sphere
        form = SphereForm()
        if form.exec_():
            radius = form.radius
            u = form.u
            v = form.v
            sphere = Sphere([0, 0, 0], radius)
            self.add(sphere, u=u, v=v)

    def add_torus(self):
        from compas.geometry import Torus
        form = TorusForm()
        if form.exec_():
            radius = form.radius
            tube = form.tube
            u = form.u
            v = form.v
            torus = Torus(([0, 0, 0], [0, 0, 1]), radius, tube)
            self.add(torus, u=u, v=v)

    def show(self):
        self.main.show()
        self.app.exec_()
