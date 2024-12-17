Installation
===========

Basic Installation
----------------

PyISI can be installed using pip:

.. code-block:: bash

   pip install pyisi

GPU Support
----------

For GPU acceleration, install with CUDA support:

.. code-block:: bash

   pip install pyisi[cuda]

Requirements
-----------

* Python 3.10+
* NumPy
* SciPy
* PyTorch
* CuPy (optional, for GPU support)
* CUDA Toolkit 11.0+ (optional, for GPU support)

Development Installation
----------------------

For development, clone the repository and install in editable mode:

.. code-block:: bash

   git clone https://github.com/Adiaslow/PyISI.git
   cd PyISI
   pip install -e ".[dev]"
