import ryvencore_qt as rc
import inspect
from compas_view2.objects import DATA_OBJECT


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

        class _Node(rc.Node):
            title = func.__name__
            init_inputs = [rc.NodeInputBP(label=name) for name in signature.parameters.keys() if name != 'self']
            init_outputs = [rc.NodeOutputBP(signature.return_annotation.__name__)]
            color = node_color

            def __init__(self, params):
                super().__init__(params)
                self._object = None
                self.block_updates = not _auto_update
                self.actions['execute'] = {'method': self.update_event}
                self.actions['enable auto update'] = {'method': self.enable_auto_update}
                self.actions['disable auto update'] = {'method': self.disable_auto_update}

            def enable_auto_update(self):
                self.block_updates = False
                self.update_event()

            def disable_auto_update(self):
                self.block_updates = True

            def place_event(self):
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
                    except Exception as e:
                        print("Function failed:", e)
                        _output = None

                    if self._object:
                        app.remove(self._object)

                    if _output and _output.__class__ in DATA_OBJECT:
                        self._object = app.add(_output)

                    app.view.update()
                    self.set_output_val(0, _output)
                except Exception as e:
                    print(e)

        app.flow.session.register_node(_Node)
        return _Node
    return decorator
