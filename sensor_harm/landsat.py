#
# This file is part of Sensor Harmonization
# Copyright (C) 2020 INPE.
#
# Sensor Harmonization (Landsat-8 and Sentinel-2) is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Sensor Harmonization of Landsat data products."""

import logging
import re
import shutil
from pathlib import Path
from typing import List, Optional, Tuple

# sensor-harm
from .harmonization_model import process_NBAR


def get_landsat_angles(productdir: str, scene_id: str) -> Tuple[str, str, str, str]:
    """Get Landsat angle bands file path.

    Args:
        productdir (str): path to directory containing angle bands.
    Returns:
        sz_path, sa_path, vz_path, va_path: file paths to solar zenith, solar azimuth, view (sensor) zenith and vier (sensor) azimuth.
    """
    img_list = list(productdir.glob(f'**/{scene_id}*.tif'))
    logging.info('Load Landsat Angles')
    pattern = re.compile('.*_solar_zenith_.*')
    sz_path = list(item for item in img_list if pattern.match(str(item)))[0]
    pattern = re.compile('.*_solar_azimuth_.*')
    sa_path = list(item for item in img_list if pattern.match(str(item)))[0]
    pattern = re.compile('.*_sensor_zenith_.*')
    vz_path = list(item for item in img_list if pattern.match(str(item)))[0]
    pattern = re.compile('.*_sensor_azimuth_.*')
    va_path = list(item for item in img_list if pattern.match(str(item)))[0]

    return sz_path, sa_path, vz_path, va_path


def get_landsat_bands(satsen: str) -> Optional[List[str]]:
    """Retrieve the bands which can be harmonized in Landsat data products."""
    if satsen == 'LT5' or satsen == 'LE7':
        return ['sr_band1', 'sr_band2', 'sr_band3', 'sr_band4', 'sr_band5', 'sr_band7']
    elif satsen == 'LC8':
        return ['sr_band2', 'sr_band3', 'sr_band4', 'sr_band5', 'sr_band6', 'sr_band7']
    return


def landsat_harmonize(satsen: str, scene_id: str, productdir: str, target_dir: Optional[str] = None):
    """Prepare Landsat-7 NBAR.

    Args:
        satsen: Scene Satellite
        productdir: path to directory containing angle bands.
        target_dir: path to output result images.

    Returns:
        str: path to folder containing result images.
    """
    productdir = Path(productdir)
    target_dir = Path(target_dir)

    logging.info(f'Loading Angles from {productdir} ...')
    sz_path, sa_path, vz_path, va_path = get_landsat_angles(productdir, scene_id)

    if target_dir is None:
        target_dir = productdir.joinpath(Path('HARMONIZED_DATA'))

    target_dir.mkdir(parents=True, exist_ok=True)

    bands = get_landsat_bands(satsen)

    process_NBAR(productdir, scene_id, bands, sz_path, sa_path, vz_path, va_path, satsen, target_dir)

    # Copy quality band
    pattern = re.compile('.*pixel_qa.*')
    img_list = list(productdir.glob('**/*.tif'))
    matching_pattern = list(item for item in img_list if pattern.match(str(item)))

    if len(matching_pattern) != 0:
        qa_path = matching_pattern[0]
        shutil.copy(qa_path, target_dir)

    pattern = re.compile('.*Fmask4.*')
    img_list = list(productdir.glob('**/*.tif'))
    matching_pattern = list(item for item in img_list if pattern.match(str(item)))

    if len(matching_pattern) != 0:
        qa_path = matching_pattern[0]
        shutil.copy(qa_path, target_dir)

    return target_dir
