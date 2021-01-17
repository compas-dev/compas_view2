from OpenGL import GL

from PySide2 import QtWidgets

from ..gl import gl_info
from ..forms.sphere import SphereForm
from ..forms.torus import TorusForm


class Controller:

    def __init__(self, app):
        self.app = app

    def about(self):
        self.app.statusbar.showMessage('Display about in text dialog.')

    def opengl_version(self):
        value = "OpenGL {}".format(GL.glGetString(GL.GL_VERSION).decode('ascii'))
        QtWidgets.QMessageBox.information(self.app.window, 'Info', value)

    def glsl_version(self):
        value = "GLSL {}".format(GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode('ascii'))
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

    # Actions: Primitives

    def add_point(self):
        pass

    def add_vector(self):
        pass

    def add_line(self):
        pass

    def add_circle(self):
        pass

    # Actions: Shapes

    def add_box(self):
        from compas.geometry import Box
        r = QtWidgets.QInputDialog.getDouble(self.app.window, 'Add Box', 'size', 1)
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
