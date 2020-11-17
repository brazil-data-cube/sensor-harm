# Sensor Harmonization (Landsat-8 and Sentinel-2)

Generate Landsat-8 and Sentinel-2 NBAR (Nadir BRDF Adjusted Reflectance) product.

## Dependencies

- GDAL
- Numpy
- Rasterio
- S2angs (https://github.com/brazil-data-cube/sentinel2_angle_bands)

## Installing via Git

```
python3 -m pip install git+https://github.com/marujore/sensor_harmonization
```

or

```
git clone https://github.com/marujore/sensor_harmonization
cd sensor_harmonization
pip install .
```

## Usage

[NBAR Landsat-5](./example_harm_l5.py)

[NBAR Landsat-7](./example_harm_l7.py)

[NBAR Landsat-8](./example_harm_l8.py)

[NBAR Sentinel-2](./example_harm_l8.py)
