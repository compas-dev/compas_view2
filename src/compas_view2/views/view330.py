from ..shaders import Shader
from .view import View


class View330(View):
    """View widget for OpenGL 3.3 and GLSL 330 and above, with a Core Profile.
    """

    def init(self):
        # init the buffers
        for guid in self.objects:
            obj = self.objects[guid]
            obj.init()
        # create the program
        self.shader = Shader()
        self.shader.bind()
        self.shader.uniform4x4(
            "projection", self.camera.projection(self.app.width, self.app.height))
        self.shader.uniform4x4("viewworld", self.camera.viewworld())
        self.shader.uniform1i("is_selected", 0)
        self.shader.uniform1f("opacity", self.opacity)
        self.shader.uniform3f("selection_color", self.selection_color)
        self.shader.release()

    def resize(self, w: int, h: int):
        self.shader.bind()
        self.shader.uniform4x4("projection", self.camera.projection(w, h))
        self.shader.release()

    def paint(self):
        self.shader.bind()
        self.shader.uniform4x4("viewworld", self.camera.viewworld())
        for guid in self.objects:
            obj = self.objects[guid]
            obj.draw(self.shader)
        self.shader.release()
