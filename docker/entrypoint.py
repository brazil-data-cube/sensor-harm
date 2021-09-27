####################################################################################################################
# This file is part of Sensor Harmonization.
# Copyright (C) 2020-2021 INPE.
#
# Sensor Harmonization (Landsat-8 and Sentinel-2) is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
####################################################################################################################

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
        landsat_harmonize(sceneid, entry, target_dir)
    else:
        raise
except:
    print("""Use Sentinel-2 or Landsat Data Surface Reflectance as input.
    Usage:
    docker run --rm
    -v /path/to/input/:/mnt/input-dir:ro
    -v /path/to/output:/mnt/output-dir:rw
    -t sensor-harm '<LANDSAT Sceneid or SENTINEL-2.SAFE>""")
    sys.exit()

end = time.time()
print(f'Harmonization duration time: {end - start}')
