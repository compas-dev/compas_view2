# COMPAS Viewers 2

![build](https://github.com/compas-dev/compas_view2/workflows/build/badge.svg)
[![GitHub - License](https://img.shields.io/github/license/compas-dev/compas_view2.svg)](https://github.com/compas-dev/compas_view2)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/compas_view2.svg)](https://pypi.python.org/project/compas_view2)
[![PyPI - Latest Release](https://img.shields.io/pypi/v/compas_view2.svg)](https://pypi.python.org/project/compas_view2)

Second generation viewers for the COMPAS framework

## Installation

See the [Getting Started](https://compas.dev/compas_view2/latest/gettingstarted.html) instructions in the docs.

## Features

* Full support for all COMPAS objects (primitives, shapes, network, mesh, volmesh)
* Pick select and Box select
* Shaded, Ghosted, Wireframe, Specular visualisation modes
* Mesh faces with individual colors
* Dynamic visualisation with simple decorators
* Text annotations
* Customizable UI and UI Controller
* Transformations in object space
* ...

### Create Objects

| Object   | Script             | Form               | Interactive        |
| -------- | ------------------ | ------------------ | ------------------ |
| Point    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Vector   | :heavy_check_mark: | :x:                | :x:                |
| Line     | :heavy_check_mark: | :x:                | :heavy_check_mark: |
| Plane    | :x:                | :x:                | :x:                |
| Circle   | :x:                | :x:                | :x:                |
| Polygon  | :x:                | :x:                | :x:                |
| Polyline | :heavy_check_mark: | :x:                | :x:                |

## Examples

The example section in the docs is under construction.
Some basic examples are available in the `scripts` folder.

## License

The code in this repo is licensed under the [MIT License](LICENCSE).

## Known Issues

Please check the [Issue Tracker](https://github.com/compas-dev/compas_view2/issues) of the repo for known issues and their solutions.
