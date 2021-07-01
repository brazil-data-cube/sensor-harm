#
# This file is part of Sensor Harmonization
# Copyright (C) 2020-2021 INPE.
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

LANDSAT_SCENE_PARSER = (
    r"^L"
    r"(?P<sensor>\w{1})"
    r"(?P<satellite>\w{2})"
    r"_"
    r"(?P<processingCorrectionLevel>\w{4})"
    r"_"
    r"(?P<path>[0-9]{3})"
    r"(?P<row>[0-9]{3})"
    r"_"
    r"(?P<acquisitionYear>[0-9]{4})"
    r"(?P<acquisitionMonth>[0-9]{2})"
    r"(?P<acquisitionDay>[0-9]{2})"
    r"_"
    r"(?P<processingYear>[0-9]{4})"
    r"(?P<processingMonth>[0-9]{2})"
    r"(?P<processingDay>[0-9]{2})"
    r"_"
    r"(?P<collectionNumber>\w{2})"
    r"_"
    r"(?P<collectionCategory>\w{2})$"
)


def landsat_angles(angle_dir: str, scene_id: str) -> Tuple[str, str, str, str]:
    """Retrieve Landsat angle bands file path.

    Args:
        angle_dir (str): path to directory containing angle bands.
    Returns:
        sz_path, sa_path, vz_path, va_path: file paths to solar zenith, solar azimuth, view (sensor) zenith and vier (sensor) azimuth.
    """
    img_list = list(angle_dir.glob(f'**/{scene_id}*.tif'))
    logging.info('Load Landsat Angles')
    try:
        pattern = re.compile('.*_solar_zenith_.*|.*_SZA.*')
        sz_path = list(item for item in img_list if pattern.match(str(item)))[0]
        pattern = re.compile('.*_solar_azimuth_.*|.*_SAA.*')
        sa_path = list(item for item in img_list if pattern.match(str(item)))[0]
        pattern = re.compile('.*_sensor_zenith_.*|.*_VZA.*')
        vz_path = list(item for item in img_list if pattern.match(str(item)))[0]
        pattern = re.compile('.*_sensor_azimuth_.*|.*_VAA.*')
        va_path = list(item for item in img_list if pattern.match(str(item)))[0]
    except:
        raise RuntimeError(f'File not Found: Missing processed Angle bands on {angle_dir}')

    return sz_path, sa_path, vz_path, va_path


def landsat_bands(satsen: str, collection='02') -> Optional[List[str]]:
    """Retrieve the bands which can be harmonized in Landsat data products."""
    if satsen == 'LT05' or satsen == 'LE07':
        if collection=='01':
            return ['sr_band1', 'sr_band2', 'sr_band3', 'sr_band4', 'sr_band5', 'sr_band7']
        else:
            ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7']
    elif satsen == 'LC08':
        if collection=='01':
            return ['sr_band2', 'sr_band3', 'sr_band4', 'sr_band5', 'sr_band6', 'sr_band7']
        else:
            return ['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7']
    return


def landsat_harmonize(scene_id: str, product_dir: str, target_dir: Optional[str] = None,
                      bands: Optional[List[str]] = None, angle_dir: Optional[str] = None,
                      cp_quality_band: Optional[bool] = True):
    """Prepare Landsat NBAR.

    Args:
        scene_id (str) - The Landsat Scene Identifier
        product_dir (str) - path to directory containing original bands.
        target_dir (Optional[str]) - path to output result images.
        bands (Optional[List[str]]) - List of bands to generate. When "None", use all.
        angle_dir (Optional[str]) - path to directory containing angle bands.
        cp_quality_band (Optional[bool]) - copy quality band to target_dir

    Returns:
        str: path to folder containing result images.
    """
    product_dir = Path(product_dir)
    target_dir = Path(target_dir)

    match = re.match(LANDSAT_SCENE_PARSER, scene_id, re.IGNORECASE)

    if not match:
        raise RuntimeError(f'Invalid Landsat scene id {scene_id}')

    satsen = f'L{match.group("sensor")}{match["satellite"]}'

    angle_dir = Path(angle_dir) if angle_dir else product_dir
    logging.info(f'Loading Angles from {angle_dir} ...')
    sz_path, sa_path, vz_path, va_path = landsat_angles(angle_dir, scene_id)

    if target_dir is None:
        target_dir = product_dir.joinpath(Path('HARMONIZED_DATA'))

    target_dir.mkdir(parents=True, exist_ok=True)

    collection = scene_id.split('_')[-2]

    if bands is None:
        bands = landsat_bands(satsen, collection)

    output_files = process_NBAR(product_dir, scene_id, bands, sz_path, sa_path, vz_path, va_path, satsen, target_dir, dataset_collection=collection)

    # Copy quality band
    if cp_quality_band:
        img_list = list(product_dir.glob('**/*.tif')) or list(product_dir.glob('**/*.TIF'))

        regex_list = ['.*pixel_qa.*', '.*qa_pixel.*', '.*Fmask4.*']
        for regex in regex_list:
            pattern = re.compile(regex, re.IGNORECASE)
            matching_pattern = list(item for item in img_list if pattern.match(str(item)))

            if len(matching_pattern) != 0:
                qa_path = matching_pattern[0]
                shutil.copy(qa_path, target_dir)
                break

    return target_dir, output_files
