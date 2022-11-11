from qtpy import QtWidgets


class Button:
    """Class representing a button wrapped in a horizontal box layout.

    Parameters
    ----------
    app : :class:`compas_view2.app.App`
        The app containing the widget.
    parent : QtWidgets.QWidget
        The parent widget for the button.
    text : str
        The text label of the button.
    action : callable
        The action associated with the button.

    Attributes
    ----------
    action : callable
        Action associated with the button click event.
    button : QtWidgets.QPushButton
        The actual button widget.

    """

    def __init__(self, app, parent, *, text, action):
        box = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        box.setLayout(layout)
        button = QtWidgets.QPushButton(text)
        layout.addWidget(button)
        parent.addWidget(box)
        # connect
        button.clicked.connect(action)
        button.clicked.connect(app.view.update)
        # attributes
        self.action = action
        self.button = button

    def __call__(self, *args, **kwargs):
        """Wrapper for the action associated with the checkbox.

        Returns
        -------
        None

        """
        return self.action()
