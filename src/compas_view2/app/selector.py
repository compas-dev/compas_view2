from random import randint
import numpy as np
import time
from .worker import Worker


class Selector:
    """Selector class manages all selection operations for the viewer.

    Parameters
    ----------
    app: :class:`compas_view2.app.App`
        The parent application.

    Attributes
    ----------
    app: :class:`compas_view2.app.App`
        The parent application.
    mode: "single" | "multi" | "deselect"
        The selection mode.
    overwrite_mode: "single" | "multi" | "deselect"
        Used in interative selection sessions to temporarily overwrite default select mode
    types: list
        Selectable types.
    select_from: "pixel" | "box"
        The selection mechanism.
    enabled: bool
        Flag indicating to the view that an instance map should be drawn.
    wait_for_selection: bool
        Flag indicating to wait for the interatice selection to finish
    wait_for_selection_on_plane: bool
        Flag indicating to wait for the user to pick a location on plane
    snap_to_grid: bool
        Turn grid snap on or off.
    colors_to_exclude: list[tuple[int, int, int]]
        The instance colors to exclude from the selection process.
    instances: dict
        Mapping between pixel colors and scene objects.
    instance_map: np.array with shape (?,?,3)
        The painted instance map as np array
    box_select_coords: list of 4 floats
        The 2D box selection coordinates on view window: [minX, minY, maxX, maxY]
    location_on_plane:
        The selected location on plane
    """

    def __init__(self, app):
        self.app = app

        # Selector options
        self.mode = "single"
        self.overwrite_mode = None
        self.types = []
        self.select_from = "pixel"  # or "box"
        # Selector state flags
        self.enabled = False
        self.wait_for_selection = False
        self.wait_for_selection_on_plane = False
        self.snap_to_grid = False
        # Selector data
        self.colors_to_exclude = [(0, 0, 0,), (255, 255, 255)]
        self.instances = {}
        self.instance_map = None
        self.box_select_coords = np.zeros((4,), np.int)
        self.location_on_plane = None

        self.start_monitor_instance_map()

    def reset(self):
        """Reset the selector state
        """
        self.mode = "single"
        self.overwrite_mode = None
        self.types = []
        self.select_from = "pixel"
        self.enabled = False
        self.box_select_coords = np.zeros((4,), np.int)
        self.wait_for_selection = False
        self.wait_for_selection_on_plane = False
        self.location_on_plane = None
        self.snap_to_grid = False
        self.deselect()

    def start_monitor_instance_map(self):
        """This function triggers a monitor loop to watch the instance map attribute,
        Once an instance map is painted, the actual selection operation is triggered here.
        """

        self.stop_monitor_instance_map = False

        def monitor_loop():
            while not self.stop_monitor_instance_map:
                time.sleep(0.02)
                if self.instance_map is not None:
                    instance_map = self.instance_map
                    if self.select_from == "pixel":
                        # Pick an object from mouse pixel
                        x = self.app.view.mouse.last_pos.x()
                        y = self.app.view.mouse.last_pos.y()
                        self.select_one_from_instance_map(x, y, instance_map)
                    if self.select_from == "box":
                        # Pick objects from box selection
                        self.select_all_from_instance_map(instance_map)
                        self.select_from = "pixel"
                    self.app.view.update()
                    self.instance_map = None

        # Stop the monitor loop when the app is being closed
        def stop():
            self.stop_monitor_instance_map = True
        self.app._app.aboutToQuit.connect(stop)

        # Start monitor loop in a separate worker thread
        worker = Worker(monitor_loop)
        worker.no_signals = True  # Prevent signal emit error when closing the app
        Worker.pool.start(worker)

    @property
    def selected(self):
        """
        Returns
        -------
        list of instances
            The instances that are selected
        """
        return [self.instances[key] for key in self.instances if self.instances[key].is_selected]

    def get_rgb_key(self):
        """
        Returns
        -------
        rgb_key
            a tuple of rgb color value in integer
        """
        while True:
            rgb_key = (randint(0, 255), randint(0, 255), randint(0, 255))
            if rgb_key not in self.instances and rgb_key not in self.colors_to_exclude:
                return rgb_key

    def add(self, obj):
        """Add an object to the list of selector instances, each object will be assigned a unique hex color key

        Returns
        -------
        rgb_key
            a rgb tuple key that represents this object
        """
        rgb_key = self.get_rgb_key()
        self.instances[rgb_key] = obj
        obj._instance_color = np.array(rgb_key)/255
        return rgb_key

    def select_one_from_instance_map(self, x, y, instance_map):
        """Select the object at given pixel location of the instance map

        Parameters
        ----------
        x : int
            x coordinate of the pixel
        y : int
            y coordinate of the pixel
        instance_map: np.array
            instance map of the current camera view

        Returns
        -------
        None
        """
        rgb_key = tuple(instance_map[y][x])
        obj = None
        if rgb_key in self.instances:
            obj = self.instances[rgb_key]
        self.select(obj)

    def select_all_from_instance_map(self, instance_map):
        """Select all the objects that appear in the instance map

        Parameters
        ----------
        instance_map: np.array
            instance map of the current camera view

        Returns
        -------
        None
        """
        unique_rgbs = np.unique(instance_map.reshape(-1, instance_map.shape[2]), axis=0)
        for rgb in unique_rgbs:
            rgb_key = tuple(rgb)
            if rgb_key in self.instances:
                obj = self.instances[rgb_key]
                self.select(obj)

    def select(self, obj=None, mode=None, types=None, update=False):
        """Perform select operation

        Parameters
        ----------
        obj : compas_view2.objects.Object
            the target object
        mode : string
            the selection mode, can be "single", "multi" or "deselect"
        types : type
            object data types to be allowed
        update : bool
            whether to trigger app update after this selection

        Returns
        -------
        None
        """
        mode = mode or self.mode
        types = types or self.types
        if mode == 'single':
            if obj:
                self.deselect()
                obj.is_selected = True
        elif mode == 'multi':
            if not obj:
                return
            if types:
                for _type in types:
                    if isinstance(obj._data, _type):
                        obj.is_selected = True
            else:
                obj.is_selected = True
        elif mode == 'deselect':
            self.deselect(obj)
        else:
            raise NotImplementedError
        if update:
            self.app.view.update()

    def deselect(self, obj=None, update=False):
        """Deselect the target object

        Parameters
        ----------
        obj : compas_view2.objects.Object
            the target object
        update : bool
            whether to trigger app update after this selection

        Returns
        -------
        None
        """
        if obj:
            obj.is_selected = False
        else:
            for key in self.instances:
                self.instances[key].is_selected = False
        if update:
            self.app.view.update()

    def start_selection(self, types=None, mode="multi", returns="data"):
        """Start an interactive selection session.

        Parameters
        ----------
        types : list of type
            the allowed types of object data
        mode : string
            the selection mode of the session, default to "multi"
        returns : string
            controls whether to return the objects or the data of objects

        Returns
        -------
        list of selected object data

        Notes
        -----
        This function has to be called inside a interactive (non-blocking) session,
        Otherwise it will freeze the main programme.
        """
        if not isinstance(types, list) and types is not None:
            types = [types]
        self.deselect(update=True)
        self.mode = self.overwrite_mode = mode
        self.types = types
        self.wait_for_selection = True
        while self.wait_for_selection:
            time.sleep(0.05)
        if returns == "data":
            selected = [obj._data for obj in self.selected]
        if returns == "object":
            selected = [obj for obj in self.selected]
        else:
            raise ValueError("must choose to return 'data' or 'object'")
        self.reset()
        return selected

    def start_selection_on_plane(self, snap_to_grid=False):
        """Start an interactive selection session to pick a location on the grid plane.

        Parameters
        ----------
        snap_to_grid : bool
            Whether to snap the location on the grid

        Returns
        -------
        List of 3 float numbers, selected location on the plane

        Notes
        -----
        This function has to be called inside a interactive (non-blocking) session,
        Otherwise it will freeze the main programme.
        """
        self.wait_for_selection_on_plane = True
        self.snap_to_grid = snap_to_grid
        while self.wait_for_selection_on_plane:
            time.sleep(0.05)
        return self.location_on_plane

    def finish_selection_on_plane(self, x, y):
        """Finish selecting location on the grid plane.

        Parameters
        ----------
        x : int
            mouse x coordinate on uv_plane_map
        y : int
            mouse y coordinate on uv_plane_map

        Returns
        -------
        None
        """
        u, v, w = self.app.selector.uv_plane_map[y, x]
        if [u, v, w] == [1, 1, 1]:
            # When clicked outside of the grid
            self.location_on_plane = None
        else:
            x_size = self.app.view.grid.x_cells * self.app.view.grid.cell_size
            y_size = self.app.view.grid.y_cells * self.app.view.grid.cell_size
            x = -x_size + 2*x_size*u
            y = -y_size + 2*y_size*v
            if self.snap_to_grid:
                x = round(x / self.app.view.grid.cell_size) * self.app.view.grid.cell_size
                y = round(y / self.app.view.grid.cell_size) * self.app.view.grid.cell_size
            self.location_on_plane = [x, y, 0]
        self.wait_for_selection_on_plane = False

    def finish_selection(self):
        """Finish the interactive selection session.
        """
        self.wait_for_selection = False
        self.wait_for_selection_on_plane = False

    def reset_box_selection(self, x, y):
        """Reset box selection start position

        Parameters
        ----------
        x : int
            current x coordinate of the mouse
        y : int
            current y coordinate of the mouse

        Returns
        -------
        None
        """
        # Set the start mouse location
        self.box_select_coords[:2] = x, y

    def perform_box_selection(self, x, y):
        """Update a box selection session.

        Parameters
        ----------
        x : int
            current x coordinate of the mouse
        y : int
            current y coordinate of the mouse

        Returns
        -------
        None
        """
        # Set the current mouse location
        box_width = abs(x - self.box_select_coords[0])
        box_height = abs(y - self.box_select_coords[1])

        if box_width > 0 and box_height > 0:
            self.select_from = "box"
            self.box_select_coords[2:] = x, y
