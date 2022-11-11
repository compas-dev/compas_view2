from qtpy import QtCore
from qtpy import QtWidgets


class Slider:
    """Class representing a horizontal slider wrapped in a grid layout with two rows.

    Parameters
    ----------
    app : :class:`compas_view2.app.App`
        The app containing the widget.
    parent : QtWidget
        The parent widget.
    action : callable
        The callback connected to the slide action.
    value : int, optional
        The initial value of the slider.
    minval : int, optional
        The minimum value of the sliding range.
    maxval : int, optional
        The maximum value of the sliding range.
    step : int, optional
        Size of value increments.
    title : str, optional
        Title label.
    annotation : str, optional
        Value annotation label.
    interval : int, optional
        The tick interval size.
    bgcolor : Color, optional
        Background color of the box containing the slider.

    Attributes
    ----------
    action : callable
        Action associated with the button click event.
    slider : QtWidgets.QSlider
        The actual slider widget.
    value : float
        The current value of the slider.

    Class Attributes
    ----------------
    STYLE : str
        Stylesheet for the visual appearance of the groove and handle of the slider.

    """

    STYLE = """
QSlider::groove::horizontal {
    border: 1px solid #cccccc;
    background-color: #eeeeee;
    height: 4px;
}
QSlider::handle:horizontal {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 6px;
    height: 12px;
    width: 12px;
    margin: -6px 0;
}
"""

    def __init__(
        self,
        app,
        parent,
        action,
        value=0,
        minval=0,
        maxval=100,
        step=1,
        title=None,
        annotation=None,
        interval=1,
        bgcolor=None,
    ):
        # row containing labels
        # with horizontal box layout
        row1 = QtWidgets.QWidget()
        if bgcolor:
            row1.setStyleSheet("background-color: {}".format(bgcolor.hex))
        row1_layout = QtWidgets.QHBoxLayout()
        row1_layout.setContentsMargins(12, 6, 12, 0)
        row1.setLayout(row1_layout)
        # the title label
        # if provided
        if title:
            row1_layout.addWidget(QtWidgets.QLabel(str(title)))
        # the label containing the current value
        # pushed to the right
        # and potentially with an annotation
        value_label = QtWidgets.QLabel(str(value))
        row1_layout.addStretch(1)
        row1_layout.addWidget(value_label)
        if annotation:
            row1_layout.addWidget(QtWidgets.QLabel(str(annotation)))
        # row containing slider
        row2 = QtWidgets.QWidget()
        if bgcolor:
            row2.setStyleSheet("background-color: {}".format(bgcolor.hex))
        row2_layout = QtWidgets.QHBoxLayout()
        row2_layout.setContentsMargins(12, 0, 12, 6)
        row2.setLayout(row2_layout)
        # slider
        slider = QtWidgets.QSlider()
        slider.setOrientation(QtCore.Qt.Horizontal)
        slider.setValue(value)
        slider.setMinimum(minval)
        slider.setMaximum(maxval)
        slider.setTickInterval(interval)
        slider.setSingleStep(step)
        slider.setStyleSheet(Slider.STYLE)
        row2_layout.addWidget(slider)
        # combine rows in grid
        grid = QtWidgets.QWidget()
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(0)
        grid_layout.addWidget(row1, 0, 0)
        grid_layout.addWidget(row2, 1, 0)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid.setLayout(grid_layout)
        parent.addWidget(grid)
        # connect slider to actions
        slider.valueChanged.connect(lambda v: value_label.setText(str(v)))
        slider.valueChanged.connect(self)
        slider.valueChanged.connect(app.view.update)
        slider.sliderReleased.connect(app.view.update)
        # define attributes
        self.action = action
        self.slider = slider

    def __call__(self, *args, **kwargs):
        """Wrapper for the action associated with the slider.

        Returns
        -------
        None

        """
        return self.action(*args, **kwargs)

    @property
    def value(self):
        return self.slider.value()

    @value.setter
    def value(self, value):
        self.slider.setValue(value)
