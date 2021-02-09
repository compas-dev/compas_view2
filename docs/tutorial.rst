********************************************************************************
Tutorial
********************************************************************************

Basic usage
===========

To launch the viewer and add objects interactively, create an instance of the app
and run the event loop.

.. code-block:: python

    from compas_view2.app import App
    viewer = App()
    viewer.run()

.. raw:: html

    <div class="mx-auto">
        <video width="800" height="500" controls>
            <source src="_videos/test.mp4" type="video/mp4">
        Your browser does not support the video tag.
        </video>
    </div>

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
