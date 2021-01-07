from typing import Tuple
from OpenGL import GL

from PySide2 import QtCore, QtWidgets

from ..shaders import Shader
from .view import View


class View120(View):
    """View widget for OpenGL version 2.1 and GLSL 120 with a Compatibility Profile.
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
