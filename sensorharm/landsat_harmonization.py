# Python Native
import glob
import logging
import re
import shutil
from pathlib import Path
# Sensorharm
from .harmonization_model import process_NBAR


def get_landsat_angles(productdir):
    """
        Get Landsat angle bands file path.

        Parameters:
            productdir (str): path to directory containing angle bands.
        Returns: 
            sz_path, sa_path, vz_path, va_path: file paths to solar zenith, solar azimuth, view (sensor) zenith and vier (sensor) azimuth.
    """
    img_list = list(productdir.glob('**/*.tif'))
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


def get_landsat_bands(satsen):
    if satsen == 'LT5' or satsen == 'LE7':
        return ['sr_band1', 'sr_band2', 'sr_band3', 'sr_band4', 'sr_band5', 'sr_band7']
    elif satsen == 'LC8':
        return ['sr_band2', 'sr_band3', 'sr_band4', 'sr_band5', 'sr_band6', 'sr_band7']
    return


def landsat_harmonize(satsen, productdir, target_dir=None):
    """
        Prepare Landsat-7 NBAR.

        Parameters:
            productdir (str): path to directory containing angle bands.
            target_dir (str): path to output result images.
        Returns:
            str: path to folder containing result images.
    """
    productdir = Path(productdir)
    target_dir = Path(target_dir)

    print(f'Loading Angles from {productdir} ...')
    sz_path, sa_path, vz_path, va_path = get_landsat_angles(productdir)

    if target_dir is None:
        target_dir = productdir.joinpath(Path('HARMONIZED_DATA'))
    target_dir.mkdir(parents=True, exist_ok=True)

    bands = get_landsat_bands(satsen)

    print('Harmonization ...')
    process_NBAR(productdir, bands, sz_path, sa_path, vz_path, va_path, satsen, target_dir)

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
