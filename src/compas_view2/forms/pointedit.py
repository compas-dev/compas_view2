from .editform import EditForm


class PointEditForm(EditForm):

    def __init__(self, point):
        super().__init__(title='Edit Point')
        self.map_number(point, 'x')
        self.map_number(point, 'y')
        self.map_number(point, 'z')
