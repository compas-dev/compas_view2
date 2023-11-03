from OpenGL import GL

from qtpy import QtWidgets
from qtpy import QtCore

from typing import Union, Dict
from pathlib import Path

from compas.geometry import Point
from compas.datastructures import Network
from compas.datastructures import Mesh
from compas_view2.scene import Mouse
from compas_view2.forms import AddForm
from compas_view2.forms import PropertyForm

from .worker import Worker


class Controller:
    """Action controller for the default config file.

    Parameters
    ----------
    app: :class:`compas_view2.app.App`
        The parent application.

    """

    def __init__(self, app, controller_config: Dict):
        self.app = app
        self.config = controller_config
        self.mouse_key = controller_config["actions"]["mouse_key"]
        self.keys = controller_config["actions"]["keys"]
        self.mouse = Mouse()
        self.key_status = {}
        self.actions = {}  # Currently, no customized actions supported.
        self.supported_keys = {
            "shift": QtCore.Qt.Key_Shift,
            "control": QtCore.Qt.Key_Control,
            "alt": QtCore.Qt.Key_Alt,
            "placeholder": None,
        }

    # ==============================================================================
    # Providing the basic key and mouse event handling functions.
    # ==============================================================================
    def mouse_key_check(self, event, key_status: Dict, mouse_key: Dict):
        """Giving the mouse key as a dictionary that is in the list of supported keys, return if it is happening (bool).

        Parameters
        ----------
        event:
            The Qt event.
        key_status : Dict
            The status dictionary that is like `"key_status": { "shift": False, "control": False, "alt": False }`.
        mouse_key : Dict
            The dictionary that is like `"mouse_key": { "mouse": "right", "key": "shift" }`.

        Returns
        ----------
        bool:
            If the mouse key is happening.


        Notes
        ----------
        This function is designed to check mouse_key combine interactions. The interactions are:
        "box_selection", "selection", "multi_selection", "deselect", "pan", "rotate", for now.
        """
        supported_buttons = {
            "left": QtCore.Qt.LeftButton,
            "right": QtCore.Qt.RightButton,
            "middle": QtCore.Qt.MiddleButton,
        }

        if event.buttons() & supported_buttons[mouse_key["mouse"]]:
            if key_status.get(mouse_key["key"]) is None:
                key_status[mouse_key["key"]] = False

            if mouse_key["key"] == "":
                for key in key_status.values():
                    if key:
                        return False
                return True

            elif key_status[mouse_key["key"]]:
                return True

        else:
            return False

    def mouse_check(self, event, button_name: str):
        """Giving the button name that is one of the supported buttons, return if the button is pressed.

        Parameters
        ----------
        event:
            The Qt event.
        button_name : str
            The name of the button. It should be exist in the list of `supported buttons`.

        Returns
        ----------
        bool:
            If the button is pressed.
        """
        supported_buttons = {
            "left": QtCore.Qt.LeftButton,
            "right": QtCore.Qt.RightButton,
            "middle": QtCore.Qt.MiddleButton,
        }
        if button_name not in supported_buttons:
            # Normally, this should not happen.
            raise KeyError(f"Button {button_name} is not supported.")
        else:
            if event.button() == supported_buttons[button_name]:
                return True
            else:
                return False

    def key_check(self, event, key_status: Dict, key_name: str):
        """Giving the key name that is one of the supported keys, return if the key is pressed.

        Parameters
        ----------
        event:
            The Qt event.
        key_status : Dict
            The status dictionary that is like `"key_status": { "shift": False, "control": False, "alt": False }`.
        key_name : str
            The name of the key. It should be exist in the list of `supported keys`.

        Returns
        ----------
        bool:
            If the key is pressed.
        """

        if key_name == "":
            for key in key_status.values():
                if key:
                    return False
            return True
        elif key_name not in self.supported_keys:
            raise KeyError(f"Key {key_name} is not supported.")
        else:
            if event.key() == self.supported_keys[key_name]:
                return True
            else:
                return False

    def interactive(action="add"):
        """Decorator for transforming functions into "data add" or "object edit" actions.

        Parameters
        ----------
        action : {'add', 'edit'}, optional
            The type of action.

        Returns
        -------
        callable

        """

        def outer(func):
            def wrapped(self):
                def add(data):
                    if data:
                        self.app.add(data)
                        self.app.view.update()

                def edit(obj):
                    if obj:
                        dock = PropertyForm("Property", obj, on_update=self.app.view.update)
                        self.app.window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)

                worker = Worker(func, [self])
                if action == "add":
                    worker.signals.result.connect(add)
                elif action == "edit":
                    worker.signals.result.connect(edit)
                else:
                    raise NotImplementedError()
                Worker.pool.start(worker)

            return wrapped

        return outer

    # ==============================================================================
    # App actions
    # ==============================================================================

    def dummy(self):
        """Dummy action for UI element stubs.

        Returns
        -------
        None

        """
        pass

    def about(self):
        """Display the about message.

        Returns
        -------
        None

        """
        self.app.about()

    def opengl_version(self):
        """Display the OpenGL version.

        Returns
        -------
        None

        """
        value = "OpenGL {}".format(GL.glGetString(GL.GL_VERSION).decode("ascii"))
        self.app.info(value)

    def glsl_version(self):
        """Display the version of the shader language.

        Returns
        -------
        None

        """
        value = "GLSL {}".format(GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode("ascii"))
        self.app.info(value)

    # ==============================================================================
    # Key mouse actions
    # ==============================================================================

    def mouse_move_action(self, event):
        # record mouse position
        self.mouse.pos = event.pos()
        # compute displacement
        dx = self.mouse.dx()
        dy = self.mouse.dy()

        # * mouse_key
        # box_selection
        if self.mouse_key_check(event, self.key_status, self.mouse_key["box_selection"]):
            self.app.selector.mode = "multi"
            self.app.selector.perform_box_selection(self.mouse.pos.x(), self.mouse.pos.y())
        # box_deselection
        elif self.mouse_key_check(event, self.key_status, self.mouse_key["box_deselection"]):
            self.app.selector.mode = "deselect"
            self.app.selector.perform_box_selection(self.mouse.pos.x(), self.mouse.pos.y())
        # pan
        elif self.mouse_key_check(event, self.key_status, self.mouse_key["pan"]):
            self.app.view.camera.pan(dx, dy)
        # rotate
        elif self.mouse_key_check(event, self.key_status, self.mouse_key["rotate"]):
            self.app.view.camera.rotate(dx, dy)

        # record mouse position
        self.mouse.last_pos = event.pos()
        self.app.view.update()

    def mouse_press_action(self, event):
        # * mouse_key
        # box_selection
        if self.mouse_key_check(event, self.key_status, self.mouse_key["box_selection"]) or self.mouse_key_check(
            event, self.key_status, self.mouse_key["box_deselection"]
        ):
            self.app.selector.reset_box_selection(event.pos().x(), event.pos().y())
        # change cursor
        elif self.mouse_key_check(event, self.key_status, self.mouse_key["pan"]):
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.OpenHandCursor)
        elif self.mouse_key_check(event, self.key_status, self.mouse_key["rotate"]):
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.SizeAllCursor)

        self.mouse.last_pos = event.pos()
        self.app.view.update()

    def mouse_release_action(self, event):
        # * mouse_key
        # selection
        if self.mouse_check(event, self.mouse_key["selection"]["mouse"]):
            if self.app.selector.wait_for_selection_on_plane:
                self.app.selector.finish_selection_on_plane(event.pos().x(), event.pos().y())
            else:
                self.app.selector.enabled = True

        QtWidgets.QApplication.restoreOverrideCursor()

    def wheel_action(self, event):
        degrees = event.delta() / 8
        steps = degrees / 15
        self.app.view.camera.zoom(steps)
        self.app.view.update()

    def key_press_action(self, event):
        # * mouse_key
        # selection
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.app.selector.finish_selection()
            self.key_status[self.mouse_key["selection"]["key"]] = True
        # multi_selection
        if self.key_check(event, self.key_status, self.mouse_key["selection"]["multi_selection"]):
            self.app.selector.mode = "multi"
            self.key_status[self.mouse_key["selection"]["multi_selection"]] = True
        # deselect
        if self.key_check(event, self.key_status, self.mouse_key["selection"]["deselect"]):
            self.app.selector.mode = "deselect"
            self.key_status[self.mouse_key["selection"]["deselect"]] = True

        # * key actions
        for action in self.actions.values():
            if action.keys_pressed_check(event):
                action.keys_pressed_action()

        self.app.view.update()

    def key_release_action(self, event):
        # * box_selection
        # box_selection
        if self.key_check(event, self.key_status, self.mouse_key["box_selection"]["key"]):
            self.key_status[self.mouse_key["box_selection"]["key"]] = False
        # box_deselection
        elif self.key_check(event, self.key_status, self.mouse_key["box_deselection"]["key"]):
            self.key_status[self.mouse_key["box_deselection"]["key"]] = False
        # pan
        elif self.key_check(event, self.key_status, self.mouse_key["pan"]["key"]):
            self.key_status[self.mouse_key["pan"]["key"]] = False
        # rotate
        elif self.key_check(event, self.key_status, self.mouse_key["rotate"]["key"]):
            self.key_status[self.mouse_key["rotate"]["key"]] = False

        # * multi_selection
        if self.key_check(event, self.key_status, self.mouse_key["selection"]["multi_selection"]):
            self.app.selector.mode = self.app.selector.overwrite_mode or "single"
            self.key_status[self.mouse_key["selection"]["multi_selection"]] = False
        # * deselect
        if self.key_check(event, self.key_status, self.mouse_key["selection"]["deselect"]):
            self.app.selector.mode = self.app.selector.overwrite_mode or "single"
            self.key_status[self.mouse_key["selection"]["deselect"]] = False

    # ==============================================================================
    # Scene actions
    # ==============================================================================

    def load_scene(self):
        """Load a scene from a file."""
        self.app.info("Not available yet...")

    def save_scene(self):
        """Save the current scene to a file."""
        self.app.info("Not available yet...")

    def redraw_scene(self):
        """Redraw the current scene.

        Returns
        -------
        None

        """
        self.app.view.update()

    def clear_scene(self):
        """Clear all objects from the current scene."""
        self.app.info("Not available yet...")

    def undo(self):
        """Undo the last scene modification."""
        self.app.info("Not available yet...")

    def redo(self):
        """Redo the last scene modification."""
        self.app.info("Not available yet...")

    def history(self):
        """Display the undo history of the scene."""
        self.app.info("Not available yet...")

    # ==============================================================================
    # Primitive actions
    # ==============================================================================

    def add_geometry_object(self):
        def on_create(data):
            self.app.add(data)
            self.app.view.update()

        form = AddForm(on_create=on_create)
        form.exec_()

    @interactive("edit")
    def edit_selected_object(self):
        if len(self.app.selector.selected) == 1:
            return self.app.selector.selected[0]
        else:
            self.app.status("Select one object on screen, Click Enter to finish")
            objects = self.app.selector.start_selection(types=[Point], mode="single", returns="object")
            if len(objects) != 1:
                self.app.status("Must select 1 object")
                return None
            self.app.status("")
            return objects[0]

    # ==============================================================================
    # Network actions
    # ==============================================================================

    def add_network_from_obj(self) -> Union[Network, None]:
        """Add a network from the data in an OBJ file.

        Returns
        -------
        :class:`compas.datastructures.Network` or None
            A network data structure,
            if the operation was successful,
            or None otherwise.

        """
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self.app.window, caption="Select File", dir="", filter="OBJ Files (*.obj)"
        )
        if filename:
            network = Network.from_obj(filename)
            self.app.add(network)
            self.app.view.update()
            return network

    # ==============================================================================
    # Mesh actions
    # ==============================================================================

    def add_mesh_from_file(self) -> Union[Mesh, None]:
        """Add a mesh from the data in an file.

        Returns
        -------
        :class:`compas.datastructures.Mesh` or None
            A mesh data structure,
            if the operation was successful,
            or None otherwise.

        Notes
        -----
        The following file formats are supported

        * OBJ
        * OFF
        * PLY
        * STL

        """
        filepath, selectedfilter = QtWidgets.QFileDialog.getOpenFileName(
            parent=self.app.window, caption="Select File", dir="", filter="Mesh Files (*.obj, *.off, *.ply, *.stl)"
        )

        if filepath:
            path = Path(filepath)

            if path.suffix == ".obj":
                mesh = Mesh.from_obj(path)
            elif path.suffix == ".off":
                mesh = Mesh.from_off(path)
            elif path.suffix == ".ply":
                mesh = Mesh.from_ply(path)
            elif path.suffix == ".stl":
                mesh = Mesh.from_stl(path)

            self.app.add(mesh)
            self.app.view.update()
            return mesh

    # ==============================================================================
    # Flow actions
    # ==============================================================================

    def show_flow(self) -> None:
        """Display the ryven flow window."""
        self.app.flow.show()

    def run_all(self) -> None:
        """Execute all the ryven nodes in the order of data flow."""
        self.app.flow.run_all()

    def enable_auto_update(self) -> None:
        """Enable auto update of all the ryven nodes."""
        self.run_all()
        for node in self.app.flow.flow_view.node_items:
            node.auto_update = True

    def disable_auto_update(self) -> None:
        """Disable auto update of all the ryven nodes."""
        for node in self.app.flow.flow_view.node_items:
            node.auto_update = False

    # ==============================================================================
    # Robot actions
    # ==============================================================================

    # ==============================================================================
    # Assembly actions
    # ==============================================================================

    # ==============================================================================
    # FEA actions
    # ==============================================================================
