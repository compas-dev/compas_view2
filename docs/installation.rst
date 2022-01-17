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

    conda create -n view2 python=3.8 git cython freeglut
    conda activate view2
    pip install git+https://github.com/compas-dev/compas_view2.git#egg=compas_view2

Mac
---

.. code-block:: bash

    conda create -n view2 python=3.8 cython python.app
    conda activate view2
    pip install git+https://github.com/compas-dev/compas_view2.git#egg=compas_view2

By installing ``python.app`` you can use ``pythonw`` to run the viewers instead of ``python``.
This ensures that all components work as expected.

To configure VS Code to use ``pythonw``, change the python path in the settings of the workspace.
In ``.vscode/settings.json``

.. code-block:: json

    {
        ...

        "python.pythonPath": "/Users/xxx/anaconda3/envs/view2/bin/pythonw"

        ...
    }

Linux
-----

.. code-block:: bash

    conda create -n view2 python=3.8 cython freetype-py
    conda activate view2
    pip install git+https://github.com/compas-dev/compas_view2.git#egg=compas_view2
