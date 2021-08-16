from typing import AnyStr, Callable, Optional, List, Dict, Any
from typing_extensions import Literal

import sys
import os
import json

from functools import partial

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtGui import QIcon

from compas.data import Data

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

    The app has a (main) window with a central OpenGL widget (i.e. the 'view'),
    and a menubar, toolbar, and statusbar.
    The menubar provides access to all supported 'actions'.
    The toolbar is meant to be a 'quicknav' to a selected set of actions.
    The app supports rotate/pan/zoom, and object selection via picking or box selections.

    Currently the app uses OpenGL 2.2 and GLSL 120 with a 'compatibility' profile.
    Support for OpenGL 3.3 and GLSL 330 with a 'core' profile is under development.

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
    The app can currently only be used 'as-is'.
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

    def __init__(self,
                 version: Literal['120', '330'] = '120',
                 width: int = 800,
                 height: int = 500,
                 viewmode: Literal['wireframe', 'shaded', 'ghosted', 'lighted'] = 'shaded',
                 controller_class: Optional[Controller] = None,
                 show_grid: bool = True,
                 config: Optional[dict] = None,
                 enable_sidebar: bool = False):

        if version not in VERSIONS:
            raise Exception('Only these versions are currently supported: {}'.format(VERSIONS))

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

        appIcon = QIcon(os.path.join(ICONS, "compas_icon_white.png"))
        app.setWindowIcon(appIcon)

        self.timer = None
        self.frame_count = 0
        self.record = False
        self.recorded_frames = []

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

        self.enable_sidebar = enable_sidebar
        self.init()
        self.resize(width, height)

    def init(self):
        self._init_statusbar()
        self._init_menubar(self.config.get('menubar'))
        self._init_toolbar(self.config.get('toolbar'))
        self._init_sidebar(self.config.get('sidebar'))

    def resize(self, width: int, height: int):
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

    def add(self, data: Data, **kwargs) -> Object:
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

    def add_reference(self, obj: Object, **kwargs) -> Object:
        """"""
        ref = obj.otype.from_other(obj, **kwargs)
        self.view.objects[ref] = ref
        self.selector.add(ref)
        if self.view.isValid():
            ref.init()
        return ref

    def remove(self, obj: Object):
        if obj in list(self.view.objects):
            del self.view.objects[obj]
        for key, value in list(self.selector.instances.items()):
            if obj == value:
                del self.selector.instances[key]

    def show(self, pause=None):
        """Show the viewer window."""
        self.window.show()
        self._app.exec_()

    run = show

    def about(self):
        """Display the about message as defined in the config file."""
        QtWidgets.QMessageBox.about(self.window, 'About', self.config['messages']['about'])

    def info(self, message: str):
        """Display info."""
        QtWidgets.QMessageBox.information(self.window, 'Info', message)

    def question(self, message: str):
        """Ask a question."""
        pass

    def warning(self, message: str):
        """Display a warning."""
        QtWidgets.QMessageBox.warning(self.window, 'Warning', message)

    def critical(self, message: str):
        """Display a critical warning."""
        QtWidgets.QMessageBox.critical(self.window, 'Critical', message)

    def status(self, message: str):
        """Display a message in the status bar."""
        self.statusText.setText(message)

    def fps(self, fps: int):
        """Update fps info in the status bar."""
        self.statusFps.setText('fps: {}'.format(fps))

    # ==============================================================================
    # UI
    # ==============================================================================

    def _get_icon(self, icon: str):
        return QtGui.QIcon(os.path.join(ICONS, icon))

    def _init_statusbar(self):
        self.statusbar = self.window.statusBar()
        self.statusbar.setContentsMargins(0, 0, 0, 0)
        self.statusText = QtWidgets.QLabel('Ready')
        self.statusbar.addWidget(self.statusText, 1)
        self.statusFps = QtWidgets.QLabel('fps: ')
        self.statusbar.addWidget(self.statusFps)

    def _init_menubar(self, items: List[Dict]):
        if not items:
            return
        self.menubar = self.window.menuBar()
        self.menubar.setNativeMenuBar(True)
        self.menubar.setContentsMargins(0, 0, 0, 0)
        self._add_menubar_items(items, self.menubar)

    def _init_toolbar(self, items: List[Dict]):
        if not items:
            return
        self.toolbar = self.window.addToolBar('Tools')
        self.toolbar.setMovable(False)
        self.toolbar.setObjectName('Tools')
        self.toolbar.setIconSize(QtCore.QSize(16, 16))
        self._add_toolbar_items(items, self.toolbar)

    def _init_sidebar(self, items: List[Dict]):
        if not self.enable_sidebar:
            return
        self.sidebar = QtWidgets.QToolBar(self.window)
        self.window.addToolBar(QtCore.Qt.LeftToolBarArea, self.sidebar)
        self.sidebar.setObjectName('Sidebar')
        self.sidebar.setMovable(False)
        self.sidebar.setIconSize(QtCore.QSize(16, 16))
        self.sidebar.setMinimumWidth(240)
        self._add_sidebar_items(items, self.sidebar)

    def _add_menubar_items(self, items: List[Dict], parent: QtWidgets.QWidget):
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
                    action = self._add_action(parent, text=item['text'], action=item['action'])
                    action.setCheckable(True)
                    action.setChecked(item['checked'])
                    radio.addAction(action)
            elif item['type'] == 'action':
                del item['type']
                self._add_action(parent, text=item['text'], action=item['action'])
            else:
                raise NotImplementedError

    def _add_toolbar_items(self, items: List[Dict], parent: QtWidgets.QWidget):
        if not items:
            return
        for item in items:
            if item['type'] == 'separator':
                parent.addSeparator()
            elif item['type'] == 'action':
                del item['type']
                self._add_action(parent, **item)
            else:
                raise NotImplementedError

    def _add_sidebar_items(self, items: List[Dict], parent: QtWidgets.QWidget):
        if not items:
            return
        for item in items:
            if item['type'] == 'separator':
                parent.addSeparator()
            elif item['type'] == 'radio':
                del item['type']
                self.add_radio(parent, **item)
            elif item['type'] == 'checkbox':
                del item['type']
                self.add_checkbox(parent, **item)
            elif item['type'] == 'slider':
                del item['type']
                self.add_slider(parent, **item)
            elif item['type'] == 'button':
                del item['type']
                self.add_button(parent, **item)
            else:
                raise NotImplementedError

    def _add_action(self,
                    parent: QtWidgets.QWidget,
                    *,
                    text: str,
                    action: Callable,
                    args: Optional[List[Any]] = None,
                    kwargs: Optional[Dict] = None,
                    icon: Optional[AnyStr] = None):
        action = action if callable(action) else getattr(self.controller, action)
        args = args or []
        kwargs = kwargs or {}
        if icon:
            icon = self._get_icon(icon)
            action = parent.addAction(icon, text, partial(action, *args, **kwargs))
        else:
            action = parent.addAction(text, partial(action, *args, **kwargs))
        return action

    def add_button(self,
                   parent: QtWidgets.QWidget,
                   *,
                   text: str,
                   action: Callable):
        box = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        button = QtWidgets.QPushButton(text)
        layout.addWidget(button)
        box.setLayout(layout)
        parent.addWidget(box)
        action = action if callable(action) else getattr(self.controller, action)
        button.clicked.connect(action)
        # button.clicked.connect(self.view.update)

    def add_radio(self,
                  parent: QtWidgets.QWidget,
                  *,
                  items: List[Dict]):
        box = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        radio = QtWidgets.QActionGroup(self.window, exclusive=True)
        layout.addWidget(radio)
        box.setLayout(layout)
        parent.addWidget(box)
        for item in items:
            action = self._add_action(parent, text=item['text'], action=item['action'])
            action.setCheckable(True)
            action.setChecked(item['checked'])
            radio.addAction(action)
        # radio.toggled.connect(self.view.update)

    def add_checkbox(self,
                     parent: QtWidgets.QWidget,
                     *,
                     text: str,
                     action: Callable,
                     checked: bool = False):
        box = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        checkbox = QtWidgets.QCheckBox(text)
        checkbox.setCheckState(QtCore.Qt.CheckState.Checked if checked else QtCore.Qt.CheckState.Unchecked)
        layout.addWidget(checkbox)
        box.setLayout(layout)
        parent.addWidget(box)
        action = action if callable(action) else getattr(self.controller, action)
        checkbox.toggled.connect(action)
        checkbox.toggled.connect(self.view.update)

    def add_input(self, parent: QtWidgets.QWidget):
        pass

    def add_colorpicker(self, parent: QtWidgets.QWidget):
        pass

    def add_slider(self,
                   parent: QtWidgets.QWidget,
                   *,
                   text: str,
                   action: Callable,
                   value: int = 0,
                   minval: int = 0,
                   maxval: int = 100,
                   step: int = 1,
                   interval: int = 1,
                   label: str = ''):
        box = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        value_label = QtWidgets.QLabel(str(value))
        slider = QtWidgets.QSlider()
        slider.setOrientation(QtCore.Qt.Horizontal)
        slider.setValue(value)
        slider.setMinimum(minval)
        slider.setMaximum(maxval)
        slider.setTickInterval(interval)
        slider.setSingleStep(step)
        layout.addWidget(QtWidgets.QLabel(text))
        layout.addWidget(slider)
        layout.addWidget(value_label)
        layout.addWidget(QtWidgets.QLabel(str(label)))
        box.setLayout(layout)
        parent.addWidget(box)
        slider.valueChanged.connect(lambda v: value_label.setText(str(v)))
        action = action if callable(action) else getattr(self.controller, action)
        slider.valueChanged.connect(action)
        slider.valueChanged.connect(self.view.update)

    # ==============================================================================
    # Decorators
    # ==============================================================================

    def button(self, text: str) -> Callable:
        def outer(func: Callable) -> Callable:
            def wrapped(*args, **kwargs):
                func(self.app, *args, **kwargs)
            self.add_button(self.sidebar, text=text, action=func)
            return wrapped
        return outer

    def checkbox(self, text: str, checked: bool = True) -> Callable:
        def outer(func: Callable) -> Callable:
            def wrapped(*args, **kwargs):
                func(self.app, *args, **kwargs)
            self.add_checkbox(self.sidebar, text=text, action=func, checked=checked)
            return wrapped
        return outer

    def slider(self,
               text: str,
               value: int = 0,
               minval: int = 0,
               maxval: int = 100,
               step: int = 1,
               label: str = '') -> Callable:
        def outer(func: Callable) -> Callable:
            def wrapped(*args, **kwargs):
                func(self.app, *args, **kwargs)
            self.add_slider(self.sidebar,
                            text=text,
                            value=value,
                            minval=minval,
                            maxval=maxval,
                            step=step,
                            label=label,
                            action=func)
            return wrapped
        return outer

    def on(self,
           interval: int = None,
           timeout: int = None,
           record: bool = False,
           frames: int = None,
           record_path: str = 'temp/out.gif',
           playback_interval: int = None) -> Callable:

        if (not interval and not timeout) or (interval and timeout):
            raise ValueError('Must specify either interval or timeout')

        def outer(func: Callable):
            def render():
                func(self.frame_count)
                self.view.update()
                self.frame_count += 1
                if frames is not None and self.frame_count >= frames:
                    self.timer.stop()
                    if self.record:
                        self.record = False
                        self.recorded_frames[0].save(
                            record_path, save_all=True, optimize=True,
                            duration=playback_interval or interval,
                            append_images=self.recorded_frames[1:],
                            loop=100)
                        print('Recorded to ', record_path)

            if interval:
                self.timer = Timer(interval=interval, callback=render)
            if timeout:
                self.timer = Timer(interval=timeout, callback=render, singleshot=True)

            self.frame_count = 0
            self.record = record

        return outer
