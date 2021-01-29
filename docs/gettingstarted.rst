********************************************************************************
Getting Started
********************************************************************************

Installation
============

The package is not yet available on ``PyPI`` or ``conda-forge``.
Therefore, currently, the recommended way to install ``compas_view2`` is directly
from the GitHub repo with ``pip`` in a ``conda`` environment.

Windows
-------

.. code-block:: bash

    conda create -n view2 python=3.8 git cython freeglut --yes
    conda activate view2
    pip install git+https://github.com/compas-dev/compas_view2.git#egg=compas_view2

Mac
---

.. code-block:: bash

    conda create -n view2 python=3.8 cython python.app --yes
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
