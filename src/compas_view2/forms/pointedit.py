from .editform import EditForm


class PointEditForm(EditForm):
    """Form class for real-time editing of PointObjects

    Parameters
    ----------
    pointobject: :class:`compas_view2.objects.PointObject`
        The point object to be edited
    on_update: function
        the function to be called when object attributes are updated from the form
    """

    def __init__(self, pointobject, on_update=None):
        super().__init__("Edit Point", on_update=on_update)
        self.map_number(pointobject._data, 'x')
        self.map_number(pointobject._data, 'y')
        self.map_number(pointobject._data, 'z')
