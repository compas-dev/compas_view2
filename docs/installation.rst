********************************************************************************
Installation
********************************************************************************

Stable
======

The recommended way to install ``compas_view2`` is with ``conda``.

.. code-block:: bash

    conda create -n view2 -c conda-forge compas compas_view2


Development
===========

To get the latest unreleased version, you can install with ``pip`` in a ``conda`` environment
directly from the github repo.

Windows
-------

.. code-block:: bash

    conda create -n view2 python=3.8 git cython freeglut freetype-py textdistance
    conda activate view2
    pip install pyside2 pyopengl qtpy ryvencore_qt
    pip install git+https://github.com/compas-dev/compas_view2.git#egg=compas_view2

to update your environment from local source.

.. code-block:: bash
    
    cd path/to/compas_view2
    pip install .

Mac
---

.. code-block:: bash

    conda create -n view2 python=3.8 cython python.app freetype-py textdistance
    conda activate view2
    pip install pyside2 pyopengl qtpy ryvencore_qt
    pip install git+https://github.com/compas-dev/compas_view2.git#egg=compas_view2

Linux
-----

.. code-block:: bash

    conda create -n view2 python=3.8 cython freetype-py textdistance
    conda activate view2
    pip install pyside2 pyopengl qtpy ryvencore_qt
    pip install git+https://github.com/compas-dev/compas_view2.git#egg=compas_view2
