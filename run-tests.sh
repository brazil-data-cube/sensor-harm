#!/usr/bin/env bash
#
# This file is part of Sensor Harmonization
# Copyright (C) 2020 INPE.
#
# Sensor Harmonization is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

pydocstyle sensor_harm examples setup.py && \
isort sensor_harm examples setup.py --check-only --diff && \
check-manifest --ignore ".travis-*" --ignore ".readthedocs.*" && \
sphinx-build -qnW --color -b doctest docs/sphinx/ docs/sphinx/_build/doctest #&& \
#pytest
