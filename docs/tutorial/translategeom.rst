Step-by-Step
=========

The following tutorial shows the process of creating an object and animating it along a path using the compas_view2 library.

The initial step is to import the relevant libraries.

.. code-block:: python

    from compas.geometry import Bezier, Polyline
    from compas.geometry import Point, Vector, Box
    from compas.geometry import Frame, Transformation
    from compas.utilities import window

    from compas_view2.app import App

Next, we generate four control points from which a bezier curve is generated. This is the curve along which the geometry will be translated. Subsquently, the direction up is identified.

.. code-block:: python

    controlpoints = [Point(0, 0, 0), Point(3, 6, 0), Point(6, -3, 3), Point(10, 0, 0)]
    curve = Bezier(controlpoints)

    up = Vector.Zaxis()


The next step is to convert the curve to a locus, which is essentially a bunch of points along the curve. These points are later used to generate a polyline for the animation.

.. code-block:: python

    points = curve.locus(resolution=83)


The intent is to locate our box at the start of the line and aligned properly in the x, y, z planes. The box is then translated along the line but taking each point we broke the curve into and using frame to frame transformations to move the box between the frames aligned at each point. 

Computing the frames requires us to first find the tangent of the curve. This is done by using a sliding window over every three curves to calculate a Vector, which is then a unitized Vector to obtain the tangent of the middle point. For each tangent, the normal Vector is obtained via the cross product of the up Vector with the tangent Vector. 


.. code-block:: python

    normals = [up.cross(vector) for vector in tangents]
    frames = [Frame(p, t, n) for p, t, n in  zip(points[1:], tangents, normals)]



These are then the frames we use and we calculated the frame to frame transformation in relation to the base frame the box initializes at. 

.. code-block:: python

    xforms = [Transformation.from_frame_to_frame(frames[0], frame) for frame in frames]


The box is generated located at the initial frame with dimensions of our choosing.

.. code-block:: python

    box = Box(frames[0], 2, 1, 0.5)


Before initializing the viewer app, it is possible to define the dimensions of the window along with camera setup. This can be altered per personal preferences, but is helpful to ensure a standardized viewpoint upon generation that is good for documentation purposes.

.. code-block:: python

    viewer = App(width=1200, height=750)
    viewer.view.camera.rz = 90
    viewer.view.camera.rx = -75
    viewer.view.camera.tx = 0
    viewer.view.camera.ty = -1
    viewer.view.camera.distance = 6

After defining the viewer window and view settings, the next step is to add geometries. First we add a Polyline generated from the points of our curve, and set its linewidth. Next, the control points are added. the box and initial frame are also added to the viewer, and their settings configured.

.. code-block:: python

    viewer.add(Polyline(points), linewidth=3)
    viewer.add(Polyline(controlpoints), show_points=True, linewidth=0.5)

    BOX = viewer.add(box, show_faces=True, opacity=0.5)
    FRAME = viewer.add(box.frame)

In order to have an animation, a move function must be defined. First, we write @viewer.on in order to activate the animation portion which runs for an interval of 100 seconds, with frames the length of our total frames in our translation frames list. 


.. code-block:: python
    @viewer.on(interval=100, frames=len(frames))
    def move(f):

        X = xforms[f]

        viewer.add(frames[f])
        BOX.matrix = X.matrix
        BOX.update()

    viewer.show()


