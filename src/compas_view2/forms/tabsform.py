from .dockform import DockForm
from .treeform import TreeForm
from qtpy import QtWidgets


class TabsForm(DockForm):
    def __init__(self, app, title="Tree", tabs=[], columns=["key", "value"], show_headers=True):
        super().__init__(app, title)
        containerwidget = QtWidgets.QWidget()
        tabwidget = QtWidgets.QTabWidget()
        for tab in tabs:
            print(tab["name"])
            treeForm = TreeForm(app, title=tab["name"], data=tab["data"], columns=columns, show_headers=show_headers)
            treeForm.setTitleBarWidget(QtWidgets.QWidget())
            tabwidget.addTab(treeForm, tab["name"])
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tabwidget)
        containerwidget.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setWidget(containerwidget)
