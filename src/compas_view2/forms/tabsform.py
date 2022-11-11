from .dockform import DockForm
from .treeform import TreeForm
from qtpy import QtWidgets


class TabsForm(DockForm):
    def __init__(self, app, title="Tree", tabs=[], columns=["key", "value"], show_headers=True, striped_rows=False):
        super().__init__(app, title)
        self.treeforms = {}
        containerwidget = QtWidgets.QWidget()
        tabwidget = QtWidgets.QTabWidget()
        for tab in tabs:
            treeForm = TreeForm(
                app,
                title=tab["name"],
                data=tab["data"],
                columns=tab.get("columns") or columns,
                show_headers=show_headers,
                striped_rows=striped_rows,
            )
            treeForm.setTitleBarWidget(QtWidgets.QWidget())
            tabwidget.addTab(treeForm, tab["name"])
            self.treeforms[tab["name"]] = treeForm
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tabwidget)
        containerwidget.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setWidget(containerwidget)

    def update(self, tabs):
        for tab in tabs:
            self.treeforms[tab["name"]].update(tab["data"])
