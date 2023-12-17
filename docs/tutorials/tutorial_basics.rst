********************************************************************************
Tutorial Basics
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


This tutorial covers basic usage of the viewer through scripting.
Other usage modes are possible and will be described in a separate tutorial.


Basic Usage
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

::

    >>> obj = viewer.add(Sphere([0, 0, 0], 1.0))

When a COMPAS object is added, the viewer looks for a corresponding view object in a registry.
If a registered view object is found, the add method wraps the COMPAS object in it and returns a view object instance.

::

    >>> type(obj)
    <class 'compas_view2.objects.sphereobject.SphereObject'>

::

    >>> obj._data
    Sphere(Point(0.000, 0.000, 0.000), 1.0)


Object Appearance
=================

The appearance of an object can be changed through various visualization options
which can be passed as keyword arguments to the add function,
or by changing the corresponding attributes of the view object.

::

    >>> viewer.add(Sphere([0, 0, 0], 1.0),
    ...     u=64,
    ...     v=64,
    ...     show_points=True,
    ...     show_lines=True,
    ...     show_faces=True,
    ...     color=(0.7, 0., 0.7),
    ...     pointcolor=(1.0, 0.0, 0.0),
    ...     linecolor=(0.0, 0.0, 1.0),
    ...     facecolor=(0.0, 1.0, 1.0),
    ...     pointsize=10,
    ...     linewidth=2,
    ...     opacity=0.5,
    ...     is_selected=False,
    ...     is_visible=True)

::

    >>> obj = viewer.add(Sphere([0, 0, 0], 1.0))
    >>> obj.u = 32
    >>> obj.v = 64
    >>> obj.show_points = False
    >>> obj.linewidth = 5


Object Collections
==================

Drawing many different objects can slow down the viewer considerably.
To avoid this, you can group same tpye objects in collections.

::

    >>> from compas.geometry import Sphere, Pointcloud
    >>> from compas_view2.objects import Collection
    >>> from compas_view2.app import App

::

    >>> viewer = App()
    >>> cloud = Pointcloud.from_bounds(10, 10, 10, 17)
    >>> spheres = []
    >>> for point in cloud:
    ...     spheres.append(Sphere(point, 0.3))
    ...
    >>> viewer.add(Collection(spheres))
    >>> viewer.show()


The objects in a collection can only be styled uniformly with the same keyword arguments
used to style the individual objects.

::

    >>> viewer.add(Collection(spheres),
    ...     facecolor=(0, 1, 1),
    ...     linecolor=(0, 0, 1),
    ...     opacity=0.5)


Individual object styling will be available for collections soon!


Object Transformations
======================

Every view object has an associated transformation matrix in world coordinates,
which is multiplied with the coordinates of the data object to determine
the final location and orientation of the object in the scene.

The default transformation matrix of a view object is the identity matrix,
which has no effect on the placement and/or orientation of the object in the scene.

To move an object through the scene, or to change its orientation,
assign a transformation matrix to the `matrix` attribute of the view object.

::

    >>> obj = viewer.add(Sphere([0, 0, 0], 1.0))
    >>> obj.matrix = Translation.from_vector([0, 2, 0]).matrix


For convenience, the translation, rotation, and scale can be modified separately.

::

    >>> obj = viewer.add(Sphere([0, 0, 0], 1.0))
    >>> obj.translation = [0, 2, 0]


Dynamic Visualization
=====================

To visualize a dynamic process, for example the process of moving a box along a curve,
use the "on" decorator (:meth:`compas_view2.app.App.on`) on a callback function.

::

    >>> from compas.geometry import Sphere
    >>> from compas_view2.app import App

::

    >>> viewer = App()
    >>> obj = viewer.add(Sphere([0, 0, 0]), 1.0)

::

    >>> @viewer.on(interval=1000, frames=10)
    >>> def move(f):
    ...     obj.translation = [f, 0, 0]
    ...     obj.update()
    ...
    >>> viewer.show()


Zoom, Pan, Rotate, and Select
==============================================================================

After launching the viewer, the view can be transformed by zooming, panning, and rotating. Object selection is also possible.

Below are list of default key-mouse combinations to perform these actions:

- To ``zoom``, "pinch" the trackpad of your laptop or use the ``mousewheel``.

- To ``rotate``, move the mouse while holding ``right click``.

- To ``pan``, move the mouse while holding ``sift + right click``.

- To ``select``, click or box select the object while holding ``left click``.

- To ``unselect``, click the object while holding ``ctrl``.

- To ``zoom-selected``, select the object (or not) and press ``f``.


View Configuration
==================

To transform the view programmatically, you can modify the relevant attributes of the camera directly.

::

    >>> viewer.view.camera.distance = 5
    >>> viewer.view.camera.rz = 30
    >>> viewer.view.camera.rx = -60


More convenient configuration methods using camera position and camera target are under construction and will be available soon.


Selections
==========

To create a selection programmatically, set the attribute :attr:`compas_view2.objects.Object.is_selected` of the objects in the selection to ``True``.

::

    >>> obj = viewer.add(Sphere([0, 0, 0], 1.0))
    >>> obj.is_selected = True


To select an object interactively, click on the object with the left mouse button.
To select multiple objects hold down ``SHIFT`` while selecting objects individually or collectively using a selection window.

To unselect objects, hold down ``COMMAND`` on Mac or ``CONTROL`` on Windows while clicking in an empty area of the view.


Capturing
=========

To grab a screenshot of the view, select "Capture" from the "View" menu (``View > Capture``) and select a location for saving the image.
To record the frames of a dynamic visualization into an animated GIF, use the relevant options of the "on" decorator.

::

    >>> @viewer.on(interval=100, record=True, frames=100, record_path='animated.gif')
    ... def move(f):
    ...     obj.translation = [0.1 * f, 0, 0]
    ...     obj.update()
    ...
    >>> viewer.show()


More Examples
==================

See the examples section for more examples.

