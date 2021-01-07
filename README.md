# COMPAS Viewers 2

Second generation viewers for the COMPAS framework

## Installation

```bash
conda create -n view2 python=3.7 cython freetype --yes
conda activate view2
pip install -r requirements-dev.txt
```

On Windows, `PyOpenGL` and `PyOpenGL-accelerate` have to be installed separately from here:
<https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl>

Make sure to select the versions that match your system.

## Notes

* Provide separate shaders for GLSL 1.20 and GLSL 3.30 and above.
* Load all available programs into shader for specific version.
* Create correct shader for GLSL version.
* Align object init and drawing methods with GLSL version.
* Use VAO for GLSL 3.30 and above.
* Provide shader programs for different types of COMPAS objects.
* Add toolbar for basic view operations: Select, Zoom Extents, Zoom Selected, Translate, Rotate, ...
* Add menu for additional operations: Load objects, Save scene, Load scene, Mesh operations, ...
* How to visualize script output in open Viewer?
* Run script button.

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

*Under Construction*...
