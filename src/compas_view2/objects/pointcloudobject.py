from .bufferobject import BufferObject


class PointcloudObject(BufferObject):
    """Object for displaying COMPAS point geometry.

    Parameters
    ----------
    data : :class: `compas.datastructures.Pointcloud`
        Pointcloud to be displayed.
    name : string
        Name of the object.
    is_selected : bool
        Whether the object is selected.
    color : list
        Float rgb color for point cloud.
    colors : list
        list of rgb colors for each points, length must equal to number of points.
        If provided, the `color` parameter will be ignored.
    size : float
        The point size to be drawn on screen.

    Attributes
    ----------
    colors : list
        list of point colors

    Raises
    -------
    ValueError
        If number of colors does not equal to number of points.

    """

    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        self.show_points = True

    def _points_data(self):
        positions = self._data
        colors = [self.pointcolors.get(i, self.pointcolor) for i in range(len(positions))]
        elements = [[i] for i in range(len(positions))]
        return positions, colors, elements
