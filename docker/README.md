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


# Docker support for sensor-harm

Sensor Harmonization (Landsat-5, Landsat-7, Landsat-8 and Sentinel-2)

## Dependencies

- Docker

## Installation

1. Run from the root of this repository.

   ```bash
   $ ./build.sh
   ```


## Usage

To process a Landsat-5, Landsat-7, Landsat-8 or Sentinel-2  scene (e.g. `LC08_L1TP_220069_20190112_20190131_01_T1` or `S2A_MSIL1C_20190105T132231_N0207_R038_T23LLF_20190105T145859.SAFE`) run

```bash
$ docker run --rm \
    -v /path/to/input/:/mnt/input-dir:ro \
    -v /path/to/output:/mnt/output-dir:rw \
    -v /path/to/angles:/mnt/angles-dir:ro \
    -t brazildatacube/sensor-harm:latest LC08_L1TP_220069_20190112_20190131_01_T1
```

```bash
$ docker run --rm \
    -v /path/to/input/:/mnt/input-dir:ro \
    -v /path/to/output:/mnt/output-dir:rw \
    -t brazildatacube/sensor-harm:latest S2A_MSIL1C_20190105T132231_N0207_R038_T23LLF_20190105T145859.SAFE
```

Results are written on mounted `/mnt/output-dir/SCENEID`.


## Usage

This package is an open source implementation of the method presented in "Claverie, M., Ju, J., Masek, J. G., Dungan, J. L., Vermote, E. F., Roger, J.-C., Skakun, S. V., & Justice, C. (2018). The Harmonized Landsat and Sentinel-2 surface reflectance data set. Remote Sensing of Environment, 219, 145-161."
