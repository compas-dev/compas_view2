from OpenGL import GL

from PySide2 import QtWidgets

from ..gl import gl_info
from ..forms import PointForm
from ..forms import LineForm
from ..forms import SphereForm
from ..forms import TorusForm
from .worker import Worker


class Controller:

    def __init__(self, app):
        self.app = app

    def about(self):
        self.app.statusbar.showMessage('Display about in text dialog.')

    def opengl_version(self):
        value = "OpenGL {}".format(
            GL.glGetString(GL.GL_VERSION).decode('ascii'))
        QtWidgets.QMessageBox.information(self.app.window, 'Info', value)

    def glsl_version(self):
        value = "GLSL {}".format(GL.glGetString(
            GL.GL_SHADING_LANGUAGE_VERSION).decode('ascii'))
        QtWidgets.QMessageBox.information(self.app.window, 'Info', value)

    # Actions: View

    def to_shaded(self):
        self.app.view.mode = 'shaded'

    def to_ghosted(self):
        self.app.view.mode = 'ghosted'

    # Actions: Scene

    def load_scene(self):
        pass

    def save_scene(self):
        pass

    def redraw_scene(self):
        pass

    def clear_scene(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass

    def history(self):
        pass

    def view_objects(self):
        pass

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

    # Actions: Primitives

    def add_point(self):
        from compas.geometry import Point
        form = PointForm()
        if form.exec_():
            x = form.x
            y = form.y
            z = form.z
            point = Point(x, y, z)
            self.app.add(point)

    def add_vector(self):
        pass

    def add_line(self):
        from compas.geometry import Point, Line
        form = LineForm()
        if form.exec_():
            Ax = form.Ax
            Ay = form.Ay
            Az = form.Az
            Bx = form.Bx
            By = form.By
            Bz = form.Bz
            show_points = form.show_points
            if Ax != Bx or Ay != By or Az != Bz:
                A = Point(Ax, Ay, Az)
                B = Point(Bx, By, Bz)
                line = Line(A, B)
                self.app.add(line, show_points=show_points)

    def add_circle(self):
        pass

    @interactive
    def add_line_from_selected_points(self):
        from compas.geometry import Point
        from compas.geometry import Line
        self.app.statusbar.showMessage(
            "Select points on screen, Click Enter to finish")
        points = self.app.selector.start_selection(types=[Point])
        if len(points) == 2:
            line = Line(*points)
            self.app.statusbar.showMessage("Line added")
            return line
        else:
            self.app.statusbar.showMessage("Must select 2 points")
            return None

    # Actions: Shapes

    def add_box(self):
        from compas.geometry import Box
        r = QtWidgets.QInputDialog.getDouble(
            self.app.window, 'Add Box', 'size', 1)
        if r[1] and r[0] > 0:
            size = r[0]
            box = Box.from_width_height_depth(size, size, size)
            self.app.add(box)

    def add_sphere(self):
        from compas.geometry import Sphere
        form = SphereForm()
        if form.exec_():
            radius = form.radius
            u = form.u
            v = form.v
            sphere = Sphere([0, 0, 0], radius)
            self.app.add(sphere, u=u, v=v)

    def add_torus(self):
        from compas.geometry import Torus
        form = TorusForm()
        if form.exec_():
            radius = form.radius
            tube = form.tube
            u = form.u
            v = form.v
            torus = Torus(([0, 0, 0], [0, 0, 1]), radius, tube)
            self.app.add(torus, u=u, v=v)

    # Actions: Networks

    def add_network_from_obj(self):
        pass

    # Actions: Meshes

    def add_mesh_from_obj(self):
        pass

    def add_mesh_from_off(self):
        pass

    def add_mesh_from_ply(self):
        pass

    def add_mesh_from_stl(self):
        pass
