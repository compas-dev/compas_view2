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
from .app import App
from .key import Key



class Controller ():
    """Action controller for the default config file.

    Parameters
    ----------
    app: :class:`compas_view2.app.App`
        The parent application.

    """

    def __init__(self, app:App, controller_config:Dict):
        self.app = app
        self.config = controller_config
        self.mouse = Mouse()

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

    def mouse_move_action(self,event):
        # record mouse position
        self.mouse.pos = event.pos()
        # compute displacement
        dx = self.mouse.dx()
        dy = self.mouse.dy()
        # do a box selection
        # if left button + SHIFT
        # TODO
        if event.buttons() & QtCore.Qt.LeftButton:
            if self.keys["shift"] or self.keys["control"]:
                self.app.selector.perform_box_selection(self.mouse.pos.x(), self.mouse.pos.y())
            # record mouse position
            self.mouse.last_pos = event.pos()
            self.update()
        # change the view
        # if right bottom
        elif event.buttons() & QtCore.Qt.RightButton:
            if self.keys["shift"]:
                self.camera.pan(dx, dy)
            else:
                self.camera.rotate(dx, dy)
            # record mouse position
            self.mouse.last_pos = event.pos()
            self.update()

    def mouse_press_action(self,event):
        # start selecting
        # if left button
        if event.buttons() & QtCore.Qt.LeftButton:
            self.mouse.buttons["left"] = True
            if self.keys["shift"] or self.keys["control"]:
                self.app.selector.reset_box_selection(event.pos().x(), event.pos().y())
        # do nothing
        # if right button
        elif event.buttons() & QtCore.Qt.RightButton:
            self.mouse.buttons["right"] = True
            if self.keys["shift"]:
                QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.OpenHandCursor)
            else:
                QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.SizeAllCursor)
        # recod mouse position
        self.mouse.last_pos = event.pos()
        self.update()

    def mouse_release_action(self,event):
        # finalize selecting
        # if left button
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouse.buttons["left"] = False
            # select location on grid
            if self.app.selector.wait_for_selection_on_plane:
                self.app.selector.finish_selection_on_plane(event.pos().x(), event.pos().y())
            # trigger object selection
            else:
                self.app.selector.enabled = True
        # do nothing
        # if right button
        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            self.mouse.buttons["right"] = False
        QtWidgets.QApplication.restoreOverrideCursor()

    def wheel_action(self,event):
        degrees = event.delta() / 8
        steps = degrees / 15
        self.camera.zoom(steps)
        self.update()

    def key_press_action(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
            self.app.selector.finish_selection()
        if key == QtCore.Qt.Key_Shift:
            self.app.selector.mode = "multi"
            self.keys["shift"] = True
        if key == QtCore.Qt.Key_Control:
            self.app.selector.mode = "deselect"
            self.keys["control"] = True
        if key == QtCore.Qt.Key_F:
            self.keys["f"] = True
            if self.app.selector.selected:
                self.camera.zoom_extents(self.app.selector.selected)
            else:
                self.camera.zoom_extents(self.objects)
            self.update()

    def key_release_action(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Shift:
            self.app.selector.mode = self.app.selector.overwrite_mode or "single"
            self.keys["shift"] = False
        if key == QtCore.Qt.Key_Control:
            self.app.selector.mode = self.app.selector.overwrite_mode or "single"
            self.keys["control"] = False
        if key == QtCore.Qt.Key_F:
            self.keys["f"] = False

    # ==============================================================================
    # View actions
    # ==============================================================================

    def view_shaded(self):
        """Switch the view to shaded.

        Returns
        -------
        None

        """
        self.app.view.mode = "shaded"
        self.app.view.update()

    def view_ghosted(self):
        """Switch the view to ghosted.

        Returns
        -------
        None

        """
        self.app.view.mode = "ghosted"
        self.app.view.update()

    def view_wireframe(self):
        """Switch the view to wireframe.

        Returns
        -------
        None

        """
        self.app.view.mode = "wireframe"
        self.app.view.update()

    def view_lighted(self):
        """Switch the view to lighted.

        Returns
        -------
        None

        """
        self.app.view.mode = "lighted"
        self.app.view.update()

    def view_capture(self, filepath=None):
        """Capture a screenshot.

        Parameters
        ----------
        filepath : str, optional
            The destination path for saving the screenshot.
            If no path is provided, a file dialog will be be opened automatically.

        Returns
        -------
        None

        """
        if filepath:
            result = filepath
        else:
            result = QtWidgets.QFileDialog.getSaveFileName(caption="File name", dir="")
            if not result:
                return
            result = result[0]
        filepath = Path(result)
        if not filepath.suffix:
            return
        qimage = self.app.view.grabFramebuffer()
        qimage.save(str(filepath), filepath.suffix[1:])

    def view_front(self):
        """Swtich to a front view.

        Returns
        -------
        None

        """
        self.app.view.current = self.app.view.FRONT
        self.app.view.camera.reset_position()
        self.app.view.update_projection()
        self.app.view.update()

    def view_right(self):
        """Swtich to a right view.

        Returns
        -------
        None

        """
        self.app.view.current = self.app.view.RIGHT
        self.app.view.camera.reset_position()
        self.app.view.update_projection()
        self.app.view.update()

    def view_top(self):
        """Swtich to a top view.

        Returns
        -------
        None

        """
        self.app.view.current = self.app.view.TOP
        self.app.view.camera.reset_position()
        self.app.view.update_projection()
        self.app.view.update()

    def view_perspective(self):
        """Swtich to a perspective view.

        Returns
        -------
        None

        """
        self.app.view.current = self.app.view.PERSPECTIVE
        self.app.view.camera.reset_position()
        self.app.view.update_projection()
        self.app.view.update()

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
