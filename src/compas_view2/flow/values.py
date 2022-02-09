import ryvencore_qt as rc


class Value(rc.Node):

    title = 'Value'
    color = '#0092D2'
    init_inputs = [rc.NodeInputBP()]
    init_outputs = [rc.NodeOutputBP()]

    @property
    def auto_update(self):
        return not self.block_updates

    @auto_update.setter
    def auto_update(self, value: bool):
        # value nodes should always auto update
        pass

    def view_place_event(self):
        self.update()

    def update_event(self, inp=-1):
        self.set_output_val(0, self.input(0))


def Integer(default: int = 1, bounds: tuple = None):

    bounds = bounds or (-10**9, 10**9)

    class IntegerNode(Value):

        title = 'Integer'

        init_inputs = [
            rc.NodeInputBP(
                dtype=rc.dtypes.Integer(default=default, bounds=bounds),
                label='Int'
            ),
        ]

    return IntegerNode


def Float(default: float = 0.0, bounds: tuple = None):

    bounds = bounds or (0, 1)

    class FloatNode(Value):

        title = 'Float'

        init_inputs = [
            rc.NodeInputBP(
                dtype=rc.dtypes.Float(default=default, bounds=bounds),
                label='Float'
            ),
        ]

    return FloatNode


def Choice(items: list, default=None):

    class ChoiceNode(Value):

        title = 'Choice'

        init_inputs = [
            rc.NodeInputBP(
                dtype=rc.dtypes.Choice(default=default, items=items),
                label='Choice'
            ),
        ]

    return ChoiceNode


def String(default=None):

    class StringNode(Value):

        title = 'String'

        init_inputs = [
            rc.NodeInputBP(
                dtype=rc.dtypes.String(default=default, size='l'),
                label='String'
            ),
        ]

    return StringNode
