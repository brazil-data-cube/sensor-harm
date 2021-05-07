#
# This file is part of Sensor Harmonization.
# Copyright (C) 2020-2021 INPE.
#
# Sensor Harmonization (Landsat-8 and Sentinel-2) is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Define a minimal example Sentinel-2 harmonization."""

# Python Native
import time
# 3rdparty
from sensor_harm.sentinel2 import sentinel_harmonize


start = time.time()

sentinel2_entry = '/path/to/S2/SR/images/'
target_dir = '/path/to/output/NBAR/'

sentinel_harmonize(sentinel2_entry, target_dir, apply_bandpass=True)

end = time.time()
print(f'Duration time: {end - start}')
