import abc
from compas.geometry import Transformation
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import Scale
from compas.geometry import decompose_matrix
import numpy as np


ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

DATA_VIEW = {}


class Object(ABC):
    """Base object for compas_view2

    Attributes
    ----------
    name : str
        The name of the object.
    is_selected : bool
        Whether the object is selected.
    translation : list
        The translation vector of the object.
    rotation : list
        The Euler rotation of the object in XYZ order.
    scale : list
        The scale factor of the object.
    matrix: list
        The 4x4 transformation matrix that is composed from translation, rotation and scale.
    """

    @staticmethod
    def register(dtype, vtype):
        """Register an object class to its corrensponding data type"""
        DATA_VIEW[dtype] = vtype

    @staticmethod
    def build(data, **kwargs):
        """Build an object class according to its corrensponding data type"""
        try:
            obj = DATA_VIEW[data.__class__](data, **kwargs)
        except KeyError:
            raise TypeError("Type {} is not supported by the viewer.".format(type(data)))
        return obj

    def __init__(self, data, name=None, is_selected=False):
        self._data = data
        self.name = name
        self.is_selected = is_selected
        self._instance_color = None
        self._translation = [0, 0, 0]
        self._rotation = [0, 0, 0]
        self._scale = [1, 1, 1]
        self._transformation = Transformation()
        self._matrix_buffer = None

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def draw(self, shader):
        pass

    def create(self):
        pass

    def edit(self):
        pass

    @property
    def translation(self):
        return self._translation

    @translation.setter
    def translation(self, vector):
        self._translation[0] = vector[0]
        self._translation[1] = vector[1]
        self._translation[2] = vector[2]

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, angles):
        self._rotation[0] = angles[0]
        self._rotation[1] = angles[1]
        self._rotation[2] = angles[2]

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, factors):
        self._scale[0] = factors[0]
        self._scale[1] = factors[1]
        self._scale[2] = factors[2]

    def _update_matrix(self):
        """Update the matrix from object's translation, rotation and scale"""
        T1 = Translation.from_vector(self.translation)
        R1 = Rotation.from_euler_angles(self.rotation)
        S1 = Scale.from_factors(self.scale)
        M = T1 * R1 * S1
        self._transformation.matrix = M.matrix
        self._matrix_buffer = np.array(self.matrix).flatten()

    @property
    def matrix(self):
        """Get the updated matrix from object's translation, rotation and scale"""
        return self._transformation.matrix

    @matrix.setter
    def matrix(self, matrix):
        """Set the object's translation, rotation and scale from given matrix, and update object's matrix"""
        scale, _, rotation, tranlation, _ = decompose_matrix(matrix)
        self.translation = tranlation
        self.rotation = rotation
        self.scale = scale
        self._update_matrix()
