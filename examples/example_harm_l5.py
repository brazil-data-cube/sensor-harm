#
# This file is part of Sensor Harmonization.
# Copyright (C) 2020-2021 INPE.
#
# Sensor Harmonization (Landsat-8 and Sentinel-2) is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Define a minimal example Landsat-5 harmonization."""

# Python Native
import time

# 3rdparty
from sensor_harm.landsat import landsat_harmonize

start = time.time()

sr_dir = '/path/to/L5/SR/images/'
target_dir = '/path/to/output/NBAR/'
scene_id = 'THE_SCENE_ID'

landsat_harmonize('LT5', scene_id, sr_dir, target_dir)

end = time.time()
print(f'Duration time: {end - start}')
