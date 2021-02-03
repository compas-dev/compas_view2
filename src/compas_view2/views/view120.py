from OpenGL import GL

from ..shaders import Shader
from .view import View

import numpy as np


class View120(View):
    """View widget for OpenGL version 2.1 and GLSL 120 with a Compatibility Profile.
    """

    def init(self):
        self.grid.init()
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

    def resize(self, w, h):
        self.shader.bind()
        self.shader.uniform4x4("projection", self.camera.projection(w, h))
        self.shader.release()

    def paint(self):
        self.shader.bind()
        if self.current != self.PERSPECTIVE:
            self.self.shader.uniform4x4("projection", self.camera.projection(self.app.width, self.app.height))
        self.shader.uniform4x4("viewworld", self.camera.viewworld())
        if self.app.selector.enabled:
            if self.app.selector.select_from == "pixel":
                self.app.selector.instance_map = self.paint_instances()
            if self.app.selector.select_from == "box":
                self.app.selector.instance_map = self.paint_instances(self.app.selector.box_select_coords)
            self.app.selector.enabled = False
            self.clear()
        if self.show_grid:
            self.grid.draw(self.shader)
        for guid in self.objects:
            obj = self.objects[guid]
            obj.draw(self.shader)
        if self.app.selector.select_from == "box":
            self.shader.draw_2d_box(self.app.selector.box_select_coords, self.app.width, self.app.height)
        self.shader.release()

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
                obj.draw_instance(self.shader)
        # create map
        r = self.devicePixelRatio()
        instance_buffer = GL.glReadPixels(
            x*r, y*r, width*r, height*r, GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
        instance_map = np.frombuffer(
            instance_buffer, dtype=np.uint8).reshape(height*r, width*r, 3)
        instance_map = instance_map[::-r, ::r, :]
        return instance_map
