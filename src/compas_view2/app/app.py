import sys
import os
import json

from functools import partial
from typing import Optional

import os
os.environ['QT_MAC_WANTS_LAYER'] = '1'

from PySide2 import QtCore, QtGui, QtWidgets

from ..views import View120
from ..views import View330
from ..objects import Object

from .controller import Controller


HERE = os.path.dirname(__file__)
ICONS = os.path.join(HERE, '../icons')
CONFIG = os.path.join(HERE, 'config.json')

VERSIONS = {'120': (2, 1), '330': (3, 3)}


class App:
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

    def __init__(self, version: str = '120', width: int = 800, height: int = 500, viewmode: str = 'shaded'):
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
        self.window = QtWidgets.QMainWindow()
        self.view = View(self, mode=viewmode)
        self.window.setCentralWidget(self.view)
        self.window.setContentsMargins(0, 0, 0, 0)
        self.controller = Controller(self)

        self._app = app
        self._app.references.add(self.window)

        self.init_statusbar()

        with open(CONFIG) as f:
            config = json.load(f)
            self.init_menubar(config.get("menubar"))
            self.init_toolbar(config.get("toolbar"))

        self.resize(width, height)

    def resize(self, width, height):
        self.window.resize(width, height)
        desktop = self._app.desktop()
        rect = desktop.availableGeometry()
        x = 0.5 * (rect.width() - width)
        y = 0.5 * (rect.height() - height)
        self.window.setGeometry(x, y, width, height)

    def add(self, data, **kwargs):
        obj = Object.build(data, **kwargs)
        self.view.objects[obj] = obj
        if self.view.isValid():
            obj.init()

    def show(self):
        self.window.show()
        self._app.exec_()

    # ==============================================================================
    # UI
    # ==============================================================================

    def init_statusbar(self):
        self.statusbar = self.window.statusBar()
        self.statusbar.setContentsMargins(0, 0, 0, 0)
        self.statusbar.showMessage('Ready')

    def init_menubar(self, items):
        if not items:
            return
        self.menubar = self.window.menuBar()
        self.menubar.setNativeMenuBar(False)
        self.menubar.setContentsMargins(0, 0, 0, 0)
        self.add_menubar_items(items, self.menubar)

    def init_toolbar(self, items):
        if not items:
            return
        toolbar = self.window.addToolBar('Tools')
        toolbar.setMovable(False)
        toolbar.setObjectName('Tools')
        toolbar.setIconSize(QtCore.QSize(24, 24))
        undotool = toolbar.addAction(QtGui.QIcon(os.path.join(ICONS, 'undo-solid.svg')), 'Undo', self.undo)
        redotool = toolbar.addAction(QtGui.QIcon(os.path.join(ICONS, 'redo-solid.svg')), 'Redo', self.redo)

    def add_menubar_items(self, items, parent):
        if not items:
            return
        for item in items:
            if item['type'] == 'separator':
                parent.addSeparator()
            elif item['type'] == 'menu':
                menu = parent.addMenu(item['text'])
                if 'items' in item:
                    self.add_menubar_items(item['items'], menu)
            elif item['type'] == 'radio':
                radio = QtWidgets.QActionGroup(self.window, exclusive=True)
                for item in item['items']:
                    action = self.add_action(item, parent)
                    action.setCheckable(True)
                    action.setChecked(item['checked'])
                    radio.addAction(action)
            elif item['type'] == 'action':
                self.add_action(item, parent)
            else:
                raise NotImplementedError

    def add_toolbar_items(self, items, parent):
        if not items:
            return
        for item in items:
            if item['type'] == 'separator':
                parent.addSeparator()
            elif item['type'] == 'action':
                self.add_action(item, parent)
            else:
                raise NotImplementedError

    def add_action(self, item, parent):
        text = item['text']
        action = getattr(self.controller, item['action'])
        args = item.get('args', None) or []
        kwargs = item.get('kwargs', None) or {}
        if 'icon' in item:
            icon = QtGui.QIcon(item['icon'])
            return parent.addAction(icon, text, partial(action, *args, **kwargs))
        return parent.addAction(text, partial(action, *args, **kwargs))
