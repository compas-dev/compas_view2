import json
import compas

from .controller import Controller  # noqa: F401
from .app import App  # noqa: F401

with open(compas.here(__file__, 'config.json')) as f:
    config = json.load(f)
