import ctypes as ct
from OpenGL import GL


def make_vertex_buffer(data):
    n = len(data)
    size = n * ct.sizeof(ct.c_float)
    vbo = GL.glGenBuffers(1)
    data = (ct.c_float * n)(* data)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, size, data, GL.GL_STATIC_DRAW)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vbo


def make_index_buffer(data):
    n = len(data)
    size = n * ct.sizeof(ct.c_uint)
    vbo = GL.glGenBuffers(1)
    data = (ct.c_int * n)(* data)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, size, data, GL.GL_STATIC_DRAW)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    return vbo
