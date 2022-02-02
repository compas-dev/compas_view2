import ryvencore_qt as rc


class Flow():
    def __init__(self, app):
        self.app = app
        self.nodes = []
        self.session = None
        self.script = None

    def init(self):
        self.session = rc.Session()
        self.session.design.set_flow_theme(name='pure dark')
        self.session.register_nodes(self.nodes)
        self.script = self.session.create_script('test', flow_view_size=(800, 500))
        self.flow = self.session.flow_views[self.script]

    def show(self):
        self.flow.show()
