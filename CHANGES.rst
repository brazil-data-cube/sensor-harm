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


Changes
=======

Version 0.8.1 (2022-09-21)
--------------------------

- Change LICENSE to GPL v3 and headers source code

Version 0.8.0 (2021-09-27)
--------------------------

- organize code imports
- fix s2angs install
- create output dir folder
- support docker

Version 0.6.1 (2021-07-01)
--------------------------

- Support both Landsat Collection 2 and Landsat Collection 1;
- Renamed get_landsat_angles to landsat_angles
- Renamed get_landsat_bands to landsat_bands
- Exception when missing angle bands


Version 0.6.0 (2021-06-07)
--------------------------

- add scale in Landsat Collection 2;


Version 0.4.0 (2021-05-13)
--------------------------

- Add support to Landsat Collection 2;

- Add support to Sentinel2 L2A.

- Change nodata default value.

- Return output files generated.

- Allows to define the folder that are the bands of the angles.


Version 0.2.0 (2020-12-03)
--------------------------

- Add support to harmonize the data products Landsat-5, Landsat-7, Landsat-8 and Sentinel-2.

- Algorithm model based in W. Lucht, C. B. Schaaf and A. H. Strahler, "`An algorithm for the retrieval of albedo from space using semiempirical BRDF models," <https://ieeexplore.ieee.org/document/841980>`_ in IEEE Transactions on Geoscience and Remote Sensing, vol. 38, no. 2, pp. 977-998, March 2000, doi: 10.1109/36.841980.

  - The coefficients are based in *Roy, D. P., Zhang, H. K., Ju, J., Gomez-Dans, J. L., Lewis, P. E., Schaaf, C. B., Sun Q., Li J., Huang H., & Kovalskyy, V. (2016). "A general method to normalize Landsat reflectance data to nadir BRDF adjusted reflectance." Remote Sensing of Environment, 176, 255-271.*

- Documentation system based on Sphinx.

- Source code versioning based on `Semantic Versioning 2.0.0 <https://semver.org/>`_.

- License: `MIT <https://github.com/brazil-data-cube/sensor-harm/blob/main/LICENSE>`_.
