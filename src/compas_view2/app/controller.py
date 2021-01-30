from OpenGL import GL

from PySide2 import QtWidgets

from typing import Union
from pathlib import Path

from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Torus
from compas.datastructures import Network
from compas.datastructures import Mesh

from ..forms import PointForm
from ..forms import SphereForm
from ..forms import TorusForm
from .worker import Worker


class Controller:

    def __init__(self, app):
        self.app = app

    def interactive(func):
        def wrapped(self):
            def add(obj):
                if obj:
                    self.app.add(obj)
                    self.app.view.update()

            worker = Worker(func, self)
            worker.signals.result.connect(add)
            Worker.pool.start(worker)
        return wrapped

    def about(self):
        self.app.about()

    def opengl_version(self):
        value = "OpenGL {}".format(GL.glGetString(GL.GL_VERSION).decode('ascii'))
        self.app.info(value)

    def glsl_version(self):
        value = "GLSL {}".format(GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode('ascii'))
        self.app.info(value)

    # Actions: View

    def to_shaded(self):
        self.app.view.mode = 'shaded'

    def to_ghosted(self):
        self.app.view.mode = 'ghosted'

    def capture(self):
        result = QtWidgets.QFileDialog.getSaveFileName(caption="File name", dir="")
        if not result:
            return
        filepath = Path(result[0])
        if not filepath.suffix:
            return
        qimage = self.app.view.grabFramebuffer()
        qimage.save(str(filepath), filepath.suffix[1:])

    def view_front(self):
        self.app.info('Not available yet...')

    def view_right(self):
        self.app.info('Not available yet...')

    def view_top(self):
        self.app.info('Not available yet...')

    def view_perspective(self):
        self.app.info('Not available yet...')

    # Actions: Scene

    def load_scene(self):
        self.app.info('Not available yet...')

    def save_scene(self):
        self.app.info('Not available yet...')

    def redraw_scene(self):
        self.app.info('Not available yet...')

    def clear_scene(self):
        self.app.info('Not available yet...')

    def undo(self):
        self.app.info('Not available yet...')

    def redo(self):
        self.app.info('Not available yet...')

    def history(self):
        self.app.info('Not available yet...')

    # Actions: Primitives

    def add_point(self):
        form = PointForm()
        if form.exec_():
            x = form.x
            y = form.y
            z = form.z
            point = Point(x, y, z)
            self.app.add(point)
            self.app.view.update()
            return point

    @interactive
    def add_line_from_selected_points(self):
        self.app.statusbar.showMessage(
            "Select points on screen, Click Enter to finish")
        points = self.app.selector.start_selection(types=[Point])
        if len(points) != 2:
            self.app.statusbar.showMessage("Must select 2 points")
            return None
        line = Line(*points)
        self.app.statusbar.showMessage("Line added")
        return line

    # Actions: Shapes

    def add_box(self) -> Union[Box, None]:
        """Add a box at the origin.

        Returns
        -------
        :class:`Box`
            If the operation was successful
        None
            Otherwise
        """
        r = QtWidgets.QInputDialog.getDouble(self.app.window, 'Add Box', 'size', 1)
        if r[1] and r[0] > 0:
            size = r[0]
            box = Box.from_width_height_depth(size, size, size)
            self.app.add(box)
            self.app.view.update()

    def add_sphere(self) -> Union[Sphere, None]:
        """Add a sphere at the origin.

        Returns
        -------
        :class:`Sphere`
            If the operation was successful
        None
            Otherwise
        """
        form = SphereForm()
        if form.exec_():
            radius = form.radius
            u = form.u
            v = form.v
            sphere = Sphere([0, 0, 0], radius)
            self.app.add(sphere, u=u, v=v)
            self.app.view.update()
            return sphere

    def add_torus(self) -> Union[Torus, None]:
        """Add a torus at the origin.

        Returns
        -------
        :class:`Torus`
            If the operation was successful
        None
            Otherwise
        """
        form = TorusForm()
        if form.exec_():
            radius = form.radius
            tube = form.tube
            u = form.u
            v = form.v
            torus = Torus(([0, 0, 0], [0, 0, 1]), radius, tube)
            self.app.add(torus, u=u, v=v)
            self.app.view.update()
            return torus

    # Actions: Networks

    def add_network_from_obj(self) -> Union[Network, None]:
        """Add a network from the data in an OBJ file.

        Returns
        -------
        :class:`Network`
            If the operation was successful
        None
            Otherwise
        """
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self.app.window,
                                                            caption="Select File",
                                                            dir="",
                                                            filter="OBJ Files (*.obj)")
        if filename:
            network = Network.from_obj(filename)
            self.app.add(network)
            self.app.view.update()
            return network

    # Actions: Meshes

    def add_mesh_from_file(self) -> Union[Mesh, None]:
        """Add a mesh from the data in an file.

        The following file formats are supported

        * OBJ
        * OFF
        * PLY
        * STL

        Returns
        -------
        :class:`Mesh`
            If the operation was successful
        None
            Otherwise
        """
        filepath, selectedfilter = QtWidgets.QFileDialog.getOpenFileName(
            parent=self.app.window,
            caption="Select File",
            dir="",
            filter="Mesh Files (*.obj, *.off, *.ply, *.stl)")

        if filepath:
            path = Path(filepath)

            if path.suffix == '.obj':
                mesh = Mesh.from_obj(path)
            elif path.suffix == '.off':
                mesh = Mesh.from_off(path)
            elif path.suffix == '.ply':
                mesh = Mesh.from_ply(path)
            elif path.suffix == '.stl':
                mesh = Mesh.from_stl(path)

            self.app.add(mesh)
            self.app.view.update()
            return mesh
