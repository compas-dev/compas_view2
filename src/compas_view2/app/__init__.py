import os
import json

from .controller import Controller  # noqa: F401
from .app import App  # noqa: F401

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'config.json')

with open(FILE) as f:
    config = json.load(f)
