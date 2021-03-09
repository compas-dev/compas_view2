from compas.utilities import flatten
from ..buffers import make_index_buffer, make_vertex_buffer, update_vertex_buffer, update_index_buffer
from .object import Object
import numpy as np


class BufferObject(Object):
    """A shared object to handle GL buffer creation and drawings

    Attributes
    ----------
    show_points : bool
        Whether to show points/vertices of the object
    show_lines : bool
        Whether to show lines/edges of the object
    show_faces : bool
        Whether to show faces of the object
    linewidth : int
        The line width to be drawn on screen
    pointsize : int
        The point size to be drawn on screen
    """

    default_color_points = [0.2, 0.2, 0.2]
    default_color_lines = [0.4, 0.4, 0.4]
    default_color_frontfaces = [0.8, 0.8, 0.8]
    default_color_backfaces = [0.8, 0.8, 0.8]

    def __init__(self, data, name=None, is_selected=False, show_points=False,
                 show_lines=False, show_faces=False, linewidth=1, pointsize=10, opacity=1):
        super().__init__(data, name=name, is_selected=is_selected)
        self._data = data
        self.show_points = show_points
        self.show_lines = show_lines
        self.show_faces = show_faces
        self.linewidth = linewidth
        self.pointsize = pointsize
        self.opacity = opacity
        self.background = False

    def make_buffer_from_data(self, data):
        """Create buffers from point/line/face data.

        Parameters
        ----------
        data: tuple
            Contains positions, colors, elements for the buffer

        Returns
        -------
        buffer_dict
           A dict with created buffer indexes
        """
        positions, colors, elements = data
        return {
                'positions': make_vertex_buffer(list(flatten(positions))),
                'colors': make_vertex_buffer(list(flatten(colors))),
                'elements': make_index_buffer(list(flatten(elements))),
                'n': len(positions)
            }

    def update_buffer_from_data(self, data, buffer, update_positions=True, update_colors=True, update_elements=True):
        """Update existing buffers from point/line/face data.

        Parameters
        ----------
        data: tuple
            Contains positions, colors, elements for the buffer
        buffer: dict
            The dict with created buffer indexes
        update_positions : bool
            Whether to update positions in the buffer dict
        update_colors : bool
            Whether to update colors in the buffer dict
        update_elements : bool
            Whether to update elements in the buffer dict
        """
        positions, colors, elements = data
        if update_positions:
            update_vertex_buffer(list(flatten(positions)), buffer["positions"])
        if update_colors:
            update_vertex_buffer(list(flatten(colors)), buffer["colors"])
        if update_elements:
            update_index_buffer(list(flatten(elements)), buffer["elements"])
        buffer["n"] = len(positions)

    def make_buffers(self):
        """Create all buffers from object's data"""
        if hasattr(self, '_points_data'):
            self._points_buffer = self.make_buffer_from_data(self._points_data())
        if hasattr(self, '_lines_data'):
            self._lines_buffer = self.make_buffer_from_data(self._lines_data())
        if hasattr(self, '_frontfaces_data'):
            self._frontfaces_buffer = self.make_buffer_from_data(self._frontfaces_data())
        if hasattr(self, '_backfaces_data'):
            self._backfaces_buffer = self.make_buffer_from_data(self._backfaces_data())

    def update_buffers(self):
        """Update all buffers from object's data"""
        if hasattr(self, '_points_data'):
            self.update_buffer_from_data(self._points_data(), self._points_buffer)
        if hasattr(self, '_lines_data'):
            self.update_buffer_from_data(self._lines_data(), self._lines_buffer)
        if hasattr(self, '_frontfaces_data'):
            self.update_buffer_from_data(self._frontfaces_data(), self._frontfaces_buffer)
        if hasattr(self, '_backfaces_data'):
            self.update_buffer_from_data(self._backfaces_data(), self._backfaces_buffer)

    def init(self):
        """Initialize the object"""
        self.make_buffers()

    def update(self):
        """Update the object"""
        self._update_matrix()
        self.update_buffers()

    def draw(self, shader, wireframe=False, is_lighted=False):
        """Draw the object from its buffers"""
        shader.enable_attribute('position')
        shader.enable_attribute('color')
        shader.uniform1i('is_selected', self.is_selected)
        if self._matrix_buffer is not None:
            shader.uniform4x4('transform', self._matrix_buffer)
        shader.uniform1i('is_lighted', is_lighted)
        shader.uniform1f('object_opacity', self.opacity)
        if hasattr(self, "_frontfaces_buffer") and self.show_faces and not wireframe:
            shader.bind_attribute('position', self._frontfaces_buffer['positions'])
            shader.bind_attribute('color', self._frontfaces_buffer['colors'])
            shader.draw_triangles(elements=self._frontfaces_buffer['elements'], n=self._frontfaces_buffer['n'], background=self.background)
        if hasattr(self, "_backfaces_buffer") and self.show_faces and not wireframe:
            shader.bind_attribute('position', self._backfaces_buffer['positions'])
            shader.bind_attribute('color', self._backfaces_buffer['colors'])
            shader.draw_triangles(elements=self._backfaces_buffer['elements'], n=self._backfaces_buffer['n'], background=self.background)
        shader.uniform1i('is_lighted', False)
        if self.show_faces and not wireframe:
            # skip coloring lines and points if faces are already highlighted
            shader.uniform1i('is_selected', 0)
        if hasattr(self, "_lines_buffer") and (self.show_lines or wireframe):
            shader.bind_attribute('position', self._lines_buffer['positions'])
            shader.bind_attribute('color', self._lines_buffer['colors'])
            shader.draw_lines(width=self.linewidth, elements=self._lines_buffer['elements'], n=self._lines_buffer['n'], background=self.background)
        if hasattr(self, "_points_buffer") and self.show_points:
            shader.bind_attribute('position', self._points_buffer['positions'])
            shader.bind_attribute('color', self._points_buffer['colors'])
            shader.draw_points(size=self.pointsize, elements=self._points_buffer['elements'], n=self._points_buffer['n'], background=self.background)
        shader.uniform1i('is_selected', 0)
        shader.uniform1f('object_opacity', 1)
        if self._matrix_buffer is not None:
            shader.uniform4x4('transform', np.identity(4).flatten())
        shader.disable_attribute('position')
        shader.disable_attribute('color')

    def draw_instance(self, shader, wireframe=False):
        """Draw the object instance for picking"""
        shader.enable_attribute('position')
        shader.enable_attribute('color')
        shader.uniform1i('is_instance_mask', 1)
        shader.uniform3f('instance_color', self._instance_color)
        if self._matrix_buffer is not None:
            shader.uniform4x4('transform', self._matrix_buffer)
        if hasattr(self, "_points_buffer") and self.show_points:
            shader.bind_attribute('position', self._points_buffer['positions'])
            shader.draw_points(size=self.pointsize, elements=self._points_buffer['elements'], n=self._points_buffer['n'])
        if hasattr(self, "_lines_buffer") and (self.show_lines or wireframe):
            shader.bind_attribute('position', self._lines_buffer['positions'])
            shader.draw_lines(width=self.linewidth, elements=self._lines_buffer['elements'], n=self._lines_buffer['n'])
        if hasattr(self, "_frontfaces_buffer") and self.show_faces and not wireframe:
            shader.bind_attribute('position', self._frontfaces_buffer['positions'])
            shader.draw_triangles(elements=self._frontfaces_buffer['elements'], n=self._frontfaces_buffer['n'])
            shader.bind_attribute('position', self._backfaces_buffer['positions'])
            shader.draw_triangles(elements=self._backfaces_buffer['elements'], n=self._backfaces_buffer['n'])
        if self._matrix_buffer is not None:
            shader.uniform4x4('transform', np.identity(4).flatten())
        shader.uniform1i('is_instance_mask', 0)
        shader.uniform3f('instance_color', [0, 0, 0])
        shader.disable_attribute('color')
        shader.disable_attribute('position')
