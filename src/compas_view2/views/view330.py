from OpenGL import GL

from ..shaders import Shader
from .view120 import View120
import numpy as np


class View330(View120):
    """View widget for OpenGL 3.3 and GLSL 330 and above, with a Core Profile.
    """

    def init(self):
        # create the program
        self.shader = Shader(name="330/mesh")
        self.shader.bind()
        self.shader.uniform4x4("projection", self.camera.projection(self.app.width, self.app.height))
        self.shader.uniform4x4("viewworld", self.camera.viewworld())
        self.shader.uniform4x4("transform", np.identity(4))
        self.shader.uniform1i("is_selected", 0)
        self.shader.uniform1f("opacity", self.opacity)
        self.shader.uniform3f("selection_color", self.selection_color)
        self.shader.release()

        self.grid.init(shader=self.shader)
        # init the buffers
        for guid in self.objects:
            obj = self.objects[guid]
            obj.init(shader=self.shader)

    def paint_instances(self, cropped_box=None):
        if cropped_box is None:
            x, y, width, height = 0, 0, self.app.width, self.app.height
        else:
            x1, y1, x2, y2 = cropped_box
            x, y = min(x1, x2), self.app.height - max(y1, y2)
            width, height = abs(x1 - x2), abs(y1 - y2)
        for guid in self.objects:
            obj = self.objects[guid]
            if hasattr(obj, "draw_instance"):
                obj.draw_instance(self.shader, self.mode == "wireframe")
        # create map
        r = self.devicePixelRatio()
        instance_buffer = GL.glReadPixels(x*r, y*r, width*r, height*r, GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
        instance_map = np.frombuffer(instance_buffer, dtype=np.uint8).reshape(height*r, width*r, 3)
        instance_map = instance_map[::-r, ::r, :]
        return instance_map