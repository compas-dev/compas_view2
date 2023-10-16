********************************************************************************
Tutorial Configuration
********************************************************************************

.. |checked| raw:: html

    <i class="far fa-check-square"></i>

.. |unchecked| raw:: html

    <i class="far fa-square"></i>

.. highlight:: python

.. rst-class:: lead

Unlike many other COMPAS packages which are categorized as python libraries with classes and functions,
:mod:`compas_view2`is closer to a software application with its solid underlying architecture and customizable features.
Thinking of the ``options`` in :mod:`Rhino`, the ``preferences..`` in :mod:`Blender`or other ``setting`` menus in other softwares,
:mod:`compas_view2`also provides a ``config`` feature to allow customize your viewer for you.


Configuration structure
===========




Setup assistant
===========


The basic process of visualizing COMPAS objects with :mod:`compas_view2` consists out of three steps:

1. Create an instance of a viewer.
2. Add objects.
3. Launch the viewer.

::

    >>> from compas.geometry import Sphere
    >>> from compas_view2.app import App
    >>> viewer = App()
    >>> viewer.add(Sphere([0, 0, 0], 1.0))
    >>> viewer.show()


Add Objects
===========
