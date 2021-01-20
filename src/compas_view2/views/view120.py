from typing import Tuple
from OpenGL import GL

from PySide2 import QtCore, QtWidgets

from ..shaders import Shader
from .view import View

import numpy as np


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
        # 1. bind the program for all shapes and meshes
        # loop over objects
        # check types and draw if appropriate
        # 2. bind program for primitives
        # loop over objects
        # check types and draw if appropriate
        # 3. bind program for ...
        # ...
        if self.enable_paint_instances:
            self.paint_instances()

        self.shader.bind()
        self.shader.uniform4x4("viewworld", self.camera.viewworld())
        for guid in self.objects:
            obj = self.objects[guid]
            obj.draw(self.shader)
        self.shader.release()

    def paint_instances(self):
        self.shader.bind()
        self.shader.uniform4x4("viewworld", self.camera.viewworld())
        for guid in self.objects:
            obj = self.objects[guid]
            if hasattr(obj, "draw_instance"):
                obj.draw_instance(self.shader)
        self.shader.release()

        r = self.devicePixelRatio()
        instance_buffer = GL.glReadPixels(0, 0, self.app.width*r, self.app.height*r, GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
        instance_map = np.frombuffer(instance_buffer, dtype=np.uint8).reshape(self.app.height*r, self.app.width*r, 3)
        instance_map = instance_map[::-r, ::r, :]

        self.clear()

        x = self.mouse.last_pos.x()
        y = self.mouse.last_pos.y()
        obj = self.app.selector.find(x, y, instance_map)
        self.app.selector.select(obj)

         # Disable painting instances until next mouse click
        self.enable_paint_instances = False
