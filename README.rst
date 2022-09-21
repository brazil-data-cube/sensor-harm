..
    This file is part of Sensor Harmonization
    Copyright (C) 2020-2022 INPE.

    Sensor Harmonization is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


=====================================================
Sensor Harmonization (Landsat-4,5,7,8 and Sentinel-2)
=====================================================


.. image:: https://img.shields.io/badge/license-MIT-green
        :target: https://github.com//brazil-data-cube/sensor-harm/blob/master/LICENSE
        :alt: Software License


.. image:: https://img.shields.io/github/tag/brazil-data-cube/sensor-harm.svg
        :target: https://github.com/brazil-data-cube/sensor-harm/releases
        :alt: Release


.. image:: https://img.shields.io/discord/689541907621085198?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/689541907621085198#
        :alt: Join us at Discord


About
=====


A library in Python for generating Landsat-8 and Sentinel-2 NBAR (Nadir BRDF Adjusted Reflectance) products.


Sensor-harm
-----------

This script uses Surface Reflectance products as inputs. It uses the c-factor approach (`Roy et. al, 2016 <https://doi.org/10.1016/j.rse.2016.01.023>`_)() and optional bandpass on Sentinel-2 data (`Claverie et. al, 2017 <https://doi.org/10.1016/j.rse.2018.09.002>`_) to produce NBAR products.


Dependencies
------------

- Click>=7.0
- jsonschema
- numpy
- rasterio
- requests>=2.20
- `s2angs <https://github.com/brazil-data-cube/s2-angs>`_


Installing via Git
------------------

.. code-block:: console

    python3 -m pip install git+https://github.com/brazil-data-cube/sensor-harm.git


or

.. code-block:: console

    git clone https://github.com/brazil-data-cube/sensor-harm.git
    cd s2-angs
    pip install .

Python Usage
------------

see:

`Example Landsat 5 <examples/exaple_harm_l5>`_

`Example Landsat 7 <examples/exaple_harm_l7>`_

`Example Landsat 8 <examples/exaple_harm_l8>`_

`Example Sentinel 2 <examples/exaple_harm_s2>`_


Docker
------

Build the image from the root of this repository.

    ```bash
    $ ./build.sh
    ```

--no-cache option can be activated by providing `-n` flag; docker base image can be change by providing `-b <baseimage>`. For instance, to build a fresh image one can run from the root of this repository:

    ```bash
    $ ./build.sh -n
    ```

Docker Usage
------------

run a docker container mounting an input-dir, an output-dir and providing the file name, e.g. S2A_MSIL1C_20201013T144731_N0209_R139_T19MGV_20201013T164036.SAFE.


.. code-block:: console

    docker run --rm -v /path/to/my/S2_file/:/mnt/input-dir -v /path/to/my/outputs/:/mnt/output-dir brazildatacube/sensor-harm S2A_MSIL1C_20201013T144731_N0209_R139_T19MGV_20201013T164036.SAFE
