..
    This file is part of Brazil Data Cube sensor-harm.
    Copyright (C) 2022 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.


Usage
=====



Python Usage
------------

see:

`Example Landsat 5 <examples/exaple_harm_l5>`_

`Example Landsat 7 <examples/exaple_harm_l7>`_

`Example Landsat 8 <examples/exaple_harm_l8>`_

`Example Sentinel 2 <examples/exaple_harm_s2>`_


Docker Usage
------------

run a docker container mounting an input-dir, an output-dir and providing the file name, e.g. S2A_MSIL1C_20201013T144731_N0209_R139_T19MGV_20201013T164036.SAFE.


.. code-block:: console

    docker run --rm -v /path/to/my/S2_file/:/mnt/input-dir -v /path/to/my/outputs/:/mnt/output-dir brazildatacube/sensor-harm S2A_MSIL1C_20201013T144731_N0209_R139_T19MGV_20201013T164036.SAFE

