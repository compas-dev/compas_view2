from OpenGL import GL
from PIL import Image

from ..shaders import Shader
from .view import View

import numpy as np
from ..objects.bufferobject import BufferObject
from ..objects.textobject import TextObject

from compas.geometry import transform_points_numpy


class View120(View):
    """View widget for OpenGL version 2.1 and GLSL 120 with a Compatibility Profile.
    """

    def init(self):
        self.grid.init()
        # init the buffers
        for guid in self.objects:
            obj = self.objects[guid]
            obj.init()

        projection = self.camera.projection(self.app.width, self.app.height)
        viewworld = self.camera.viewworld()
        transform = np.identity(4)
        # create the program
        self.shader_model = Shader(name='120/model')
        self.shader_model.bind()
        self.shader_model.uniform4x4("projection", projection)
        self.shader_model.uniform4x4("viewworld", viewworld)
        self.shader_model.uniform4x4("transform", transform)
        self.shader_model.uniform1i("is_selected", 0)
        self.shader_model.uniform1f("opacity", self.opacity)
        self.shader_model.uniform3f("selection_color", self.selection_color)
        self.shader_model.release()

        self.shader_text = Shader(name='120/text')
        self.shader_text.bind()
        self.shader_text.uniform4x4("projection", projection)
        self.shader_text.uniform4x4("viewworld", viewworld)
        self.shader_text.uniform4x4("transform", transform)
        self.shader_text.uniform1f("opacity", self.opacity)
        self.shader_text.release()

        self.shader_instance = Shader(name='120/instance')
        self.shader_instance.bind()
        self.shader_instance.uniform4x4("projection", projection)
        self.shader_instance.uniform4x4("viewworld", viewworld)
        self.shader_instance.uniform4x4("transform", transform)
        self.shader_instance.release()

        self.shader_grid = Shader(name='120/grid')
        self.shader_grid.bind()
        self.shader_grid.uniform4x4("projection", projection)
        self.shader_grid.uniform4x4("viewworld", viewworld)
        self.shader_grid.uniform4x4("transform", transform)
        self.shader_grid.release()

    def update_projection(self, w=None, h=None):
        w = w or self.app.width
        h = h or self.app.height

        projection = self.camera.projection(w, h)
        self.shader_model.bind()
        self.shader_model.uniform4x4("projection", projection)
        self.shader_model.release()

        self.shader_text.bind()
        self.shader_text.uniform4x4("projection", projection)
        self.shader_text.release()

        self.shader_instance.bind()
        self.shader_instance.uniform4x4("projection", projection)
        self.shader_instance.release()

        self.shader_grid.bind()
        self.shader_grid.uniform4x4("projection", projection)
        self.shader_grid.release()

    def resize(self, w, h):
        self.update_projection(w, h)

    def sort_objects_from_viewworld(self, viewworld):
        """Sort objects by the distances from their bounding box centers to camera location"""
        opaque_objects = []
        transparent_objects = []
        centers = []
        for guid in self.objects:
            obj = self.objects[guid]
            if isinstance(obj, BufferObject):
                if obj.opacity * self.opacity < 1:
                    transparent_objects.append(obj)
                    centers.append(transform_points_numpy([obj.bounding_box_center], obj.matrix)[0])
                else:
                    opaque_objects.append(obj)
        if transparent_objects:
            centers = transform_points_numpy(centers, viewworld)
            transparent_objects = sorted(zip(transparent_objects, centers), key=lambda pair: pair[1][2])
            transparent_objects, _ = (zip(*transparent_objects))
        return opaque_objects + list(transparent_objects)

    def paint(self):
        viewworld = self.camera.viewworld()
        if self.current != self.PERSPECTIVE:
            self.update_projection()

        # Draw instance maps
        if self.app.selector.enabled:
            self.shader_instance.bind()
            # set projection matrix
            self.shader_instance.uniform4x4("viewworld", viewworld)
            if self.app.selector.select_from == "pixel":
                self.app.selector.instance_map = self.paint_instances()
            if self.app.selector.select_from == "box":
                self.app.selector.instance_map = self.paint_instances(self.app.selector.box_select_coords)
            self.app.selector.enabled = False
            self.clear()
            self.shader_model.release()

        # Draw grid
        self.shader_grid.bind()
        self.shader_grid.uniform4x4("viewworld", viewworld)
        if self.app.selector.wait_for_selection_on_plane:
            self.app.selector.uv_plane_map = self.paint_plane()
            self.clear()
        if self.show_grid:
            self.grid.draw(self.shader_grid)
        self.shader_grid.release()

        # Draw model objects in the scene
        self.shader_model.bind()
        self.shader_model.uniform4x4("viewworld", viewworld)
        for obj in self.sort_objects_from_viewworld(viewworld):
            if obj.visible:
                obj.draw(self.shader_model, self.mode == "wireframe", self.mode == "lighted")
        self.shader_model.release()

        # draw text sprites
        self.shader_text.bind()
        self.shader_text.uniform4x4("viewworld", viewworld)
        for guid in self.objects:
            obj = self.objects[guid]
            if isinstance(obj, TextObject):
                if obj.visible:
                    obj.draw(self.shader_text)
        self.shader_text.release()

        # draw 2D box for multi-selection
        if self.app.selector.select_from == "box":
            self.shader_model.draw_2d_box(self.app.selector.box_select_coords, self.app.width, self.app.height)

        if self.app.record:
            r = self.devicePixelRatio()
            x, y, width, height = 0, 0, self.app.width, self.app.height
            buffer = GL.glReadPixels(x*r, y*r, width*r, height*r, GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
            arr = np.frombuffer(buffer, dtype=np.uint8).reshape(height*r, width*r, 3)
            arr = arr[::-r, ::r, :]
            im = Image.fromarray(arr)
            print("recording frame:", self.app.frame_count)
            self.app.recorded_frames.append(im)

    def paint_instances(self, cropped_box=None):
        GL.glDisable(GL.GL_POINT_SMOOTH)
        GL.glDisable(GL.GL_LINE_SMOOTH)
        if cropped_box is None:
            x, y, width, height = 0, 0, self.app.width, self.app.height
        else:
            x1, y1, x2, y2 = cropped_box
            x, y = min(x1, x2), self.app.height - max(y1, y2)
            width, height = abs(x1 - x2), abs(y1 - y2)
        for guid in self.objects:
            obj = self.objects[guid]
            if hasattr(obj, "draw_instance"):
                if obj.visible:
                    obj.draw_instance(self.shader_instance, self.mode == "wireframe")
        # create map
        r = self.devicePixelRatio()
        instance_buffer = GL.glReadPixels(x*r, y*r, width*r, height*r, GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
        instance_map = np.frombuffer(instance_buffer, dtype=np.uint8).reshape(height*r, width*r, 3)
        instance_map = instance_map[::-r, ::r, :]
        GL.glEnable(GL.GL_POINT_SMOOTH)
        GL.glEnable(GL.GL_LINE_SMOOTH)
        return instance_map

    def paint_plane(self):
        x, y, width, height = 0, 0, self.app.width, self.app.height
        self.grid.draw_plane(self.shader_grid)
        r = self.devicePixelRatio()
        plane_uv_map = GL.glReadPixels(x*r, y*r, width*r, height*r, GL.GL_RGB, GL.GL_FLOAT)
        plane_uv_map = plane_uv_map.reshape(height*r, width*r, 3)
        plane_uv_map = plane_uv_map[::-r, ::r, :]
        return plane_uv_map
