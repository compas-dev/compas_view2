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
from compas_view2.actions import action_manager, mouse_key_check, mouse_check, key_check


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
        self.actions = action_manager(self)

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
        if mouse_key_check(event, self.key_status, self.mouse_key["box_selection"]):
            self.app.selector.mode = "multi"
            self.app.selector.perform_box_selection(self.mouse.pos.x(), self.mouse.pos.y())
        # box_deselection
        elif mouse_key_check(event, self.key_status, self.mouse_key["box_deselection"]):
            self.app.selector.mode = "deselect"
            self.app.selector.perform_box_selection(self.mouse.pos.x(), self.mouse.pos.y())
        # pan
        elif mouse_key_check(event, self.key_status, self.mouse_key["pan"]):
            self.app.view.camera.pan(dx, dy)
        # rotate
        elif mouse_key_check(event, self.key_status, self.mouse_key["rotate"]):
            self.app.view.camera.rotate(dx, dy)

        # record mouse position
        self.mouse.last_pos = event.pos()
        self.app.view.update()

    def mouse_press_action(self, event):
        # * mouse_key
        # box_selection
        if mouse_key_check(event, self.key_status, self.mouse_key["box_selection"]) or mouse_key_check(
            event, self.key_status, self.mouse_key["box_deselection"]
        ):
            self.app.selector.reset_box_selection(event.pos().x(), event.pos().y())
        # change cursor
        elif mouse_key_check(event, self.key_status, self.mouse_key["pan"]):
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.OpenHandCursor)
        elif mouse_key_check(event, self.key_status, self.mouse_key["rotate"]):
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.SizeAllCursor)

        self.mouse.last_pos = event.pos()
        self.app.view.update()

    def mouse_release_action(self, event):
        # * mouse_key
        # selection
        if mouse_check(event, self.mouse_key["selection"]["mouse"]):
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
        if key_check(event, self.key_status, self.mouse_key["selection"]["multi_selection"]):
            self.app.selector.mode = "multi"
            self.key_status[self.mouse_key["selection"]["multi_selection"]] = True
        # deselect
        if key_check(event, self.key_status, self.mouse_key["selection"]["deselect"]):
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
        if key_check(event, self.key_status, self.mouse_key["box_selection"]["key"]):
            self.key_status[self.mouse_key["box_selection"]["key"]] = False
        # box_deselection
        elif key_check(event, self.key_status, self.mouse_key["box_deselection"]["key"]):
            self.key_status[self.mouse_key["box_deselection"]["key"]] = False
        # pan
        elif key_check(event, self.key_status, self.mouse_key["pan"]["key"]):
            self.key_status[self.mouse_key["pan"]["key"]] = False
        # rotate
        elif key_check(event, self.key_status, self.mouse_key["rotate"]["key"]):
            self.key_status[self.mouse_key["rotate"]["key"]] = False

        # * multi_selection
        if key_check(event, self.key_status, self.mouse_key["selection"]["multi_selection"]):
            self.app.selector.mode = self.app.selector.overwrite_mode or "single"
            self.key_status[self.mouse_key["selection"]["multi_selection"]] = False
        # * deselect
        if key_check(event, self.key_status, self.mouse_key["selection"]["deselect"]):
            self.app.selector.mode = self.app.selector.overwrite_mode or "single"
            self.key_status[self.mouse_key["selection"]["deselect"]] = False

        for action in self.actions.values():
            if action.keys_released_check(event):
                action.keys_released_action()

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
