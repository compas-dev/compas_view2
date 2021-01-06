import numpy as np
from glumpy import app, gl, gloo, glm
from glumpy.geometry import colorcube
from glumpy.transforms import PVMProjection, Position, Trackball, PanZoom

from math import tan, cos, sin, radians

from compas.datastructures import Mesh
from compas.geometry import Box

from compas.geometry import Transformation, Translation, Rotation, Frame
from compas.geometry import normalize_vector, subtract_vectors, scale_vector, cross_vectors, dot_vectors

from compas.utilities import i_to_rgb
from compas.utilities import flatten


VSHADER = """
attribute vec3 position;
attribute vec3 color;

uniform vec4 colormask;
uniform int is_selected;
uniform float opacity;

uniform mat4 P;
uniform mat4 V;
uniform mat4 M;

varying vec4 vertex_color;

void main()
{
    if (is_selected == 1){
        vertex_color = vec4(1.0, 1.0, 0.0, opacity) * colormask;
    }
    else {
        vertex_color = vec4(color, opacity) * colormask;
    }

    gl_Position = P * V * M * vec4(position, 1.0);
}
"""

FSHADER = """
varying vec4 vertex_color;

void main()
{
    gl_FragColor = vertex_color;
}
"""


window = app.Window(width=800, height=500, title="Minimal Glumpy", color=(1, 1, 1, 1))


@window.event
def on_init():
    gl.glPolygonOffset(1.0, 1.0)
    gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
    gl.glEnable(gl.GL_CULL_FACE)
    gl.glCullFace(gl.GL_BACK)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glDepthFunc(gl.GL_LESS)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glEnable(gl.GL_POINT_SMOOTH)
    gl.glEnable(gl.GL_LINE_SMOOTH)
    gl.glEnable(gl.GL_POLYGON_SMOOTH)
    gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)
    gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_NICEST)


@window.event
def on_resize(width, height):
    program['P'] = glm.perspective(45.0, width / height, 0.1, 100.0)


@window.event
def on_draw(dt):
    global Rx, Rz
    window.clear()

    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, Rz, 0, 0, 1)
    glm.rotate(model, Rx, 1, 0, 0)
    glm.translate(model, 0, 0, -10)
    program['M'] = model

    program['colormask'] = [1.0, 1.0, 1.0, 1.0]
    program.draw(gl.GL_TRIANGLES, F)
    program['colormask'] = [0.0, 0.0, 0.0, 1.0]
    program.draw(gl.GL_LINES, E)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons):
    global Rx, Rz
    if buttons == 1:
        Rx += dy
        Rz += dx


box = Box.from_width_height_depth(1, 1, 1)
mesh = Mesh.from_shape(box)

vertices = []
edges = []
i = 0
for face in mesh.faces():
    a, b, c, d = mesh.face_coordinates(face)
    vertices.append(a)  # 0
    vertices.append(b)  # 1
    vertices.append(c)  # 2
    vertices.append(a)  # 3
    vertices.append(c)  # 4
    vertices.append(d)  # 5
    edges.append([i + 0, i + 1])
    edges.append([i + 1, i + 2])
    edges.append([i + 2, i + 5])
    edges.append([i + 5, i + 0])
    i += 6

program = gloo.Program(VSHADER, FSHADER)

V = np.zeros(len(vertices), dtype=[("position", np.float32, 3), ("color", np.float32, 3)])
F = np.array(list(range(len(vertices))), dtype=np.uint32)
E = np.array(list(flatten(edges)), dtype=np.uint32)

V["position"] = vertices
V["color"] = [(0.7, 0.7, 0.7)] * len(vertices)

V = V.view(gloo.VertexBuffer)
F = F.view(gloo.IndexBuffer)
E = E.view(gloo.IndexBuffer)

view = np.eye(4, dtype=np.float32)
model = np.eye(4, dtype=np.float32)
projection = np.eye(4, dtype=np.float32)

program['position'] = V['position']
program['color'] = V['color']

program['P'] = projection
program['V'] = view
program['M'] = model

program['is_selected'] = 1
program['opacity'] = 1.0

Rx = -60
Rz = -30

app.run()

