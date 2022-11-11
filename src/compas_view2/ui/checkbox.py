from qtpy import QtWidgets
from qtpy import QtCore


class Checkbox:
    """Add a checkbox.

    Parameters
    ----------
    app : :class:`compas_view2.app.App`
        The app containing the widget.
    parent : QtWidgets.QWidget
        The parent widget for the checkbox.
    text : str
        The text label of the checkbox.
    action : callable
        The action associated with the checkox.
    checked : bool, optional
        If True, the checkbox will be displayed as checked.

    Attributes
    ----------
    checkbox : QtWidgets.QCheckBox
        The actual checkbox widget.
    action : callable
        The action associated with the toggle event of the checkbox.

    """

    def __init__(self, app, parent, *, text, action, checked=False):

        box = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        checkbox = QtWidgets.QCheckBox(text)
        checkbox.setCheckState(QtCore.Qt.CheckState.Checked if checked else QtCore.Qt.CheckState.Unchecked)
        layout.addWidget(checkbox)
        box.setLayout(layout)
        parent.addWidget(box)
        # connect actions
        checkbox.toggled.connect(self)
        checkbox.toggled.connect(app.view.update)
        # identify attributes
        self.checkbox = checkbox
        self.action = action

    def __call__(self, *args, **kwargs):
        """Wrapper for the action associated with the checkbox.

        Returns
        -------
        None

        """
        self.action(args[0])
