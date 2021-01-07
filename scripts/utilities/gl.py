from OpenGL import GL


def gl_info():
    info = """
        Vendor: {0}
        Renderer: {1}
        OpenGL Version: {2}
        Shader Version: {3}
        """.format(
        GL.glGetString(GL.GL_VENDOR),
        GL.glGetString(GL.GL_RENDERER),
        GL.glGetString(GL.GL_VERSION),
        GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION)
    )
    return info
