import ryvencore_qt as rc
from typing import List, Tuple, Union
from compas.geometry import Vector as Vector


class ValueNode(rc.Node):
    """Base class for all input value nodes."""

    title = "Value"
    color = "#0092D2"
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


def IntegerNode(title: str = "Integer", default: int = 1, bounds: Tuple[float, float] = None) -> ValueNode:
    """Builds an integer node class.

    Parameters
    ----------
    title : str
        Displayed title of node.
        Defaults to 'Integer'.
    default : int
        Default value.
        Defaults to 1.
    bounds : Tuple[float, float]
        Min and max bounds of value.
        Defaults to (-10**9, 10**9).

    Returns
    -------
    :class:`compas_view2.flow.ValueNode`
        An extension of :class:`compas_view2.flow.ValueNode` that represents an integer value.

    """
    _title = title
    bounds = bounds or (-(10**9), 10**9)

    class IntegerNode(ValueNode):

        title = _title

        init_inputs = [
            rc.NodeInputBP(dtype=rc.dtypes.Integer(default=default, bounds=bounds), label="Int"),
        ]

    return IntegerNode


def FloatNode(title: str = "Float", default: float = 0.0, bounds: tuple = None) -> ValueNode:
    """Builds an float node class.

    Parameters
    ----------
    title : str
        Displayed title of node.
        Defaults to 'Float'.
    default : float
        Default value.
        Defaults to 0.0.
    bounds : Tuple[float, float]
        Min and max bounds of value.
        Defaults to (-10**9, 10**9).

    Returns
    -------
    :class:`compas_view2.flow.ValueNode`
        An extension of :class:`compas_view2.flow.ValueNode` that represents an float value.

    """

    _title = title
    bounds = bounds or (-(10**9), 10**9)

    class FloatNode(ValueNode):

        title = _title

        init_inputs = [
            rc.NodeInputBP(dtype=rc.dtypes.Float(default=default, bounds=bounds), label="Float"),
        ]

    return FloatNode


def ChoiceNode(title: str = "Choice", default: str = None, items: List[str] = None) -> ValueNode:
    """Builds an choice node class.

    Parameters
    ----------
    title : str
        Displayed title of node.
        Defaults to 'Choice'.
    default : str
        Default choice.
        Defaults to None.
    items : List[str]
        List of items to choose from.
        Defaults to [].

    Returns
    -------
    :class:`compas_view2.flow.ValueNode`
        An extension of :class:`compas_view2.flow.ValueNode` that represents a choice from list of values.

    """

    _title = title
    items = items or []

    class ChoiceNode(ValueNode):

        title = _title

        init_inputs = [
            rc.NodeInputBP(dtype=rc.dtypes.Choice(default=default, items=items), label="Choice"),
        ]

    return ChoiceNode


def StringNode(title: str = "String", default: str = None) -> ValueNode:
    """Builds an string node class.

    Parameters
    ----------
    title : str
        Displayed title of node.
        Defaults to 'String'.
    default : str
        Default string.
        Defaults to None.

    Returns
    -------
    :class:`compas_view2.flow.ValueNode`
        An extension of :class:`compas_view2.flow.ValueNode` that represents a string value.

    """

    _title = title

    class StringNode(ValueNode):

        title = _title

        init_inputs = [
            rc.NodeInputBP(dtype=rc.dtypes.String(default=default, size="l"), label="String"),
        ]

    return StringNode


def VectorNode(
    title: str = "Vector", default: Union[List[float], Tuple[float, float, float], Vector] = None
) -> ValueNode:
    """Builds an vector node class.

    Parameters
    ----------
    title : str
        Displayed title of node.
        Defaults to 'Vector'.
    default : Union[List[float], Tuple[float, float, float], Vector]
        Default vector.
        Defaults to [0, 0, 0].

    Returns
    -------
    :class:`compas_view2.flow.ValueNode`
        An extension of :class:`compas_view2.flow.ValueNode` that represents a vector value.

    """

    _title = title
    default = default or [0, 0, 0]

    class VectorNode(ValueNode):

        title = _title

        init_inputs = [
            rc.NodeInputBP(dtype=rc.dtypes.Float(default=default[0]), label="x"),
            rc.NodeInputBP(dtype=rc.dtypes.Float(default=default[1]), label="y"),
            rc.NodeInputBP(dtype=rc.dtypes.Float(default=default[2]), label="z"),
        ]

        def update_event(self, inp=-1):
            self.set_output_val(0, Vector(self.input(0), self.input(1), self.input(2)))

    return VectorNode
