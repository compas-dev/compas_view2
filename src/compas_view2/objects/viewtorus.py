from compas.datastructures import Mesh

from .viewshape import ViewShape


class ViewTorus(ViewShape):

    default_color_vertices = [0.2, 0.2, 0.2]
    default_color_edges = [0.4, 0.4, 0.4]
    default_color_front = [0.8, 0.8, 0.8]
    default_color_back = [0.8, 0.8, 0.8]

    def __init__(self, data, *args, u=16, v=16, **kwargs):
        super().__init__(data, *args, **kwargs)
        self._u = u
        self._v = v
        self._mesh = Mesh.from_shape(data, u=u, v=v)
