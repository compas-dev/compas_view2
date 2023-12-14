********************************************************************************
Tutorial Configuration
********************************************************************************

.. |checked| raw:: html

    <i class="far fa-check-square"></i>

.. |unchecked| raw:: html

    <i class="far fa-square"></i>

.. highlight:: python

.. rst-class:: lead

.. autosummary::
    :toctree:
    :nosignatures:

Unlike many other COMPAS packages which are categorized as python libraries with classes and functions,
:mod:`compas_view2` is closer to a software application with its solid underlying architecture and customizable features.
Thinking of the ``options`` in :mod:`Rhino` , the ``preferences..`` in :mod:`Blender` or other ``setting`` menus in other softwares,
:mod:`compas_view2` also provides a ``config`` feature to allow you to customize your viewer.


Customize Your Viewer
=====================

There are two ways to customize your viewer:

1. Using the configuration file:

::

    >>> # This invokes the default configuration.
    >>> from compas_view2.app import App
    >>> viewer = App()

::

    >>> # You can put your configuration by inputting the file location.
    >>> from compas_view2.app import App
    >>> viewer = App(config = "PATH/TO/YOUR_CONFIG.json")

This is a sustainable and sharable way to customize your viewer.



2. In-code definition which overwrites the configuration:

::

    >>> from compas_view2.app import App
    >>> viewer = App(viewmode="lighted", enable_sceneform=True, enable_propertyform=True, enable_sidebar=True, width=2000, height=1000)

::

    >>> # You can put your configuration as a dictionary. If you input incomplete configuration, the rest will be filled by the default values.
    >>> from compas_view2.app import App
    >>> config = {....}
    >>> viewer = App(config = config)

This is a quick way to customize your viewer. It is suitable for task-specific customization.


Configuration Structure
======================
The default configuration file can be downloaded here: :download:`Link <files/config_default.json>`,
or can be printed by the following code:

::

    >>> # This prints the default configuration
    >>> from compas_view2 import Info
    >>> Info().show_config()

It it the template for creating your own settings, keyboard preferences, etc.

Supported Keys
===============
In the `controller -> keys`, you can add you preferred keys. Currently, :mod:`compas_view2` supports below keys:

.. figure:: /_images/keyboard.png
    :figclass: figure
    :class: figure-img img-fluid
