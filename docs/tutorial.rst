********************************************************************************
Tutorial
********************************************************************************

Basic usage
===========

Add COMPAS objects in a script and visualize the result.

.. code-block:: python

    from compas.geometry
    from compas_view2.app import App
    viewer = App()


    viewer.run()

Scripting
=========

To add COMPAS objects through scripting, before launching the viewer window,
simply add the objects to the scene.

.. code-block:: python

    from compas_view2.app import App
    from compas.geometry import Box, Frame

    viewer = App()

    box = Box(Frame.worldXY(), 1, 1, 1)
    viewer.add(box)

    viewer.run()

Selecting
=========

*More info coming soon*...

Modifying
=========

*More info coming soon*...
