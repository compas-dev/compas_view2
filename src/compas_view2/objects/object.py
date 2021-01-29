import abc
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

DATA_VIEW = {}


class Object(ABC):
    """Base object."""

    @staticmethod
    def register(dtype, vtype):
        DATA_VIEW[dtype] = vtype

    @staticmethod
    def build(data, **kwargs):
        return DATA_VIEW[data.__class__](data, **kwargs)

    def __init__(self, data, name=None, is_selected=False):
        self._data = data
        self.name = name
        self.is_selected = is_selected
        self.instance_color = None

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
