import ryvencore_qt as rc
import inspect
from compas_view2.objects import DATA_OBJECT
from qtpy.QtGui import QColor
from .widgets import ExecutionControl
from compas.colors import Color
from typing import Union
import traceback


def Node(app, color: Union[Color, str, list, tuple] = "#0092D2", auto_update: bool = None, **kwargs):
    """Decorator for creating a custom ryven node in compas_view2 flow.

    Parameters
    ----------
    app: :class:`compas_view2.app.App`
        The compas_view2 app instance.
    color : Union[Color, str, list, tuple]
        The color theme of the ndoe.
        Defaults to '#0092D2'.
    auto_update : bool
        Whether to auto update the node.
        Defaults to the global flow setting.
    **kwargs : dict
        Additional keyword arguments for the node output visualisation.

    Returns
    -------
    callable
        A CustomNode class that wraps the decorated function.

    """

    if Color.is_hex(color):
        color = Color.from_hex(color)
    elif Color.is_rgb255(color):
        color = Color.from_rgb255(*color)
    elif Color.is_rgb1(color):
        color = Color(*color)
    else:
        raise ValueError("Invalid color: {}".format(color))

    node_color = color.hex

    def decorator(func):

        signature = inspect.signature(func)

        if auto_update is None:
            _auto_update = app.flow.flow_auto_update
        else:
            _auto_update = auto_update

        class CustomNode(rc.Node):
            """Class that wraps the decorated function."""

            title = func.__name__
            init_inputs = [rc.NodeInputBP(label=name) for name in signature.parameters.keys() if name != "self"]
            init_outputs = [rc.NodeOutputBP(signature.return_annotation.__name__)]
            color = node_color
            main_widget_class = ExecutionControl
            main_widget_pos = "below ports"  # or 'between ports'

            def __init__(self, params):
                super().__init__(params)
                self.block_updates = not _auto_update
                self.actions["execute"] = {"method": self.update_event}
                self.actions["show_object"] = {"method": self.show_object}
                self.actions["hide_object"] = {"method": self.hide_object}
                self.actions["select_object"] = {"method": self.select_object}
                self.object = None
                self.app = app
                self.object_properties = kwargs
                if not self.object_properties.get("facecolor"):
                    self.object_properties["facecolor"] = color

            def __repr__(self) -> str:
                return f"<{self.__class__.__name__}({self.title})>"

            @property
            def auto_update(self):
                return not self.block_updates

            @auto_update.setter
            def auto_update(self, value):
                """Two direction binding to the checkbox widget."""
                self.block_updates = not value
                self.item.main_widget.set_auto_update(None, value=value, update_node=False)

            def select_object(self):
                """Select the object in the scene."""
                if self.object:
                    self.app.selector.select(self.object)
                    self.app.view.update()

            def show_object(self):
                """Show the object in the scene."""
                if self.object:
                    self.object_properties["is_visible"] = self.object.is_visible = True
                    self.object.is_visible = True
                    self.app.view.update()

            def hide_object(self):
                """Hide the object in the scene."""
                if self.object:
                    self.object_properties["is_visible"] = self.object.is_visible = False
                    self.app.view.update()

            def place_event(self):
                """Called upon node placement."""
                # This is to suppress a ryven exception to parse and empty dict when initiating the main widget
                self.init_data = None

            def remove_event(self):
                """Called upon node removal."""
                if self.object:
                    app.remove(self.object)
                    app.view.update()

            def update_event(self, inp=-1):
                """execute wrapped function."""

                if not self.app.started:
                    return

                _inputs = [self.input(i) for i in range(len(self.init_inputs))]
                try:
                    _output = func(*_inputs)
                    # Restore to default color if the function succeeded
                    self.item.main_widget.set_message()
                    self.change_color()

                except Exception as e:
                    _output = None
                    # Change node color and display error message
                    print("Function failed at", self)
                    print(traceback.format_exc())
                    self.item.main_widget.set_message(str(e))
                    self.change_color("#FF0000")

                finally:
                    if self.object:
                        app.remove(self.object)

                    if _output and _output.__class__ in DATA_OBJECT:
                        self.object = app.add(_output, **self.object_properties)

                    app.view.update()
                    self.set_output_val(0, _output)

            def change_color(self, color=None):
                """Change the theme color of the node."""
                color = color or self.color
                self.item.animator.stop()  # The animator must be stopped before changing the color
                self.item.color = QColor(color)
                self.item.update_design()

        app.flow.session.register_node(CustomNode)
        return CustomNode

    return decorator
