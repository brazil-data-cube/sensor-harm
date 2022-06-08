# Docker support for sensor-harm

Sensor Harmonization (Landsat-5, Landsat-7, Landsat-8 and Sentinel-2)

## Dependencies

- Docker

## Installation

1. Run from the docker directory of this repository.

   ```bash
   $ docker build -t brazildatacube/sensor-harm .
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
