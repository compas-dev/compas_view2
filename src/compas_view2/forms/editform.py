from PySide2 import QtWidgets

from .form import Form


class EditForm(Form):
    """Form class for real-time editing of objects

    Parameters
    ----------
    title: string
        The title of the form

    Attributes
    ----------
    on_update: function
        the function to be called when object attributes are updated from the form
    """

    def __init__(self, title, on_update=None):
        super().__init__(title)
        self.on_update = on_update

    def map_number(self, obj, attribute):
        """Map number input field to an object attribute

        Parameters
        ----------
        obj: compas_view2.objects.Object
            object to be edited
        attribute: string
            the name of attribute to be mapped

        Returns
        -------
        None
        """
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(attribute)
        _input = QtWidgets.QDoubleSpinBox()
        _input.setMinimum(float('-inf'))
        _input.setMaximum(float('inf'))
        _input.setValue(getattr(obj, attribute))
        layout.addWidget(label)
        layout.addWidget(_input)
        setattr(self, attribute + "_input", _input)

        def set_number(value):
            setattr(obj, attribute, value)
            if self.on_update:
                self.on_update()

        _input.valueChanged.connect(set_number)
        self._inputs.addLayout(layout)

    def map_color(self, obj, attribute):
        """Map color input field to an object attribute
        """
        raise NotImplementedError()

    def inputs(self):
        """Creates layout for input fields

        Returns
        -------
        QtWidgets.QVBoxLayout
        """
        return QtWidgets.QVBoxLayout()
