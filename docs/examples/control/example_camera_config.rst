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

You can customize the camera configreation by passing the dictionary to the viewer: fov, near, fac 100, position, target, scale.


.. figure:: /_images/example_camera_config_2.jpg
    :figclass: figure
    :class: figure-img img-fluid

.. literalinclude:: example_camera_config.py
    :language: python
