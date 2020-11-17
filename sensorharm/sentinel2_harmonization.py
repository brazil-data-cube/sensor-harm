# Python Native
import glob
import logging
import os
import re
from pathlib import Path
# 3rdparty
import s2angs
# Sensorharm
from .harmonization_model import process_NBAR


def sentinel_harmonize_SAFE(safel1c, safel2a, target_dir=None, apply_bandpass=True):
    """
        Prepare Sentinel-2 NBAR from Sen2cor.

        Parameters:
            safel1c (str): path to SAFEL1C directory.
            safel2a (str): path to SAFEL2A directory.
            target_dir (str): path to output result images.
        Returns:
            str: path to folder containing result images.
    """
    # Generating Angle bands
    sz_path, sa_path, vz_path, va_path = s2angs.gen_s2_ang(str(safel1c))

    if target_dir is None:
        target_dir = safel2a.joinpath('GRANULE', os.listdir(safel2a.joinpath('GRANULE'))[0], 'HARMONIZED_DATA/')
    target_dir.mkdir(parents=True, exist_ok=True)

    logging.info('Harmonization ...')
    # Sentinel-2 data set
    satsen = safel2a.name[:3]
    logging.info('SatSen: {}'.format(satsen))

    img_dir = safel2a.joinpath('GRANULE', os.listdir(safel2a.joinpath('GRANULE'))[0], 'IMG_DATA/R10m/')
    bands10m = ['B02', 'B03', 'B04', 'B08']
    process_NBAR(img_dir, bands10m, sz_path, sa_path, vz_path, va_path, satsen, target_dir, apply_bandpass)

    img_dir = safel2a.joinpath('GRANULE', os.listdir(safel2a.joinpath('GRANULE'))[0], 'IMG_DATA/R20m/')
    bands20m = ['B8A', 'B11', 'B12']
    process_NBAR(img_dir, bands20m, sz_path, sa_path, vz_path, va_path, satsen, target_dir, apply_bandpass)

    # COPY quality band
    pattern = re.compile('.*SCL.*')
    img_list = img_dir.glob('**/*.jp2')
    qa_filepath = Path(list(item for item in img_list if pattern.match(str(item)))[0])
    # Convert jp2 to tiff
    os.system('gdal_translate -of Gtiff ' + str(qa_filepath) + ' ' + str(target_dir) + '/' + str(Path(qa_filepath.name).with_suffix('.tif')))

    return target_dir


def sentinel_harmonize_sr(safel1c, sr_dir, target_dir, apply_bandpass=True):
    """
        Prepare Sentinel-2 NBAR from LaSRC.

        Parameters:
            safel1c (str): path to SAFEL1C directory.
            sr_dir (str): path to directory containing surface reflectance.
            target_dir (str): path to output result images.
        Returns:
            str: path to folder containing result images.
    """

    # Generating Angle bands
    sz_path, sa_path, vz_path, va_path = s2angs.gen_s2_ang(str(safel1c))

    target_dir.mkdir(parents=True, exist_ok=True)

    print('Harmonization ...', flush=True)
    # Sentinel-2 data set
    satsen = sr_dir.name[0:3]
    print(f'SatSen: {satsen}', flush=True)

    bands = ['sr_band2', 'sr_band3', 'sr_band4', 'sr_band8', 'sr_band8a', 'sr_band11', 'sr_band12']

    process_NBAR(sr_dir, bands, sz_path, sa_path, vz_path, va_path, satsen, target_dir, apply_bandpass)

    return target_dir


def sentinel_harmonize(safel1c, reflectance_data, target_dir, apply_bandpass=True):
    """
        Checks if input surface reflectance is from Sen2cor or LaSRC and direct NBAR processing.

        Parameters:
            safel1c (str): path to SAFEL1C directory.
            reflectance_data (str): path to directory containing surface reflectance.
            target_dir (str): path to output result images.
    """
    safel1c = Path(safel1c)
    reflectance_data = Path(reflectance_data)
    target_dir = Path(target_dir)

    if reflectance_data.name.endswith('.SAFE'): #Check if was processed with Sen2cor
        sentinel_harmonize_SAFE(safel1c, reflectance_data, target_dir, apply_bandpass)
    else:
        sentinel_harmonize_sr(safel1c, reflectance_data, target_dir, apply_bandpass)

    return
