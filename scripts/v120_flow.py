import random
from compas_view2.app import App
import ryvencore_qt as rc


class PrintNode(rc.Node):
    """Prints your data"""

    title = 'Print'
    init_inputs = [
        rc.NodeInputBP(),
    ]
    init_outputs = []
    color = '#A9D5EF'

    # we could also skip the constructor here
    def __init__(self, params):
        super().__init__(params)

    def update_event(self, inp=-1):
        print(
            self.input(0)  # get data from the first input
        )


class RandNode(rc.Node):
    """Generates scaled random float values"""

    title = 'Rand'
    init_inputs = [
        rc.NodeInputBP(dtype=rc.dtypes.Data(default=1)),
    ]
    init_outputs = [
        rc.NodeOutputBP(),
    ]
    color = '#fcba03'

    def update_event(self, inp=-1):
        # random float between 0 and value at input
        val = random() * self.input(0)

        # setting the value of the first output
        self.set_output_val(0, val)


viewer = App(viewmode="shaded", enable_sidebar=True, width=800, height=500)
viewer.flow = None


@viewer.button(text="Flow Dialog")
def show_flow_dialog():
    session = rc.Session()
    session.design.set_flow_theme(name='pure dark')
    session.register_nodes([PrintNode, RandNode])
    script = session.create_script('test', flow_view_size=(800, 500))
    viewer.flow = session.flow_views[script]
    viewer.flow.show()


viewer.run()
