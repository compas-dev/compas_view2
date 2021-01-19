# COMPAS Viewers 2

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

## Notes

* Provide separate shaders for GLSL 1.20 and GLSL 3.30 and above.
* Load all available programs into shader for specific version.
* Align object init and drawing methods with GLSL version.
* Use VAO for GLSL 3.30 and above.
* Provide shader programs for different types of COMPAS objects.
* Add toolbar for basic view operations: Select, Zoom Extents, Zoom Selected, Translate, Rotate, ...
* Add menu for additional operations: Load objects, Save scene, Load scene, Mesh operations, ...
* How to visualize script output in open Viewer?
* Run script button.

