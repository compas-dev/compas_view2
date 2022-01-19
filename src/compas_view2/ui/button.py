from PySide2 import QtWidgets


class Button:
    """Add a button to the sidebar.

    Parameters
    ----------
    parent : QtWidgets.QWidget
        The parent widget for the button.
    text : str
        The text label of the button.
    action : callable
        The action associated with the button.

    Returns
    -------
    None

    """

    def __init__(self,
                 app,
                 parent,
                 *,
                 text,
                 action):
        # HBox with 
        box = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        button = QtWidgets.QPushButton(text)
        layout.addWidget(button)
        box.setLayout(layout)
        # add widget
        parent.addWidget(box)
        # connect
        button.clicked.connect(action)
        button.clicked.connect(app.view.update)
