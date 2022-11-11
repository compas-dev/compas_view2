from typing import AnyStr
from typing import Callable
from typing import Optional
from typing import Union
from typing import Tuple
from typing import List
from typing import Dict
from typing import Any
from typing_extensions import Literal

import sys
import os
import json
import tempfile
import shutil

from functools import partial

from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets
from qtpy.QtGui import QIcon

from compas.data import Data
from compas.colors import Color
from compas.utilities import gif_from_images

from compas_view2.views import View120
from compas_view2.views import View330
from compas_view2.objects import Object
from compas_view2.forms.dockform import DockForm
from compas_view2.forms.sceneform import SceneForm
from compas_view2.forms.propertyform import PropertyForm
from compas_view2.forms.treeform import TreeForm
from compas_view2.forms.tabsform import TabsForm

from compas_view2.ui import Button
from compas_view2.ui import Slider
from compas_view2.ui import Radio
from compas_view2.ui import Checkbox
from compas_view2.ui import Select

try:
    from compas_view2.flow import Flow
except ImportError:
    Flow = None

from .timer import Timer
from .selector import Selector
from .controller import Controller
from .worker import Worker
from .plot import MplCanvas

HERE = os.path.dirname(__file__)
ICONS = os.path.join(HERE, "../icons")
CONFIG = os.path.join(HERE, "config.json")

VERSIONS = {"120": (2, 1), "330": (3, 3)}


class App:
    """Viewer app.

    Parameters
    ----------
    title : str, optional
        The title of the viewer window.
    version: {'120', '330'}, optional
        The version of the GLSL used by the shaders.
        Default is ``'120'`` with a compatibility profile.
        The option ``'330'`` is not yet available.
    width: int, optional
        The width of the app window at startup.
    height: int, optional
        The height of the app window at startup.
    viewmode: {'shaded', 'ghosted', 'wireframe', 'lighted'}, optional
        The display mode of the OpenGL view.
        In `ghosted` mode, all objects have a default opacity of 0.7.
    show_grid: bool, optional
        Show the XY plane.
    controller_class: :class:`compas_view2.app.Controller`, optional
        A custom controller corresponding to a custom config file.
        Default is None, in which case the default controller is used, matching the default config file.
    config: dict | filepath, optional
        A configuration dict for the UI, or a path to a JSON file containing such a dict.
        Default is None, in which case the default configuration is used.

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
    The app has a (main) window with a central OpenGL widget (i.e. the 'view'),
    and a menubar, toolbar, and statusbar.
    The menubar provides access to all supported 'actions'.
    The toolbar is meant to be a 'quicknav' to a selected set of actions.
    The app supports rotate/pan/zoom, and object selection via picking or box selections.

    Currently the app uses OpenGL 2.2 and GLSL 120 with a 'compatibility' profile.
    Support for OpenGL 3.3 and GLSL 330 with a 'core' profile is under development.

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

    def __init__(
        self,
        title: str = "COMPAS View2",
        version: Literal["120", "330"] = "120",
        width: int = 800,
        height: int = 500,
        viewmode: Literal["wireframe", "shaded", "ghosted", "lighted"] = "shaded",
        controller_class: Optional[Controller] = None,
        show_grid: bool = True,
        config: Optional[dict] = None,
        enable_sidebar: bool = False,
        enable_sidedock1: bool = False,
        enable_sidedock2: bool = False,
        enable_sceneform: bool = False,
        enable_propertyform: bool = False,
        show_flow: bool = False,
        flow_view_size: Union[Tuple[int], List[int]] = None,
        flow_auto_update: bool = True,
    ):

        if version not in VERSIONS:
            raise Exception("Only these versions are currently supported: {}".format(VERSIONS))

        glFormat = QtGui.QSurfaceFormat()
        glFormat.setVersion(*VERSIONS[version])

        if version == "330":
            View = View330
            glFormat.setProfile(QtGui.QSurfaceFormat.CoreProfile)
        elif version == "120":
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
        app.setApplicationName(title)

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

        self.show_flow = show_flow
        if Flow:
            self.flow = Flow(
                self,
                flow_view_size=flow_view_size or (self.width, self.height),
                flow_auto_update=flow_auto_update,
            )

        self.enable_sidebar = enable_sidebar
        self.enable_sidedock1 = enable_sidedock1
        self.enable_sidedock2 = enable_sidedock2
        self.enable_sceneform = enable_sceneform
        self.enable_propertyform = enable_propertyform
        self.dock_slots = {
            "sceneform": None,
            "propertyform": None,
        }

        self.init()
        self.resize(width, height)
        self.started = False
        self.on_object_selected = []

    def init(self):
        """Initialize the components of the user interface.

        Returns
        -------
        None

        """
        self._init_statusbar()
        self._init_menubar(self.config.get("menubar"))
        self._init_toolbar(self.config.get("toolbar"))
        self._init_sidebar(self.config.get("sidebar"))
        self._init_sidedocks()

    def resize(self, width: int, height: int):
        """Resize the main window programmatically.

        Parameters
        ----------
        width: int
            Width of the viewer window.
        height: int
            Height of the viewer window.

        Returns
        -------
        None

        """
        self.window.resize(width, height)
        desktop = self._app.desktop()
        rect = desktop.availableGeometry()
        x = 0.5 * (rect.width() - width)
        y = 0.5 * (rect.height() - height)
        self.window.setGeometry(x, y, width, height)

    def add(
        self,
        data: Data,
        name: str = None,
        is_selected: bool = None,
        is_visible: bool = None,
        show_points: bool = None,
        show_lines: bool = None,
        show_faces: bool = None,
        pointcolor: Union[Color, Dict[Union[str, int], Color]] = None,
        linecolor: Union[Color, Dict[Union[str, int], Color]] = None,
        facecolor: Union[Color, Dict[Union[str, int], Color]] = None,
        linewidth: int = None,
        pointsize: int = None,
        opacity: int = None,
        **kwargs,
    ) -> Object:
        """Add a COMPAS object.

        Parameters
        ----------
        data: :class:`compas.data.Data`
            A COMPAS data object.
        is_selected : bool, optional
            Whether the object is selected.
            Default to False.
        is_visible : bool, optional
            Whether to show object.
            Default to True.
        show_points : bool, optional
            Whether to show points/vertices of the object.
            Default to False.
        show_lines : bool, optional
            Whether to show lines/edges of the object.
            Default to True.
        show_faces : bool, optional
            Whether to show faces of the object.
            Default to True.
        pointcolor : Union[Color, Dict[Union[str, int], Color]], optional
            The color or the dict of colors of the points.
            Default to `compas_view2.objects.Object.default_color_points`.
        linecolor : Union[Color, Dict[Union[str, int], Color]], optional
            The color or the dict of colors of the lines.
            Default to `compas_view2.objects.Object.default_color_lines`.
        facecolor : Union[Color, Dict[Union[str, int], Color]], optional
            The color or the dict of colors of the faces.
            Default to `compas_view2.objects.Object.default_color_faces`.
        linewidth : int, optional
            The line width to be drawn on screen
            Default to 1.
        pointsize : int, optional
            The point size to be drawn on screen
            Default to 10.
        opacity : float, optional
            The opacity of the object.
            Default to 1.0.
        **kwargs : dict, optional
            Additional visualization options for specific objects.

        Returns
        -------
        :class:`compas_view2.objects.Object`
            The added object.

        """
        if name is not None:
            kwargs["name"] = name
        if is_selected is not None:
            kwargs["is_selected"] = is_selected
        if is_visible is not None:
            kwargs["is_visible"] = is_visible
        if show_points is not None:
            kwargs["show_points"] = show_points
        if show_lines is not None:
            kwargs["show_lines"] = show_lines
        if show_faces is not None:
            kwargs["show_faces"] = show_faces
        if pointcolor is not None:
            kwargs["pointcolor"] = pointcolor
        if linecolor is not None:
            kwargs["linecolor"] = linecolor
        if facecolor is not None:
            kwargs["facecolor"] = facecolor
        if linewidth is not None:
            kwargs["linewidth"] = linewidth
        if pointsize is not None:
            kwargs["pointsize"] = pointsize
        if opacity is not None:
            kwargs["opacity"] = opacity

        obj = Object.build(data, app=self, **kwargs)

        self.view.objects[obj] = obj
        self.selector.add(obj)
        if self.view.isValid():
            obj.init()
            if self.dock_slots["sceneform"]:
                self.dock_slots["sceneform"].update()
        return obj

    def add_reference(self, obj: Object, **kwargs) -> Object:
        """Add an object as a reference to another object.

        Parameters
        ----------
        obj : :class:`compas_view2.objects.Object`
            A view object.
        **kwargs : dict, optional
            Additional visualization options.

        Returns
        -------
        :class:`compas_view2.objects.Object`

        """
        ref = obj.otype.from_other(obj, **kwargs)
        self.view.objects[ref] = ref
        self.selector.add(ref)
        if self.view.isValid():
            ref.init()
        return ref

    def remove(self, obj: Object) -> None:
        """Remove an object from the view.

        Parameters
        ----------
        obj : :class:`compas_view2.objects.Object`
            A view object.

        Returns
        -------
        None

        """
        if obj in list(self.view.objects):
            del self.view.objects[obj]
        for key, value in list(self.selector.instances.items()):
            if obj == value:
                del self.selector.instances[key]

    def show(self) -> None:
        """Show the viewer window.

        Returns
        -------
        None

        """
        self.started = True
        self.window.show()
        if Flow and self.show_flow:
            self.flow.show()

        if self.dock_slots["sceneform"]:
            self.dock_slots["sceneform"].update()

        self._app.exec_()

    run = show

    def about(self) -> None:
        """Display the about message as defined in the config file.

        Returns
        -------
        None

        """
        QtWidgets.QMessageBox.about(self.window, "About", self.config["messages"]["about"])

    def info(self, message: str) -> None:
        """Display info.

        Parameters
        ----------
        message : str
            An info message.

        Returns
        -------
        None

        """
        result = QtWidgets.QMessageBox.information(self.window, "Info", message)
        print(result)

    def warning(self, message: str) -> None:
        """Display a warning.

        Parameters
        ----------
        message : str
            A warning message.

        Returns
        -------
        None

        """
        result = QtWidgets.QMessageBox.warning(self.window, "Warning", message)
        print(result)

    def critical(self, message: str) -> None:
        """Display a critical warning.

        Parameters
        ----------
        message : str
            A critical warning message.

        Returns
        -------
        None

        """
        result = QtWidgets.QMessageBox.critical(self.window, "Critical", message)
        print(result)

    def question(self, message: str) -> None:
        """Ask a question.

        Parameters
        ----------
        message : str
            A question.

        Returns
        -------
        None

        """
        flags = QtWidgets.QMessageBox.StandardButton.Yes
        flags |= QtWidgets.QMessageBox.StandardButton.No
        response = QtWidgets.QMessageBox.question(self.window, "Question", message, flags)
        if response == QtWidgets.QMessageBox.Yes:
            return True
        return False

    def confirm(self, message: str):
        """Confirm the execution of an action.

        Parameters
        ----------
        message : str
            Message to inform the user.

        Returns
        -------
        bool
            True if the user confirms.
            False otherwise.

        Examples
        --------
        .. code-block:: python

            if viewer.confirm("Should i continue?"):
                continue

        """
        flags = QtWidgets.QMessageBox.StandardButton.Ok
        flags |= QtWidgets.QMessageBox.StandardButton.Cancel
        response = QtWidgets.QMessageBox.warning(self.window, "Confirmation", message, flags)
        if response == QtWidgets.QMessageBox.StandardButton.Ok:
            return True
        return False

    def status(self, message: str) -> None:
        """Display a message in the status bar.

        Parameters
        ----------
        message : str
            A status message.

        Returns
        -------
        None

        """
        self.statusText.setText(message)

    def fps(self, fps: int) -> None:
        """Update fps info in the status bar.

        Parameters
        ----------
        fps : int
            The number of frames per second.

        Returns
        -------
        None

        """
        self.statusFps.setText("fps: {}".format(fps))

    def sidedock(self, title: str = "", slot: str = None, location: str = "right"):
        """Create a side dock widget."""
        if slot and slot in self.dock_slots:
            self.dock_slots[slot].close()

        locations = {
            "left": QtCore.Qt.LeftDockWidgetArea,
            "right": QtCore.Qt.RightDockWidgetArea,
            "top": QtCore.Qt.TopDockWidgetArea,
            "bottom": QtCore.Qt.BottomDockWidgetArea,
        }

        dock = DockForm(self, title)
        self.window.addDockWidget(locations[location], dock)

        if slot:
            self.dock_slots[slot] = dock

        return dock

    def sceneform(self):
        """Create a side object tree form widget."""
        if self.dock_slots["sceneform"]:
            self.dock_slots["sceneform"].show()
            return self.dock_slots["sceneform"]

        sceneform = SceneForm(self)
        self.window.addDockWidget(QtCore.Qt.RightDockWidgetArea, sceneform)
        self.dock_slots["sceneform"] = sceneform

        return sceneform

    def propertyform(self):
        """Create a side object tree form widget."""
        if self.dock_slots["propertyform"]:
            self.dock_slots["propertyform"].show()
            return self.dock_slots["propertyform"]

        propertyform = PropertyForm("Properties", on_update=self.view.update)
        self.window.addDockWidget(QtCore.Qt.RightDockWidgetArea, propertyform)
        self.dock_slots["propertyform"] = propertyform

        return propertyform

    def treeform(
        self,
        title="tree",
        data=None,
        slot: str = None,
        location: str = "left",
        floating=False,
        columns=["key", "value"],
        show_headers=True,
        striped_rows=False,
    ):
        """Create a side object tree form widget."""
        if slot and slot in self.dock_slots:
            treeform = self.dock_slots[slot]
            treeform.setWindowTitle(title)
            treeform.update(data)
            return treeform

        locations = {
            "left": QtCore.Qt.LeftDockWidgetArea,
            "right": QtCore.Qt.RightDockWidgetArea,
            "top": QtCore.Qt.TopDockWidgetArea,
            "bottom": QtCore.Qt.BottomDockWidgetArea,
        }

        treeform = TreeForm(
            self,
            title=title,
            data=data,
            columns=columns,
            show_headers=show_headers,
            striped_rows=striped_rows,
        )
        self.window.addDockWidget(locations[location], treeform)

        if slot:
            self.dock_slots[slot] = treeform
        if floating:
            treeform.setFloating(True)

        return treeform

    def tabsform(
        self,
        title="tree",
        tabs=[],
        slot: str = None,
        location: str = "left",
        floating=False,
        columns=["key", "value"],
        show_headers=True,
        striped_rows=False,
    ):
        """Create a tabs form widget."""
        if slot and slot in self.dock_slots:
            tabsform = self.dock_slots[slot]
            tabsform.setWindowTitle(title)
            tabsform.update(tabs)
            return tabsform

        locations = {
            "left": QtCore.Qt.LeftDockWidgetArea,
            "right": QtCore.Qt.RightDockWidgetArea,
            "top": QtCore.Qt.TopDockWidgetArea,
            "bottom": QtCore.Qt.BottomDockWidgetArea,
        }

        tabsform = TabsForm(
            self,
            title=title,
            tabs=tabs,
            columns=columns,
            show_headers=show_headers,
            striped_rows=striped_rows,
        )
        self.window.addDockWidget(locations[location], tabsform)

        if slot:
            self.dock_slots[slot] = tabsform
        if floating:
            tabsform.setFloating(True)

        return tabsform

    def popup(self, title: str = "", slot: str = None):
        """Create a side dock widget."""
        popup = self.sidedock(title, slot)
        popup.setFloating(True)
        return popup

    def plot(
        self,
        title: str = "",
        location: str = "bottom",
        floating: bool = False,
        min_height: int = 200,
        min_width: int = 200,
    ):
        """Create a matplotlib canvas as dock widget."""
        dock = self.sidedock(title, location=location)
        dock.setFloating(floating)
        dock.setMinimumHeight(min_height)
        dock.setMinimumWidth(min_width)
        sc = MplCanvas()
        dock.content_layout.addWidget(sc)
        return sc.figure

    def threading(
        self,
        func: Callable,
        args: list = [],
        kwargs: dict = {},
        on_progress: Callable = None,
        on_result: Callable = None,
        include_self: bool = False,
    ) -> None:
        """Execute a multi-threaded function.

        Parameters
        ----------
        func : function
            The function to be executed.
        args : list, optional
            The arguments to be passed to the function.
        kwargs : dict, optional
            The keyword arguments to be passed to the function.
        on_progress : function, optional
            A function to be called on progress event.
        on_result : function, optional
            A function to be called on result event.
        include_self : bool, optional
            Include the thread worker instance in the arguments, for sending out progress singals.

        Returns
        -------
        None

        """
        worker = Worker(func, args=args, kwargs=kwargs, include_self=include_self)
        if on_progress:
            worker.signals.progress.connect(on_progress)
        if on_result:
            worker.signals.result.connect(on_result)
        Worker.pool.start(worker)

    # ==============================================================================
    # UI
    # ==============================================================================

    def _get_icon(self, icon: str):
        return QtGui.QIcon(os.path.join(ICONS, icon))

    def _init_statusbar(self):
        self.statusbar = self.window.statusBar()
        self.statusbar.setContentsMargins(0, 0, 0, 0)
        self.statusText = QtWidgets.QLabel("Ready")
        self.statusbar.addWidget(self.statusText, 1)
        self.statusFps = QtWidgets.QLabel("fps: ")
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
        self.toolbar = self.window.addToolBar("Tools")
        self.toolbar.setMovable(False)
        self.toolbar.setObjectName("Tools")
        self.toolbar.setIconSize(QtCore.QSize(16, 16))
        self._add_toolbar_items(items, self.toolbar)

    def _init_sidebar(self, items: List[Dict]):
        if not self.enable_sidebar:
            return
        self.sidebar = QtWidgets.QToolBar(self.window)
        self.window.addToolBar(QtCore.Qt.LeftToolBarArea, self.sidebar)
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setMovable(False)
        self.sidebar.setIconSize(QtCore.QSize(16, 16))
        self.sidebar.setMinimumWidth(240)
        self._add_sidebar_items(items, self.sidebar)

    def _init_sidedocks(self):
        if self.enable_sidedock1:
            self.sidedock1 = self.sidedock(slot="sidedock1")
            self.sidedock1.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        if self.enable_sidedock2:
            self.sidedock2 = self.sidedock(slot="sidedock2")
            self.sidedock2.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        if self.enable_sceneform:
            self.sceneform()
        if self.enable_propertyform:
            self.propertyform()

    def _add_menubar_items(self, items: List[Dict], parent: QtWidgets.QWidget):
        if not items:
            return
        for item in items:
            if item["type"] == "separator":
                parent.addSeparator()
            elif item["type"] == "menu":
                menu = parent.addMenu(item["text"])
                if "items" in item:
                    self._add_menubar_items(item["items"], menu)
            elif item["type"] == "radio":
                radio = QtWidgets.QActionGroup(self.window, exclusive=True)
                for item in item["items"]:
                    action = self._add_action(parent, text=item["text"], action=item["action"])
                    action.setCheckable(True)
                    action.setChecked(item["checked"])
                    radio.addAction(action)
            elif item["type"] == "action":
                del item["type"]
                self._add_action(parent, text=item["text"], action=item["action"])
            else:
                raise NotImplementedError

    def _add_toolbar_items(self, items: List[Dict], parent: QtWidgets.QWidget):
        if not items:
            return
        for item in items:
            if item["type"] == "separator":
                parent.addSeparator()
            elif item["type"] == "action":
                del item["type"]
                self._add_action(parent, **item)
            else:
                raise NotImplementedError

    def _add_sidebar_items(self, items: List[Dict], parent: QtWidgets.QWidget):
        if not items:
            return
        for item in items:
            if item["type"] == "separator":
                parent.addSeparator()
            elif item["type"] == "radio":
                del item["type"]
                Radio(self, self.sidebar, **item)
            elif item["type"] == "checkbox":
                del item["type"]
                Checkbox(self, self.sidebar, **item)
            elif item["type"] == "slider":
                del item["type"]
                Slider(self, self.sidebar, **item)
            elif item["type"] == "button":
                del item["type"]
                Button(self, self.sidebar, **item)
            else:
                raise NotImplementedError

    def _add_action(
        self,
        parent: QtWidgets.QWidget,
        *,
        text: str,
        action: Callable,
        args: Optional[List[Any]] = None,
        kwargs: Optional[Dict] = None,
        icon: Optional[AnyStr] = None,
    ):
        action = action if callable(action) else getattr(self.controller, action)
        args = args or []
        kwargs = kwargs or {}
        if icon:
            icon = self._get_icon(icon)
            action = parent.addAction(icon, text, partial(action, *args, **kwargs))
        else:
            action = parent.addAction(text, partial(action, *args, **kwargs))
        return action

    # ==============================================================================
    # Decorators
    # ==============================================================================

    def select(self, items: List[Dict[str, Any]], parent=None) -> Callable:
        """Decorator for combo boxes.

        Parameters
        ----------
        items

        Returns
        -------
        callable

        """

        def outer(func: Callable) -> Callable:
            select = Select(self, parent or self.sidebar, items=items, action=func)
            return select

        return outer

    def radio(self, items: List[Dict[str, Any]], title="", parent=None) -> Callable:
        """Decorator for radio actions.

        Parameters
        ----------
        items

        Returns
        -------
        callable

        """

        def outer(func: Callable) -> Callable:
            radio = Radio(self, parent or self.sidebar, title=title, items=items, action=func)
            return radio

        return outer

    def button(self, text: str, parent=None) -> Callable:
        """Decorator for button actions.

        Parameters
        ----------
        text : str
            The button text label.

        Returns
        -------
        callable

        Notes
        -----
        Use this method to convert a function into the callback action of a button,
        and automatically add the button to the sidebar.

        Examples
        --------
        .. code-block:: python

            @viewer.button('Click me!')
            def click(app):
                app.info('Thanks for clicking...')

        """

        def outer(func: Callable) -> Callable:
            button = Button(self, parent or self.sidebar, text=text, action=func)
            return button

        return outer

    def checkbox(self, text: str, checked: bool = True, parent=None) -> Callable:
        """Decorator for checkbox actions.

        Parameters
        ----------
        text : str
            The text label of the checkbox.
        checked : bool, optional
            If True, the checkbox will be displayed as checked.

        Returns
        -------
        callable

        Notes
        -----
        Use this method to convert a function into the callback action of a checkbox,
        and automatically add the checkbox to the sidebar.

        Examples
        --------
        .. code-block:: python

            @viewer.checkbox('Check me!')
            def check(app):
                app.info('Thanks for checking...')

        """

        def outer(func: Callable) -> Callable:
            checkbox = Checkbox(self, parent or self.sidebar, text=text, action=func, checked=checked)
            return checkbox

        return outer

    def slider(
        self,
        title: str,
        value: int = 0,
        minval: int = 0,
        maxval: int = 100,
        step: int = 1,
        annotation: str = "",
        bgcolor: Color = None,
        parent=None,
    ) -> Callable:
        """Decorator for slider actions.

        Parameters
        ----------
        title : str
            The text label of the slider.
        value : int, optional
            Initial value of the slider.
        minval : int, optional
            Minimum value of the sliding range.
        maxval : int, optional
            Maximum value of the sliding range.
        step : int, optional
            Size of the sliding step.
        annotation : str, optional
            Value annotation.

        Returns
        -------
        callable

        Notes
        -----
        Use this method to convert a function into the callback action of a slider,
        and automatically add the slider to the sidebar.

        Examples
        --------
        .. code-block:: python

            @viewer.slider(title='Slide me!')
            def slide(app):
                app.info('Thanks for sliding...')

        """

        def outer(func: Callable) -> Callable:
            slider = Slider(
                self,
                parent or self.sidebar,
                func,
                value=value,
                minval=minval,
                maxval=maxval,
                step=step,
                title=title,
                annotation=annotation,
                bgcolor=bgcolor,
            )
            return slider

        return outer

    def on(
        self,
        interval: int = None,
        timeout: int = None,
        frames: int = None,
        record: bool = False,
        record_path: str = "temp/out.gif",
        record_fps: int = None,
        playback_interval: int = None,
    ) -> Callable:
        """Decorator for callbacks of a dynamic drawing process.

        Parameters
        ----------
        interval : int, optional
            Interval between subsequent calls to this function, in milliseconds.
        timeout : int, optional
            Timeout between subsequent calls to this function, in milliseconds.
        frames : int, optional
            The number of frames of the process.
            If no frame number is provided, the process continues until the viewer is closed.
        record : bool, optional
            If True, record a screenshot of every frame.
        record_path : str, optional
            The path where the recording should be saved.
        playback_interval : int, optional
            Interval between frames in the recording, in milliseconds.

        Returns
        -------
        callable

        Notes
        -----
        The difference between `interval` and `timeout` is that the former indicates
        the time between subsequent calls to the callback, without taking into account the duration of the execution of the call,
        whereas the latter indicates a pause after the completed execution of the previous call, before starting the next one.

        Examples
        --------
        .. code-block:: python

            angle = math.radians(5)

            @viewer.on(interval=1000)
            def rotate(frame):
                obj.rotation = [0, 0, frame * angle]
                obj.update()

        """
        if (not interval and not timeout) or (interval and timeout):
            raise ValueError("Must specify either interval or timeout")

        if record:
            # check if record_path is writable
            # create temp dir for frames
            self.tempdir = tempfile.mkdtemp()
            record_fps = record_fps or 1000 / interval

        def outer(func: Callable):
            def render():
                func(self.frame_count)
                self.view.update()
                self.frame_count += 1
                if frames is not None and self.frame_count >= frames:
                    self.timer.stop()
                    if self.record:
                        self.record = False
                        # self.recorded_frames[0].save(
                        #     record_path, save_all=True, optimize=False,
                        #     duration=playback_interval or interval,
                        #     append_images=self.recorded_frames[1:],
                        #     loop=100)
                        files = [os.path.join(self.tempdir, f"{i}.png") for i in range(frames)]
                        gif_from_images(
                            files=files,
                            gif_path=record_path,
                            fps=record_fps,
                            delete_files=True,
                        )
                        shutil.rmtree(self.tempdir)
                        print("Recorded to ", record_path)

            if interval:
                self.timer = Timer(interval=interval, callback=render)
            if timeout:
                self.timer = Timer(interval=timeout, callback=render, singleshot=True)

            self.frame_count = 0
            self.record = record

        return outer
