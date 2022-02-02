import ryvencore_qt as rc
import inspect
from compas_view2.objects import DATA_OBJECT


def Node(app):
    """
    Decorator for creating a node in a flow.
    """
    def decorator(func):

        signature = inspect.signature(func)

        class _Node(rc.Node):
            title = func.__name__
            init_inputs = [rc.NodeInputBP(label=name) for name in signature.parameters.keys() if name != 'self']
            init_outputs = [rc.NodeOutputBP(signature.return_annotation.__name__)]
            color = '#A9D5EF'

            def __init__(self, params):
                super().__init__(params)
                self._object = None

            def place_event(self):
                self.update()

            def remove_event(self):
                if self._object:
                    app.remove(self._object)

            def update_event(self, inp=-1):
                try:
                    print("Updating", self.title)
                    _inputs = [self.input(i) for i in range(len(self.init_inputs))]
                    print("Inputs:", _inputs)

                    try:
                        _output = func(*_inputs)
                    except Exception as e:
                        print("Function failed:", e)
                        _output = None

                    print("Output:", _output)

                    if self._object:
                        app.remove(self._object)

                    if _output and _output.__class__ in DATA_OBJECT:
                        self._object = app.add(_output)

                    app.view.update()
                    self.set_output_val(0, _output)
                except Exception as e:
                    print(e)

        app.flow.nodes.append(_Node)

        return func
    return decorator
