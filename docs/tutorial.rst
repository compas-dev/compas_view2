********************************************************************************
Tutorial
********************************************************************************

.. |checked| raw:: html

    <i class="far fa-check-square"></i>

.. |unchecked| raw:: html

    <i class="far fa-square"></i>

.. rst-class:: lead

This tutorial covers basic usage of the viewer through scripting.
Other usage modes are possible and will be described in a separate tutorial.


Basic Usage
===========

The process of visualizing COMPAS objects with :mod:`compas_view2` consists out of three steps:

1. Create an instance of a viewer.
2. Do stuff (like adding objects).
3. Launch the viewer.

.. code-block:: python

    from compas_view2.app import App

    viewer = App()

    # add objects

    viewer.show()


Add Objects
===========

Most COMPAS geometry objects and data structures can simply be "added" to a visualization using :meth:`compas_view2.app.App.add`.

.. code-block:: python

    from compas.geometry import Sphere
    from compas_view2.app import App


    viewer.add(Sphere([0, 0, 0], 1.0))


The "add" method (:meth:`compas_view2.app.App.add`) returns an instance


Object Appearance
=================


Object Collections
==================


Zoom, Pan, Rotate
=================


Dynamic Visualization
=====================


Capturing
=========


Interactive Mode
================


Viewer Configuration
====================


Custom UI Elements
==================