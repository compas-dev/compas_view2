from qtpy import QtWidgets


class Radio:
    """Class representing a radio button group wrapped in a group box.

    Parameters
    ----------
    app : :class:`compas_view2.app.App`
        The app containing the widget.
    parent : QtWidgets.QWidget
        The parent widget for the radio button group.
    title : str
        The label for the radio button group.
    items : list[dict[str, Any]]
        A list of radio button group items, with each item defined as a dict with a particular structure.
        See Notes for more info.
    action : callable
        The action associated with the radio button group.

    Attributes
    ----------
    radio : QtWidgets.QButtonGroup
        The button group containing the exclusive radio items.
    action : callable
        The action associated with the click event of the radio button group.
    values : dict[QtWidgets.QRadioButton, Any]
        Mapping between radio buttons and their values.

    Notes
    -----
    Every `item` dict should have the following structure.

    .. code-block:: python

        item['text']     # str  : The text label of the item.
        item['value']    # Any  : The value of the item, if different from the item text.
        item['checked']  # bool : If True, the item should be marked as checked.

    """

    def __init__(self, app, parent, *, title, items, action):

        box = QtWidgets.QGroupBox(title)
        layout = QtWidgets.QVBoxLayout()
        group = QtWidgets.QButtonGroup(app.window, exclusive=True)
        # add the options
        button_value = {}
        for item in items:
            button = QtWidgets.QRadioButton()
            button.setText(item["text"])
            button.setChecked(item["checked"])
            group.addButton(button)
            layout.addWidget(button)
            button_value[button] = item.get("value", item["text"])
        # connect actions
        group.buttonClicked.connect(self)
        group.buttonClicked.connect(app.view.update)
        # put together
        box.setLayout(layout)
        parent.addWidget(box)
        # define attributes
        self.radio = group
        self.action = action
        self.values = button_value

    def __call__(self, *args, **kwargs):
        """Wrapper for the action associated with the radio button group.

        Returns
        -------
        None

        """
        button = self.radio.checkedButton()
        self.action(self.values[button])
