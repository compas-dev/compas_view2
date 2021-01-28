# COMPAS Viewers 2

**THIS PACKAGE IS UNDER DEVELOPMENT. USE IT AT YOUR OWN RISK :)**

Second generation viewers for the COMPAS framework

## Installation

## Windows

```bash
conda create -n view2 python=3.8 cython freeglut --yes
conda activate view2
pip install -r requirements-dev.txt
```

## Mac

```bash
conda create -n view2 python=3.8 cython python.app --yes
conda activate view2
pip install -r requirements-dev.txt
```

By installing `python.app` you can use `pythonw` to run the viewers instead of `python`.
This ensures that all components work as expected.

To configure VS Code to use `pythonw`, change the python path in the settings of the workspace.
In `.vscode/settings.json`

```json
{
    ...

    "python.pythonPath": "/Users/xxx/anaconda3/envs/view2/bin/pythonw"

    ...
}
```

## Features

*More info coming soon...*

## Examples

`scripts/minimal_120.py`

OpenGL 2.1 and GLSL 1.20 with Compatibility Profile works on Mac and on Windows (via Parallels).

* VAO not supported.
* Windows (my machine) only accepts drawing of elements (not arrays).
* Defaults for shader values not supported.
* Location binding not supported.

```bash
python scripts/minimal_120.py
```

`scripts/minimal_330.py`

OpenGL 3.3 (or higher) and corresponding GLSL 3.30 (with Core Profile) works only on Mac (on my machine).

* State management with VAOs
* Modern OpenGL and GLSL only

*Under Construction*...

## License

The code in this repo is licensed under the [MIT License](LICENCSE).

The icons used on the toolbars of the viewers are part of the collection of free Font Awesome (FA) icons.
The free icons of FA are subject to a Creative Commons 4.0 license.
More information about FA free and the icon license can be found here <https://fontawesome.com/license/free>.

The icons bundled with this repo can be found in `src/compas_view2/icons`.

### Big Sur

After updating to Big Sur, a few things had to be updated.
Some of these fixes will no longer be necessary in Python 3.9
but COMPAS and Numpy are not yet available for this version of Python...

* <https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos>
* <https://developer.apple.com/documentation/xcode/porting_your_macos_apps_to_apple_silicon>
* <https://github.com/PixarAnimationStudios/USD/issues/1372>
* <https://forum.openframeworks.cc/t/big-sur-and-opengl/35661>
* <https://forum.qt.io/topic/120846/big-sur-pyside2-not-showing-a-widgets/7>
* <https://stackoverflow.com/questions/64833558/apps-not-popping-up-on-macos-big-sur-11-0-1#_=>
