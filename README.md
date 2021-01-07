# COMPAS Viewers 2

Second generation viewers for the COMPAS framework

## Installation

```bash
conda create -n view2 python=3.7 cython freetype --yes
conda activate view2
pip install -r requirements-dev.txt
```

## Scripts

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

* VAO supported.
