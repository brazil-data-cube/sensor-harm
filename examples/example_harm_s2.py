#
# This file is part of Sensor Harmonization.
# Copyright (C) 2020 INPE.
#
# Sensor Harmonization (Landsat-8 and Sentinel-2) is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Define a minimal example Sentinel-2 harmonization."""

# Python Native
import time
# 3rdparty
import sensor_harm


start = time.time()

safel1c = '/path/to/S2/L1C.SAFE'
sr_dir = '/path/to/S2/SR/images/' #can also use L2A.SAFE dir
target_dir = '/path/to/output/NBAR/'

sensor_harm.sentinel_harmonize(safel1c, sr_dir, target_dir, apply_bandpass=True)

end = time.time()
print(f'Duration time: {end - start}')
