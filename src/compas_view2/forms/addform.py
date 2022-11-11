from qtpy import QtWidgets

from compas_view2.objects import DATA_OBJECT

from .form import Form


class AddForm(Form):
    def __init__(self, on_create=None):
        super().__init__("Add Object")

        for data_cls in DATA_OBJECT:
            self.add_create_button(data_cls, on_create)

    def add_create_button(self, data_cls, on_create):
        object_cls = DATA_OBJECT[data_cls]
        if hasattr(object_cls, "create_default"):
            layout = QtWidgets.QHBoxLayout()
            self._inputs.addLayout(layout)
            button = QtWidgets.QPushButton()
            button.setText(data_cls.__name__)

            def _on_create():
                default_data = object_cls.create_default()
                on_create(default_data)
                self.accept()

            button.clicked.connect(_on_create)
            layout.addWidget(button)

    def inputs(self):
        """Creates layout for input fields

        Returns
        -------
        QtWidgets.QVBoxLayout
        """
        return QtWidgets.QVBoxLayout()
