import ryvencore_qt as rc
from typing import List, Tuple, Union
from compas.geometry import Vector as Vector


class ValueNode(rc.Node):

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


def IntegerNode(title: str = 'Integer', default: int = 1, bounds: Tuple[float, float] = None) -> ValueNode:

    _title = title
    bounds = bounds or (-10**9, 10**9)

    class IntegerNode(ValueNode):

        title = _title

        init_inputs = [
            rc.NodeInputBP(
                dtype=rc.dtypes.Integer(default=default, bounds=bounds),
                label='Int'
            ),
        ]

    return IntegerNode


def FloatNode(title: str = 'Float', default: float = 0.0, bounds: tuple = None) -> ValueNode:

    _title = title
    bounds = bounds or (0, 1)

    class FloatNode(ValueNode):

        title = _title

        init_inputs = [
            rc.NodeInputBP(
                dtype=rc.dtypes.Float(default=default, bounds=bounds),
                label='Float'
            ),
        ]

    return FloatNode


def ChoiceNode(title: str = 'Choice', items: List = None, default=None) -> ValueNode:

    _title = title
    items = items or []

    class ChoiceNode(ValueNode):

        title = _title

        init_inputs = [
            rc.NodeInputBP(
                dtype=rc.dtypes.Choice(default=default, items=items),
                label='Choice'
            ),
        ]

    return ChoiceNode


def StringNode(title: str = 'String', default: str = None) -> ValueNode:

    _title = title

    class StringNode(ValueNode):

        title = _title

        init_inputs = [
            rc.NodeInputBP(
                dtype=rc.dtypes.String(default=default, size='l'),
                label='String'
            ),
        ]

    return StringNode


def VectorNode(title: str = 'String', default: Union[List[float], Tuple[float, float, float], Vector] = None) -> ValueNode:

    _title = title
    default = default or [0, 0, 0]

    class VectorNode(ValueNode):

        title = _title

        init_inputs = [
            rc.NodeInputBP(
                dtype=rc.dtypes.Float(default=default[0]),
                label='x'
            ),
            rc.NodeInputBP(
                dtype=rc.dtypes.Float(default=default[1]),
                label='y'
            ),
            rc.NodeInputBP(
                dtype=rc.dtypes.Float(default=default[2]),
                label='z'
            ),
        ]

        def update_event(self, inp=-1):
            self.set_output_val(0, Vector(self.input(0), self.input(1), self.input(2)))

    return VectorNode
