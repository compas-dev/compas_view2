*******************************************************************************
Camera Config
*******************************************************************************

.. autosummary::
    :toctree:
    :nosignatures:

Default Camera Config
====================

By default, the camera is configed 45 dregees perspective:

.. figure:: /_images/example_camera_config.jpg
    :figclass: figure
    :class: figure-img img-fluid



Custom Camera Config
====================

You can customize the camera configreation by passing the dictionary to the viewer: fov, near, fac, position, target, scale.

.. note::
   The `position` is not editable and would be ingored from the config file in `TOP`, `FRONT`, `RIGHT`modes.

.. figure:: /_images/example_camera_config_2.jpg
    :figclass: figure
    :class: figure-img img-fluid

.. literalinclude:: example_camera_config.py
    :language: python
