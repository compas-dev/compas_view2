********************************************************************************
Installation
********************************************************************************

Stable
======

The recommended way to install ``compas_view2`` is with ``conda``.

To create a new environment:

.. code-block:: bash

    conda create -n view2 -c conda-forge compas compas_view2


To add ``compas_view2`` into your existing environment (``python 3.8`` required):

.. code-block:: bash

        conda activate YOUR_ENVIRONMENT
        pip install pyside2 pyopengl qtpy
        pip install ryvencore_qt == 0.3.1.4 #optional if you want to have `Flow` functionality.
        pip install git+https://github.com/compas-dev/compas_view2.git#egg=compas_view2

Development
===========

To get the latest unreleased version, you can install with ``pip`` in a ``conda`` environment
directly from the github repo.

Windows
-------

.. code-block:: bash

    conda create -n view2 python=3.8 git cython freeglut freetype-py textdistance
    conda activate view2
    pip install pyside2 pyopengl qtpy ryvencore_qt == 0.3.1.4
    pip install git+https://github.com/compas-dev/compas_view2.git#egg=compas_view2

Mac
---

.. code-block:: bash

    conda create -n view2 python=3.8 cython python.app freetype-py textdistance
    conda activate view2
    pip install pyside2 pyopengl qtpy ryvencore_qt == 0.3.1.4
    pip install git+https://github.com/compas-dev/compas_view2.git#egg=compas_view2

Linux
-----

.. code-block:: bash

    conda create -n view2 python=3.8 cython freetype-py textdistance
    conda activate view2
    pip install pyside2 pyopengl qtpy ryvencore_qt == 0.3.1.4
    pip install git+https://github.com/compas-dev/compas_view2.git#egg=compas_view2
