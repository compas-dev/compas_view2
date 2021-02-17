# import ctypes as ct
# from OpenGL import GL

from .bufferobject import BufferObject
# from ..forms import PointEditForm


class PointObject(BufferObject):
    """Object for displaying COMPAS point geometry."""

    def __init__(self, data, name=None, is_selected=False, color=None, size=10):
        super().__init__(data, name=name, is_selected=is_selected, show_points=True, pointsize=size)
        self.color = color

    def _points_data(self):
        positions = [self._data]
        colors = [self.color or self.default_color_points]
        elements = [[0]]
        return positions, colors, elements

    # def edit(self, on_update=None):
    #     self.editform = PointEditForm(self, on_update=on_update)
    #     self.editform.show()

    # def update(self):
    #     data = list(self._data)
    #     n = len(data)
    #     size = n * ct.sizeof(ct.c_float)
    #     data = (ct.c_float * n)(* data)
    #     GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._points['positions'])
    #     GL.glBufferSubData(GL.GL_ARRAY_BUFFER, 0, size, data)
    #     GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
