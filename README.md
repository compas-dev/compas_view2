# COMPAS Viewers 2

Second generation viewers for the COMPAS framework

## Installation

## Windows

```bash
conda create -n view2 python=3.7 cython freetype --yes
conda activate view2
pip install -r requirements-dev.txt
```

Install `PyOpenGL` and `PyOpenGL-accelerate` from here:
<https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl>

Make sure to select the versions of the wheels that match your system.
For example, for Python3.7

```bash
pip install PyOpenGL‑3.1.5‑cp37‑cp37m‑win_amd64.whl
pip install PyOpenGL_accelerate‑3.1.5‑cp37‑cp37m‑win_amd64.whl
```

## Mac

```bash
conda create -n view2 python=3.7 cython freetype python.app --yes
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

