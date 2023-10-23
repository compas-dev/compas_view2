from .action import Action, mouse_check, mouse_key_check, key_check  # noqa : F401

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
