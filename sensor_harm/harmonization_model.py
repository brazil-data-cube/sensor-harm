#
# This file is part of Sensor Harmonization
# Copyright (C) 2020-2021 INPE.
#
# Sensor Harmonization (Landsat-8 and Sentinel-2) is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Define the models for data harmonization.

References:
    Ross-thick Li-sparse model in:
    Lucht, W., Schaaf, C. B., & Strahler, A. H. (2000).
    An algorithm for the retrieval of albedo from space using semiempirical BRDF models.
    IEEE Transactions on Geoscience and Remote Sensing, 38(2), 977-998.
"""

# Python Native
import logging
import os
import re
from pathlib import Path

# 3rdparty
import numpy
import numpy.ma
import rasterio
from rasterio.enums import Resampling
from rasterio.windows import Window

br_ratio = 1.0  # shape parameter
hb_ratio = 2.0  # crown relative height
DE2RA = 0.0174532925199432956  # Degree to Radian proportion

# Coeffients in  Roy, D. P., Zhang, H. K., Ju, J., Gomez-Dans, J. L., Lewis, P. E., Schaaf, C. B., Sun Q., Li J., Huang H., & Kovalskyy, V. (2016).
# A general method to normalize Landsat reflectance data to nadir BRDF adjusted reflectance.
# Remote Sensing of Environment, 176, 255-271.
brdf_coefficients = {
    'blue': {
        'fiso': 774,
        'fgeo': 79,
        'fvol': 372
    },
    'green': {
        'fiso': 1306,
        'fgeo': 178,
        'fvol': 580
    },
    'red': {
        'fiso': 1690,
        'fgeo': 227,
        'fvol': 574
    },
    'nir': {
        'fiso': 3093,
        'fgeo': 330,
        'fvol': 1535
    },
    'swir1': {
        'fiso': 3430,
        'fgeo': 453,
        'fvol': 1154
    },
    'swir2': {
        'fiso': 2658,
        'fgeo': 387,
        'fvol': 639
    }
}


def consult_band(b: str, satsen: str):
    """Consult band common name.

    Args:
        b (str): band name.
        satsen (str): satellite sensor.

    Returns:
        str: band common name.
    """
    if satsen == 'LT05':
        common_name = {'sr_band1': 'blue', 'sr_band2':'green', 'sr_band3':'red', 'sr_band4':'nir', 'sr_band5':'swir1',
                       'sr_band7':'swir2',
                       'SR_B1': 'blue', 'SR_B2':'green', 'SR_B3':'red', 'SR_B4':'nir', 'SR_B5':'swir1',
                       'SR_B7':'swir2'}
        return common_name[b]
    elif satsen == 'LE07':
        common_name = {'sr_band1': 'blue', 'sr_band2':'green', 'sr_band3':'red', 'sr_band4':'nir', 'sr_band5':'swir1',
                       'sr_band7':'swir2',
                       'SR_B1': 'blue', 'SR_B2':'green', 'SR_B3':'red', 'SR_B4':'nir', 'SR_B5':'swir1',
                       'SR_B7':'swir2'}
        return common_name[b]
    elif satsen == 'LC08':
        common_name = {'sr_band1': 'coastal', 'sr_band2':'blue', 'sr_band3':'green', 'sr_band4':'red', 'sr_band5':'nir',
                       'sr_band6':'swir1', 'sr_band7':'swir2',
                       'SR_B1': 'coastal', 'SR_B2':'blue', 'SR_B3':'green', 'SR_B4':'red', 'SR_B5':'nir',
                       'SR_B6':'swir1', 'SR_B7':'swir2'}
        return common_name[b]
    elif satsen == 'S2A' or satsen == 'S2B':
        common_name = {'sr_band1': 'coastal', 'sr_band2': 'blue', 'sr_band3': 'green', 'sr_band4': 'red',
                       'sr_band5': 'rededge1', 'sr_band6': 'rededge2', 'sr_band7': 'rededge3',
                       'sr_band8': 'nir', 'sr_band8a': 'nir', 'sr_band11': 'swir1', 'sr_band12': 'swir2',
                       'B01': 'coastal', 'B02': 'blue', 'B03': 'green', 'B04': 'red',
                       'B05': 'rededge1', 'B06': 'rededge2', 'B07': 'rededge3',
                       'B08': 'nir', 'B8A': 'nir', 'B11': 'swir1', 'B12': 'swir2'}
        return common_name[b]
    return


def is_landsat(scene_id: str):
    """Verify if a scene id is from a Landsat image.

    Args:
        scene_id (str): scene id.
    Returns:
        bool: True if it is a Landsat scene id, False otherwise.
    """
    if (scene_id.startswith('LC08') or scene_id.startswith('LE07') or scene_id.startswith('LT05') or scene_id.startswith('LT04')):
        return True
    return False


def is_sentinel2(scene_id: str):
    """Verify if a scene id is from a Sentinel-2 image.

    Args:
        scene_id (str): scene id.
    Returns:
        bool: True if it is a Sentinel-2 scene id, False otherwise.
    """
    if scene_id.startswith('S2'):
        return True
    return False


def load_raster_resampled(img_path, resample_factor=1/2, window=None):
    """Load and resample image.

    Args:
        img_path (str): path to image.
        resample_factor (str): resample factor.
        window (Window): window.

    Returns:
        raster: numpy.array.
    """
    # Resample the window
    res_window = Window(window.col_off * resample_factor, window.row_off * resample_factor,
                        window.width * resample_factor, window.height * resample_factor)
    with rasterio.open(img_path) as dataset:
        try:
            raster = dataset.read(
                out_shape=(
                    1,
                    int(window.height),
                    int(window.width),
                ),
                resampling=Resampling.average,
                masked=True,
                window=res_window
            )
        except:
            logging.info("BREAK RES WINDOW {}".format(res_window))
            return
        return raster


def load_img(img_path, window=None):
    """Load image into an xarray Data Array.

    Args:
        img_path (str): path to input file.
        window (Window): rasterio window.

    Returns:
        raster: numpy.array.
    """
    logging.debug('Loading {} ...'.format(img_path))
    with rasterio.open(img_path) as dataset:
        raster = dataset.read(1, masked=True, window=window)

    return raster


def prepare_angles(sz_path, sa_path, vz_path, va_path, satsen, band, window=None):
    """Scale angle bands, convert from radians, calculate relative azimuth angle band.

    Args:
        sz_path (str): path to solar zenith file.
        sa_path (str): path to solar azimuth file.
        vz_path (str): path to view (sensor) zenith file.
        va_path (str): path to view (sensor) azimuth file.
        satsen (str): satellite sensor.
        band (str): band.
        window (Window): rasterio window.

    Returns:
        raster, raster, raster: numpy.array (view_zenith, solar_zenith, relative_azimuth).
    """
    if satsen == 'S2A' or satsen == 'S2B':
        if band in ['sr_band8a', 'sr_band11', 'sr_band12']: # ['B8A','B11','B12']:
            relative_azimuth = numpy.divide(
                numpy.subtract(load_raster_resampled(va_path, 0.5, window),
                               load_raster_resampled(sa_path, 0.5, window)),
                100) * DE2RA
            solar_zenith = numpy.divide(load_raster_resampled(sz_path, 0.5, window), 100) * DE2RA
            view_zenith = numpy.divide(load_raster_resampled(vz_path, 0.5, window), 100) * DE2RA

            return view_zenith, solar_zenith, relative_azimuth

    relative_azimuth = numpy.divide(numpy.subtract(load_img(va_path, window), load_img(sa_path, window)), 100) * DE2RA
    solar_zenith = numpy.divide(load_img(sz_path, window), 100) * DE2RA
    view_zenith = numpy.divide(load_img(vz_path, window), 100) * DE2RA

    return view_zenith, solar_zenith, relative_azimuth


def sec(angle):
    """Calculate secant.

    Args:
        angle (numpy array): raster band of angle.

    Returns:
        secant : numpy.array.
    """
    return 1./numpy.cos(angle) #numpy.divide(1./numpy.cos(angle))


def calc_cos_t(hb_ratio, d, theta_s_i, theta_v_i, relative_azimuth):
    """Calculate t cossine.

    Args:
        hb_ratio (int): h/b.
        d (numpy array): d.
        theta_s_i (numpy array): theta_s_i.
        theta_v_i (numpy array): theta_v_i.
        relative_azimuth (numpy array): relative_azimuth.

    Returns:
        cos_t : numpy.array.
    """
    return hb_ratio * numpy.sqrt(d*d + numpy.power(numpy.tan(theta_s_i)*numpy.tan(theta_v_i)*numpy.sin(relative_azimuth), 2)) / (sec(theta_s_i) + sec(theta_v_i))


def calc_d(theta_s_i, theta_v_i, relative_azimuth):
    """Calculate d.

    Args:
        theta_s_i (numpy array): theta_s_i.
        theta_v_i (numpy array): theta_v_i.
        relative_azimuth (numpy array): relative_azimuth.

    Returns:
        d : numpy.array.
    """
    return numpy.sqrt(
    numpy.tan(theta_s_i)*numpy.tan(theta_s_i) + numpy.tan(theta_v_i)*numpy.tan(theta_v_i) - 2*numpy.tan(theta_s_i)*numpy.tan(theta_v_i)*numpy.cos(relative_azimuth))


def calc_theta_i(angle, br_ratio):
    """Calculate calc_theta_i.

    Args:
        angle (numpy array): theta_s_i.
        br_ratio (int): b/r.

    Returns:
        theta_i : numpy.array.
    """
    return numpy.arctan(br_ratio * numpy.tan(angle))


def li_kernel(view_zenith, solar_zenith, relative_azimuth):
    """Calculate Li Kernel - Li X. and Strahler A. H., (1986) - Geometric-Optical Bidirectional Reflectance Modeling of a Conifer Forest Canopy.

    Args:
        view_zenith (numpy array): view zenith.
        solar_zenith (numpy array): solar zenith.
        relative_azimuth (numpy array): relative_azimuth.

    Returns:
        li_kernel : numpy.array.
    """
    # ref 1986
    theta_s_i = calc_theta_i(solar_zenith, br_ratio)
    theta_v_i = calc_theta_i(view_zenith, br_ratio)
    d = calc_d(theta_s_i, theta_v_i, relative_azimuth)
    cos_t = calc_cos_t(hb_ratio, d, theta_s_i, theta_v_i, relative_azimuth)
    t = numpy.arccos(numpy.maximum(-1., numpy.minimum(1., cos_t)))
    big_o = (1./numpy.pi)*(t-numpy.sin(t)*cos_t)*(sec(theta_v_i)*sec(theta_s_i))
    cos_e_i = numpy.cos(theta_s_i)*numpy.cos(theta_v_i) + numpy.sin(theta_s_i)*numpy.sin(theta_v_i)*numpy.cos(relative_azimuth)

    return big_o - sec(theta_s_i) - sec(theta_v_i) + 0.5*(1. + cos_e_i)*sec(theta_v_i)*sec(theta_s_i)


def ross_kernel(view_zenith, solar_zenith, relative_azimuth):
    """Calculate Ross-Thick Kernel.

    Args:
        view_zenith (numpy array): view zenith.
        solar_zenith (numpy array): solar zenith.
        relative_azimuth (numpy array): relative_azimuth.

    Returns:
        ross_thick_kernel : numpy.array.
    """
    cos_e = numpy.cos(solar_zenith)*numpy.cos(view_zenith) + numpy.sin(solar_zenith)*numpy.sin(view_zenith)*numpy.cos(relative_azimuth)
    e = numpy.arccos(cos_e)
    return ((((numpy.pi / 2.) - e)*cos_e + numpy.sin(e)) / (numpy.cos(solar_zenith) + numpy.cos(view_zenith))) - (numpy.pi / 4)


def calc_brf(view_zenith, solar_zenith, relative_azimuth, band_coef):
    """Calculate brf.

    Args:
        view_zenith (numpy array): view zenith.
        solar_zenith (numpy array): solar zenith.
        relative_azimuth (numpy array): relative_azimuth.
        band_coef (float): MODIS band coefficient.

    Returns:
        brf : numpy.array.
    """
    logging.debug('Calculating Li Sparce Reciprocal Kernel')
    li = li_kernel(view_zenith, solar_zenith, relative_azimuth)
    logging.debug('Calculating Ross Thick Kernel')
    ross = ross_kernel(view_zenith, solar_zenith, relative_azimuth)

    return band_coef['fiso'] + band_coef['fvol']*ross +band_coef['fgeo']*li


def bandpassHLS_1_4(img, band, satsen):
    """Bandpass function applied to Sentinel-2 data as followed in HLS 1.4 products.

     Reference:
        Claverie et. al, 2018 - The Harmonized Landsat and Sentinel-2 surface reflectance data set.

    Args:
        img (array): Array containing image pixel values.
        band (str): Band that will be processed, which can be 'B02','B03','B04','B8A','B01','B11' or 'B12'.
        satsen (str): Satellite sensor, which can be 'S2A' or 'S2B'.
    Returns:
        array: Array containing image pixel values bandpassed.
    """
    logging.info('Applying bandpass band {} satsen {}'.format(band, satsen))
    # Skakun et. al, 2018 - Harmonized Landsat Sentinel-2 (HLS) Product User’s Guide
    if satsen == 'S2A':
        if band == 'coastal':  # UltraBlue/coastal #MODIS don't have this band # B01
            slope = 0.9959
            offset = -0.0002
        elif band == 'blue':  # Blue # B02
            slope = 0.9778
            offset = -0.004
        elif band == 'green':  # Green # B03
            slope = 1.0053
            offset = -0.0009
        elif band == 'red':  # Red # B04
            slope = 0.9765
            offset = 0.0009
        elif band == 'nir':  # Nir # B08 B8A
            slope = 0.9983
            offset = -0.0001
        elif band == 'swir1':  # Swir 1 # B11
            slope = 0.9987
            offset = -0.0011
        elif band == 'swir2':  # Swir 2 # B12
            slope = 1.003
            offset = -0.0012
        img = numpy.add(numpy.multiply(img, slope), offset)

    elif satsen == 'S2B':
        logging.debug("S2B")
        if band == 'coastal':  # UltraBlue/coastal #MODIS don't have this band # B01
            slope = 0.9959
            offset = -0.0002
        elif band == 'blue':  # Blue # B02
            slope = 0.9778
            offset = -0.004
        elif band == 'green':  # Green # B03
            slope = 1.0075
            offset = -0.0008
        elif band == 'red':  # Red # B04
            slope = 0.9761
            offset = 0.001
        elif band == 'nir':  # Nir # B08 B8A
            slope = 0.9966
            offset = 0.000
        elif band == 'swir1':  # Swir 1 # B11
            slope = 1.000
            offset = -0.0003
        elif band == 'swir2':  # Swir 2 # B12
            slope = 0.9867
            offset = -0.0004

        img = numpy.add(numpy.multiply(img, slope), offset)

    return img


def process_NBAR(parsed_sceneid, img_dir, bands, sz_path, sa_path, vz_path, va_path, out_dir, apply_bandpass=True, nodata = 0):
    """Calculate Normalized BRDF Adjusted Reflectance (NBAR).

    Args:
        parsed_sceneid (dict): parsed scene id.
        img_dir (str): input directory.
        bands (list): list of bands to process.
        sz_path (str): solar zenith angle.
        sa_path (str): solar azimuth angle.
        vz_path (str): view (sensor) zenith angle.
        va_path (str): view (sensor) azimuth angle.
        out_dir: output directory.
        apply_bandpass (bool): verify if band pass will be applied.
    """
    scene_id = parsed_sceneid.group(0)
    output_files = []

    for b in bands:
        logging.info(f"Harmonizing band {b} ...")
        # Search for input file
        r = re.compile('.*_{}.tif$|.*_{}.*jp2$'.format(b, b))
        imgs_in_dir = os.listdir(img_dir)
        logging.debug(list(filter(r.match, imgs_in_dir)))

        # TODO: We should use file name. Check which of them have same filename and try to get from some angle band
        if is_sentinel2(scene_id):
            satsen = f'S{parsed_sceneid["sensor"]}{parsed_sceneid["satellite"]}'
            input_file = Path(list(filter(r.match, imgs_in_dir))[0])
            output_file = out_dir.joinpath(Path(input_file).stem + '_NBAR').with_suffix('.tif')
        elif is_landsat(scene_id):
            satsen = f'L{parsed_sceneid["sensor"]}{parsed_sceneid["satellite"]}'
            if parsed_sceneid["collectionNumber"] == '01':
                nodata = -9999
                _extension = 'tif'
                _processing_level = '_sr_'
            elif parsed_sceneid["collectionNumber"] == '02':
                nodata = 0
                _extension = 'TIF'
                _processing_level = '_SR_'

            input_file = Path(img_dir).joinpath(f'{scene_id}_{b}.{_extension}')
            output_file = out_dir.joinpath(Path(input_file.name.replace(_processing_level, '_NBAR_')).with_suffix('.tif'))

        img_path = img_dir.joinpath(input_file)

        # Prepare template band
        with rasterio.open(img_path) as src:
            profile = src.profile
            tilelist = list(src.block_windows())
            height, width = src.shape
            profile['nodata'] = nodata
        nbar = numpy.full((height, width), dtype='float', fill_value=nodata)

        band_common_name = consult_band(b, satsen)
        band_coef = brdf_coefficients[band_common_name]

        for _, window in tilelist:
            logging.debug(f"Harmonizing band {b} window {window}")
            row_offset = window.row_off + window.height
            col_offset = window.col_off + window.width

            # Load angle bands
            view_zenith, solar_zenith, relative_azimuth = prepare_angles(sz_path, sa_path, vz_path, va_path, satsen, b,
                                                                         window)

            brf_sensor = calc_brf(view_zenith, solar_zenith, relative_azimuth, band_coef)
            brf_ref = calc_brf(numpy.zeros(view_zenith.shape), solar_zenith, numpy.zeros(view_zenith.shape), band_coef)
            c_factor = brf_ref/brf_sensor

            # Reading input reflectance image
            reflectance_img = load_img(img_path, window)

            # Apply scale for Landsat Collection-2
            if is_landsat(scene_id) and \
            (not numpy.all(reflectance_img.mask)) and \
            parsed_sceneid["collectionNumber"] == '02':
                reflectance_img =  ((reflectance_img * 0.275)-2000) #Rescale data to 0-10000 -> ((raster1_arr * 0.0000275)-0.2)

            # Producing NBAR band
            nbar[window.row_off: row_offset, window.col_off: col_offset] = reflectance_img * c_factor

        # Check if apply bandpass
        if apply_bandpass:
            if (satsen == 'S2A') or (satsen == 'S2B'):
                logging.info("Performing bandpass ...")
                nbar = bandpassHLS_1_4(nbar, consult_band(b, satsen), satsen).astype(profile['dtype'])

        logging.info(profile)
        profile['dtype'] = numpy.intc
        nbar_dataset = rasterio.open(
            str(output_file),
            'w',
            driver='GTiff',
            height=profile['height'],
            width=profile['width'],
            count=profile['count'],
            dtype=numpy.intc,#str(resampled_array.dtype),
            crs=profile['crs'],
            transform=profile['transform'],
            nodata=profile['nodata'],
            compress='deflate'
        )
        nbar_dataset.write(nbar.astype(numpy.intc), 1)
        nbar_dataset.close()

        output = {}
        output[b] = output_file
        output_files.append(output)

    return output_files
