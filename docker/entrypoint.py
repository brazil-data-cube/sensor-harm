#
# This file is part of Brazil Data Cube sensor-harm.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

import os
import sys
import time
from pathlib import Path

# 3rdparty
from sensor_harm.sentinel2 import sentinel_harmonize
from sensor_harm.landsat import landsat_harmonize


start = time.time()

try:
    sceneid = sys.argv[1]
    entry = os.path.join('/mnt/input-dir/', sceneid)
    target_dir = '/mnt/output-dir/'

    if sceneid.startswith('S2'):
        # Sentinel
        print(f'Harmonizing Sentinel-2 scene: {sceneid}')
        sentinel_harmonize(entry, target_dir, apply_bandpass=True)
    elif sceneid.startswith(('LT04', 'LT05', 'LE07', 'LC08')):
        # Landsat
        angle_dir = os.path.join('/mnt/angles-dir/', sceneid)

        landsat_harmonize(sceneid, entry, target_dir, angle_dir=angle_dir)
    else:
        raise
except:
    print("""Use Sentinel-2 or Landsat Data Surface Reflectance as input.
    Usage:
    docker run --rm
    -v /path/to/input/:/mnt/input-dir:ro
    -v /path/to/angles:/mnt/angles-dir:ro
    -v /path/to/output:/mnt/output-dir:rw
    -t brazildatacube/sensor-harm '<LANDSAT Sceneid or SENTINEL-2.SAFE>""")
    sys.exit()

end = time.time()
print(f'Harmonization duration time: {end - start}')
