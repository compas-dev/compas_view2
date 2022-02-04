import ryvencore_qt as rc


class Value(rc.Node):

    title = 'Value'
    color = '#0092D2'
    init_inputs = [rc.NodeInputBP()]
    init_outputs = [rc.NodeOutputBP()]

    def place_event(self):
        self.update()

    def update_event(self, inp=-1):
        self.set_output_val(0, self.input(0))


class Integer(Value):

    title = 'Integer'

    init_inputs = [
        rc.NodeInputBP(
            dtype=rc.dtypes.Integer(default=1),
            label='Int'
        ),
    ]


class Float(Value):

    title = 'Float'

    init_inputs = [
        rc.NodeInputBP(
            dtype=rc.dtypes.Float(default=1.0),
            label='Float'
        ),
    ]
