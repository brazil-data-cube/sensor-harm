..
    This file is part of Sensor Harmonization
    Copyright (C) 2020 INPE.

    Sensor Harmonization (Landsat-8 and Sentinel-2) is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Installation
============


Development installation
------------------------


Pre-Requirements
++++++++++++++++


The ``Sensor Harmonization`` (``sensor-harm``) depends essentially on:

- `NumPY <https://numpy.org/>`_.

- `Rasterio <https://rasterio.readthedocs.io/en/latest/>`_


Clone the software repository
+++++++++++++++++++++++++++++


Use ``git`` to clone the software repository::

    git clone https://github.com/brazil-data-cube/sensor-harm.git


Install sensor-harm in Development Mode
+++++++++++++++++++++++++++++++++++++++


Go to the source code folder::

    cd sensor-harm


Install in development mode::

    pip3 install -e .[all]


.. note::

    If you want to create a new *Python Virtual Environment*, please, follow this instruction:

    *1.* Create a new virtual environment linked to Python 3.7::

        python3.7 -m venv venv


    **2.** Activate the new environment::

        source venv/bin/activate


    **3.** Update pip and setuptools::

        pip3 install --upgrade pip

        pip3 install --upgrade setuptools


Build the Documentation
+++++++++++++++++++++++


You can generate the documentation based on Sphinx with the following command::

    python setup.py build_sphinx


The above command will generate the documentation in HTML and it will place it under::

    docs/sphinx/_build/html/


The above command will generate the documentation in HTML and it will place it under::

    docs/sphinx/_build/html/


You can open the above documentation in your favorite browser, as::

    firefox docs/sphinx/_build/html/index.html

