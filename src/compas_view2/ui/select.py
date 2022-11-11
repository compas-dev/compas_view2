from qtpy import QtWidgets


class Select:
    """Class representing a selection list.

    Parameters
    ----------
    app : :class:`compas_view2.app.App`
        The app containing the widget.
    parent : QtWidgets.QWidget
        The parent widget for the combo box.
    items : list[dict[str, Any]]
        A list of selection options, with each item defined as a dict with a particular structure.
        See Notes for more info.
    action : callable
        The action associated with the combo box.

    Attributes
    ----------
    combo : QtWidgets.QComboBox
        The combo box containing the selection options.
    action : callable
        The action associated with the index change event of the combo box.

    Notes
    -----
    Every `item` dict should have the following structure.

    .. code-block:: python

        item['text']     # str  : The text label of the item.

    """

    def __init__(self, app, parent, *, items, action):

        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        combo = QtWidgets.QComboBox()
        for item in items:
            combo.addItem(item["text"])
        layout.addWidget(combo)
        container.setLayout(layout)
        parent.addWidget(container)
        combo.currentIndexChanged.connect(self)
        combo.currentIndexChanged.connect(app.view.update)
        self.combo = combo
        self.action = action

    def __call__(self, *args, **kwargs):
        """Wrapper for the action associated with the combo box.

        Returns
        -------
        None

        """
        index = self.combo.currentIndex()
        text = self.combo.currentText()
        self.action(index, text)
