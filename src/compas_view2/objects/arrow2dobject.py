from .object import Object
from .bufferobject import BufferObject
from compas_view2 import HOME

from OpenGL import GL
from ..buffers import make_index_buffer, make_vertex_buffer

import freetype as ft
import numpy as np
import os


class Arrow2dObject(Object):
    """Object for displaying text sprites."""

    def __init__(self, data, name=None, color=None, opacity=1):
        super().__init__(data, name=name)
        self.color = color or [0, 0, 0]
        self.opacity = opacity

    def init(self):
        self.make_buffers()
        self._update_matrix()

    def make_buffers(self):
        self._arrow_buffer = {
            'positions': make_vertex_buffer([0, 0, 0]),
            'directions': make_vertex_buffer([0, 0, 1]),
            'elements': make_index_buffer([0]),
            'n': 1
        }

    def draw(self, shader):
        # print('drawing arrow')
        """Draw the object from its buffers"""
        shader.enable_attribute('position')
        shader.enable_attribute('direction')
        shader.uniform4x4('transform', self.matrix)
        # shader.uniform1f('object_opacity', self.opacity)
        # shader.uniform3f('arrow_color', self.color)
        shader.bind_attribute('position', self._arrow_buffer['positions'])
        shader.bind_attribute('direction', self._arrow_buffer['directions'])
        # shader.draw_arrows(elements=self._arrow_buffer['elements'], n=self._arrow_buffer['n'])
        shader.draw_arrows(elements=self._arrow_buffer['elements'], n=self._arrow_buffer['n'])
        # shader.uniform1f('object_opacity', 1)
        shader.disable_attribute('position')
        shader.disable_attribute('direction')


        # shader.enable_attribute('position')
        # shader.enable_attribute('color')
        # shader.uniform3f('single_color', [1, 0, 0])
        # shader.uniform1i('use_single_color', True)
        # shader.bind_attribute('position', self._arrow_buffer['positions'])
        # shader.bind_attribute('color', self._arrow_buffer['directions'])
        # shader.draw_points(size=10, elements=self._arrow_buffer['elements'], n=self._arrow_buffer['n'], background=self.background)
        # shader.disable_attribute('position')
        # shader.disable_attribute('color')