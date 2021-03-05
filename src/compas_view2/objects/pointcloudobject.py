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

    def __init__(self, data, name=None, is_selected=False, color=None, colors=None, size=10):
        super().__init__(data, name=name, is_selected=is_selected, show_points=True, pointsize=size)
        self.colors = colors or [color or self.default_color_points] * len(data)
        if len(self.colors) != len(data):
            raise ValueError("Number of colors must equal to number of points")

    def _points_data(self):
        positions = self._data
        colors = self.colors
        elements = [[i] for i in range(len(positions))]
        return positions, colors, elements
