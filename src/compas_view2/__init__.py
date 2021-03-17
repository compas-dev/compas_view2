import os

os.environ['QT_MAC_WANTS_LAYER'] = '1'

__author__ = ["tom van mele"]
__copyright__ = "Block Research Group - ETH Zurich"
__license__ = "MIT License"
__email__ = "van.mele@arch.ethz.ch"
__version__ = "0.2.1"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


try:
    from OpenGL import GL  # noqa: F401
except Exception:
    from ctypes import util
    orig_util_find_library = util.find_library

    def new_util_find_library(name):
        res = orig_util_find_library(name)
        if res:
            return res
        return '/System/Library/Frameworks/' + name + '.framework/' + name
    util.find_library = new_util_find_library


__all__ = ["HOME", "DATA", "DOCS", "TEMP", "DATA_VIEW", "register"]
