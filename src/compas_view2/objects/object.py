import abc
from compas.geometry import Vector
from compas.geometry import Transformation
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import Scale
from compas.geometry import decompose_matrix


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
    translation : :class: `compas.geometry.Vector`
        The translation vector of the object.
    rotation : :class: `compas.geometry.Vector`
        The Euler rotation vector of the object in XYZ order.
    scale : :class: `compas.geometry.Vector`
        The scale vector of the object.
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
        return DATA_VIEW[data.__class__](data, **kwargs)

    def __init__(self, data, name=None, is_selected=False):
        self._data = data
        self.name = name
        self.is_selected = is_selected
        self._instance_color = None
        self._translation = Vector(0, 0, 0)
        self._rotation = Vector(0, 0, 0)
        self._scale = Vector(1, 1, 1)
        self._transformation = Transformation()

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
    def translation(self, data):
        self._translation.data = data

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, data):
        self._rotation.data = data

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, data):
        self._scale.data = data

    def _update_matrix(self):
        """Update the matrix from object's translation, rotation and scale"""
        T1 = Translation.from_vector(self.translation)
        R1 = Rotation.from_euler_angles(self.rotation)
        S1 = Scale.from_factors(self.scale)
        M = T1 * R1 * S1
        self._transformation.data = M.data

    @property
    def matrix(self):
        """Get the updated matrix from object's translation, rotation and scale"""
        self._update_matrix()
        return self._transformation.matrix

    @matrix.setter
    def matrix(self, matrix):
        """Set the object's translation, rotation and scale from given matrix, and update object's matrix"""
        scale, _, rotation, tranlation, _ = decompose_matrix(matrix)
        self.translation = tranlation
        self.rotation = rotation
        self.scale = scale
        self._update_matrix()
