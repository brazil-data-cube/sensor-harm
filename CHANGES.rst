..
    This file is part of Sensor Harmonization
    Copyright (C) 2020 INPE.

    Sensor Harmonization is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Changes
=======


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
