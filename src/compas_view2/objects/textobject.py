import os
import numpy as np
import freetype as ft
from OpenGL import GL

from compas_view2.gl import make_index_buffer
from compas_view2.gl import make_vertex_buffer

from .object import Object

here = os.path.dirname(__file__)
fonts = os.path.join(here, "..", "fonts")


class TextObject(Object):
    """Object for displaying text sprites."""

    def __init__(self, data, color=None, height=10, **kwargs):
        super().__init__(data, **kwargs)
        self.color = color or [0, 0, 0]
        self.characters = []
        self.buffers = []
        self.height = height

    def init(self):
        self.make_buffers()

    def make_buffers(self):
        self._text_buffer = {
            "positions": make_vertex_buffer(self._data.position),
            "elements": make_index_buffer([0]),
            "text_texture": self.make_text_texture(),
            "n": 1,
        }

    def make_text_texture(self):
        # change the filename if necessary
        face = ft.Face(os.path.join(fonts, "FreeSans.ttf"))

        char_width = 48
        char_height = 80
        # the size is specified in 1/64 pixel
        face.set_char_size(64 * char_width)

        text = self._data.text
        string_buffer = np.zeros(shape=(char_height, char_width * len(text)))

        for i, c in enumerate(text):
            if c == " ":
                continue
            face.load_char(c, ft.FT_LOAD_FLAGS["FT_LOAD_RENDER"])
            glyph = face.glyph
            bitmap = glyph.bitmap
            char = np.array(bitmap.buffer)
            char = char.reshape((bitmap.rows, bitmap.width))
            string_buffer[-char.shape[0] :, i * char_width : i * char_width + char.shape[1]] = char

        string_buffer = string_buffer.reshape((string_buffer.shape[0] * string_buffer.shape[1]))

        # create glyph texture
        texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_R8,
            char_width * len(text),
            char_height,
            0,
            GL.GL_RED,
            GL.GL_UNSIGNED_BYTE,
            string_buffer,
        )
        return texture

    def draw(self, shader):
        """Draw the object from its buffers"""
        shader.enable_attribute("position")
        shader.uniform4x4("transform", self.matrix)
        shader.uniform1f("object_opacity", self.opacity)
        shader.uniform1i("text_height", self._data.height)
        shader.uniform1i("text_num", len(self._data.text))
        shader.uniform3f("text_color", self.color)
        shader.uniformTex("text_texture", self._text_buffer["text_texture"])
        shader.bind_attribute("position", self._text_buffer["positions"])
        shader.draw_texts(elements=self._text_buffer["elements"], n=self._text_buffer["n"])
        shader.uniform1i("is_text", 0)
        shader.uniform1f("object_opacity", 1)
        shader.disable_attribute("position")
