from .bufferobject import BufferObject
import freetype as ft
from OpenGL import GL
import numpy as np
import os
from compas_view2 import DATA


class TextObeject(BufferObject):
    """Object for displaying COMPAS point geometry."""

    def __init__(self, data, name=None, is_selected=False, color=None, height=10):
        super().__init__(data, name=name, is_selected=is_selected, show_texts=True)
        self.color = color or [0, 0, 0]
        self.characters = []
        self.buffers = []
        self.height = height

    def init(self):
        self.make_buffers()
        self.make_fonts()

    def make_fonts(self):
        # change the filename if necessary
        face = ft.Face(os.path.join(DATA, "FreeSans.ttf"))
        # the size is specified in 1/64 pixel
        face.set_char_size(48*64)

        text = self._data.text

        char_width = 48
        char_height = 80
        text_buffer = np.zeros(shape=(char_height, char_width*len(text)))

        # glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        # glActiveTexture(GL_TEXTURE0)

        for i, c in enumerate(text):
            if c == " ":
                continue
            face.load_char(c, ft.FT_LOAD_FLAGS['FT_LOAD_RENDER'])
            glyph = face.glyph
            bitmap = glyph.bitmap
            char = np.array(bitmap.buffer)
            char = char.reshape((bitmap.rows, bitmap.width))
            text_buffer[-char.shape[0]:, i*char_width: i*char_width+char.shape[1]] = char
            # print(char.shape)

        text_buffer = text_buffer.reshape((text_buffer.shape[0]*text_buffer.shape[1]))

        # create glyph texture
        texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_R8, char_width*len(text), char_height, 0, GL.GL_RED, GL.GL_UNSIGNED_BYTE, text_buffer)

        self.texture = texture

        # glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
        # glBindTexture(GL_TEXTURE_2D, 0)

    def _texts_data(self):
        positions = [self._data.position]
        colors = [self.color or self.default_color_points]
        elements = [[0]]
        return positions, colors, elements
