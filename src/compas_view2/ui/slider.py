from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtGui import QIcon


class Slider:
    """Horizontal slider widget.

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

    """

    def __init__(self,
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
                 bgcolor=None):
        # row containing labels
        # ---------------------
        row1 = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        # the title label
        if title:
            title_label = QtWidgets.QLabel(str(title))
            layout.addWidget(title_label)
        layout.addStretch(1)
        # the label containing the current value
        value_label = QtWidgets.QLabel(str(value))
        layout.addWidget(value_label)
        # the label containing the value annotation
        if annotation:
            annotation_label = QtWidgets.QLabel(str(annotation))
            layout.addWidget(annotation_label)
        # margins
        layout.setContentsMargins(12, 6, 12, 0)  # left, top, right, bottom
        row1.setLayout(layout)
        if bgcolor:
            row1.setStyleSheet("background-color: {}".format(bgcolor.hex))
        # row containing slider
        # ---------------------
        row2 = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        slider = QtWidgets.QSlider()
        slider.setOrientation(QtCore.Qt.Horizontal)
        slider.setValue(value)
        slider.setMinimum(minval)
        slider.setMaximum(maxval)
        slider.setTickInterval(interval)
        slider.setSingleStep(step)
        slider.setStyleSheet("""
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
""")
        # connect actions
        slider.valueChanged.connect(lambda v: value_label.setText(str(v)))
        slider.valueChanged.connect(self)
        slider.valueChanged.connect(app.view.update)
        # slider.sliderReleased.connect(action)
        slider.sliderReleased.connect(app.view.update)
        # add to layout
        layout.addWidget(slider)
        layout.setContentsMargins(12, 0, 12, 6)  # left, top, right, bottom
        row2.setLayout(layout)
        if bgcolor:
            row2.setStyleSheet("background-color: {}".format(bgcolor.hex))
        # combine rows in grid
        # --------------------
        grid = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        layout.setSpacing(0)
        layout.addWidget(row1, 0, 0)
        layout.addWidget(row2, 1, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        grid.setLayout(layout)
        # add to parent
        # -------------
        parent.addWidget(grid)
        self.action = action
        self.slider = slider

    def __call__(self, *args, **kwargs):
        return self.action(*args, **kwargs)
