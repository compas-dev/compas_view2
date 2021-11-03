from compas.geometry import Vector
from compas.geometry import Shape


__all__ = ['Arrow2d']


class Arrow2d(Shape):

    def __init__(self, positions, directions):
        super().__init__()
        self.positions = [Vector(*p) for p in positions]
        self.directions = [Vector(*d) for d in directions]

    @property
    def data(self):
        """Returns the data dictionary that represents the Arrow.

        Returns
        -------
        dict
            The arrow data.

        """
        return {'positions': [list(p) for p in self.positions], 'directions': [list(d) for d in self.directions]}

    @data.setter
    def data(self, data):
        self.positions = [Vector(*p) for p in data['positions']]
        self.directions = [Vector(*d) for d in data['directions']]

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __repr__(self):
        return 'Arrow2D[]'.format(len(self.positions))

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_data(cls, data):
        """Construct a Arrow from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        Arrow
            The constructed arrow.

        Examples
        --------
        >>> from compas.geometry import Arrow
        >>> from compas.geometry import Vector
        >>> data = {'position': Vector(0, 0, 0), 'direction': Vector(0, 0, 1)}
        >>> arrow = Arrow.from_data(data)

        """
        arrow = cls()
        arrow.data = data
        return arrow

    # ==========================================================================
    # methods
    # ==========================================================================
    def transform(self, transformation):
        """Transform the Arrow.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the cone.

        """
        for p in self.positions:
            p.transform(transformation)
        for d in self.directions:
            d.transform(transformation)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod()
