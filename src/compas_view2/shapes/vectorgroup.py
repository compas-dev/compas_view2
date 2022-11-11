from compas.geometry import Vector
from compas.geometry import Shape


class VectorGroup(Shape):
    def __init__(self, vectors, positions=None):
        super().__init__()
        print(vectors[0])
        self.vectors = [Vector(*v) for v in vectors]
        if positions:
            self.positions = [Vector(*p) for p in positions]
        else:
            self.positions = [Vector(0, 0, 0) for _ in range(len(vectors))]

    @property
    def data(self):
        return {
            "positions": [list(p) for p in self.positions],
            "vectors": [list(d) for d in self.vectors],
            "sizes": self.sizes,
            "colors": self.colors,
        }

    @data.setter
    def data(self, data):
        self.positions = [Vector(*p) for p in data["positions"]]
        self.vectors = [Vector(*d) for d in data["vectors"]]
        self.colors = data["colors"]
        self.sizes = data["sizes"]

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __repr__(self):
        return "VectorGroup[{}]".format(len(self.positions))

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_data(cls, data):
        vectorgroup = cls()
        vectorgroup.data = data
        return vectorgroup

    # ==========================================================================
    # methods
    # ==========================================================================
    def transform(self, transformation):
        for p in self.positions:
            p.transform(transformation)
        for d in self.vectors:
            d.transform(transformation)
