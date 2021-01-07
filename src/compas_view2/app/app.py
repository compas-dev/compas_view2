import sys

from OpenGL import GL
from PySide2 import QtCore, QtGui, QtWidgets

from ..gl import gl_info
from ..views import View120
from ..views import View330
from ..objects import ViewObject


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

    def __init__(self, version: str = '120', width=800, height=500):
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

        self.view = View(self)

        self.main.setCentralWidget(self.view)
        self.main.setContentsMargins(0, 0, 0, 0)

        statusbar = self.main.statusBar()
        statusbar.setContentsMargins(0, 0, 0, 0)
        statusbar.showMessage('Ready')

        menubar = self.main.menuBar()
        menubar.setContentsMargins(0, 0, 0, 0)
        menubar.setNativeMenuBar(True)
        scenemenu = menubar.addMenu('Scene')
        scenemenu.addAction('Load Scene', lambda: statusbar.showMessage('Load scene...'))
        scenemenu.addAction('Save Scene', lambda: statusbar.showMessage('Save scene...'))
        scenemenu.addSeparator()
        scenemenu.addAction('Undo', lambda: statusbar.showMessage('Undo scene change...'))
        scenemenu.addAction('Redo', lambda: statusbar.showMessage('Redo scene change...'))
        scenemenu.addAction('Clear', lambda: statusbar.showMessage('Clear scene...'))
        scenemenu.addAction('Redraw', lambda: statusbar.showMessage('Redraw scene...'))
        openglmenu = menubar.addMenu('OpenGL')
        openglmenu.addAction('OpenGL Version', lambda: statusbar.showMessage("OpenGL {}".format(GL.glGetString(GL.GL_VERSION).decode('ascii'))))
        openglmenu.addAction('GLSL Version', lambda: statusbar.showMessage("GLSL {}".format(GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode('ascii'))))

        toolbar = self.main.addToolBar('Tools')
        toolbar.setMovable(False)
        toolbar.setObjectName('Tools')
        toolbar.setIconSize(QtCore.QSize(24, 24))
        toolbar.setContentsMargins(0, 0, 0, 0)

        self.resize(width, height)

    def resize(self, width, height):
        self.main.resize(width, height)
        desktop = self.app.desktop()
        rect = desktop.availableGeometry()
        x = 0.5 * (rect.width() - width)
        y = 0.5 * (rect.height() - height)
        self.main.setGeometry(x, y, width, height)

    def add(self, data, **kwargs):
        self.view.objects[data] = ViewObject.build(data, **kwargs)

    def show(self):
        self.main.show()
        self.main.raise_()
        self.app.exec_()
