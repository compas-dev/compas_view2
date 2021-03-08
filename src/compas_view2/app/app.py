import sys
import os
import json

from functools import partial

from PySide2 import QtCore, QtGui, QtWidgets

from ..views import View120
from ..views import View330
from ..objects import Object

from .controller import Controller
from .selector import Selector
from .timer import Timer

HERE = os.path.dirname(__file__)
ICONS = os.path.join(HERE, '../icons')
CONFIG = os.path.join(HERE, 'config.json')

VERSIONS = {'120': (2, 1), '330': (3, 3)}


class App:
    """Viewer app.

    The app has a (main) window with a central OpenGL widget (i.e. the "view"),
    and a menubar, toolbar, and statusbar.
    The menubar provides access to all supported "actions".
    The toolbar is meant to be a "quicknav" to a selected set of actions.
    The app supports rotate/pan/zoom, and object selection via picking or box selections.

    Currently the app uses OpenGL 2.2 and GLSL 120 with a "compatibility" profile.
    Support for OpenGL 3.3 and GLSL 330 with a "core" profile is under development.

    Parameters
    ----------
    version: '120' | '330', optional
        The version of the GLSL used by the shaders.
        Default is ``'120'`` with a compatibility profile.
        The option ``'330'`` is not yet available.
    width: int, optional
        The width of the app window at startup.
        Default is ``800``.
    height: int, optional
        The height of the app window at startup.
        Default is ``500``.
    viewmode: 'shaded' | 'ghosted' | 'wireframe' | 'lighted', optional
        The display mode of the OpenGL view.
        Default is ``'shaded'``.
        In ``'ghosted'`` mode, all objects have a default opacity of ``0.7``.
    show_grid: bool, optional
        Show the XY plane.
        Default is ``True``.
    controller_class: :class:`compas_view2.app.Controller`, optional
        A custom controller corresponding to a custom config file.
        Default is ``None``, in which case the default controller is used,
        matching the default config file.
    config: dict | filepath, optional
        A configuration dict for the UI, or a path to a JSON file containing such a dict.
        Default is ``None``, in which case the default configuration is used.

    Attributes
    ----------
    window: :class:`PySide2.QtWidgets.QMainWindow`
        The main window of the application.
        This window contains the view and any other UI components
        such as the menu, toolbar, statusbar, ...
    view: :class:`compas_view2.View`
        Instance of OpenGL view.
        This view is the central widget of the main window.
    controller: :class:`compas_view2.app.Controller`
        The action controller of the app.

    Notes
    -----
    The app can currently only be used "as-is".
    This means that there is no formal mechanism for adding actions to the controller
    or to add functionality to the shader, other than by extending the core classes.
    In the future, such mechanism will be provided by allowing the user to overwrite
    the configuration file and add actions to the controller, without having
    to modify the package source code.

    Currently the app has no scene graph.
    All added COMPAS objects are wrapped in a viewer object and stored in a dictionary,
    mapping the object's ID (``id(object)``) to the instance.

    Examples
    --------
    >>> from compas_view2 import app
    >>> viewer = app.App()
    >>> viewer.show()

    """

    def __init__(self, version='120', width=800, height=500, viewmode='shaded', controller_class=None, show_grid=True, config=None):
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

        self.timer = None
        self.width = width
        self.height = height
        self.window = QtWidgets.QMainWindow()
        self.view = View(self, mode=viewmode, show_grid=show_grid)
        self.window.setCentralWidget(self.view)
        self.window.setContentsMargins(0, 0, 0, 0)

        controller_class = controller_class or Controller
        self.controller = controller_class(self)

        config = config or CONFIG
        if not isinstance(config, dict):
            with open(config) as f:
                config = json.load(f)

        self.config = config

        self._app = app
        self._app.references.add(self.window)
        self.selector = Selector(self)

        self._init_statusbar()
        self._init_menubar(config.get("menubar"))
        self._init_toolbar(config.get("toolbar"))

        self.resize(width, height)

    def resize(self, width, height):
        """Resize the main window programmatically.

        Parameters
        ----------
        width: int
        height: int
        """
        self.window.resize(width, height)
        desktop = self._app.desktop()
        rect = desktop.availableGeometry()
        x = 0.5 * (rect.width() - width)
        y = 0.5 * (rect.height() - height)
        self.window.setGeometry(x, y, width, height)

    def add(self, data, **kwargs):
        """Add a COMPAS object.

        Parameters
        ----------
        data: :class:`compas.geometry.Primitive` | :class:`compas.geometry.Shape` | :class:`compas.geometry.Datastructure`

        Returns
        -------
        :class:`compas_view2.objects.Object`
        """
        obj = Object.build(data, **kwargs)
        self.view.objects[obj] = obj
        self.selector.add(obj)
        if self.view.isValid():
            obj.init()
        return obj

    def show(self):
        """Show the viewer window."""
        self.window.show()
        self._app.exec_()

    run = show

    def about(self):
        """Display the about message as defined in the config file."""
        QtWidgets.QMessageBox.about(self.window, 'About', self.config['messages']['about'])

    def info(self, message):
        """Display info."""
        QtWidgets.QMessageBox.information(self.window, 'Info', message)

    def question(self, message):
        """Ask a question."""
        pass

    def warning(self, message):
        """Display a warning."""
        QtWidgets.QMessageBox.warning(self.window, 'Warning', message)

    def critical(self, message):
        """Display a critical warning."""
        QtWidgets.QMessageBox.critical(self.window, 'Critical', message)

    def status(self, message):
        """Display a message in the status bar."""
        self.statusText.setText(message)

    def fps(self, _fps):
        """Update fps info in the status bar."""
        self.statusFps.setText("fps: {}".format(_fps))

    # ==============================================================================
    # UI
    # ==============================================================================

    def _get_icon(self, icon):
        return QtGui.QIcon(os.path.join(ICONS, icon))

    def _init_statusbar(self):
        self.statusbar = self.window.statusBar()
        self.statusbar.setContentsMargins(0, 0, 0, 0)
        self.statusText = QtWidgets.QLabel("Ready")
        self.statusbar.addWidget(self.statusText, 1)
        self.statusFps = QtWidgets.QLabel("fps: ")
        self.statusbar.addWidget(self.statusFps)

    def _init_menubar(self, items):
        if not items:
            return
        self.menubar = self.window.menuBar()
        self.menubar.setNativeMenuBar(True)
        self.menubar.setContentsMargins(0, 0, 0, 0)
        self._add_menubar_items(items, self.menubar)

    def _init_toolbar(self, items):
        if not items:
            return
        self.toolbar = self.window.addToolBar('Tools')
        self.toolbar.setMovable(False)
        self.toolbar.setObjectName('Tools')
        self.toolbar.setIconSize(QtCore.QSize(16, 16))
        self._add_toolbar_items(items, self.toolbar)

    def _add_menubar_items(self, items, parent):
        if not items:
            return
        for item in items:
            if item['type'] == 'separator':
                parent.addSeparator()
            elif item['type'] == 'menu':
                menu = parent.addMenu(item['text'])
                if 'items' in item:
                    self._add_menubar_items(item['items'], menu)
            elif item['type'] == 'radio':
                radio = QtWidgets.QActionGroup(self.window, exclusive=True)
                for item in item['items']:
                    action = self._add_action(item, parent)
                    action.setCheckable(True)
                    action.setChecked(item['checked'])
                    radio.addAction(action)
            elif item['type'] == 'action':
                self._add_action(item, parent)
            else:
                raise NotImplementedError

    def _add_toolbar_items(self, items, parent):
        if not items:
            return
        for item in items:
            if item['type'] == 'separator':
                parent.addSeparator()
            elif item['type'] == 'action':
                self._add_action(item, parent)
            else:
                raise NotImplementedError

    def _add_action(self, item, parent):
        text = item['text']
        action = getattr(self.controller, item['action'])
        args = item.get('args', None) or []
        kwargs = item.get('kwargs', None) or {}
        if 'icon' in item:
            icon = self._get_icon(item['icon'])
            return parent.addAction(icon, text, partial(action, *args, **kwargs))
        return parent.addAction(text, partial(action, *args, **kwargs))

    def on(self, interval=None, timeout=None):
        self.frame_count = 0

        if (not interval and not timeout) or (interval and timeout):
            raise ValueError("Must specify either interval or timeout")

        def outer(func):
            def render():
                func(self.frame_count)
                self.view.update()
                self.frame_count += 1

            if interval:
                self.timer = Timer(interval=interval, callback=render)
            if timeout:
                self.timer = Timer(interval=timeout, callback=render, singleshot=True)
        return outer
