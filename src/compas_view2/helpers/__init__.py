from rich import print as rprint  # noqa: F401


def print(string):
    """
    Customized print function for a better terminal display.
    """

    if isinstance(string, str):
        string = string.replace("[INFO]", "[italic green][INFO][/italic green]")
        string = string.replace("[DEBUG]", "[italic magenta][DEBUG][/italic magenta]")
        string = string.replace("[WARN]", "[italic yellow][WARN][/italic yellow]")
        string = string.replace("[ERROR]", "[italic red][ERROR][/italic red]")
        string = string.replace("[INPUT]", "[italic blue][INPUT][/italic blue]")
    return rprint(string)


# from .setting_assistant import setting_assistant  # noqa: F401
from .info import Info  # noqa: F401, F403, E402
