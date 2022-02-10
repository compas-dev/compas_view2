import ryvencore_qt as rc
import inspect
from compas_view2.objects import DATA_OBJECT
from qtpy.QtGui import QColor
from .widgets import ExecutionControl
import traceback


def Node(app, color='#0092D2', auto_update=None):
    """
    Decorator for creating a node in a flow.
    """

    node_color = color

    def decorator(func):

        signature = inspect.signature(func)

        if auto_update is None:
            _auto_update = app.flow.flow_auto_update
        else:
            _auto_update = auto_update

        class CustomNode(rc.Node):

            title = func.__name__
            init_inputs = [rc.NodeInputBP(label=name) for name in signature.parameters.keys() if name != 'self']
            init_outputs = [rc.NodeOutputBP(signature.return_annotation.__name__)]
            color = node_color
            main_widget_class = ExecutionControl
            main_widget_pos = 'below ports'  # or 'between ports'

            def __init__(self, params):
                super().__init__(params)
                self._object = None
                self.block_updates = not _auto_update
                self.actions['execute'] = {'method': self.update_event}

            def __repr__(self) -> str:
                return f'<{self.__class__.__name__}({self.title})>'

            @property
            def auto_update(self):
                return not self.block_updates

            @auto_update.setter
            def auto_update(self, value):
                self.block_updates = not value
                self.item.main_widget.set_auto_update(None, value=value, update_node=False)

            def place_event(self):
                # This is to suppress a ryven exception to parse and empty dict when initiating the main widget
                self.init_data = None
                self.update()

            def remove_event(self):
                if self._object:
                    app.remove(self._object)
                    app.view.update()

            def update_event(self, inp=-1):
                try:
                    _inputs = [self.input(i) for i in range(len(self.init_inputs)) if self.input(i) is not None]
                    try:
                        _output = func(*_inputs)
                        self.change_color()
                        self.item.main_widget.set_message()
                    except Exception as e:
                        print("Function failed at", self)
                        print(traceback.format_exc())
                        self.item.main_widget.set_message(str(e))
                        self.change_color('#FF0000')
                        _output = None

                    if self._object:
                        app.remove(self._object)

                    if _output and _output.__class__ in DATA_OBJECT:
                        self._object = app.add(_output)

                    app.view.update()
                    self.set_output_val(0, _output)
                except Exception as e:
                    print(e)

            def change_color(self, color=None):
                color = color or self.color
                self.item.animator.stop()  # The animator must be stopped before changing the color
                self.item.color = QColor(color)
                self.item.update_design()

        app.flow.session.register_node(CustomNode)
        return CustomNode

    return decorator
