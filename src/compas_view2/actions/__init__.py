from .action import Action, supported_keys  # noqa : F401
from typing import Dict  # noqa : F401
from qtpy import QtCore  # noqa : F401

from .view_top import ViewTop  # noqa : F401
from .view_front import ViewFront  # noqa : F401
from .view_right import ViewRight  # noqa : F401
from .view_perspective import ViewPerspective  # noqa : F401

from .view_shaded import ViewShaded  # noqa : F401
from .view_ghosted import ViewGhosted  # noqa : F401
from .view_wireframe import ViewWireframe  # noqa : F401
from .view_lighted import ViewLighted  # noqa : F401

from .zoom_selected import ZoomSelected  # noqa : F401
from .select_all import SelectAll  # noqa : F401
from .grid_show import GridShow  # noqa : F401
from .view_capture import ViewCapture  # noqa : F401


def mouse_key_check(event, key_status: Dict, mouse_key: Dict):
    """Giving the mouse key as a dictionary that is in the list of supported keys, return if it is happening (bool).

    Parameters
    ----------
    event:
        The Qt event.
    key_status : Dict
        The status dictionary that is like `"key_status": { "shift": False, "control": False, "alt": False }`.
    mouse_key : Dict
        The dictionary that is like `"mouse_key": { "mouse": "right", "key": "shift" }`.

    Returns
    ----------
    bool:
        If the mouse key is happening.


    Notes
    ----------
    This function is designed to check mouse_key combine interactions. The interactions are:
    "box_selection", "selection", "multi_selection", "deselect", "pan", "rotate", for now.
    """
    supported_buttons = {
        "left": QtCore.Qt.LeftButton,
        "right": QtCore.Qt.RightButton,
        "middle": QtCore.Qt.MiddleButton,
    }

    if event.buttons() & supported_buttons[mouse_key["mouse"]]:
        if key_status.get(mouse_key["key"]) is None:
            key_status[mouse_key["key"]] = False

        if mouse_key["key"] == "":
            for key in key_status.values():
                if key:
                    return False
            return True

        elif key_status[mouse_key["key"]]:
            return True

    else:
        return False


def mouse_check(event, button_name: str):
    """Giving the button name that is one of the supported buttons, return if the button is pressed.

    Parameters
    ----------
    event:
        The Qt event.
    button_name : str
        The name of the button. It should be exist in the list of `supported buttons`.

    Returns
    ----------
    bool:
        If the button is pressed.
    """
    supported_buttons = {
        "left": QtCore.Qt.LeftButton,
        "right": QtCore.Qt.RightButton,
        "middle": QtCore.Qt.MiddleButton,
    }
    if button_name not in supported_buttons:
        # Normally, this should not happen.
        raise KeyError(f"Button {button_name} is not supported.")
    else:
        if event.button() == supported_buttons[button_name]:
            return True
        else:
            return False


def key_check(event, key_status: Dict, key_name: str):
    """Giving the key name that is one of the supported keys, return if the key is pressed.

    Parameters
    ----------
    event:
        The Qt event.
    key_status : Dict
        The status dictionary that is like `"key_status": { "shift": False, "control": False, "alt": False }`.
    key_name : str
        The name of the key. It should be exist in the list of `supported keys`.

    Returns
    ----------
    bool:
        If the key is pressed.
    """

    if key_name == "":
        for key in key_status.values():
            if key:
                return False
        return True
    elif key_name not in supported_keys():
        raise KeyError(f"Key {key_name} is not supported.")
    else:
        if event.key() == supported_keys()[key_name]:
            return True
        else:
            return False


def action_manager(controller):
    """Initialize all the supported actions. This is the key entry to add more actions for more functionalities.
            The format is like: `"action_name": ActionClass(controller_class, controller_class.keys.get(action_name)),`.
            i.e. `"zoom_selected": ZoomSelected(controller, controller.keys.get("zoom_selected")),`.

    Parameters
    ----------
    controller_class: :class:`compas_view2.app.Controller`
        The controller class

    Returns
    ----------
    supported_actions: Dict
        The dictionary of all the supported action instances.
    """

    supported_actions = {
        "view_top": ViewTop(controller, controller.keys.get("view_top")),
        "view_front": ViewFront(controller, controller.keys.get("view_front")),
        "view_right": ViewRight(controller, controller.keys.get("view_right")),
        "view_perspective": ViewPerspective(controller, controller.keys.get("view_perspective")),
        "view_shaded": ViewShaded(controller, controller.keys.get("view_shaded")),
        "view_ghosted": ViewGhosted(controller, controller.keys.get("view_ghosted")),
        "view_wireframe": ViewWireframe(controller, controller.keys.get("view_wireframe")),
        "view_lighted": ViewLighted(controller, controller.keys.get("view_lighted")),
        "zoom_selected": ZoomSelected(controller, controller.keys.get("zoom_selected")),
        "select_all": SelectAll(controller, controller.keys.get("select_all")),
        "grid_show": GridShow(controller, controller.keys.get("grid_show")),
        "view_capture": ViewCapture(controller, controller.keys.get("view_capture")),
    }
    return supported_actions
