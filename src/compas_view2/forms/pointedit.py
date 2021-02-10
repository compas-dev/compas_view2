from .editform import EditForm


class PointEditForm(EditForm):

    def __init__(self, pointobject, on_update=None):
        super().__init__("Edit Point", on_update=on_update)
        self.map_number(pointobject._data, 'x')
        self.map_number(pointobject._data, 'y')
        self.map_number(pointobject._data, 'z')
