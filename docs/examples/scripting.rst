********************************************************************************
Scripting mode
********************************************************************************

.. rst-class:: lead

To use the viewer in "scripting" mode,
make an instance of the app,
and add a bunch of objects before showing the main window.

.. code-block:: python

    from compas_view2.app import App

    viewer = App()

    # add objects

    viewer.show()
